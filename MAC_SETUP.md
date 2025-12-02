# 🍎 macOS Setup Guide

Complete instructions for running the Concurrent File Server on macOS.

---

## 📋 Prerequisites

1. **macOS** (any recent version)
2. **Python 3.7+** (usually pre-installed on modern macOS)
3. **Terminal** (built-in application)

---

## 🚀 Quick Setup (5 Minutes)

### Step 1: Check Python Installation

Open **Terminal** (Cmd+Space, type "Terminal", press Enter) and run:

```bash
python3 --version
```

If Python is not installed, download from: https://www.python.org/downloads/mac-osx/

---

### Step 2: Navigate to Project Folder

```bash
cd /path/to/Abhi_2
```

Example:
```bash
cd ~/Desktop/Abhi_2
```

---

### Step 3: Make Scripts Executable

```bash
chmod +x start_all.sh start_server.sh start_web.sh
```

---

### Step 4: Install Dependencies

```bash
pip3 install -r requirements.txt
```

---

### Step 5: Start the Server

```bash
./start_all.sh
```

---

### Step 6: Open Browser

Navigate to: **http://localhost:5000**

✅ **Done!** You can now upload and download files.

---

## 🎯 Running Methods

### Method 1: Everything at Once (Easiest)

```bash
./start_all.sh
```

Both servers start together. Open: http://localhost:5000

---

### Method 2: Separate Terminals (Better Control)

**Terminal Window 1 - File Server:**
```bash
./start_server.sh
```

**Terminal Window 2 - Web Interface:**
```bash
./start_web.sh
```

Then open: http://localhost:5000

---

### Method 3: Manual Python Commands

**Terminal 1:**
```bash
python3 file_server.py
```

**Terminal 2:**
```bash
python3 web_interface.py
```

---

## 🔧 Troubleshooting

### Problem: "Permission denied"

**Solution:**
```bash
chmod +x *.sh
```

---

### Problem: "python3: command not found"

**Solution:** Install Python from https://www.python.org/downloads/mac-osx/

Or using Homebrew:
```bash
brew install python3
```

---

### Problem: "No module named 'flask'"

**Solution:**
```bash
pip3 install flask flask-cors
```

---

### Problem: "Address already in use"

**Solution:** Kill existing processes
```bash
# Kill process on port 9999
lsof -ti:9999 | xargs kill -9

# Kill process on port 5000
lsof -ti:5000 | xargs kill -9
```

---

### Problem: Can't access localhost:5000

**Solutions:**
1. Check if web interface is running (should see output in terminal)
2. Try: http://127.0.0.1:5000
3. Check firewall: System Preferences → Security & Privacy → Firewall

---

## 📱 How to Use

### Upload Files
1. Open http://localhost:5000
2. Drag & drop files OR click "Choose File"
3. Files appear in available files list

### Download Files
1. Click "Download" button
2. File downloads to: **~/Downloads/** (your Mac's Downloads folder)

### Delete Files
1. Click "Delete" button
2. Confirm deletion

---

## 🧪 Test Concurrent Downloads

1. Open http://localhost:5000 in **3 browser tabs**
2. Download different files in each tab simultaneously
3. Watch the server terminal - you'll see multiple threads!

Example output:
```
[SERVER] ClientThread-1: Sending sample.txt
[SERVER] ClientThread-2: Sending sample_script.py
[SERVER] ClientThread-3: Sending solutions.docx
```

---

## 🛑 Stopping Servers

Press **Ctrl+C** in the terminal(s) running the servers.

Or kill all:
```bash
pkill -f "python3 file_server.py"
pkill -f "python3 web_interface.py"
```

---

## 🆘 Quick Commands Reference

```bash
# Navigate to project
cd ~/Desktop/Abhi_2

# Install dependencies
pip3 install -r requirements.txt

# Make scripts executable
chmod +x *.sh

# Start everything
./start_all.sh

# Start only file server
./start_server.sh

# Start only web interface
./start_web.sh

# Check what's running on ports
lsof -i:9999    # File server
lsof -i:5000    # Web interface

# Kill processes by port
lsof -ti:9999 | xargs kill -9
lsof -ti:5000 | xargs kill -9
```

---

## 📁 Project Structure

```
Abhi_2/
├── file_server.py          # Multi-threaded TCP server
├── file_client.py          # Client module
├── web_interface.py        # Flask web application
├── config.py               # Configuration
├── requirements.txt        # Python dependencies
├── README.md              # Full documentation
├── QUICKSTART.txt         # Quick start guide
├── MAC_SETUP.md           # This file (macOS specific)
├── start_all.sh           # Start both servers (macOS)
├── start_server.sh        # Start file server (macOS)
├── start_web.sh           # Start web interface (macOS)
├── start_all.bat          # Windows version
├── start_server.bat       # Windows version
├── start_web.bat          # Windows version
├── templates/
│   └── index.html         # Web UI
├── server_files/          # Files available for download
└── downloads/             # Temporary cache
```

---

## 🔍 Key Differences from Windows

| Feature | Windows | macOS |
|---------|---------|-------|
| Python command | `python` | `python3` |
| Pip command | `pip` | `pip3` |
| Script extension | `.bat` | `.sh` |
| Make executable | Not needed | `chmod +x *.sh` |
| Path separator | `\` | `/` |

---

## ✅ Verification Checklist

Before using, verify:

- [ ] Python 3 installed: `python3 --version`
- [ ] Pip installed: `pip3 --version`
- [ ] Scripts executable: `ls -l *.sh` (should show 'x' permission)
- [ ] Dependencies installed: `pip3 list | grep -i flask`
- [ ] File server starts without errors
- [ ] Web interface starts without errors
- [ ] Can access http://localhost:5000
- [ ] Can upload files
- [ ] Can download files (check ~/Downloads/)
- [ ] Can see concurrent threads in server console

---

## 🎓 How It Works

1. **File Server** (port 9999) - Handles file transfers using multi-threading
2. **Web Interface** (port 5000) - Provides web UI and acts as a client
3. **Concurrent Model** - Each download gets its own thread
4. **Chunked Transfer** - Files sent in 1000-byte chunks with 200ms delays

---

## 💡 Tips

- Use `./start_all.sh` for easiest startup
- Keep terminal windows visible to see server activity
- Downloads go to your Mac's Downloads folder automatically
- Test with multiple browser tabs to see concurrency
- Press Ctrl+C to stop servers gracefully

---

## 📞 Need Help?

Check README.md for complete documentation and architecture details.

---

**Created for macOS users** | Tested on macOS 10.15+
