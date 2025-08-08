import requests
import os
import dotenv

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

url = "https://api.spotify.com/v1/artists/2DaxqgrOhkeH0fpeiQq2f4?si=V9dcndhEQG6U8s93jTuuKA"
response = requests.get(url, headers=headers)
artist_info = response.json()
print(artist_info)
