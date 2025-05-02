# spotify\_to\_ytmusic

Python script to transfer Spotify playlists to YouTube Music.

---

## ✅ Overview

This script does the following:

* Authenticates with your Spotify account and fetches playlist data.
* Uses YouTube Data API v3 to find matching tracks and create playlists in YouTube Music.
* Supports command-line arguments for filtering playlists, naming new ones, and more.

---

## 📌 Setup Instructions

> ⚠️ These steps **must be completed before running the script for the first time**. The script will guide you through authorization, but it cannot register API apps or generate credentials for you.

### 🔐 Step 1: Register a Spotify Application

Why? You need API credentials to access your playlists programmatically.

1. Visit [https://developer.spotify.com/dashboard/](https://developer.spotify.com/dashboard/)
2. Log in and click **"Create an App"**.
3. Note your **Client ID** and **Client Secret**.
4. Set the Redirect URI to: `http://localhost:8888/callback`
5. Save your credentials for later use.

### 🔐 Step 2: Enable YouTube Data API

Why? The YouTube Data API lets you search for tracks and create playlists.

1. Visit [https://console.developers.google.com/](https://console.developers.google.com/)
2. Create a new project (or select an existing one).
3. Go to **"APIs & Services" > "Library"** and enable **YouTube Data API v3**.
4. Go to **"Credentials"**, click **"Create Credentials" → "OAuth Client ID"**.
5. Choose **Desktop App**.
6. Download the `client_secret.json` file and place it in the script directory.

---

## ▶️ Example Usage

```bash
python spotify_to_ytmusic.py \
    --spotify-client-id YOUR_CLIENT_ID \
    --spotify-client-secret YOUR_CLIENT_SECRET \
    --youtube-credentials client_secret.json
```

To copy **all playlists**, simply run without any playlist filter flags:

```bash
python spotify_to_ytmusic.py --spotify-client-id ... --spotify-client-secret ... --youtube-credentials ...
```

Use `--delay` to insert a pause between YouTube Music API calls (in seconds) to avoid rate limiting:

```bash
--delay 1.5  # Wait 1.5 seconds between each upload step
```

---

## 📦 Installation Instructions

### ✅ Requirements

* Python 3.8 or newer
* A Spotify Developer account
* A Google Cloud project with YouTube Data API v3 enabled

---

### 🪟 Windows

1. **Download and unzip the repo**

   * On GitHub, click the green `Code` button → `Download ZIP`
   * Right-click the ZIP file → **Extract All**

2. **Open Command Prompt**

   * Press `Win + R`, type `cmd`, and press Enter
   * Navigate to the folder:

     ```cmd
     cd path\to\spotify_to_ytmusic
     ```

3. **Install dependencies**

   ```cmd
   pip install -r requirements.txt
   ```

4. **Run the script**

   ```cmd
   python spotify_to_ytmusic.py --spotify-client-id YOUR_ID --spotify-client-secret YOUR_SECRET --youtube-credentials client_secret.json
   ```

---

### 🐧 Linux / 🍎 macOS

1. **Download and unzip the repo**

   ```bash
   wget https://github.com/jake5253/spotify_to_ytmusic/archive/refs/heads/main.zip
   unzip main.zip
   cd spotify-to-ytmusic-main
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the script**

   ```bash
   python3 spotify_to_ytmusic.py --spotify-client-id YOUR_ID --spotify-client-secret YOUR_SECRET --youtube-credentials client_secret.json
   ```

---

### 📝 Final Notes

* The script will open browser tabs to authorize access to Spotify and YouTube.
* Your playlists will be transferred privately.
* Double-check track matches as YouTube’s search might not always be perfect.

---

Happy migrating! 🎵
