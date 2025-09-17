import requests
from datetime import datetime
import json
import ast

# 오늘 날짜 구하기
today = datetime.today()

searchStartDate = today.strftime("%Y-%m") + '-01'
searchEndDate = today.strftime("%Y-%m-%d")

url = "https://www.tjmedia.com/legacy/api/topAndHot100"
headers = {
    "User-Agent": "Mozilla/5.0 ...",
    "Referer": "https://www.tjmedia.com/chart/top100",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
}

base_payload = {
    "chartType": "TOP",
    "searchStartDate": searchStartDate,
    "searchEndDate": searchEndDate,
}

def get_chart(strType):
    payload = base_payload.copy()
    payload["strType"] = strType
    response = requests.post(url, headers=headers, data=payload)
    return response.json()


# total_chart = get_chart("0") # 종합
# kpop_chart = get_chart("1")  # 가요
# pop_chart = get_chart("2")  # pop
# jpop_chart = get_chart("3")  # jpop


# tj노래방 종합, 가요,pop, jpop을 웹 상 index로 변환

def total_chart_result_title(genre_number):
    genre_chart = get_chart(genre_number)  # jpop, kpop...
    # 디버깅: genre_chart 타입 확인
    print("type(genre_chart) =", type(genre_chart))
    print("genre_chart =", genre_chart)

    result_data = genre_chart.get("resultData", {})
    items = result_data.get("items", [])
    results = []
    # pro: 곡번호
    # indexTitle: 제목
    # indexsong: 가수
    for item in items:
        if all(k in item for k in ("pro", "indexTitle", "indexSong")):
            title = str(item["indexTitle"]).split("(")[0].strip()  # 괄호 제거
            artist = str(item["indexSong"]).strip()
            results.append({
                "pro": item["pro"],
                "title": title,
                "artist": artist
            })
    return results

