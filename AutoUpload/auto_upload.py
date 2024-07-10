import os
import subprocess
import webbrowser
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import requests
import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs, urlencode
from datetime import datetime
from vod_upload_settings import FILE_SUFFIX, TWITCH_CHANNEL_NAME, TWITCH_CLIENT_ID, YOUTUBE_CATEGORY, YOUTUBE_TAGS, YOUTUBE_PRIVACY, VOD_FOLDER, SHUTDOWN, DELETE_VOD_FILES_AFTER, UPSCALE_WIDTH, UPSCALE_HEIGHT

# We need this handler to get the twitch access token
# Delivers a html page that simply gets the access token and sends it back to the temp local server
class TokenHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        # Send our access token getter on /
        if self.path == '/':
            self._set_headers()
            with open('twitch_oauth.html', 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        # Got token via our html page that gets the access token
        if self.path == '/receive-token':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            token_data = json.loads(post_data)

            twitch_access_token = token_data.get('access_token')
            print(f'Received access token!')

            # Store the access token in the server instance
            self.server.twitch_access_token = twitch_access_token

            self._set_headers()
            self.wfile.write(json.dumps({'message': 'Token received'}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
           
# Find the latest video with the vod suffix in the provided folder           
def get_latest_video(folder_path):
    video_files = [f for f in os.listdir(folder_path) if f.endswith(FILE_SUFFIX)]
    if not video_files:
        return None
    latest_video = max(video_files, key=lambda x: os.path.getctime(os.path.join(folder_path, x)))
    return os.path.join(folder_path, latest_video)

def is_cuda_available():
    try:
        # Check for CUDA support in ffmpeg
        ffmpeg_path = 'ffmpeg'
        result = subprocess.run([ffmpeg_path, '-hwaccels'], capture_output=True, text=True)
        return 'cuda' in result.stdout
    except Exception as e:
        print(f"An error occurred while checking for CUDA availabe")
        return False

# Upscale routine using ffmpeg    
def recode_video(input_video, output_video):
    ffmpeg_path = "ffmpeg" 
    if is_cuda_available():
        # use nvenc if our ffmpeg instance can do it
        ffmpeg_command = [
            'ffmpeg',
            '-y',                    # Skip ffmpeg overwrite check
            '-hwaccel', 'cuda',      # Use CUDA for hardware acceleration
            '-hwaccel_output_format', 'cuda',  # Output format for hardware acceleration
            '-i', input_video,
            '-vf', f'scale_cuda={UPSCALE_WIDTH}:{UPSCALE_HEIGHT}',  # Video filter: scale to users choice using CUDA
            '-c:a', 'copy',          # Copy audio codec
            '-c:v', 'h264_nvenc',    # use nvenc
            '-maxrate:v', '10M',     # set a maximum
            '-preset', 'slow',       # set the quality preset (slower = better quality but takes more ressources)
            '-b:v', '6M',            
            output_video
]
    else:
        # should be x264 by default
        ffmpeg_command = [
            ffmpeg_path, '-y', '-i', input_video, '-vf', f'scale={UPSCALE_WIDTH}:{UPSCALE_HEIGHT}', '-c:a', 'copy', output_video
        ]
    
    subprocess.run(ffmpeg_command)

# Starts a simple web server to retrieve the twitch access token    
def start_twitch_token_server():
    server_address = ('', 8008)
    httpd = HTTPServer(server_address, TokenHandler)
    # Attach an empty twitch_access_token attribute to the server instance
    httpd.twitch_access_token = None
    
    authorize_url = 'https://id.twitch.tv/oauth2/authorize'
    params = {
        'client_id': TWITCH_CLIENT_ID,
        'redirect_uri': 'http://localhost:8008',
        'response_type': 'token',
        'scope': ''  
    }
    auth_url = authorize_url + '?' + urlencode(params)
    
    # Open the authorization URL in the default web browser
    webbrowser.open(auth_url)
    
    print(f"Visit this URL to authorize access (if it doesn't open automatically):\n{auth_url}")
    
    print(f'Starting server on port 8008...')
    # Run until we have an twitch_access_token
    while(httpd.twitch_access_token == None):
        httpd.handle_request()

    return httpd.twitch_access_token


def get_youtube_access_token():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        'client_secrets_youtube_vod.json', ["https://www.googleapis.com/auth/youtube.upload"])
    credentials = flow.run_local_server(port=0)
    return googleapiclient.discovery.build('youtube', 'v3', credentials=credentials)

# Use twitch api to get the channel id from channel name
def get_twitch_channel_id(channel_name, client_id, twitch_access_token):
    url = f'https://api.twitch.tv/helix/users?login={channel_name}'
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {twitch_access_token}'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    if data['data']:
        return data['data'][0]['id']
    return None

# Get channel info so we can get the latest title while the stream is offline
def get_twitch_channel_info(channel_id, client_id, twitch_access_token):
    url = f'https://api.twitch.tv/helix/channels?broadcaster_id={channel_id}'
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {twitch_access_token}'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    if data['data']:
        return data['data'][0]
    return None
    
# Simple io stuff
def read_file_into_variable(file_path):
    with open(file_path, 'r') as file:
        return file.read()
 
# Upload routine 
def upload_video(youtube, video_file, title, description, tags, category_id):
    print(f"Starting upload!")
    # Put in metadata
    request_body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': category_id
        },
        'status': {
            'privacyStatus': YOUTUBE_PRIVACY
        }
    }

    # Start the upload
    media = googleapiclient.http.MediaFileUpload(video_file, chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    )
    response = None
    while response is None:
        status, response = request.next_chunk()
    print(f"Upload complete: {response['id']}")

# Main routine    
def run_script():
    folder_path = VOD_FOLDER
    latest_video = get_latest_video(folder_path)
    print(f"Latest video file: {latest_video}")
    output_video = f'{folder_path}/latest_rescale.mp4'
    
    if latest_video:
        # Do the stuff with user interaction first so they can go afk
        youtube = get_youtube_access_token()

        # Start HTTP server to handle Twitch OAuth redirect
        twitch_access_token = start_twitch_token_server()
        
        # Get Twitch channel info using access token
        channel_id = get_twitch_channel_id(TWITCH_CHANNEL_NAME, TWITCH_CLIENT_ID, twitch_access_token)
        if channel_id:
            channel_info = get_twitch_channel_info(channel_id, TWITCH_CLIENT_ID, twitch_access_token)
            if channel_info:
                title = channel_info['title']
            else:
                title = "Default Title"
        else:
            title = "Default Title"
    
        # Check if we should recode. We don't recode if both the height and width user inputs are -1
        do_recode = UPSCALE_HEIGHT != -1 and UPSCALE_WIDTH != -1
        
        if do_recode:
            recode_video(latest_video, output_video)
        else:
            output_video = latest_video
      
        # Read descriptino file and replace the variables
        description = read_file_into_variable('vod_default_description.txt')
        description = description.replace('{day}', datetime.now().strftime('%m-%d-%Y'))
        
        # Fill in other preset stuff    
        tags = YOUTUBE_TAGS
        category_id = YOUTUBE_CATEGORY 

        # Finally upload our video
        upload_video(youtube, output_video, title, description, tags, category_id)
        
        # Post job cleanup
        if DELETE_VOD_FILES_AFTER:
            if do_recode:
                os.remove(output_video)
            os.remove(latest_video)
        if SHUTDOWN:
            os.system("shutdown /s /t 1")
            
        
    else:
        print("No video files found in the specified folder.")

if __name__ == "__main__":
    run_script()