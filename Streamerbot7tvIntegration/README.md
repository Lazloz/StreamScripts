# 7TV Emote Adder for Streamer.bot

This Streamer.bot action allows viewers to add emotes to your 7TV emote set using either direct emote IDs or 7TV URLs.

## Features

- ✅ Accept both 7TV URLs (`https://7tv.app/emotes/EMOTE_ID`) and direct emote IDs
- ✅ Automatic URL parsing and validation
- ✅ Comprehensive error handling and logging
- ✅ Ready for channel point rewards, chat commands, or manual triggers

## Setup Instructions

### 1. Import the Function

Copy and paste this code into a new C# action in Streamer.bot:

```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
```

### 2. Get Your 7TV Auth Token

⚠️ **IMPORTANT**: This token is essentially your password. Never share it with anyone!

1. Go to [7tv.app](https://7tv.app) and make sure you're logged in
2. Open your browser's developer console:
   - **Chrome/Edge**: Press `F12` or `Ctrl+Shift+I`
   - **Firefox**: Press `F12` or `Ctrl+Shift+K`
3. Go to the **Console** tab
4. Type this command and press Enter:
   ```javascript
   localStorage.getItem("7tv-auth-token")
   ```
5. Copy the token that appears (it should be a long string)
6. In Streamer.bot, change the "Set Argument" sub-action before your C# code:
   - **Argument Name**: `bearerToken`
   - **Value**: Paste your token (without quotation marks) here

> **Note**: This token may expire periodically. If the action stops working, you'll need to repeat this step to get a new token.

### 3. Get Your Emote Set ID

1. Navigate to your emote set on 7TV
2. The URL in the address bar will look like this:
   ```
   https://7tv.app/emote-sets/01FPE4GDKG000FZADBM40VTXC6
   ```
3. Copy the ID after `https://7tv.app/emote-sets/` (in this example: `01FPE4GDKG000FZADBM40VTXC6`)
4. In Streamer.bot, add another "Set Argument" sub-action:
   - **Argument Name**: `setId`
   - **Value**: Paste your emote set ID here

### 4. Set Up Your Trigger

I've configured this as a **Channel Point Reward** by default, but you can change it to whatever you prefer:

#### Channel Point Reward Setup:
1. Create a new Channel Point Reward in Streamer.bot
2. Set it to require user input
3. Link it to your 7TV emote action
4. The `%rawInput%` will automatically be passed as the emote URL/ID

#### Alternative Setups:
- **Chat Command**: Create a command like `!addemote` with `%rawInput%` as the argument
- **Manual Trigger**: Set specific emote IDs directly in the arguments

## Usage Examples

Once set up, viewers can use either format:

**With 7TV URL:**
```
https://7tv.app/emotes/01F7M225F8000AWSXNQ65M4PKG
```

**With direct emote ID:**
```
01F7M225F8000AWSXNQ65M4PKG
```

## Troubleshooting

- **"Bearer token is required"**: Make sure you've set the `bearerToken` argument with your 7TV auth token
- **"Set ID is required"**: Make sure you've set the `setId` argument with your emote set ID
- **"Invalid emote ID or 7TV URL format"**: Check that the URL/ID is correct
- **Action stops working**: Your auth token may have expired - repeat step 2

## Security Note

Your 7TV auth token has the same permissions as your account. Keep it secure and never share it publicly!

---

**Have fun adding emotes to your set! 🎉**