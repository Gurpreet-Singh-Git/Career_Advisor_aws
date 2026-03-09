# 🚀 How to Run the Demo

## Quick Start Guide for Your Presentation

---

## ✅ What You Need

- Node.js installed
- This project downloaded
- 5 minutes to set up

---

## 🎯 Step-by-Step Instructions

### Step 1: Open Terminal

**Windows:**
- Press `Win + R`
- Type `cmd` or `powershell`
- Press Enter

**Mac/Linux:**
- Press `Cmd + Space`
- Type `terminal`
- Press Enter

### Step 2: Navigate to Project

```bash
cd path/to/Career_Advisor_aws
```

**Example:**
```bash
cd C:\Users\YourName\Desktop\Career_Advisor_aws
```

### Step 3: Go to Frontend Folder

```bash
cd frontend
```

### Step 4: Install Dependencies (First Time Only)

```bash
npm install
```

**Wait 2-3 minutes for installation to complete.**

### Step 5: Start the Application

```bash
npm start
```

**Wait 30 seconds. Browser will open automatically at:**
```
http://localhost:3000
```

### Step 6: Verify Demo Mode

Open `frontend/src/App.js` and check line 8:

```javascript
const DEMO_MODE = true;  // ✅ Should be true
```

If it's `false`, change it to `true` and save.

---

## 🎬 Ready to Record!

Your application is now running at: **http://localhost:3000**

**What you'll see:**
- Landing page with title
- Chat interface
- "Ask me anything about careers..." input box

**You're ready to start your demo!**

---

## 🎯 Quick Test Before Recording

### Test 1: Chat Works
1. Type: "Is BTech worth it in 2026?"
2. Press Enter or click Send
3. You should see an alert with AI response

✅ **If you see the response:** Chat is working!

### Test 2: Form Works
1. Type: "I want personalized recommendations"
2. Press Enter
3. Click OK on consent dialog
4. You should see the form

✅ **If you see the form:** Navigation is working!

### Test 3: Results Work
1. Fill the form:
   - Education: BTech
   - Skills: Python, JavaScript, Problem Solving
   - Interests: Technology, Innovation
   - Location: Bangalore
2. Click "Get Recommendations"
3. You should see 3 career recommendations

✅ **If you see results:** Everything is working!

---

## 🎥 Recording Setup

### Option 1: OBS Studio (Free, Recommended)

**Download:** https://obsproject.com/

**Setup:**
1. Open OBS
2. Click "+" under Sources
3. Select "Window Capture"
4. Choose your browser window
5. Click "Start Recording"
6. Do your demo
7. Click "Stop Recording"

**Output:** Video saved in `Videos` folder

### Option 2: Windows Game Bar (Built-in)

**Steps:**
1. Press `Win + G`
2. Click the record button (circle)
3. Do your demo
4. Press `Win + Alt + R` to stop

**Output:** Video saved in `Videos/Captures` folder

### Option 3: Mac QuickTime (Built-in)

**Steps:**
1. Open QuickTime Player
2. File → New Screen Recording
3. Click record button
4. Select area or full screen
5. Do your demo
6. Click stop in menu bar

**Output:** Video saved to Desktop

### Option 4: Chrome Extension

**Extension:** Loom or Screencastify

**Steps:**
1. Install extension
2. Click extension icon
3. Select "Record Tab"
4. Do your demo
5. Click stop

**Output:** Video uploaded to cloud

---

## 🎤 Audio Setup

### Test Your Microphone

**Windows:**
1. Right-click speaker icon
2. Open Sound settings
3. Test microphone
4. Adjust volume to 70-80%

**Mac:**
1. System Preferences
2. Sound → Input
3. Test microphone
4. Adjust volume to 70-80%

### Tips for Clear Audio
- Close windows (reduce outside noise)
- Turn off fans/AC
- Speak 6-12 inches from mic
- Test recording 10 seconds first
- Listen to test before full demo

---

## 🖥️ Browser Setup

### Recommended: Chrome or Edge

**Before Recording:**

1. **Zoom In** (Make text bigger)
   - Press `Ctrl +` (Windows)
   - Press `Cmd +` (Mac)
   - Zoom to 125-150%

2. **Full Screen** (Optional)
   - Press `F11` (Windows)
   - Press `Cmd + Ctrl + F` (Mac)

3. **Close Other Tabs**
   - Only keep demo tab open
   - Reduces distractions

4. **Clear Notifications**
   - Turn on "Do Not Disturb"
   - Close Slack, Teams, etc.

---

## 🎯 Demo Checklist

### Before Starting

- [ ] Application running at localhost:3000
- [ ] Browser zoomed to 125-150%
- [ ] Other tabs closed
- [ ] Notifications turned off
- [ ] Microphone tested
- [ ] Recording software ready
- [ ] Script nearby
- [ ] Timer ready (3 minutes)
- [ ] Tested all 3 steps (chat, form, results)

### During Recording

- [ ] Speak clearly
- [ ] Follow the script
- [ ] Don't rush
- [ ] Show enthusiasm
- [ ] Check timer at 1:30

### After Recording

- [ ] Watch the video
- [ ] Check audio quality
- [ ] Verify all features shown
- [ ] Confirm under 3 minutes
- [ ] Export in HD (1080p)

---

## 🚨 Troubleshooting

### Problem: "npm: command not found"

**Solution:** Install Node.js
1. Go to https://nodejs.org/
2. Download LTS version
3. Install
4. Restart terminal
5. Try again

### Problem: "Port 3000 already in use"

**Solution:** Kill the process
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID_NUMBER> /F

# Mac/Linux
lsof -ti:3000 | xargs kill
```

Or use a different port:
```bash
PORT=3001 npm start
```

### Problem: Application won't start

**Solution:** Clear cache and reinstall
```bash
rm -rf node_modules
rm package-lock.json
npm install
npm start
```

### Problem: Demo mode not working

**Solution:** Check App.js
1. Open `frontend/src/App.js`
2. Find line 8: `const DEMO_MODE = true;`
3. Make sure it's `true` not `false`
4. Save file
5. Refresh browser

### Problem: Blank screen

**Solution:** Check console
1. Press `F12` (open DevTools)
2. Click "Console" tab
3. Look for errors
4. If you see errors, refresh page
5. If still errors, restart `npm start`

---

## 💡 Pro Tips

### Make Recording Smoother

1. **Practice First**
   - Do a test run without recording
   - Time yourself
   - Get comfortable with flow

2. **Have Script Ready**
   - Print QUICK_DEMO_SCRIPT.md
   - Or have it on second monitor
   - Or memorize key points

3. **Prepare Responses**
   - Know what to type
   - Know what to select
   - No hesitation during demo

4. **Check Everything**
   - Test all 3 steps before recording
   - Make sure demo mode is on
   - Verify browser zoom

### If Something Goes Wrong

**Don't panic!**

- If you make a mistake, keep going
- If app crashes, restart and re-record
- If you stutter, that's okay - judges understand
- If you go over time, edit the video

---

## 🎬 Recording Quality Settings

### Resolution
- **Minimum:** 1280x720 (HD)
- **Recommended:** 1920x1080 (Full HD)
- **Maximum:** 2560x1440 (2K)

### Frame Rate
- **Minimum:** 24 fps
- **Recommended:** 30 fps
- **Maximum:** 60 fps (not necessary)

### Audio
- **Format:** MP3 or AAC
- **Bitrate:** 128 kbps minimum
- **Sample Rate:** 44.1 kHz

### File Format
- **Recommended:** MP4 (H.264)
- **Alternative:** MOV, AVI, WebM

---

## 📤 After Recording

### Export Settings

**For YouTube/Vimeo:**
- Format: MP4
- Codec: H.264
- Resolution: 1920x1080
- Frame rate: 30 fps
- Bitrate: 8-10 Mbps

**For File Upload:**
- Same as above
- Keep file under 500 MB
- If too large, reduce bitrate

### Where to Upload

**Option 1: YouTube**
- Upload as "Unlisted"
- Share link with judges
- Easy to access

**Option 2: Google Drive**
- Upload video
- Set sharing to "Anyone with link"
- Share link with judges

**Option 3: Vimeo**
- Upload video
- Set privacy to "Anyone"
- Share link with judges

**Option 4: Direct Upload**
- If hackathon has upload portal
- Follow their instructions

---

## ✅ Final Checklist

### Technical Setup
- [ ] Node.js installed
- [ ] Dependencies installed (`npm install`)
- [ ] Application running (`npm start`)
- [ ] Demo mode enabled (DEMO_MODE = true)
- [ ] Browser at localhost:3000
- [ ] Browser zoomed to 125-150%

### Recording Setup
- [ ] Recording software ready
- [ ] Microphone tested
- [ ] Audio levels good (70-80%)
- [ ] Notifications off
- [ ] Other apps closed
- [ ] Script ready
- [ ] Timer ready

### Content Ready
- [ ] Practiced 2-3 times
- [ ] Know what to type
- [ ] Know what to select
- [ ] Know what to say
- [ ] Timing is good (under 3 min)

---

## 🎉 You're All Set!

**Your application is running.**
**Your recording setup is ready.**
**Your script is prepared.**

**Now go create that amazing demo video!** 🚀

---

## 📞 Quick Commands Reference

```bash
# Start the demo
cd frontend
npm start

# Stop the demo
Ctrl + C (in terminal)

# Restart if needed
npm start

# Check if running
# Open browser: http://localhost:3000
```

---

**Good luck with your recording!** 🎬🏆

