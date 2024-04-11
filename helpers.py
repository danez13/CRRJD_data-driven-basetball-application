import streamlit as st
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import playercareerstats, commonplayerinfo, scoreboardv2, teamdetails, leaguestandings
import requests
import json
import redi_helpers
from streamlit_image_select import image_select
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0' } 
@st.cache_data(show_spinner=False,experimental_allow_widgets=True)
def display_player(player:dict):
    with st.container() as container:
        photo_link = f'https://cdn.nba.com/headshots/nba/latest/1040x760/{player["id"]}.png'
        request = requests.get(photo_link,headers=headers)
        if request.status_code > 300:
            img = st.image("placeholder.png",width=180)
        else:
            img = st.image(photo_link,width = 180)
        st.write(player["full_name"])
        
    st.divider()

@st.cache_data(show_spinner=False)
def search_for_player(playerSearch:str|None,activity:str|None=None):
    success=False
    if playerSearch is not None:
        if activity == "active":
            for player in players.get_active_players():
                if playerSearch.upper() in player["full_name"].upper():
                    success=True
                    display_player(player)
        else:
            for player in players.get_players():
                if playerSearch.upper() in player["full_name"].upper():
                    success=True
                    display_player(player)
    else:
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

def test():
    return