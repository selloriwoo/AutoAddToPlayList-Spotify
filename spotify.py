import requests
import os
import dotenv
import ast

import CrawlingKaraoke

dotenv.load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

url = "https://accounts.spotify.com/api/token"
preHeaders = {
    "Content-Type": "application/x-www-form-urlencoded"
}
data = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret
}

response = requests.post(url, headers=preHeaders, data=data)

if response.status_code == 200:
    token_info = response.json()
    access_token = token_info['access_token']
    print("Access Token:", access_token)
else:
    print("Failed to get token:", response.status_code, response.text)
    exit(Exception)

#엑세스 토큰 추가
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": f"Bearer {access_token}"
}

#아티스트 검색
# url = "https://api.spotify.com/v1/artists/2DaxqgrOhkeH0fpeiQq2f4?si=V9dcndhEQG6U8s93jTuuKA"
# response = requests.get(url, headers=headers)
# artist_info = response.json()
# print(artist_info)

#곡 검색
# url = "https://api.spotify.com/v1/search?q=%E3%82%B5%E3%83%A0%E3%83%A9%E3%82%A4%E3%83%8F%E3%83%BC%E3%83%88&type=track&market=JP&limit=1"
# response = requests.get(url, headers=headers)
# print(response.json().get("tracks").get("items")[0].get("external_urls").get("spotify"))
# print(CrawlingKaraoke.resultTitle)

result_spotify_song_url= []
for item in CrawlingKaraoke.resultTitle:
    url = f"https://api.spotify.com/v1/search?q={item}&type=track&market=JP&limit=1"
    response = requests.get(url, headers=headers)
    result_spotify_song_url.append(response.json().get("tracks").get("items")[0].get("external_urls").get("spotify"))

print(result_spotify_song_url)