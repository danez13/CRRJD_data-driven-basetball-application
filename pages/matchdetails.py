from nba_api.live.nba.endpoints import boxscore, scoreboard
from nba_api.stats.endpoints import scoreboardv2
import streamlit as st
import json
import requests
from streamlit_folium import folium_static
import folium
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from PIL import Image

image = Image.open("nba.jpg")
st.set_page_config(
    page_title="NBA Stats And Games", 
    page_icon=image,
    initial_sidebar_state="collapsed"
)

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
def map_creator(location):

    lat_and_long = get_lat_and_long(location=location)
    latitude = lat_and_long[0]
    longitude = lat_and_long[1]

    # center on the station
    m = folium.Map(location=[latitude, longitude], zoom_start=15)

    # add marker for the station
    folium.Marker([latitude, longitude], popup="Station", tooltip="Station").add_to(m)

    # call to render Folium map in Streamlit
    folium_static(m)

@st.cache_data(show_spinner=False)
def get_home_team_name(match_details):
    team_city = match_details['game']['homeTeam']['teamCity']
    team_name = match_details['game']['homeTeam']['teamName']
    return f"{team_city} {team_name}"

@st.cache_data(show_spinner=False)
def get_away_team_name(match_details):
    team_city = match_details['game']['awayTeam']['teamCity']
    team_name = match_details['game']['awayTeam']['teamName']
    return f"{team_city} {team_name}"

@st.cache_data(show_spinner=False)
def get_team_name(team_id, val = 0):

    if val == 0:
        with open("league.json", "r") as file:
            team_json = json.load(file)

        teams = team_json['resultSets'][0]['rowSet']

        for entry in teams:
            if team_id == entry[2]:
                team_name = entry[3] + " " + entry[4]

        return team_name
    
    else:
        with open("league.json", "r") as file:
            team_json = json.load(file)

        teams = team_json['resultSets'][0]['rowSet']

        for entry in teams:
            if team_id == entry[2]:
                return entry[3]


def get_city_name(val, team_id, match_details):
    if val == 0:
        return match_details['game']['homeTeam']['teamCity']
    else:
        return get_team_name(team_id=team_id, val=val)



with open("game_id.txt", "r") as file:
    game_id = file.readline()
    game_id = game_id[:len(game_id)-1]
    game_date = file.readline()


st.header("Match Details")


try:
    score = boxscore.BoxScore(game_id=game_id)
    state = True
except Exception:
    score = scoreboardv2.ScoreboardV2(game_date=game_date)
    state = False

if state:
    with open("game_details.json", "w") as file:
        file.write(score.get_json())

    match_details = score.get_dict()

    col1, col2, col3 = st.columns([1, 5, 1])

    with col1:
        image_link = f'https://cdn.nba.com/logos/nba/{match_details['game']['homeTeam']['teamId']}/primary/L/logo.svg'
        st.image(image_link, width=50)

    with col2:
        st.subheader(f'{get_home_team_name(match_details=match_details)} vs. {get_away_team_name(match_details=match_details)}')

    with col3:
        image_link = f'https://cdn.nba.com/logos/nba/{match_details['game']['awayTeam']['teamId']}/primary/L/logo.svg'
        st.image(image_link, width=50) 

    st.markdown("""---""")
    

    map = {
        "Points": [match_details['game']['homeTeam']['score'], match_details['game']['awayTeam']['score']],
        "Field Goals Attempted": [match_details['game']['homeTeam']['statistics']['fieldGoalsAttempted'], match_details['game']['awayTeam']['statistics']['fieldGoalsAttempted']],
        "Field Goals Made": [match_details['game']['homeTeam']['statistics']['fieldGoalsMade'], match_details['game']['awayTeam']['statistics']['fieldGoalsMade']],
        "Field Goals Percentage": [round(match_details['game']['homeTeam']['statistics']['fieldGoalsPercentage'], 2), round(match_details['game']['awayTeam']['statistics']['fieldGoalsPercentage'], 2)],
        "Two Pointers Attempted": [match_details['game']['homeTeam']['statistics']['twoPointersAttempted'], match_details['game']['awayTeam']['statistics']['twoPointersAttempted']],
        "Two Pointers Made": [match_details['game']['homeTeam']['statistics']['twoPointersMade'], match_details['game']['awayTeam']['statistics']['twoPointersMade']],
        "Two Pointers Percentage": [round(match_details['game']['homeTeam']['statistics']['twoPointersPercentage'], 2), round(match_details['game']['awayTeam']['statistics']['twoPointersPercentage'], 2)],
        "Three Pointers Attempted": [match_details['game']['homeTeam']['statistics']['threePointersAttempted'], match_details['game']['awayTeam']['statistics']['threePointersAttempted']],
        "Three Pointers Made": [match_details['game']['homeTeam']['statistics']['threePointersMade'], match_details['game']['awayTeam']['statistics']['threePointersMade']],
        "Three Pointers Percentage": [round(match_details['game']['homeTeam']['statistics']['threePointersPercentage'], 2), round(match_details['game']['awayTeam']['statistics']['threePointersPercentage'], 2)]
    }

    for entry in map:
        col4, col5, col6 = st.columns([4, 5, 4])

        with col4:
            st.markdown(f"<p style='text-align: center; color: white; font-size:100%'>{map[entry][0]}</p>", unsafe_allow_html=True)
        with col5:
            st.markdown(f"<p style='text-align: center; color: red; font-size:100%'>{entry}</p>", unsafe_allow_html=True)
        with col6:
            st.markdown(f"<p style='text-align: center; color: white; font-size:100%'>{map[entry][1]}</p>", unsafe_allow_html=True)

        st.markdown("""---""")

    df_home = {
        "Period": [],
        "Points": []
    }

    df_away = {
        "Period": [],
        "Points": []
    }

    home_team_periods = match_details['game']['homeTeam']['periods']
    away_team_periods = match_details['game']['awayTeam']['periods']

    for i in range(len(home_team_periods)):
        df_home['Period'].append(int(home_team_periods[i]['period']))
        df_home['Points'].append(home_team_periods[i]['score'])

        df_away['Period'].append(int(away_team_periods[i]['period']))
        df_away['Points'].append(away_team_periods[i]['score'])

     # Sample data for demonstration
    trace1 = go.Bar(x=df_home['Period'], y=df_home['Points'], name=get_home_team_name(match_details=match_details))
    trace2 = go.Bar(x=df_away['Period'], y=df_away['Points'], name=get_away_team_name(match_details=match_details))

    # Create a figure containing both traces
    fig = go.Figure([trace1, trace2])

    #   Update layout to customize the appearance
    fig.update_layout(barmode='group', xaxis_title='Period', yaxis_title='Points', title='Points per Period')

    # Render the plotly figure using Plotly Streamlit method
    st.plotly_chart(fig)


    st.markdown("""---""")

    st.subheader("Starting Lineups")
    col7, col8 = st.columns([1, 1])

    with col7:

        st.markdown(f"<p style='color: white; font-size:150%'>{get_home_team_name(match_details=match_details)}</p>", unsafe_allow_html=True)

        players = match_details['game']['homeTeam']['players']
        starting_lineup = []

        for player in players:
            if player['starter'] == "1":
                starting_lineup.append(player)
        
        for player in starting_lineup:
            st.text(f"{player['name']} ({player['jerseyNum']})")

    with col8:
        st.markdown(f"<p style='color: white; font-size:150%'>{get_away_team_name(match_details=match_details)}</p>", unsafe_allow_html=True)

        players = match_details['game']['awayTeam']['players']
        starting_lineup = []

        for player in players:
            if player['starter'] == "1":
                starting_lineup.append(player)

        for player in starting_lineup:
            st.text(f"{player['name']} ({player['jerseyNum']})")

    st.markdown("""---""")
    display_map = st.button("Display Location")

    if display_map:
        map_creator(f"{match_details['game']['arena']['arenaName']} {match_details['game']['arena']['arenaCity']}")
        st.caption(f"Arena Name: {match_details['game']['arena']['arenaName']}")
        st.caption(f"Location: {match_details['game']['arena']['arenaCity']}, {match_details['game']['arena']['arenaState']}, {match_details['game']['arena']['arenaCountry']}")
        st.caption(f"Attendance: {match_details['game']['attendance']}")

    _, col = st.columns([7, 1])

    with col:
        go_back_button = st.button("Go Back")

        if go_back_button:
            st.switch_page("main.py")

    


else:

    score = scoreboardv2.ScoreboardV2(game_date=game_date)
    
    matches = score.get_dict()['resultSets'][0]['rowSet']

    for entry in matches:
        if entry[2] == game_id:
            start_time = entry[4]
            home_team_id = entry[6]
            away_team_id = entry[7]
            stadium_name = entry[15]
            break
    
    col1, col2, col3 = st.columns([1, 5, 1])

    with col1:
        image_link = f'https://cdn.nba.com/logos/nba/{home_team_id}/primary/L/logo.svg'
        st.image(image_link, width=50)

    with col2:
        st.subheader(f'{get_team_name(home_team_id)} vs. {get_team_name(away_team_id)}')

    with col3:
        image_link = f'https://cdn.nba.com/logos/nba/{away_team_id}/primary/L/logo.svg'
        st.image(image_link, width=50)

    st.caption(f"Start Time: {start_time}")
    st.caption(f"Stadium Place: {stadium_name}, {get_city_name(val = 1, team_id=home_team_id, match_details="")}")

    display_map = st.button("Display Map")

    if display_map:
        map_creator(f"{stadium_name} {get_city_name(val = 1, team_id=home_team_id, match_details="")}")
        
    _, col = st.columns([7, 1])

    with col:
        go_back_button = st.button("Go Back")

        if go_back_button:
            st.switch_page("main.py")


    