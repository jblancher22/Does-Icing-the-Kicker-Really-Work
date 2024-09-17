import requests
from requests.exceptions import HTTPError
import time
import json
import pandas as pd
import re

log=[]
YARDS_PATTERN=r'(\d+)\s*yards?'

with open('id_log_2009_onwards.json', 'r') as file:
    game_ids=json.load(file)

for game_id in game_ids:   

    response=requests.get(f'https://cdn.espn.com/core/nfl/playbyplay?xhr=1&gameId={game_id}')
    response.raise_for_status()
    apijson=response.json()
    year=apijson["gamepackageJSON"]['header']['season']['year']
    playoffs_ind=int(apijson["gamepackageJSON"]['header']['season']['type'])
    if playoffs_ind==3:
        playoffs=1
    else:
        playoffs=0
        
    

    try:
        drives=apijson["gamepackageJSON"]['drives']['previous']
    
        for drive in drives:
            try:
                if drive['displayResult'] in ['Missed FG','Field Goal','Made FG']:
                    
                    minutes_on_clock=drive['plays'][-1]['clock']['displayValue'][:2]
                    minutes_on_clock=int(minutes_on_clock.replace(':',''))
                    quarter=drive['plays'][-1]['period']['number']

                    if (minutes_on_clock<2 and quarter==4) or quarter>4: #Finds all FG attempts in 4th quarter and less than 2 mins left or at any point in overtime 
                        for play_num in range(len(drive['plays'])):#find play in drive where the field goal occurs. Sometimes not last play because "end of game" is the last pla
                            text=drive['plays'][play_num]['text']
                            
                            if ('field goal' in text) and ("PENALTY" not in text) and ('BLOCKED' not in text): #this is the play where FG is attempted #exclude FG where there was a penalty or it was blocked
                                attempt_distance=re.search(YARDS_PATTERN, drive['plays'][play_num]['text']).group(1)
                                opposing_team_unsplit=drive['plays'][play_num]['start']['possessionText']#checks which side of the field the ball is, assumes that is opponent as teams don't kick FG from their side of the field
                                opposing_team=opposing_team_unsplit.split(' ')[0]
                                
                                try:
                                    previous_play=drive['plays'][play_num-1]['type']['text'] #checks the play prior to see if its a timeout
                                except IndexError: 
                                    iced=0
                                    
                                else:
                                    
                                    if previous_play=='Timeout': 
                                        
                                        timeout_taker_unsplit=drive['plays'][play_num-1]['text'] #notation for timeouts has changed too much
                                        #check differences between gameIds 211015006,261230028, 290920006. Just starting in 2009 
                                        try:
                                            timeout_taker=timeout_taker_unsplit.split(' ')[3] #sees if the timeout was taken by the kicking team
                                        except IndexError: #skip drives that aren't formatted correctly. See the last drive in game id 320930027 for reference.
                                            pass
                                        else:

                                            if timeout_taker==opposing_team:
                                                iced=1
                                            else:
                                                iced=0
                                    else:
                                        iced=0
                                        
                                finally:
                                    
                                    if drive['displayResult']!='Missed FG':
                                        converted=1
                                    else:
                                        converted=0
                                  
                                row={'Year':year,'Game Id':game_id, 'playoffs?': playoffs ,'distance':attempt_distance,'Timeout by opposing team the play prior?':iced, 'Converted?':converted} 
                                log.append(row)
            except KeyError: #skip drives that aren't formatted correctly. See the first drive in game id 331201020 for reference.
                pass

    except KeyError: #excludes games that have no play-by-play, because they were postponed or simply unavailable. See game ids 400554331, 400554366, 400951581 
        pass
    
            
                    

df=pd.DataFrame(log)
df.to_json('fg_log_8.json',orient='records', lines=True)
print('done')

