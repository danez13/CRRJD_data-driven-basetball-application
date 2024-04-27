import streamlit as st
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import playercareerstats, commonplayerinfo, scoreboardv2, teamdetails, leaguestandings,CommonTeamRoster
import requests
import json
import redi_helpers
from datetime import date, timedelta
from array import array
import pandas as pd
import plotly.express as px
from streamlit.delta_generator import DeltaGenerator
import folium
from streamlit_folium import folium_static#
import plotly.graph_objs as go
################################################################################################################
################################################################################################################
################################################################################################################
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0' } 

def display_detailedPlayer(playerList:list,_container:DeltaGenerator):
    regularSeasonTotalStats=[]
    colums = []
    playerNames = []
    allTimeStats = []
    postSeasonTotalStats = []
    colums.extend(_container.columns(len(playerList)))
    for col,playerName in zip(colums,playerList):
        player=players.find_players_by_full_name(f"{playerName}")[0]
        details = common_player_details(player["id"])
        totalSeasons=len(availableSeasons(player["id"]))
        regularSeasonTotalStats.append(totalRegularSeason(player["id"]))
        allTimeStats.append(redi_helpers.get_api_dataframe(player_id=player["id"]))
        playerNames.append(playerName)
        postSeasonTotalStats.append(totalPostSeason(player["id"]))
        with col:
            player_link = f'https://cdn.nba.com/headshots/nba/latest/1040x760/{player["id"]}.png'
            request = requests.get(player_link,headers=headers)
            if request.status_code > 300:
                col.image("placeholder.png",width=180)
            else:
                col.image(player_link,width = 180)
            details["HEIGHT"].replace("-","\'")
            st.write()
            col.write(details["DISPLAY_FIRST_LAST"])
            col.write(f"Country: {details['COUNTRY']}")
            col.write(f"Height: {details['HEIGHT']}")
            col.write(f"Weight: {details['WEIGHT']}")
            col.write(f"Jersey: {details['JERSEY']}")
            col.write(f"Position: {details['POSITION']}")
            col.write(f"Team: {details['TEAM_CITY']} {details['TEAM_NAME']}")
            col.write(f"Total Seasons Played: {totalSeasons}")  
    st.divider()
    op1,op2,op3,op4,op5,op6=st.columns([0.8,0.85,0.85,0.8,1,1])
    with op1:
        opt1 = op1.checkbox("Points")
    with op2:
        opt2 = op2.checkbox("Games Played")
    with op3:
        opt3 = op3.checkbox("Minutes Played")
    with op4:
        opt4 = op4.checkbox("Field Goals Made (FGM)")
    with op5:
        opt5 = op5.checkbox("Field Goals Attempted (FGA)")
    with op6:
        opt6 = op6.checkbox("Field Goals Percentage (FGP in %)")
    parameters = [opt1, opt2, opt3, opt4, opt5, opt6]

    button = st.button("Display Stats")
    if button:
        for i, player_stats in enumerate(allTimeStats):
            st.subheader(f"{playerNames[i]}")
            redi_helpers.dataframe2(parameters, player_stats)
    tab1, tab2, tab3 = st.tabs(["Points Scored", "Assists Made", "Minutes Played"])
    with tab1:
        traces = []

        for i, entry in enumerate(allTimeStats):
            traces.append(go.Line(y=entry['PTS'], name=playerNames[i]))

        fig = go.Figure(traces)
        fig.update_layout(barmode='group', xaxis_title='Season Index', yaxis_title='Points', title='Points per Season')

        st.plotly_chart(fig,True)
    
    with tab2:
        traces = []

        for i, entry in enumerate(allTimeStats):
            traces.append(go.Line(y=entry['AST'], name=playerNames[i]))

        fig = go.Figure(traces)
        fig.update_layout(barmode='group', xaxis_title='Season Index', yaxis_title='Asists', title='Asists per Season')

        st.plotly_chart(fig,True)

    with tab3:
        traces = []

        for i, entry in enumerate(allTimeStats):
            traces.append(go.Line(y=entry['MIN'], name=playerNames[i]))

        fig = go.Figure(traces)
        fig.update_layout(barmode='group', xaxis_title='Season Index', yaxis_title='Minutes', title='Minutes per Season')

        st.plotly_chart(fig,True)


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
def availableSeasons(id):
    player_common_details = commonplayerinfo.CommonPlayerInfo(player_id=id)

    with open("test_file.json", "w") as file:
        file.write(player_common_details.get_normalized_json())
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

################################################################################################################
################################################################################################################
################################################################################################################
@st.cache_data(show_spinner=False)
def get_scoreboard(gameday):
    score = scoreboardv2.ScoreboardV2(game_date=gameday)
    
    with open("scoreboard.json", "w") as file:
        file.write(score.get_json())

    with open("scoreboard.json", "r") as file:
        score_json = json.load(file)

    return score_json

def get_league_teams():

    league_standings = leaguestandings.LeagueStandings()

    with open("league.json", "w") as file:
        file.write(league_standings.get_json())

def display_matchups(matchups, day,_container:DeltaGenerator):
    
    global match_team_ids
    global index
    global button_list
    global days
    # get_league_teams()

    _container.subheader(f"Game Day: {day}")
    _container.divider()
        
    for entry in matchups:
        col1, col2, col3 = _container.columns([0.4,1,0.15])
        team_1_name = get_team_name(team_id=entry[6])
        team_2_name = get_team_name(team_id=entry[7])
        cont=_container.container()
        with cont:
            with col1:
                teamPic=f"https://cdn.nba.com/logos/nba/{entry[6]}/primary/L/logo.svg"
                col1.image(teamPic,width=50)
            with col2:
                col2.text(f"{team_1_name} vs. {team_2_name}")
            with col3:
                teamPic=f"https://cdn.nba.com/logos/nba/{entry[7]}/primary/L/logo.svg"
                col3.image(teamPic,width=50)
            col4, col5, col6 = st.columns([0.65,1,0.15])
            with col5:
                details=col5.button("view matchup details",key=int(entry[2]))  
            if details:
                cont2=cont.container()
                with cont2:
                    with open("game_id.txt", "w") as file:
                        file.write(f"{entry[2]}\n")
                        file.write(f"{entry[0][:10]}")

                    st.switch_page("pages/matchdetails.py")
        # st.divider() 

@st.cache_data(show_spinner=False)
def get_team_details(team_id):
    team_details = teamdetails.TeamDetails(team_id=team_id)

    with open("temp.json", "w") as file:
       file.write(team_details.get_json())

    with open("temp.json", "r") as file:
       details_json = json.load(file)

    return details_json

@st.cache_data(show_spinner=False)
def map_creator(location):

    lat_and_long = get_lat_and_long(location=location)
    latitude = lat_and_long[0]
    longitude = lat_and_long[1]

    # center on the station
    m = folium.Map(location=[latitude, longitude], zoom_start=10)

    # add marker for the station
    folium.Marker([latitude, longitude], popup="Station", tooltip="Station").add_to(m)

    # call to render Folium map in Streamlit
    folium_static(m)

@st.cache_data(show_spinner=False)
def get_lat_and_long(location: str):
    url = "https://api.geoapify.com/v1/geocode/search?text="
    api_key = "&apiKey=d404cec595b9452ea04c1bb1fe910f18"

    location_list = location.split()

    location_search = ""

    for i in location_list:
        location_search = location_search + i + "%20"
    
    location_search = location_search[:len(location_search)-3]

    fullURL = url+location_search+api_key

    request = requests.get(fullURL)

    loc_json = request.json()

    return [loc_json['features'][0]['properties']['lat'], loc_json['features'][0]['properties']['lon']]

@st.cache_data(show_spinner=False)
def get_team_name(team_id):

    with open("league.json", "r") as file:
        team_json = json.load(file)

    teams = team_json['resultSets'][0]['rowSet']

    for entry in teams:
        if team_id == entry[2]:
            team_name = entry[3] + " " + entry[4]

    return team_name
################################################################################################################
################################################################################################################
################################################################################################################
def displayTeamRoster():
    pass
def TeamRoster(team_id):
    player_common_details = CommonTeamRoster(team_id)

    with open("test_file3.json", "w") as file:
        file.write(player_common_details.get_normalized_json())

    with open("test_file3.json", "r") as file:
        player_json = json.load(file)

    # player_json = json.load(player_common_details.get_normalized_json())
    return player_json["CommonTeamRoster"]