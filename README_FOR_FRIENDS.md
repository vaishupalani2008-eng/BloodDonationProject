# Blood Donation Camp Management System

## For Your Friends - How to Access the Website

### Option 1: Access from Same WiFi Network (RECOMMENDED)

1. Make sure your friends are on the **same WiFi network** as you
2. Have them open any browser and go to:
   ```
   http://192.168.31.227:5000
   ```
3. They should see the Blood Donation Camp website!

**Note:** This address only works while your computer is running the app.

---

### Option 2: Run on Their Own Computer

1. Have your friends download and extract this project folder
2. They need Python installed (download from python.org)
3. Open the project folder and double-click **RUN_ME.bat**
4. The app will start automatically
5. They can access it at: `http://localhost:5000`

---

### Option 3: If WiFi Connection Not Working

**Check these things:**

1. **Are you on the same WiFi?**
   - Both phone and your computer should connect to the same WiFi network

2. **Is the server running?**
   - Look at your computer - you should see "Running on http://192.168.31.227:5000"

3. **Is Windows Firewall blocking it?**
   - Go to Windows Defender Firewall → Inbound Rules
   - Create a new rule for Port 5000 → Allow Connection

4. **Try this address instead:**
   - Ask your friend to try: `http://192.168.31.227:5000` or `192.168.31.227:5000`

---

## What Can Friends Do?

- ✅ View the dashboard with donor statistics
- ✅ Register as new donors
- ✅ Check if they're eligible to donate
- ✅ See blood inventory reports
- ✅ View recent donor records

---

## Troubleshooting

**Problem:** Friends can't reach the website
**Solution:** Make sure the Flask app is running on your computer (you should see output in the terminal)

**Problem:** Website loads but is slow
**Solution:** This is normal for the development server. It's not designed for many users at once.

**Problem:** Data doesn't save
**Solution:** The data is saved in `donors.json` file in the project folder

---

## To Stop the App

Press **CTRL + C** in the terminal where the app is running

---

Need help? Contact the developer!
