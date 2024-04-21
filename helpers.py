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
    athletes=[]
    colums = []
    colums.extend(_container.columns(len(playerList)))
    for col,playerName in zip(colums,playerList):
        player=players.find_players_by_full_name(f"{playerName}")[0]
        details = common_player_details(player["id"])
        totalSeasons=len(availableSeasons())
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


# working on
def match(val):

    match val:
        case 'Points':
            return 'PTS'
        case 'Games Played':
            return 'GP'
        case 'Minutes Played':
            return 'MIN'
        case 'Field Gols Made (FGM)':
            return 'FGM'
        case 'Field Goals Attempted (FGA)':
            return 'FGA'
        case 'Field Goals Percentage (FGP in %)':
            return 'FG_PCT'

@st.cache_data(show_spinner=False)
def getData(df, index):
    data = []

    if index == 'FG_PCT':
        for i in df[index]:
            data.append(i*100)
    else:
        for i in df[index]:
            data.append(i)
        
    return data
@st.cache_data(show_spinner=False)
def get_custom_dataframe(parameters, df):
    data_map = {}

    seasons = []
    for season in df['SEASON_ID']:
        seasons.append(season)
    data_map['Season'] = seasons

    for i in parameters:
        data_map[i] = getData(df, match(i))
    
    return pd.DataFrame(data_map)
@st.cache_data(show_spinner=False)
def get_api_dataframe(player_id):
    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    return career.get_data_frames()[0]

def dataframe(player_id, df):

    parameters = st.multiselect(
        "Select the data you want to see.",
        options=[
            "Points",
            "Games Played",
            "Minutes Played",
            "Field Gols Made (FGM)",
            "Field Goals Attempted (FGA)",
            "Field Goals Percentage (FGP in %)"
        ]
    )   
    
    button = st.button("Display Stats")
    if button:
        dataFrame = get_custom_dataframe(parameters=parameters, df=df)
        st.dataframe(dataFrame)
def player_details(player_id):

    df = get_api_dataframe(player_id)
    dataframe(player_id=player_id, df=df)

    points, minutes, games_played = st.tabs(['Points', 'Minutes', 'Games'])

    with points:
        st.subheader("Points scored each season")
        st.line_chart(df, x='SEASON_ID', y='PTS')

    with minutes:
        st.subheader("Minutes played each season")
        st.line_chart(df, x='SEASON_ID', y='MIN')

    with games_played:
        st.subheader("Number of games played each season")
        st.line_chart(df, x='SEASON_ID', y='GP')