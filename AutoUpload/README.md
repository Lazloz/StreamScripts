# VOD Autouploader

Upload your latest vod file with your latest stream title and some default values to Youtube. You can also rescale the file if needed.

This script was written by Lazloz  
Visit me: [https://twitch.tv/Lazloz](https://twitch.tv/Lazloz)  

## Requirements
- Python (tested on Python 3.10.11)
- Twitch channel
- Google account with YouTube channel
- ffmpeg in path (get the full release [here](https://ffmpeg.org/))

## Setup
1. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
2. Setup an application in the Google Cloud with access to the YouTube Data API v3 (you don't need to publish it):
    1. Setup the OAuth consent screen (select "External" and "Desktop App" if asked)
    2. Create an OAuth client ID
    3. Download the JSON for it
    4. Paste the content of the JSON file to `client_secrets_youtube_vod.json`
3. Modify `vod_upload_settings.py` as needed
4. Update `vod_default_description.txt` with your default description. It allows for a `{date}` variable that will be replaced with the current day.
5. Run the `auto_upload.py` script and enjoy. You can use tools like streamer.bot to start the script automatically.

## How to Get a Twitch Client ID from the Developer Console

1. Go to the [Twitch Developer Console](https://dev.twitch.tv/console).
2. Log in with your Twitch account.
3. Click on the "Applications" tab.
4. Click on the "Register Your Application" button.
5. Fill out the form:
    - **Name**: Give your application a name.
    - **OAuth Redirect URLs**: Enter the following redirect URL `http://localhost:8008`
    - **Category**: Select a category for your application. I would recommend Website Integration
    - **Client Type**: Select public.
6. Click the "Create" button.
7. After creating your application, you'll be redirected to the application's details page. Here you will find your **Client ID**.
8. Paste it to the `vod_upload_settings.py`