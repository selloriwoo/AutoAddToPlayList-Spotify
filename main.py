from flask import Flask, request, redirect, session, url_for, render_template
import os
import CrawlingKaraoke
from TJGenreEnum import TJGenreEnum
import dotenv
import requests
import spotify
import urllib.parse
from pykospacing import Spacing
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


@app.route("/")
def home():
    return '<a href="/login">Spotify 로그인</a>'

@app.route("/login")
def login():
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
        "show_dialog": "true"
    }
    url = AUTH_URL + "?" + urllib.parse.urlencode(params)
    return redirect(url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "인증 코드가 없습니다.", 400

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(TOKEN_URL, data=data, headers=headers)
    if response.status_code != 200:
        return f"토큰 요청 실패: {response.text}", response.status_code

    tokens = response.json()
    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")

    session["access_token"] = access_token
    session["refresh_token"] = refresh_token

    return (
        redirect(url_for("main"))
    )
@app.route("/main")
def main():
    access_token = session.get("access_token")
    if not access_token:
        return redirect(url_for("login"))
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get("https://api.spotify.com/v1/me", headers=headers)

    if response.status_code !=200:
        return f"spotify api 호출 실패: {response.text}", response.status_code

    user_data = response.json()
    user_country = user_data["country"]
    radio_options = ["종합", "가요", "POP", "JPOP"]

    return render_template("main.html",
                           user=user_data,
                           radios=radio_options,
                           user_country=user_country)

@app.route("/submit", methods=["POST"])
def submit():
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {session.get('access_token')}"
    }
    playlist_url = request.form.get("playlist_url")
    country = request.form.get("country")
    choice = request.form.get("genre")

    genre_mapping = {
        "종합": TJGenreEnum.total.value,
        "가요": TJGenreEnum.kpop.value,
        "POP": TJGenreEnum.pop.value,
        "JPOP": TJGenreEnum.jpop.value
    }

    # 0,1,2,3
    strType = genre_mapping.get(choice, TJGenreEnum.total.value)  # 기본은 종합
    genre_top100_title = CrawlingKaraoke.total_chart_result_title(strType)
    print(genre_top100_title)

    #곡 100개 각각 검색후 리스트에 추가
    add_song_list_body = {
        "uris": spotify.getTop100Songs(headers, genre_top100_title, country)
    }
    #100개의 곡 플레이 리스트에 추가
    spotify.addSongToPlaylist(headers, add_song_list_body, playlist_url)
    # 완료 후 리디렉션
    return redirect(playlist_url)
if __name__ == "__main__":
    app.run(port=8080, debug=True)