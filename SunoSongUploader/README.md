# Suno to Youtube Song Upload Script
Create a video from a suno song automatically and upload it to Youtube. It creates a static 16:9 image for your video and bundles it with your song.

This script was written by [Lazloz](https://twitch.tv/Lazloz)

## Requirements
- Python (tested on Python 3.10.11 but newer versions should work fine)
- Google account with a YouTube channel
- `ffmpeg` in path (you can download it [here](https://ffmpeg.org/))

## Setup
1. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

2. **Setup Google Cloud Application**
   - Access the [Google Cloud Console](https://console.cloud.google.com/).
   - Enable the YouTube Data API v3.
   - **OAuth Consent Screen**: Select external and Desktop App if asked.
   - **Create OAuth Client ID**: Download the JSON file for it.
   - **Save Credentials**: Paste the content of the JSON file into `client_secrets_youtube_vod.json`.

3. **Configuration**
   - Edit `song_uploader_upload_settings.py` to change any necessary settings.
   - Update `upload_default_description.txt` with your default description. You can use the `{date}` variable, which will be replaced with the current date, the `{title}` variable, which will be replaced with your songs name on suno and `{user}`, which will be replaced with your suno usernae. 

4. **Suno Token**
   - Obtain your Suno token following the instructions under "Prerequisites" on this [unofficial Suno API GitHub page](https://github.com/Malith-Rukshan/Suno-API).
   - Save the token into `suno_token.txt`.

5. **Run the Script**
   ```sh
   python song_uploader.py
   ```

   You can automate this process using tools like `streamer.bot`.

Enjoy uploading your songs to YouTube!

## Shoutouts 
- [Malith-Rokshans Suno library](https://github.com/Malith-Rukshan/Suno-API) which made building this script easy.
