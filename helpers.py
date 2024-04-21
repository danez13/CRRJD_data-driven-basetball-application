import streamlit as st
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import playercareerstats, commonplayerinfo, scoreboardv2, teamdetails, leaguestandings
import requests
import json
import redi_helpers
import datetime
from array import array
import pandas as pd
import plotly.express as px
from streamlit.delta_generator import DeltaGenerator
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0' } 
@st.cache_data(show_spinner=False,experimental_allow_widgets=True)
def display_detailedPlayer(playerList:list,_container:DeltaGenerator):
    regularSeasonTotalStats=[]
    colums = []
    postSeasonTotalStats = []
    colums.extend(_container.columns(len(playerList)))
    for col,playerName in zip(colums,playerList):
        player=players.find_players_by_full_name(f"{playerName}")[0]
        details = common_player_details(player["id"])
        totalSeasons=len(availableSeasons())
        regularSeasonTotalStats.append(totalRegularSeason(player["id"]))
        postSeasonTotalStats.append(totalPostSeason(player["id"]))
        with col:
            player_link = f'https://cdn.nba.com/headshots/nba/latest/1040x760/{player["id"]}.png'
            request = requests.get(player_link,headers=headers)
            if request.status_code > 300:
                col.image("placeholder.png",width=180)
            else:
                col.image(player_link,width = 180)
            st.write()
            col.write(details["DISPLAY_FIRST_LAST"])
            col.write(f"Country: {details["COUNTRY"]}")
            col.write(f"Height: {details["HEIGHT"].replace("-","'")}")
            col.write(f"Weight: {details["WEIGHT"]}")
            col.write(f"Jersey: {details["JERSEY"]}")
            col.write(f"Position: {details["POSITION"]}")
            col.write(f"Team: {details["TEAM_CITY"]} {details["TEAM_NAME"]}")
            col.write(f"Total Seasons Played: {totalSeasons}")
    totalStats,averageStats = _container.tabs(["total stats", "average stats"])  
    with totalStats:
        df = pd.DataFrame(regularSeasonTotalStats)
        newdf=df.drop(columns=["PLAYER_ID","LEAGUE_ID","Team_ID"],axis=1)
        fig=px.histogram(x=['GP', 'GS', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS'],y=newdf.values.tolist(),barmode="group")
        totalStats.plotly_chart(fig,True)
    with averageStats:
        averageStats.write("goodbye")  
# get a list of all players
@st.cache_data(show_spinner=False)
def get_all_players():
    all_players = players.get_players()

    player_names = []
    for player in all_players:
        player_names.append(player['full_name'])

    return player_names

# get athlete basic details
@st.cache_resource(show_spinner=False,experimental_allow_widgets=True)
def common_player_details(player_id):
    player_common_details = commonplayerinfo.CommonPlayerInfo(player_id=player_id)

    with open("test_file.json", "w") as file:
        file.write(player_common_details.get_normalized_json())

    with open("test_file.json", "r") as file:
        player_json = json.load(file)

    # player_json = json.load(player_common_details.get_normalized_json())
    return player_json['CommonPlayerInfo'][0]

# get number of seasons an athlete played
@st.cache_resource(show_spinner=False,experimental_allow_widgets=True)
def availableSeasons():
    with open("test_file.json", "r") as file:
        player_json = json.load(file)

    # player_json = json.load(player_common_details.get_normalized_json())
    return player_json["AvailableSeasons"]

# total regular season stats
@st.cache_resource(show_spinner=False,experimental_allow_widgets=True)
def totalRegularSeason(id):
    test = playercareerstats.PlayerCareerStats(id)
    jsonResponse=test.get_normalized_json()
    with open("test_file2.json","w") as file:
        file.write(jsonResponse)

    with open("test_file2.json", "r") as file:
        player_json = json.load(file)
    return player_json["CareerTotalsRegularSeason"][0]
    
@st.cache_resource(show_spinner=False,experimental_allow_widgets=True)
def totalPostSeason(id):
    with open("test_file2.json", "r") as file:
        player_json = json.load(file)
    return player_json["CareerTotalsPostSeason"][0]