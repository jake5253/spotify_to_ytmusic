
"""
spotify_to_ytmusic.py

This script transfers playlists from your Spotify account to YouTube Music.

✔ Supports multiple playlists
✔ Logs errors and skipped tracks
✔ CLI-driven with argparse
✔ Explains setup steps and automates OAuth login flows

---
SETUP INSTRUCTIONS (You must do this once):

1. 🔐 Spotify API Setup:
   - Go to https://developer.spotify.com/dashboard/
   - Log in and click "Create an App"
   - Note your **Client ID** and **Client Secret**
   - Set the redirect URI to `http://localhost:8888/callback`
   - These allow this script to read your playlists (OAuth)

2. 🔐 YouTube Data API Setup:
   - Go to https://console.developers.google.com/
   - Create a new project
   - Enable **YouTube Data API v3** in API Library
   - Go to "Credentials" > Create Credentials > OAuth client ID
     - Application type: **Desktop App**
   - Download the `client_secret.json` file and place it next to this script
   - This is needed so the script can create playlists and add songs to your account

---
"""

import argparse
import json
import os
import time
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# ----- Constants -----
SPOTIFY_SCOPE = "playlist-read-private"
YOUTUBE_SCOPES = ["https://www.googleapis.com/auth/youtube"]
REDIRECT_URI = "http://localhost:8888/callback"

# ----- Spotify Setup -----
def get_spotify_client(client_id, client_secret):
    sp_oauth = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=REDIRECT_URI,
        scope=SPOTIFY_SCOPE
    )
    return Spotify(auth_manager=sp_oauth)

# ----- YouTube Setup -----
def get_youtube_client(credentials_file):
    flow = InstalledAppFlow.from_client_secrets_file(credentials_file, YOUTUBE_SCOPES)
    creds = flow.run_local_server(port=8080)
    return build("youtube", "v3", credentials=creds)

# ----- Playlist Functions -----
def get_spotify_playlists(sp):
    playlists = []
    results = sp.current_user_playlists()
    while results:
        playlists.extend(results["items"])
        results = sp.next(results) if results["next"] else None
    return playlists

def get_spotify_tracks(sp, playlist_id):
    tracks = []
    results = sp.playlist_items(playlist_id)
    while results:
        for item in results["items"]:
            track = item["track"]
            if track:
                title = f"{track['name']} {track['artists'][0]['name']}"
                tracks.append(title)
        results = sp.next(results) if results["next"] else None
    return tracks

def youtube_search(youtube, query):
    request = youtube.search().list(
        part="snippet",
        q=query,
        type="video",
        videoCategoryId="10",
        maxResults=1
    )
    response = request.execute()
    if response["items"]:
        return response["items"][0]["id"]["videoId"]
    return None

def create_youtube_playlist(youtube, name, description="Imported from Spotify"):
    request = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {"title": name, "description": description},
            "status": {"privacyStatus": "private"}
        }
    )
    response = request.execute()
    return response["id"]

def add_video_to_playlist(youtube, playlist_id, video_id):
    youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id
                }
            }
        }
    ).execute()

# ----- Main Logic -----
def main():
    parser = argparse.ArgumentParser(description="Transfer Spotify playlists to YouTube Music")
    parser.add_argument("--spotify-client-id", required=True)
    parser.add_argument("--spotify-client-secret", required=True)
    parser.add_argument("--youtube-credentials", default="client_secret.json")
    parser.add_argument("--include", nargs="*", help="Optional list of playlist names to include")
    parser.add_argument("--exclude", nargs="*", help="Optional list of playlist names to skip")
    parser.add_argument("--log", default="errors.log", help="Log file for skipped tracks")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay between YouTube API calls")
    args = parser.parse_args()

    sp = get_spotify_client(args.spotify_client_id, args.spotify_client_secret)
    yt = get_youtube_client(args.youtube_credentials)

    playlists = get_spotify_playlists(sp)
    with open(args.log, "w") as log:
        for playlist in playlists:
            name = playlist["name"]
            if args.include and name not in args.include:
                continue
            if args.exclude and name in args.exclude:
                continue

            print(f"[*] Transferring playlist: {name}")
            tracks = get_spotify_tracks(sp, playlist["id"])
            yt_playlist_id = create_youtube_playlist(yt, name)

            for idx, track in enumerate(tracks, 1):
                print(f"  [{idx}/{len(tracks)}] Searching: {track}")
                video_id = youtube_search(yt, track)
                if video_id:
                    add_video_to_playlist(yt, yt_playlist_id, video_id)
                else:
                    print(f"  !! Skipped: {track}")
                    log.write(f"{name} - {track}\n")
                time.sleep(args.delay)

    print(f"[✓] Done. Skipped tracks (if any) logged to: {args.log}")

if __name__ == "__main__":
    main()
