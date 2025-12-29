# 🚀 GILLIAN - COMPLETE WINDOWS INSTALLATION GUIDE

## ⚠️ IMPORTANT: DO EVERY SINGLE STEP IN ORDER

---

## 📋 **STEP 1: OPEN POWERSHELL**

1. Press `Windows Key + X`
2. Click **"Windows PowerShell"** or **"Terminal"**
3. You should see a blue window

---

## 📥 **STEP 2: CLONE THE REPOSITORY**

**Copy and paste this EXACT command:**

```powershell
cd $HOME\Desktop
git clone https://github.com/thecorporationcorp/gillian.git
cd gillian
```

**What this does:**
- Goes to your Desktop
- Downloads all the code from GitHub
- Opens the gillian folder

**Expected output:** You should see "Cloning into 'gillian'..."

---

## 🐍 **STEP 3: CHECK PYTHON**

**Run this command:**

```powershell
python --version
```

**Expected output:** `Python 3.x.x`

**If you see an error:**
1. Download Python from: https://www.python.org/downloads/
2. During install, CHECK ✅ "Add Python to PATH"
3. Restart PowerShell
4. Try again

---

## 📦 **STEP 4: INSTALL DEPENDENCIES**

**Run these commands ONE AT A TIME:**

```powershell
# Upgrade pip
python -m pip install --upgrade pip

# Install Flask
python -m pip install flask

# Install Flask-CORS
python -m pip install flask-cors

# Optional: Install spaCy (for better AI)
python -m pip install spacy
```

**Expected output:** "Successfully installed..."

---

## 🚀 **STEP 5: START THE SERVER**

**Run this command:**

```powershell
python gillian_server/gillian_advanced.py
```

**Expected output:**
```
╔════════════════════════════════════════════╗
║  GILLIAN AI - PRODUCTION GRADE ASSISTANT   ║
╚════════════════════════════════════════════╝

🚀 Server: http://0.0.0.0:8770
🧠 AI: Advanced NLP with Learning
📱 PWA: Enabled

Ready! Press Ctrl+C to stop.

 * Running on http://127.0.0.1:8770
```

**Leave this window OPEN!** The server must stay running.

---

## 🌐 **STEP 6: OPEN IN BROWSER**

1. Open **Chrome** or **Edge**
2. Go to: `http://localhost:8770`

**You should see:**
- Purple/blue gradient background
- "Good day, I'm Gillian" message
- Big microphone button

---

## 🎤 **STEP 7: TEST IT**

1. **Click** the microphone button
2. **Allow** microphone access (if asked)
3. **Hold** the button and say: **"Hello Gillian"**
4. **Release** the button

**You should get a response!**

---

## 🐛 **IF IT DOESN'T WORK:**

### **Problem: "python: command not found"**
**Solution:**
```powershell
# Try python3 instead
python3 --version
# If that works, use python3 in all commands
```

### **Problem: "No module named flask"**
**Solution:**
```powershell
# Reinstall Flask
python -m pip install --force-reinstall flask flask-cors
```

### **Problem: "Address already in use"**
**Solution:**
```powershell
# Kill anything on port 8770
netstat -ano | findstr :8770
# Note the PID number at the end
taskkill /PID <number> /F
# Then start the server again
```

### **Problem: "localhost refused to connect"**
**Solution:**
- Make sure the Python server is still running (step 5)
- Try: `http://127.0.0.1:8770` instead
- Check Windows Firewall isn't blocking it

---

## ✅ **VERIFICATION CHECKLIST**

Before asking for help, verify:

- [ ] Python is installed (`python --version`)
- [ ] You cloned the repo (`cd gillian` works)
- [ ] Dependencies installed (no errors in step 4)
- [ ] Server is running (you see "Running on http://127.0.0.1:8770")
- [ ] PowerShell window is still open
- [ ] Browser is at `http://localhost:8770`

---

## 📸 **WHAT YOU SHOULD SEE**

**In PowerShell:**
```
 * Running on http://127.0.0.1:8770
 * Running on http://0.0.0.0:8770
```

**In Browser:**
- Dark background
- "Gillian AI" logo at top
- Welcome message
- Microphone button (purple/blue)
- Text input box

---

## 🆘 **STILL NOT WORKING?**

**Run this diagnostic command:**

```powershell
# Check if files exist
dir gillian_server\gillian_advanced.py
dir pwa\index.html

# Check if server starts
python gillian_server\gillian_advanced.py
```

**Send me the EXACT error message you see!**

---

## 💡 **QUICK COMMANDS REFERENCE**

```powershell
# Navigate to project
cd $HOME\Desktop\gillian

# Start server
python gillian_server\gillian_advanced.py

# Stop server
# Press Ctrl+C in the PowerShell window

# Restart server
# Ctrl+C, then run start command again
```

---

## 🎯 **THAT'S IT!**

If you followed every step:
- ✅ Python is installed
- ✅ Code is downloaded
- ✅ Dependencies are installed
- ✅ Server is running
- ✅ Browser is open to http://localhost:8770

**You should have a working voice AI assistant with ZERO API costs!**

---

## 🔄 **TO RUN IT LATER:**

1. Open PowerShell
2. Run:
   ```powershell
   cd $HOME\Desktop\gillian
   python gillian_server\gillian_advanced.py
   ```
3. Open browser to `http://localhost:8770`

---

**Need help? Tell me EXACTLY which step failed and the error message.**
