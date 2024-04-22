from nba_api.stats.endpoints import commonallplayers, leaguestandings, commonplayerinfo
import streamlit as st
import json
from PIL import Image

image = Image.open("nba.jpg")
st.set_page_config(
    page_title="NBA Stats And Games", 
    page_icon=image,
    initial_sidebar_state="collapsed"
)

@st.cache_data(show_spinner=False)
def get_league_teams():

    league_standings = leaguestandings.LeagueStandings()

    teams = league_standings.get_dict()
    with open("league.json", "w") as file:
        file.write(league_standings.get_json())
    
    with open("league.json", "r") as file:
        teams = json.load(file)

    return teams['resultSets'][0]['rowSet']


@st.cache_data(show_spinner=False)
def get_team_details(team_id):
    league_teams = get_league_teams()

    for entry in league_teams:
        if entry[2] == team_id:
            return entry


@st.cache_data(show_spinner=False)
def get_team_players(team_id):

    team_players = []

    all_players = commonallplayers.CommonAllPlayers()

    for player in all_players.get_dict()['resultSets'][0]['rowSet']:
        if player[8] == team_id:
            team_players.append(player)

    return team_players

@st.cache_data(show_spinner=False)
def get_player_stats(player_id):
    career = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
    
    return career.get_dict()['resultSets'][0]['rowSet']
    

with open("team_id.txt", "r") as file:
    team_id = int(file.read())

team_logo = f'https://cdn.nba.com/logos/nba/{team_id}/primary/L/logo.svg'


col1, col2 = st.columns([1, 1])

with col1:
    st.image(team_logo, width=250)

with col2:
    team_details = get_team_details(team_id=team_id)
    team_name = f"{team_details[3]} {team_details[4]}" # type: ignore
    st.header(team_name)

team_players = get_team_players(team_id=team_id)

for player in team_players:
    col1, col2 = st.columns([1, 1])

    player_stats = get_player_stats(player_id=player[0])


    with col1:
        photo_link = f'https://cdn.nba.com/headshots/nba/latest/1040x760/{player[0]}.png'
        st.image(photo_link, width=250)
    with col2:
        st.caption(f"Player Name: {player_stats[0][4]}")
        st.caption(f"Player Birthday: {player_stats[0][7][:10]}")
        st.caption(f"Player Height: {player_stats[0][11][0]}'{player_stats[0][11][2]}''")
        st.caption(f"Player Weight: {player_stats[0][12]}")
        st.caption(f"Player Number: {player_stats[0][14]}")
        st.caption(f"Player Position: {player_stats[0][15]}")
    st.markdown("""---""")

_, col5 = st.columns([7, 1])

with col5:
    button = st.button("Go Back")
    if button:
        st.switch_page("main.py")