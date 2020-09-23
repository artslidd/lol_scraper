def get_standings(soup):
    groups = soup.find_all('table', class_='wikitable2 standings')
    standings = {'Group A': [], 'Group B': [], 'Group C': [], 'Group D': []}
    for group in groups:
        name = group.find('div').get_text()[:7]
        teams_tree = group.find_all(
            'tr', class_='teamhighlight teamhighlighter')
        for team_tree in teams_tree:
            standings[name].append(get_informations(team_tree))
    return standings


def get_informations(team_tree):
    standing = int(team_tree.find(
        'td', {'class': lambda x: 'standings-place' in x.split()}).get_text())
    team_name = team_tree.find('span', class_='teamname').get_text()
    v_d, ratio, *_ = [x.get_text()
                      for x in team_tree.find_all('td', class_='')]
    return standing, team_name, v_d, ratio
