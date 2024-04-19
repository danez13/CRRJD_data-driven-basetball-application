import streamlit as st
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import playercareerstats, commonplayerinfo, scoreboardv2, teamdetails, leaguestandings
import requests
import json
import redi_helpers
import datetime
from array import array
# from streamlit_image_select import image_select
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0' } 
@st.cache_data(show_spinner=False,experimental_allow_widgets=True)
def display_player(player:dict):
    col1,col2,col3,col4= st.columns([0.35,1,0.35,1])
    with col1:
        playerData=common_player_details(player["id"])
        player_link = f'https://cdn.nba.com/headshots/nba/latest/1040x760/{player["id"]}.png'
        request = requests.get(player_link,headers=headers)
        if request.status_code > 300:
            st.image("placeholder.png",width=50)
        else:
            st.image(player_link,width = 50)
    with col2:
        st.write(playerData["DISPLAY_FIRST_LAST"])
    with col3:
        Team_link=f"https://cdn.nba.com/logos/nba/{playerData["TEAM_ID"]}/primary/L/logo.svg"
        request = requests.get(Team_link,headers=headers)
        if request.status_code > 300:
            st.image("teamPlaceHolder.png",width=50)
        else:
            st.image(Team_link,width = 50)
    with col4:
        st.write(f"{playerData["TEAM_CITY"]} {playerData["TEAM_NAME"]}")

@st.cache_data(show_spinner=False,experimental_allow_widgets=True)
def display_detailedPlayer(playerList:list):
    colums = []
    colums.extend(st.columns(len(playerList)))
    for col,playerName in zip(colums,playerList):
        player=players.find_players_by_full_name(f"{playerName}")[0]
        details = common_player_details(player["id"])
        with col:
            player_link = f'https://cdn.nba.com/headshots/nba/latest/1040x760/{player["id"]}.png'
            request = requests.get(player_link,headers=headers)
            if request.status_code > 300:
                st.image("placeholder.png",width=180)
            else:
                st.image(player_link,width = 180)
            st.write(details["DISPLAY_FIRST_LAST"])
            st.write(f"country: {details["COUNTRY"]}")
            st.write(f"height: {details["HEIGHT"].replace("-","'")}")
            st.write(f"weight: {details["WEIGHT"]}")
            st.write(f"Jersey: {details["JERSEY"]}")
            st.write(f"position: {details["POSITION"]}")
            st.write(f"{details["TEAM_CITY"]} {details["TEAM_NAME"]}")
        
    
@st.cache_data(show_spinner=False)
def search_for_player(activity:str|None=None):
    success=False
    if activity == "active":
        for player in players.get_active_players():
            success=True
            display_player(player)
    else:
        for player in players.get_players():
            success=True
            display_player(player)
    if not success:
        st.warning("Failure")

# get a list of all players
@st.cache_data(show_spinner=False)
def get_all_players():
    all_players = players.get_players()

    player_names = []
    for player in all_players:
        player_names.append(player['full_name'])

    return player_names

@st.cache_resource(show_spinner=False)
def common_player_details(player_id):
    player_common_details = commonplayerinfo.CommonPlayerInfo(player_id=player_id)

    with open("test_file.json", "w") as file:
        file.write(player_common_details.get_normalized_json())

    with open("test_file.json", "r") as file:
        player_json = json.load(file)

    # player_json = json.load(player_common_details.get_normalized_json())
    return player_json['CommonPlayerInfo'][0]

def test():
    return