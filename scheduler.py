import dateparser
from collections import defaultdict


def get_schedule(soup):
    big_scheduler = soup.find(id='matchlist')
    daily_schedule = big_scheduler.find_all(
        'div', class_="matchlist-tab-wrapper")

    daily_matches = defaultdict(list)
    for day_parsed in daily_schedule:
        matches = get_matches(day_parsed)
        for match in matches:
            date = dateparser.parse(match['Date'])
            daily_matches[f'{date.month}-{date.day}'].append(match)

    return daily_matches


def get_matches(day):
    classes = ['ml-allw', 'ml-row', 'ml-row-tbd']
    matches_rows = day.find_all(lambda tag: tag.name == 'tr' and all(
        class_ in tag.get('class', []) for class_ in classes))
    matches = []
    for row in matches_rows:
        team_1, date, team_2 = get_match(row)
        matches.append({'Team 1': team_1, 'Team 2': team_2, 'Date': date})
    return matches


def get_match(row):
    team_1, team_2 = [x.get_text()
                      for x in row.find_all('span', class_='teamname')]
    hour = row.find(
        'td', class_='matchlist-time-cell plainlinks').get_text().split('+')[0][:-1]
    return team_1, hour, team_2
