import requests
import os
import dotenv
import ast
import urllib.parse
from flask import Flask, request, redirect, session, url_for, render_template
import requests
import urllib.parse
import os
import urllib.parse
from pykospacing import Spacing
import CrawlingKaraoke
from TJGenreEnum import TJGenreEnum

dotenv.load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

CLIENT_ID = client_id
CLIENT_SECRET = client_secret
REDIRECT_URI = os.getenv("REDIRECT_URL")
SCOPE = "playlist-modify-public playlist-modify-private user-read-private user-read-email"

#곡 검색
def findSong(headers,songTitle):
    query = urllib.parse.quote(songTitle)
    url = f"https://api.spotify.com/v1/search?q={query}&type=track&market=JP&limit=1"
    response = requests.get(url, headers=headers)
    print(response.json().get("tracks").get("items")[0].get("external_urls").get("spotify"))
    print(CrawlingKaraoke.resultTitle)

# 아티스트 검색
def findArtist(headers):
    url = "https://api.spotify.com/v1/artists/2DaxqgrOhkeH0fpeiQq2f4?si=V9dcndhEQG6U8s93jTuuKA"
    response = requests.get(url, headers=headers)
    artist_info = response.json()
    print(artist_info)

# 곡 100개 스포티파이 id 리스트
def getTop100Songs(headers, genre_title_list, user_country):
    result_spotify_song_id = []

    for song in genre_title_list:
        title = song["title"]
        artist = song["artist"]

        # 띄어쓰기 자연어 처리
        spacing = Spacing()
        corrected_title = spacing(title)
        # 1차 검색: track + artist
        query1 = urllib.parse.quote(f'track:"{corrected_title}" artist:"{artist}"')
        url1 = f"https://api.spotify.com/v1/search?q={query1}&type=track&market={user_country}&limit=1"
        response1 = requests.get(url1, headers=headers)
        items1 = response1.json().get("tracks", {}).get("items", [])

        if items1:
            # 1차 검색 성공
            track_id = items1[0]["id"]
            result_spotify_song_id.append(f"spotify:track:{track_id}")
            print(f"✅ 검색 성공 (track+artist): {corrected_title} - {artist}")
            continue
        # 1차 검색 실패 → 2차 검색: "제목 아티스트"
        query2 = urllib.parse.quote(f"{corrected_title} {artist}")
        url2 = f"https://api.spotify.com/v1/search?q={query2}&type=track&market={user_country}&limit=1"
        response2 = requests.get(url2, headers=headers)
        items2 = response2.json().get("tracks", {}).get("items", [])
        track_id = items2[0]["id"]
        result_spotify_song_id.append(f"spotify:track:{track_id}")
        print(f"❌ 검색 실패: {corrected_title} {artist} (문자열로 검색)")

    print("✅ 리스트 추가 완료")
    return result_spotify_song_id

def addSongToPlaylist(headers, add_song_list_body, my_playlist_url):
    #id만 추출
    playlist_id = my_playlist_url.split("/")[-1].split("?")[0]
    query = urllib.parse.quote(playlist_id)
    # 해당 플레이 리스트에 곡 추가
    url = f"https://api.spotify.com/v1/playlists/{query}/tracks"
    response = requests.post(url, headers=headers, json=add_song_list_body)
    print(" 플레이 리스트에 삽입결과: ", response.status_code)

#클라이언트 ID의 엑세스 토큰 받기
preHeaders = {
    "Content-Type": "application/x-www-form-urlencoded"
}
data = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret
}

