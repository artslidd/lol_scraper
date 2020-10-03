#!/home/arthur/Documents/esport_task/.env/bin/python3.7

from bs4 import BeautifulSoup
from pprint import pprint
import requests
from standings import get_standings
from scheduler import get_schedule
from config import initialize_app, name_to_contraction
import time

def initialize_teams(db, soup):
    standings = get_standings(soup)
    
    for group_name, teams in standings.items():
        for standing, name, wins, losses in teams:
            contraction = name_to_contraction[name]
            data = {
                'contraction': contraction,
                'standing': standing,
                'wins': wins,
                'losses': losses,
                'name': name,
                'group': group_name
            }
            db.collection('teams').document(contraction).set(data)

def initialize_matches(db, soup):
    schedule = get_schedule(soup)
    for match in schedule:
        db.collection('matches').add(match)

def update_scores(db, soup):
    schedule = get_schedule(soup)
    for match in schedule:
        docs = db.collection('matches').where('home', '==', match['home']).where('away', '==', match['away']).stream()
        for doc in docs:
            id_ = doc.id
            document_dict = doc.to_dict()
        if document_dict['score_home'] != match['score_home'] and document_dict['score_away'] != match['score_away']:
            db.collection('matches').document(id_).update({'score_home': match['score_home'], 'score_away': match['score_away']})

def update_teams(db, soup):
    schedule = get_schedule(soup)
    for match in schedule:
        if 'date' in match:
            docs = db.collection('matches').where('date', '==', match['date']).stream()
            for doc in docs:
                id_ = doc.id
                document_dict = doc.to_dict()
            if document_dict['home'] != match['home'] and document_dict['away'] != match['away']:
                db.collection('matches').document(id_).update({'home': match['home'], 'away': match['away']})

if __name__ == '__main__':
    headers = {
        "User-agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    worlds_html_file = requests.request(
        'GET', 'https://lol.gamepedia.com/2020_Season_World_Championship/Main_Event', headers=headers).content

    soup = BeautifulSoup(worlds_html_file, 'html.parser')
    db = initialize_app()

    initialize_teams(db, soup)
    update_scores(db, soup)
