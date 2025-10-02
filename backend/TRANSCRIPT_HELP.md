# 🔧 Transcript Fetching Troubleshooting Guide

## Problem: "no element found: line 1, column 0" Error

This error occurs when YouTube blocks or rate-limits transcript requests.

---

## ✅ Solution 1: Use yt-dlp (Recommended)

**This is more reliable and works better with rate limiting:**

```powershell
# Install yt-dlp (if not already installed)
pip install yt-dlp

# Use the alternative script
python scripts/get_transcripts_alternative.py --delay 3.0
```

**Why it works better:**
- Uses YouTube's official subtitle API
- Less likely to be blocked
- More robust error handling

---

## ✅ Solution 2: Longer Delays

If yt-dlp doesn't work, try much longer delays:

```powershell
python scripts/get_transcripts.py --delay 10.0
```

---

## ✅ Solution 3: Use VPN

If you're getting blocked:
1. Connect to a VPN
2. Change your IP address
3. Try again

---

## ✅ Solution 4: Wait It Out

YouTube blocks are usually temporary:
1. Wait 1-2 hours
2. Try again with longer delays
3. Process videos in smaller batches

---

## 📊 Expected Success Rates

- **Educational channels (TED, Khan Academy):** 70-90%
- **Tech channels:** 50-70%
- **Entertainment channels:** 20-50%

**Note:** Even with transcripts enabled, success rate varies by:
- Channel settings
- Video age
- YouTube's API limits

---

## 🎯 Quick Commands

```powershell
# Best method - Use yt-dlp
python scripts/get_transcripts_alternative.py --delay 3.0

# Original method with long delays
python scripts/get_transcripts.py --delay 10.0

# Check what worked
python status.py
```

---

## 📝 Next Steps After Getting Transcripts

Once you have transcripts (even if only 50% success):

```powershell
# 1. Generate embeddings
python scripts/embed_and_index.py

# 2. Start backend
uvicorn app.main:app --reload

# 3. Start frontend
cd ../frontend
npm run dev

# 4. Search at http://localhost:3000
```

You don't need 100% success - even 50% gives you plenty of searchable content!
