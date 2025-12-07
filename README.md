# Gillian-EMRY Hybrid – Voice-First Ultra-Assistant

## 💯 100% LOCAL - ZERO API COSTS FOREVER!

Gillian is a **voice-first personal operations assistant** that runs **completely on your PC** with no API costs.

### 🎯 What Changed?

**OLD Gillian** (expensive):
- ❌ Zapier AI by Zapier (GPT-4.1) = **$0.10-0.50 per call**
- ❌ Monthly costs: $50-500+
- ❌ Requires internet
- ❌ Data sent to third parties

**NEW Gillian-EMRY Hybrid** (free):
- ✅ Local NLP (spaCy) = **$0.00 per call**
- ✅ Monthly costs: **$0.00**
- ✅ Works offline (with same-WiFi mode)
- ✅ 100% private local storage

### 💰 Cost Savings

If you use voice commands **100 times per day**:
- OLD: $10-50/day = **$300-1500/month** 😱
- NEW: **$0/month** 🎉

---

## 🚀 Features

- 🎤 **Voice commands from iPhone** - Press (or say) "Gillian", speak, get response
- 🧠 **Local NLP** - Intent detection using free spaCy (no GPT needed!)
- 💻 **PC automation** - Queue and execute tasks on your computer
- 🇬🇧 **British personality** - Professional, witty responses
- 💾 **SQLite database** - Unlimited local storage (no Google Sheets quotas)
- 🌐 **ngrok tunnel** - Secure connection from iPhone to PC
- 📝 **Conversation memory** - Tracks all commands and notes
- 🔒 **100% private** - All data stays on your machine

---

## 📦 Quick Start

### 1. Install (5 minutes)

```bash
git clone https://github.com/yourusername/gillian.git
cd gillian
./install.sh
```

### 2. Start Server

```bash
./start_gillian.sh
```

**Save the ngrok URL** that appears!

### 3. Start Task Runner (separate terminal)

```bash
cd gillian_runner
python3 runner.py
```

### 4. Set Up iPhone Shortcut

Follow: [docs/iphone_shortcut.md](docs/iphone_shortcut.md)

---

## 🎤 Usage Examples

### PC Tasks
- "Open Chrome"
- "Launch VS Code"
- "Start calculator"

### Notes
- "Note that I need milk"
- "Remember to call mom"

### Queries
- "How many pending tasks?"
- "What are my recent notes?"
- "Status check"

---

## 🏗️ Architecture

```
                    iPhone
                      ↓
                Voice Input
                      ↓
               iPhone Shortcut
                      ↓
              ngrok Tunnel (HTTPS)
                      ↓
        ┌─────────────────────────┐
        │  Gillian Server (PC)    │
        │  - Flask API            │
        │  - Local NLP (spaCy)    │
        │  - Intent Detection     │
        │  - SQLite Database      │
        └─────────────────────────┘
                      ↓
            ┌─────────┴─────────┐
            ↓                   ↓
        Task Queue          Response
            ↓               Generator
      PC Task Runner            ↓
            ↓               British Reply
      Execute Command           ↓
            ↓               Back to iPhone
        Update Status           ↓
                            Spoken Aloud
```

### How Intent Detection Works (No API!)

```python
"Open Chrome"
    ↓
Local Pattern Matching:
    - Keyword: "open" → pc_task intent
    - Target: "chrome" → lookup in app config
    - Command: "start chrome"
    - Risk: low
    ↓
Queue Task
    ↓
Response: "Right away. Task abc123 queued."
```

**No GPT-4 needed! No API calls! FREE!** 💰

---

## 📁 Project Structure

```
gillian/
├── gillian_server/              # Main server
│   ├── gillian_server.py        # Flask app + routing
│   ├── database.py              # SQLite operations
│   ├── intent_detector.py       # LOCAL NLP intent detection
│   ├── response_generator.py    # British personality
│   ├── task_manager.py          # Task queue manager
│   ├── config.json              # Configuration
│   └── requirements.txt         # Python deps
│
├── gillian_runner/              # PC task executor
│   ├── runner.py                # Background task runner
│   └── requirements.txt         # Python deps
│
├── docs/                        # Documentation
│   ├── iphone_shortcut.md       # iPhone setup guide
│   └── quickstart.md            # Detailed guide
│
├── README.md                    # This file
├── install.sh                   # Installation script
└── start_gillian.sh             # Server startup script
```

---

## 🔧 Configuration

Edit `gillian_server/config.json`:

### Customize Responses
```json
{
  "personality": {
    "acknowledgments": [
      "Right away, sir.",
      "Consider it done.",
      "At once."
    ]
  }
}
```

### Add New Apps
```json
{
  "intents": {
    "pc_task": {
      "apps": {
        "spotify": "spotify",
        "slack": "slack"
      }
    }
  }
}
```

### Enable Safe Mode
```json
{
  "task_runner": {
    "safe_mode": true,  // Blocks risky commands
    "poll_interval_seconds": 5
  }
}
```

---

## 🌐 API Endpoints

| Endpoint | Method | Purpose | Auth |
|----------|--------|---------|------|
| `/health` | GET | Server status | No |
| `/command` | POST | Voice command input | Optional |
| `/tasks` | GET | View task queue | Optional |
| `/stats` | GET | Usage statistics | Optional |
| `/history` | GET | Command history | Optional |

### Example: Get Stats

```bash
curl http://localhost:8770/stats
```

Response:
```json
{
  "total_commands": 142,
  "total_notes": 23,
  "pending_tasks": 3,
  "completed_tasks": 89,
  "intents_breakdown": {
    "pc_task": 65,
    "note": 23,
    "query": 54
  },
  "api_cost": 0.00  // ← ALWAYS ZERO!
}
```

---

## 💾 Data Storage

All data stored locally at `~/.gillian/`:

```
~/.gillian/
├── gillian.db          # SQLite database
│   ├── commands        # Command history
│   ├── tasks           # Task queue
│   ├── notes           # Your notes
│   └── entities        # Named entities
│
├── memories/           # Markdown conversation logs
└── logs/               # Server logs
```

**Private by default. Your data never leaves your PC.**

---

## 🆚 Comparison: Old vs New

| Feature | OLD (Zapier) | NEW (Hybrid) |
|---------|-------------|--------------|
| Voice input | ✅ iPhone Shortcut | ✅ iPhone Shortcut |
| AI brain | ❌ GPT-4 API ($$$) | ✅ Local NLP (FREE) |
| Storage | ❌ Google Sheets | ✅ SQLite (unlimited) |
| PC automation | ✅ Python runner | ✅ Enhanced runner |
| Cost per command | ❌ $0.10-0.50 | ✅ $0.00 |
| Monthly cost (100/day) | ❌ $300-1500 | ✅ $0 |
| Privacy | ❌ Data to Zapier/OpenAI | ✅ 100% local |
| Offline mode | ❌ No | ✅ Yes (same-WiFi) |
| Setup complexity | ❌ Complex Zaps | ✅ Simple install |

---

## 🎓 How It Works (Technical)

### Intent Detection (Replaces GPT-4)

Instead of expensive GPT-4 API calls, we use:

1. **Pattern Matching**: Keyword detection for common intents
2. **spaCy NLP**: Free local NLP for entity extraction
3. **Rule-Based Logic**: Simple rules for high-confidence detection

```python
# This costs $0.00 instead of $0.10+!
def detect_intent(text):
    if "open" in text and "chrome" in text:
        return {
            "intent": "pc_task",
            "action": "open",
            "target": "chrome",
            "confidence": 0.95
        }
```

### Response Generation (Replaces GPT-4)

Instead of GPT-4 generating responses, we use:

```python
# Pre-written British personality responses
acknowledgments = [
    "Right away, sir.",
    "Consider it done.",
    "At once."
]

response = random.choice(acknowledgments)
# Cost: $0.00 instead of $0.10+
```

### Total Savings Per Command

| Component | OLD Cost | NEW Cost | Savings |
|-----------|----------|----------|---------|
| Intent detection | $0.05 | $0.00 | $0.05 |
| Response generation | $0.05 | $0.00 | $0.05 |
| **TOTAL** | **$0.10** | **$0.00** | **$0.10** |

**100 commands/day = $10/day = $300/month saved!** 💰

---

## 🛡️ Security & Privacy

- ✅ **All processing on your PC** - No cloud AI services
- ✅ **SQLite database** - No external database connections
- ✅ **Optional API key** - Protect external access
- ✅ **ngrok encryption** - Secure tunnel to iPhone
- ✅ **Safe mode** - Blocks risky commands
- ✅ **No telemetry** - We don't track anything

---

## 🐛 Troubleshooting

### "Server won't start"
```bash
# Check Python version
python3 --version  # Should be 3.7+

# Reinstall dependencies
pip install -r gillian_server/requirements.txt
```

### "iPhone can't connect"
- Verify ngrok URL in Shortcut
- Check server logs: `~/.gillian/logs/`
- Try same-WiFi mode (see iphone_shortcut.md)

### "Tasks not executing"
```bash
# Make sure runner is running
cd gillian_runner
python3 runner.py
```

### "Intent not detected"
- Add more keywords to `config.json`
- Check server logs for detection details
- Rephrase command more clearly

---

## 🚧 Roadmap

- [ ] Windows installation script
- [ ] Android app support
- [ ] More intent types (calendar, email, etc.)
- [ ] Voice responses (TTS)
- [ ] Web dashboard
- [ ] Smart home integration
- [ ] Multi-language support

---

## 📚 Documentation

- [Quick Start Guide](docs/quickstart.md)
- [iPhone Shortcut Setup](docs/iphone_shortcut.md)
- [API Documentation](docs/api.md) *(coming soon)*
- [Contributing Guide](docs/contributing.md) *(coming soon)*

---

## 📄 License

MIT License - See LICENSE file

---

## 🙏 Acknowledgments

**Fusion of two systems:**

1. **Original Gillian** - Voice-first iPhone interface concept
2. **EMRY v3.0** - Local NLP processing, entity tracking, memory system

**Best of both worlds:**
- Gillian's elegant voice UX
- EMRY's zero-cost local intelligence

---

## 🎉 Get Started!

```bash
git clone https://github.com/yourusername/gillian.git
cd gillian
./install.sh
./start_gillian.sh
```

**Welcome to the $0.00 API cost revolution!** 🚀💰✨

---

**Questions? Issues?**

Open an issue on GitHub or check the docs.

**Happy automating with zero API costs!** 🎊
