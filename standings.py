def get_standings(soup):
    groups = soup.find_all('table', class_='wikitable2 standings')
    classes = ['teamhighlight', 'teamhighlighter']
    standings = {'Group A': [], 'Group B': [], 'Group C': [], 'Group D': []}
    for group in groups:
        name = group.find('div').find_all(text=True, recursive=False)[0]
        teams_tree = group.find_all(lambda tag: tag.name == 'tr' and all(
        class_ in tag.get('class', []) for class_ in classes))
        for team_tree in teams_tree:
            standings[name].append(get_informations(team_tree))
    return standings


def get_informations(team_tree):
    standing = int(team_tree.find(
        'td', {'class': lambda x: 'standings-place' in x.split()}).get_text())
    team_name = team_tree.find('span', class_='teamname').get_text()
    v_d, *_ = [x.get_text()
               for x in team_tree.find_all('td', class_='')]
    wins = int(v_d[0])
    losses = int(v_d[-1])

    return standing, team_name, wins, losses
