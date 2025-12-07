# iPhone Shortcut Setup Guide

## How to Connect Your iPhone to Gillian (Voice Commands)

### Step 1: Get Your ngrok URL

1. Start the Gillian server: `./start_gillian.sh`
2. The server will print an ngrok URL like: `https://abcd1234.ngrok.io`
3. **Save this URL** - you'll need it for the iPhone Shortcut

### Step 2: Create the iPhone Shortcut

1. Open the **Shortcuts** app on your iPhone
2. Tap the **+** button to create a new shortcut
3. Add these actions **in order**:

---

#### Action 1: Speak Text
- **Action**: `Speak Text`
- **Text**: `At your service.`
- **Wait Until Finished**: YES

---

#### Action 2: Dictate Text
- **Action**: `Dictate Text`
- This captures your voice command
- Result variable: `Dictated Text`

---

#### Action 3: Get Contents of URL
- **Action**: `Get Contents of URL`
- **URL**: `https://YOUR-NGROK-URL.ngrok.io/command`
  - Replace `YOUR-NGROK-URL` with the URL from Step 1
  - **IMPORTANT**: Add `/command` at the end!
- **Method**: `POST`
- **Request Body**: `JSON`
- **Fields**:
  - Key: `text` → Value: `Dictated Text` (from step 2)
  - Key: `device` → Value: `iphone`
  - Key: `client_time` → Value: `Current Date` (formatted as ISO 8601)

---

#### Action 4: Speak Text
- **Action**: `Speak Text`
- **Text**: `Contents of URL` (result from step 3)
- This speaks Gillian's response!

---

### Step 3: Configure Shortcut Settings

1. Tap the shortcut name at top
2. Rename it to: **Gillian**
3. Tap the **info icon** (ℹ️)
4. Enable: **Show in Share Sheet** (optional)
5. Enable: **Add to Home Screen** (recommended)
6. Choose an icon (suggestion: blue gear or robot)

### Step 4: Add to Back Tap (Optional but AMAZING!)

1. Go to iPhone **Settings**
2. **Accessibility** → **Touch** → **Back Tap**
3. Choose **Double Tap** or **Triple Tap**
4. Select your **Gillian** shortcut

Now you can activate Gillian by tapping the back of your iPhone! 🤯

---

## Usage Examples

### PC Tasks
- **"Open Chrome"** → Opens Chrome browser
- **"Open VS Code"** → Opens Visual Studio Code
- **"Launch Firefox"** → Opens Firefox

### Notes
- **"Note that I need to buy milk"** → Saves a note
- **"Remember to call Sarah tomorrow"** → Saves a reminder

### Queries
- **"How many pending tasks?"** → Returns task count
- **"What are my recent notes?"** → Returns last notes
- **"What's the status?"** → Status update

---

## Troubleshooting

### "I'm afraid I didn't quite catch that"
- Server couldn't parse your command
- Try rephrasing more clearly
- Check server logs for details

### No response / timeout
- Check if server is running: `./start_gillian.sh`
- Verify ngrok URL is correct in shortcut
- Check ngrok didn't change (restart ngrok to get new URL)

### "Unauthorized" error
- If you set an API key, add it to the shortcut:
- In "Get Contents of URL", add Header:
  - Key: `Authorization`
  - Value: `Bearer YOUR_API_KEY`

---

## Advanced: Using Without ngrok (Same WiFi Only)

If your iPhone is on the same WiFi network as your PC:

1. Find your PC's local IP address:
   - Linux/Mac: `hostname -I` or `ifconfig`
   - Windows: `ipconfig`
2. In the shortcut, use: `http://YOUR_PC_IP:8770/command`
3. Example: `http://192.168.1.100:8770/command`

**Note**: This only works when iPhone is on the same WiFi network!

---

## Cost Comparison

| Method | Cost Per Command |
|--------|-----------------|
| Zapier AI by Zapier (GPT-4) | $0.10 - $0.50 |
| **Gillian-EMRY Hybrid** | **$0.00** ✨ |

**You're saving money with every command!** 💰
