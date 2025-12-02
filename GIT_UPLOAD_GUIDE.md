# 📤 Git Commands to Upload Project to GitHub

## Step-by-Step Guide

### 1. Initialize Git Repository

```bash
cd c:\Users\Dabasis\Desktop\Abhi_2
git init
```

---

### 2. Add Remote Repository

```bash
git remote add origin https://github.com/deba75/Concurrent-File-Server-with-Multi-Threading-Web-Interface.git
```

---

### 3. Add All Files

```bash
git add .
```

---

### 4. Commit Changes

```bash
git commit -m "Initial commit: Multi-threaded Concurrent File Server with Web Interface"
```

---

### 5. Push to GitHub

```bash
git branch -M main
git push -u origin main
```

---

## 📸 Adding the Screenshot

### Option 1: Save Screenshot from Attachment

1. Save the screenshot image you shared as `screenshot.png` in the project folder
2. Add and commit it:

```bash
git add screenshot.png
git commit -m "Add web interface screenshot"
git push
```

---

### Option 2: Upload via GitHub Web Interface

1. Go to: https://github.com/deba75/Concurrent-File-Server-with-Multi-Threading-Web-Interface
2. Click "Add file" → "Upload files"
3. Drag and drop `screenshot.png`
4. Commit changes

---

## 🔄 If Repository Already Has Content

If the repository already has files, use:

```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

---

## ✅ Verify Upload

After pushing, visit:
https://github.com/deba75/Concurrent-File-Server-with-Multi-Threading-Web-Interface

You should see:
- ✅ All project files
- ✅ README.md with screenshot
- ✅ Professional documentation

---

## 🎯 Quick Commands Summary

```bash
# Navigate to project
cd c:\Users\Dabasis\Desktop\Abhi_2

# Initialize and setup
git init
git remote add origin https://github.com/deba75/Concurrent-File-Server-with-Multi-Threading-Web-Interface.git

# Add screenshot.png to the folder first, then:
git add .
git commit -m "Initial commit: Multi-threaded Concurrent File Server"
git branch -M main
git push -u origin main
```

---

## 📝 Future Updates

To update the repository later:

```bash
git add .
git commit -m "Your update message"
git push
```

---

**Note**: Make sure to save the screenshot as `screenshot.png` in the project root directory before running `git add .`
