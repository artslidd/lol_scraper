from bs4 import BeautifulSoup
from pprint import pprint
import requests
from standings import get_standings
from scheduler import get_schedule

if __name__ == '__main__':
    headers = {
        "User-agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    worlds_html_file = requests.request(
        'GET', 'https://lol.gamepedia.com/2020_Season_World_Championship/Main_Event', headers=headers).content

    soup = BeautifulSoup(worlds_html_file, 'html.parser')
    all_matches = get_schedule(soup)
    standings = get_standings(soup)
