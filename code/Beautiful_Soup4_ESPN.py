

import requests
from bs4 import BeautifulSoup
import json

def get_game_ids(year, week,seasontype):
    url = f"https://www.espn.com/nfl/schedule/_/week/{week}/year/{year}/seasontype/{seasontype}"
    
    # Add headers to mimic a browser so that I'm not blocked from the API
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        for link in soup.find_all('a', href=True):
            if '/gameId/' in link['href']:
                game_id_p1 = link['href'].split('/gameId/')[1]
                game_id=game_id_p1.split('/')[0]
                if game_id_p1.split('/')!='nfc-afc' and game_id_p1.split('/')!='afc-nfc': #excludes probowls
                    if game_id not in game_id_log: #prevents accidental duplicates
                        game_id_log.append(game_id)
    else:
        print(f"Failed to retrieve page, status code: {response.status_code}")



game_id_log=[]

for year in range(2001,2024): #get all regular season games between 2001 and 2023 and weeks 1-17
    for week in range(1,18):
        get_game_ids(year, week,2)

for year in range(2021,2024): #gets all week 18 games
    get_game_ids(year,18,2)


for year in range(2001,2024): #gets playoff games
    for week in range(1,6):
        get_game_ids(year,week,3)

get_game_ids(2024,1,2) #gets week 1 2024 games
            

    
with open('id_log.json','w') as file:
    json.dump(game_id_log,file)


print('done')
