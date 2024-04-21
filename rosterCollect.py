from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import playercareerstats, commonplayerinfo, scoreboardv2, teamdetails, leaguestandings
import requests
import json
import pandas as pd
import html
def common_player_details(player_id):
    player_common_details = commonplayerinfo.CommonPlayerInfo(player_id=player_id)

    with open("test_file.json", "w") as file:
        file.write(player_common_details.get_normalized_json())

    with open("test_file.json", "r") as file:
        player_json = json.load(file)

    # player_json = json.load(player_common_details.get_normalized_json())
    return player_json['CommonPlayerInfo'][0]

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0' } 
# ACTIVE ROSTER
print("ACTIVE ROSTER")
fullName = []
Picture=[]
Team=[]
TeamPic=[]
i=0
for player in players.get_active_players():
    playerPic = f'https://cdn.nba.com/headshots/nba/latest/1040x760/{player["id"]}.png'
    detail = common_player_details(player["id"])
    teamPic=f"https://cdn.nba.com/logos/nba/{detail["TEAM_ID"]}/primary/L/logo.svg"
    fullName.append(detail["DISPLAY_FIRST_LAST"])
    Picture.append(playerPic)
    Team.append(f"{detail["TEAM_CITY"]} {detail["TEAM_NAME"]}")
    TeamPic.append(teamPic)
    print(f"{i}: {detail["DISPLAY_FIRST_LAST"]}")
    i+=1
data={"fullName":fullName,"Picture":Picture,"TeamPic":TeamPic,"Team":Team}
df = pd.DataFrame(data,index=None)
df.to_json("activeRoster_file.json",index=False)

import time
time.sleep(5)

# ALL TIME ROSTER
print("ALL TIME ROSTER")
fullName = []
Picture=[]
Team=[]
TeamPic=[]
i=0
for player in players.get_players():
    playerPic = f'https://cdn.nba.com/headshots/nba/latest/1040x760/{player["id"]}.png'
    detail = common_player_details(player["id"])
    teamPic=f"https://cdn.nba.com/logos/nba/{detail["TEAM_ID"]}/primary/L/logo.svg"
    fullName.append(detail["DISPLAY_FIRST_LAST"])
    Picture.append(playerPic)
    Team.append(f"{detail["TEAM_CITY"]} {detail["TEAM_NAME"]}")
    TeamPic.append(teamPic)
    print(f"{i}: {detail["DISPLAY_FIRST_LAST"]}")
    i+=1
data={"fullName":fullName,"Picture":Picture,"TeamPic":TeamPic,"Team":Team}
df = pd.DataFrame(data,index=None)
df.to_json("allRoster_file.json",index=False)
import plotly.express as px
df = px.data.tips()
fig = px.histogram(df, x="sex", y="total_bill",
             color='smoker', barmode='group',
             histfunc='avg',
             height=400)
fig.show()