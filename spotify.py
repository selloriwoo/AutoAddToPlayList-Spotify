import requests
import os
import dotenv
import ast
import urllib.parse
from flask import Flask, request, redirect
import requests
import urllib.parse
import os

import CrawlingKaraoke

dotenv.load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
#자신의 스포티파이 url
my_playList = os.getenv("MY_PLAYLIST_ID")
AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
app = Flask(__name__)

CLIENT_ID = client_id
CLIENT_SECRET = client_secret
REDIRECT_URI = os.getenv("REDIRECT_URL")
SCOPE = "playlist-modify-public playlist-modify-private"



# @app.route("/")
# def home():
#     return '<a href="/login">Spotify 로그인</a>'
#
# @app.route("/login")
# def login():
#     params = {
#         "client_id": CLIENT_ID,
#         "response_type": "code",
#         "redirect_uri": REDIRECT_URI,
#         "scope": SCOPE,
#         "show_dialog": "true"
#     }
#     url = AUTH_URL + "?" + urllib.parse.urlencode(params)
#     return redirect(url)
#
# @app.route("/callback")
# def callback():
#     code = request.args.get("code")
#     if not code:
#         return "인증 코드가 없습니다.", 400
#
#     data = {
#         "grant_type": "authorization_code",
#         "code": code,
#         "redirect_uri": REDIRECT_URI,
#         "client_id": CLIENT_ID,
#         "client_secret": CLIENT_SECRET
#     }
#
#     headers = {
#         "Content-Type": "application/x-www-form-urlencoded"
#     }
#
#     response = requests.post(TOKEN_URL, data=data, headers=headers)
#     if response.status_code != 200:
#         return f"토큰 요청 실패: {response.text}", response.status_code
#
#     tokens = response.json()
#     access_token = tokens.get("access_token")
#     refresh_token = tokens.get("refresh_token")
#
#     return (
#         f"Access Token:<br>{access_token}<br><br>"
#         f"Refresh Token:<br>{refresh_token}<br><br>"
#         f"이제 이 토큰으로 Spotify API를 호출할 수 있습니다."
#     )
#
# if __name__ == "__main__":
#     app.run(port=8080)


#클라이언트 ID의 엑세스 토큰 받기
preHeaders = {
    "Content-Type": "application/x-www-form-urlencoded"
}
data = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret
}

response = requests.post(TOKEN_URL, headers=preHeaders, data=data)

if response.status_code == 200:
    token_info = response.json()
    access_token = token_info['access_token']
    print("성공 ! Access Token:", access_token)
else:
    print("Failed to get token:", response.status_code, response.text)
    exit(Exception)

# 클라이언트 ID로 발급 받은 토큰을 헤더에 적용
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": f"Bearer {access_token}"
}

#곡 검색
def findSong(headers,songTitle):
    url = f"https://api.spotify.com/v1/search?q={songTitle}&type=track&market=JP&limit=1"
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
def getTop100Songs(headers):
    result_spotify_song_id = []
    for item in CrawlingKaraoke.resultTitle:
        url = f"https://api.spotify.com/v1/search?q={item}&type=track&market=JP&limit=1"
        response = requests.get(url, headers=headers)
        result_spotify_song_id.append('spotify:track:' +
                                      response.json().get("tracks").get("items")[0].get("external_urls").get(
                                          "spotify").split("track/")[1])
    return result_spotify_song_id

def addSongToPlaylist(headers, add_song_list_body):
    # 해당 플레이 리스트에 곡 추가
    url = f"https://api.spotify.com/v1/playlists/{my_playList}/tracks"
    response = requests.post(url, headers=headers, json=add_song_list_body)
    print(response.status_code)

#oauth 인증 토근 적용
oauthToken = os.getenv("OAUTH_TOKEN")

headersOauth = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {oauthToken}"
}

#플레이 리스트에 추가할 곡 body
add_song_list_body = {
    "uris": getTop100Songs(headers)
}

#플레이 리스트 100개 추가
addSongToPlaylist(headersOauth, add_song_list_body)