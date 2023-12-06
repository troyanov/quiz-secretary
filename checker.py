import os
import requests
from bs4 import BeautifulSoup
from pathlib import Path

token = os.environ["TOKEN"]
chat_id = os.environ["CHAT_ID"]
data_file = os.environ["DATA_FILE"]

# Change URL for a different city or game types
url = "https://tbilisi.quizplease.ru/schedule?QpGameSearch%5BcityId%5D=160&QpGameSearch%5Bdates%5D=&QpGameSearch%5Bstatus%5D%5B0%5D=1&QpGameSearch%5Btype%5D%5B0%5D=all&QpGameSearch%5Btype%5D%5B1%5D=1&QpGameSearch%5Btype%5D%5B2%5D=3&QpGameSearch%5Btype%5D%5B3%5D=5&QpGameSearch%5Btype%5D%5B4%5D=9&QpGameSearch%5Bbars%5D%5B0%5D=all&QpGameSearch%5Bbars%5D%5B1%5D=1231&QpGameSearch%5Bbars%5D%5B2%5D=1453"

r = requests.get(url)

print(f"Fetching games data: HTTP {r.status_code}")

soup = BeautifulSoup(r.text, "html.parser")
data = soup.css.select(".schedule-block-head.w-inline-block")

games = list(
    map(
        lambda x: x.attrs["href"].rsplit("=")[-1],
        data,
    )
)

filename = Path(data_file)
filename.touch(exist_ok=True)
with open(filename, "r+") as f:
    lines = f.read().splitlines()
    for game in games:
        if game in lines:
            continue
        msg = f"ЗАПИШИСЬ БЛЯТЬ НА ИГРУ!\nhttps://quizplease.ru/game-page?id={game}"
        print("Game found: https://quizplease.ru/game-page?id={game}")
        r = requests.post(
            url=f"https://api.telegram.org/bot{token}/sendMessage",
            data={"chat_id": chat_id, "text": msg},
        )
        print(f"Sending message: HTTP {r.status_code}")
        f.write(game + "\n")
