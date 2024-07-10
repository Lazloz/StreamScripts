# Paste your channel name here. Create the client id yourself. It's explained in the readme
TWITCH_CLIENT_ID = ''
TWITCH_CHANNEL_NAME = 'lazloz'

# Default vod information. The script takes your current twitch title as youtube title!
YOUTUBE_TAGS = ["sample tag 1", "sample tag 2"]
# Category ID index: https://mixedanalytics.com/blog/list-of-youtube-video-category-ids/
YOUTUBE_CATEGORY = '20'
YOUTUBE_PRIVACY = 'private'

# If you want to upscale the video put in your preferred resolution, put in -1 otherwise
UPSCALE_WIDTH=1920
UPSCALE_HEIGHT=1080

# Where are your vods stored?
VOD_FOLDER = 'C:/Users/Lazloz/Videos/vods'
# What's the file format of your vod files?
FILE_SUFFIX = '.mkv'

# Shall the script shutdown the pc after it is run (e.g. because you stream into the night and want to render overnight). Allows True or False. Only works on Windows
SHUTDOWN = False
# Shall the script delete the upscaled and original vod files?
DELETE_VOD_FILES_AFTER = True