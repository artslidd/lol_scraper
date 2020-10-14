import dateparser
from collections import defaultdict
from datetime import datetime

def get_schedule(soup):
    big_scheduler = soup.find(id='matchlist')
    daily_schedule = big_scheduler.find_all(
        'div', class_="matchlist-tab-wrapper")
    all_matches = []
    for day_parsed in daily_schedule:
        matches = get_matches(day_parsed)
        for match in matches:
            if match['date'] is not None:
                match['date'] = dateparser.parse(match['date'])
            all_matches.append(match)

    return all_matches


def get_matches(day):
    classes = ['ml-allw', 'ml-row']
    matches_rows = day.find_all(lambda tag: tag.name == 'tr' and all(
        class_ in tag.get('class', []) for class_ in classes))
    matches = []
    category = day.find('tr', class_="").find('th').find_all(text=True, recursive=False)[0]
    for row in matches_rows:
        team_1, date, team_2, score_home, score_away = get_match(row)

        matches.append({'home': team_1, 'away': team_2, 'date': date, 'category': category, 'score_home': score_home, 'score_away': score_away})
    return matches


def get_match(row):
    team_1, team_2 = [x.get_text()
                      for x in row.find_all('span', class_='teamname')]
    brut_date = row.find(
        'td', class_='matchlist-time-cell plainlinks')
    date = None
    if brut_date:
        date = brut_date.get_text().split('+')[0][:-1]
    
    brut_scores = row.find_all(lambda tag: tag.name == 'td' and 'matchlist-score' in tag.get('class', []))
    score_home, score_away = 0, 0
    if brut_scores:
        score_home, score_away = [x.get_text() for x in brut_scores]
    return team_1, date, team_2, score_home, score_away
