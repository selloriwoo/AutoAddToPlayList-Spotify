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


# kpop_chart = get_chart("1")  # 가요
# kpop_chart = get_chart("2")  # pop
jpop_chart = get_chart("3")  # jpop
jpop_chart = str(jpop_chart)
jpop_chart_json = ast.literal_eval(jpop_chart)
results = []

for item in jpop_chart_json.get("GNB_MENU", []):
    if all(k in item for k in ("pro", "indexTitle", "indexSong")):
        results.append({k: item[k] for k in ("pro", "indexTitle", "indexSong")})
result_data = jpop_chart_json.get("resultData", {})
items = result_data.get("items", [])

results = []
#pro: 곡번호
#indexTitle: 제목
#indexsong: 가수
for item in items:
    if all(k in item for k in ("pro", "indexTitle", "indexSong")):
        results.append({k: item[k] for k in ("pro", "indexTitle", "indexSong")})
resultTitle = []
for item in results:
    resultTitle.append(str(item["indexTitle"]).split('(')[0].strip())
print(resultTitle)
print(f"{len(items)}개의 jpop 차트 데이터")
print(len(jpop_chart), "개의 jpop 차트 데이터")
