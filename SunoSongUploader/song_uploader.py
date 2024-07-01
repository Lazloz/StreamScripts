from PIL import Image, ImageDraw, ImageFont, ImageFilter
import sys
import suno
import requests
import subprocess
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from datetime import datetime

from song_uploader_config import SONG_ID, YOUTUBE_TITLE, YOUTUBE_TAGS, YOUTUBE_CATEGORY, YOUTUBE_PRIVACY

def read_file_to_variable(file_path):
    with open(file_path, 'r') as file:
        file_content = file.read()
    return file_content
    
def download_image(image_url, image_id) :
    response = requests.get(image_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Open a file in binary-write mode
        with open("suno_downloads/" + image_id + ".png", "wb") as file:
            # Write the content of the response (the image) to the file
            file.write(response.content)
        print("Image downloaded successfully")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")
        
def read_file_to_variable(file_path):
    with open(file_path, 'r') as file:
        file_content = file.read()
    return file_content
    
def download_image(image_url, image_id) :
    response = requests.get(image_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Open a file in binary-write mode
        image_path = "suno_downloads/" + image_id + ".png"
        with open(image_path, "wb") as file:
            # Write the content of the response (the image) to the file
            file.write(response.content)
        print("Image downloaded successfully")
        return image_path
    else:
        print(f"Failed to download image. Status code: {response.status_code}")
    
# Function to darken an image
def darken_image(image, factor=0.5):
    darkened_image = image.point(lambda p: p * factor)
    return darkened_image

def upload_video(youtube, video_file, title, description, tags, category_id):
    print(f"Starting upload!")
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

    media = googleapiclient.http.MediaFileUpload(video_file, chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    )
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")
    print(f"Upload complete: {response['id']}")

def get_authenticated_service():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        'client_secrets_youtube_vod.json', ["https://www.googleapis.com/auth/youtube.upload"])
    credentials = flow.run_local_server(port=0)
    return googleapiclient.discovery.build('youtube', 'v3', credentials=credentials)
    
client = suno.Suno(cookie=read_file_to_variable('suno_token.txt'))

song = client.get_songs([SONG_ID])[0]

# Download mp3
song_path = client.download(song=song, path="./suno_downloads")
print(f"Song downloaded to: {song_path}")

# Download generated thumbnail: 
image_url = song.image_url 
image_path = download_image(image_url, SONG_ID)


# Get meta stuff for my video
song_title = song.title
song_user = song.display_name
print("Title: " + song_title)
print("User: " + song_user)

square_image = Image.open(image_path)

# Create a new image
image_width = 1920
image_height = 1080
image_padding = 100

output_image = Image.new("RGB", (image_width, image_height))

# Resize the square image to fit the background, maintaining aspect ratio
bg_image = square_image.resize((image_width, image_height), Image.LANCZOS)
bg_image = darken_image(bg_image, factor=0.3)
bg_image = bg_image.filter(ImageFilter.GaussianBlur(radius=10))

# Paste the background image onto the output image
output_image.paste(bg_image, (0, 0))

# Resize the square image to 50% of the height of the output image
square_image_height = image_height // 2
square_image = square_image.resize((square_image_height, square_image_height), Image.LANCZOS)

# Paste the square image on the left side
x_offset = image_padding
y_offset = (image_height - square_image_height) // 2
output_image.paste(square_image, (x_offset, y_offset))

# Draw the text
draw = ImageDraw.Draw(output_image)

# Load a font
font_path = "arial.ttf" 
title_font = ImageFont.truetype(font_path, 64)
subtitle_font = ImageFont.truetype(font_path, 32)

# Title and subtitle text
title_text =song_title
subtitle_text = song_user

# Calculate text positions
title_x = x_offset + square_image_height + image_padding
title_y = image_height // 2 - 80 
subtitle_x = title_x
subtitle_y = image_height // 2 + 10

# Draw the title and subtitle text
draw.text((title_x, title_y), title_text, font=title_font, fill="white")
draw.text((subtitle_x, subtitle_y), subtitle_text, font=subtitle_font, fill="white")

# Save the output image
output_image_path = "suno_downloads/video_bg_" + SONG_ID + ".png"
output_image.save(output_image_path)

# Create our video
output_video_path = "suno_downloads/output_video_" + SONG_ID + ".mp4"
ffmpeg_command = [
    "ffmpeg",
    "-y",
    "-loop", "1",
    "-i", output_image_path,
    "-i", song_path,
    "-c:v", "libx264",
    "-tune", "stillimage",
    "-c:a", "aac",
    "-b:a", "192k",
    "-pix_fmt", "yuv420p",
    "-shortest",
    output_video_path
]

# Run the ffmpeg command
subprocess.run(ffmpeg_command)

# Let the user choose the youtube channel
youtube = get_authenticated_service()

title = YOUTUBE_TITLE
description = read_file_to_variable('upload_default_description.txt')
        
# Replace variables in the description and title
description = description.replace("{day}", datetime.now().strftime('%Y-%m-%d'))
title = title.replace("{day}", datetime.now().strftime('%Y-%m-%d'))   

description = description.replace("{title}", song_title)
title = title.replace("{title}", song_title)
   
description = description.replace("{user}", song_user)
title = title.replace("{user}", song_user)

# Fill in other preset stuff    
tags = YOUTUBE_TAGS
category_id = YOUTUBE_CATEGORY 

upload_video(youtube, output_video_path, title, description, tags, category_id)
        