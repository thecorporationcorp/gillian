# Gillian – Voice-First Ultra-Assistant

Gillian is a **voice-first personal operations assistant** driven by:

- iPhone Shortcuts (minimal, 3–4 actions)
- Zapier Webhooks + AI by Zapier (GPT-4.1)
- Google Sheets (behavior + PC task queues)
- A PC runner that executes queued tasks

You press (or say) **"Gillian"**, speak your command, and the system:

1. Captures your voice on iPhone.
2. Sends the text to a Zapier webhook.
3. Runs Gillian's AI brain (strict JSON schema).
4. Logs behavior/task data into Google Sheets.
5. Optionally executes PC automations via the runner.
6. Speaks back a **short British reply** on your phone.

---

## Core Pieces

- **iPhone Shortcut** – _Minimal_: Speak → Dictate Text → POST to Zapier → Speak response.
- **Zapier Zap – "Gillian – Command In"**
  - Trigger: Webhooks by Zapier (Catch Hook)
  - AI: AI by Zapier (GPT-4.1) with a strict JSON persona prompt
  - Response: Returns `speak_text` as **plain text** (no JSON)
  - Paths:
    - Behavior log → `Gillian_Behavior_Log` sheet
    - PC tasks → `Gillian_PC_Tasks` sheet
- **Google Sheets**
  - `Gillian_Behavior_Log`
  - `Gillian_PC_Tasks`
- **PC Runner**
  - Polls `Gillian_PC_Tasks`
  - Executes `ps_code` shell commands (PowerShell-friendly)
  - Updates status, completed_time, last_error

---

## Minimal iPhone Shortcut (Conceptual)

Actions:

1. **Speak Text**  
   - Text: `At your service, Michael.`

2. **Dictate Text**  
   - Result variable: `Dictated Text`

3. **Get Contents of URL**
   - URL: `https://hooks.zapier.com/hooks/catch/XXXXXXXX/YYYYYYYY/` (your Zap URL)
   - Method: `POST`
   - Request Body: `JSON`
   - Field:
     - Key: `text`
     - Value: `Dictated Text`

4. **Speak Text**
   - Text: (Result of `Get Contents of URL`)
   - This is Gillian's `speak_text` returned by Zapier.

See `docs/shortcut_setup.md` for a step-by-step build description.

---

## Zapier – "Gillian – Command In"

High-level steps:

1. **Trigger: Webhooks by Zapier – Catch Hook**
   - Expects JSON:
     ```json
     {
       "text": "string",
       "device": "iphone",
       "source": "gillian_command",
       "client_time": "string (optional)"
     }
     ```

2. **AI by Zapier – Analyze and Return Data**
   - Model: GPT-4.1
   - System prompt: `config/system_prompt.txt`
   - Output fields (JSON):
     - `mode`
     - `speak_text`
     - `pc_task` (object or null)
     - `behavior_update` (object or null)

3. **Custom Response Layer (via Code by Zapier or Webhook custom request)**
   - HTTP response back to caller (Shortcut) is:
     - Body: `speak_text` (plain text)
     - Status: 200
     - `Content-Type: text/plain`
   - No `attempt`, `request_id`, or other JSON noise.

4. **Paths for logging**

   - **Path A – Behavior log (if `behavior_update` exists)**
     - App: Google Sheets
     - Spreadsheet: `Gillian_Behavior_Log`
     - Columns:
       - `timestamp`
       - `utterance`
       - `intent`
       - `duration_minutes`
       - `escalation_level`
       - `tags`

   - **Path B – PC tasks (if `pc_task` exists)**
     - App: Google Sheets
     - Spreadsheet: `Gillian_PC_Tasks`
     - Columns:
       - `task_id`
       - `summary`
       - `ps_code`
       - `risk_level`
       - `status` (default "pending")
       - `queued_time`
       - `completed_time`
       - `last_error`

Zapier config is documented structurally in `config/zapier_config.json`.

---

## PC Runner

Location: `pc_runner/runner.py`

Responsibilities:

- Poll `Gillian_PC_Tasks` every N seconds.
- Select rows where `status == "pending"`.
- Execute `ps_code` in a shell (PowerShell-friendly).
- Update `status` → "completed" or "error".
- Set `completed_time` and `last_error` as needed.

You can run it via:

```bash
cd pc_runner
pip install -r requirements.txt
python runner.py
```

You'll need Google API credentials configured (see comments in `runner.py`).

---

## Data Contracts

See `docs/api_spec.md` for full JSON schemas, including:

- iPhone → Zapier
- Zapier → AI
- AI → Zapier
- Zapier → iPhone
- Zapier ↔ Google Sheets
- Google Sheets ↔ PC Runner

---

## Next Extensions

- More PC automation task templates (open apps, rearrange files, backups).
- Smarter behavior analysis and escalation levels.
- Optional replacement of Sheets with a database.
- Optional standalone app to replace iOS Shortcuts.

---

## License

See `LICENSE` (MIT License)