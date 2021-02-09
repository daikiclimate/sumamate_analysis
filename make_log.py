import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import time


def get_soup(url="https://smashmate.net/rate/1082871/"):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    return soup


def get_infomation(soup):
    names = soup.find_all('div', {'class': 'flex-list-auto text3reader bold'})

    player1_name = names[0].text.strip()
    player2_name = names[1].text.strip()

    df = pd.DataFrame()
    links = [url.get("href") for url in soup.find_all("a")]
    room_id = [i.split("=")[2] for i in links if "room_id" in i][0]
    df["room_id"] = [room_id]
    _rate = [int(i.text) for i in soup.find_all("span", class_="rate_text")]

    player_index = [i for i in links if "smashmate.net/user" in i]
    player1 = links.index(player_index[0])
    player2 = links.index(player_index[1])
    player1_links = links[player1:player2]
    player2_links = links[player2:]

    user = [i for i in player1_links if "user" in i]
    user = int(user[0].split("/")[4])
    df["player1"] = user
    df["player1_name"] = player1_name
    df["player1_final_rate"] = _rate[0]

    fighters = [i for i in player1_links if "fighter" in i]
    fighters = [i.split("/")[4] for i in fighters]
    if len(fighters) == 0:
        df["player1_fighter_main"] = None
        df["player1_fighter_sub"] = None
    else:
        df["player1_fighter_main"] = fighters[0]
        if len(fighters) > 1:
            df["player1_fighter_sub"] = fighters[1]
        else:
            df["player1_fighter_sub"] = None

    user = [i for i in player2_links if "user" in i]
    user = int(user[0].split("/")[4])
    df["player2"] = user
    df["player2_name"] = player2_name
    df["player2_final_rate"] = _rate[1]

    fighters = [i for i in player2_links if "fighter" in i]
    fighters = [i.split("/")[4] for i in fighters]
    if len(fighters) == 0:
        df["player1_fighter_main"] = None
        df["player1_fighter_sub"] = None
    else:
        df["player2_fighter_main"] = fighters[0]
        if len(fighters) > 1:
            df["player2_fighter_sub"] = fighters[1]
        else:
            df["player2_fighter_sub"] = None

    _win_lose = [
        i.text
        for i in soup.find_all("div", class_="w65 text-center insert-update-status")
    ]
    win_lose = ["win" if "勝ち" in i else "lose" for i in _win_lose]
    if win_lose[0] == win_lose[1] == "lose":
        df["winner"] = "cancelled"
    elif win_lose[0] == "win":
        df["winner"] = "player1"
    else:
        df["winner"] = "player2"
    return df


def get_newest_room_id():
    rate_top_page = "https://smashmate.net/rate/"
    soup = get_soup(rate_top_page)
    links = [url.get("href") for url in soup.find_all("a")]
    links = [i for i in links if type(i) == str]
    newest_room_id = [i.split("/")[4] for i in links if "rate" in i][1]
    return int(newest_room_id)


def check_room_exist(soup):
    win_lose = [
        i.text
        for i in soup.find_all("div", class_="w65 text-center insert-update-status")
    ]
    if len(win_lose) == 0:
        return False
    else:
        return True


def main():
    newest_room_id = get_newest_room_id()
    df = pd.DataFrame()
    filename = "sumamate_log.xlsx"
    start = 1
    resume = False
    if resume:
        df = pd.read_excel(filename)
        start = 1
    for i in tqdm(range(start, newest_room_id)):
    # for i in tqdm(range(90, 130)):
        url = "https://smashmate.net/rate/" + str(i)
        soup = get_soup(url)
        if check_room_exist(soup):
            _df = get_infomation(soup)
            _df = _df.reset_index().drop(columns=["index"])
            df = pd.concat([df, _df])
            df.to_excel(filename)
            #take 0.1 sec by above process
            time.sleep(0.9)
    df.to_excel(filename)


if __name__ == "__main__":
    main()
