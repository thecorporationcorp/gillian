## Gillian-EMRY Hybrid - Quick Start Guide

### 🎯 What is This?

A **100% FREE** voice-first personal assistant that runs entirely on your PC - no API costs!

- ✅ Voice commands from iPhone
- ✅ Local NLP (no GPT-4 costs)
- ✅ PC task automation
- ✅ British personality
- ✅ Full conversation memory
- ✅ SQLite database (unlimited storage)

### 💰 Cost Savings

- **OLD** (Zapier + GPT-4): $0.10-0.50 per command
- **NEW** (Gillian-EMRY): **$0.00 per command**

If you use it 100 times/day, you save **$10-50/day** = **$300-1500/month**!

---

## Installation (5 minutes)

### Linux/Mac:
```bash
cd gillian
./install.sh
```

### Windows:
*Coming soon - for now use WSL or Linux*

---

## Usage

### 1. Start the Server
```bash
./start_gillian.sh
```

This starts:
- Flask server on port 8770
- ngrok tunnel (for iPhone access)
- NLP engine (local spaCy)

**Save the ngrok URL** that prints out - you need it for iPhone!

### 2. Start the Task Runner (separate terminal)
```bash
cd gillian_runner
python3 runner.py
```

This polls the task queue and executes PC commands.

### 3. Set Up iPhone Shortcut

Follow: `docs/iphone_shortcut.md`

---

## Example Commands

### PC Tasks
- "Open Chrome"
- "Launch VS Code"
- "Start Firefox"
- "Open calculator"

### Notes
- "Note that I need to buy milk"
- "Remember to call mom tomorrow"
- "Log meeting at 3pm"

### Queries
- "How many pending tasks?"
- "What are my recent notes?"
- "Status check"

---

## How It Works

```
iPhone (you speak)
      ↓
   "Open Chrome"
      ↓
iPhone Shortcut (dictate text)
      ↓
POST to ngrok URL
      ↓
Gillian Server (your PC)
      ↓
Intent Detector (LOCAL NLP - FREE!)
   → Detects: "pc_task" intent
   → Action: "open"
   → Target: "chrome"
      ↓
Task Queue (SQLite)
   → Saves: task_id, command, risk_level
      ↓
Response Generator
   → "Right away. Task abc123 queued."
      ↓
iPhone speaks response
      ↓
PC Runner (separate process)
   → Polls queue every 5 seconds
   → Executes: "start chrome"
   → Updates status: "completed"
```

---

## File Structure

```
gillian/
├── gillian_server/           # Main server
│   ├── gillian_server.py     # Flask app
│   ├── database.py           # SQLite handler
│   ├── intent_detector.py    # LOCAL NLP (replaces GPT-4)
│   ├── response_generator.py # British personality
│   ├── task_manager.py       # Task queue
│   └── config.json           # Settings
│
├── gillian_runner/           # PC task executor
│   └── runner.py             # Task runner
│
├── docs/                     # Documentation
│   ├── iphone_shortcut.md    # iPhone setup
│   └── quickstart.md         # This file
│
├── install.sh                # Installation script
└── start_gillian.sh          # Server startup
```

---

## Data Storage

All data stored locally at: `~/.gillian/`

```
~/.gillian/
├── gillian.db         # SQLite database
│   ├── commands       # Command history
│   ├── tasks          # Task queue
│   ├── notes          # Your notes
│   └── entities       # People/places/things
│
├── memories/          # Markdown conversation logs
└── logs/              # Server logs
```

---

## Configuration

Edit `gillian_server/config.json`:

### Change Port
```json
"server": {
  "port": 8770  ← change this
}
```

### Add ngrok Auth Token (for better stability)
```json
"ngrok_authtoken": "your_token_here"
```
Get token from: https://dashboard.ngrok.com/get-started/your-authtoken

### Customize Personality
```json
"personality": {
  "acknowledgments": [
    "Right away, sir.",
    "Your wish is my command."  ← add custom phrases
  ]
}
```

### Add New Intents
```json
"intents": {
  "pc_task": {
    "apps": {
      "spotify": "spotify"  ← add new apps
    }
  }
}
```

---

## Advanced Features

### API Endpoints

- `GET /health` - Server status
- `POST /command` - Voice command (used by iPhone)
- `GET /tasks` - View task queue
- `GET /stats` - Usage statistics
- `GET /history` - Command history

### Example: Get Stats
```bash
curl http://localhost:8770/stats
```

Returns:
```json
{
  "total_commands": 142,
  "total_notes": 23,
  "pending_tasks": 3,
  "completed_tasks": 89,
  "api_cost": 0.00  ← ALWAYS ZERO!
}
```

---

## Troubleshooting

### Server won't start
- Check Python 3.7+ installed: `python3 --version`
- Install dependencies: `pip install -r gillian_server/requirements.txt`

### ngrok not working
- Install pyngrok: `pip install pyngrok`
- Get auth token: https://dashboard.ngrok.com/
- Add to config.json

### iPhone can't connect
- Verify ngrok URL in Shortcut
- Check server logs
- Try same-WiFi method (see iphone_shortcut.md)

### Tasks not executing
- Make sure runner is running: `python3 gillian_runner/runner.py`
- Check task queue: `curl http://localhost:8770/tasks`
- Check runner logs

---

## FAQ

**Q: Do I need an OpenAI API key?**
A: NO! This is 100% local. No API keys needed.

**Q: Does this work offline?**
A: Server works offline, but iPhone needs internet to reach ngrok tunnel. Use same-WiFi mode for true offline.

**Q: Can I use Google Home / Alexa instead of iPhone?**
A: Not yet, but possible! ngrok URL works with any HTTP client.

**Q: Is my data private?**
A: YES! Everything stored locally on your PC. Nothing sent to cloud (except through ngrok tunnel which is encrypted).

**Q: What's the catch?**
A: No catch! Just learning and building cool stuff. 🚀

---

## What's Next?

- [ ] Add more intent types
- [ ] Connect to calendar
- [ ] Email integration
- [ ] Smart home control
- [ ] Android app
- [ ] Voice responses (TTS)

---

## Support

Having issues? Open an issue on GitHub or check the logs:
- Server logs: `~/.gillian/logs/`
- Runner logs: Console output

---

**Enjoy your $0.00 API cost voice assistant!** 🎉💰✨
