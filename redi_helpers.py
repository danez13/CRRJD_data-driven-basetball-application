from nba_api.stats.static import players

from nba_api.stats.endpoints import playercareerstats, commonplayerinfo, scoreboardv2, teamdetails, leaguestandings
from datetime import date, timedelta
import json
import requests
import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium
# GLOBAL VARIABLES
index = 0
button_list = []
match_team_ids = []
days = []
# 


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

# PLAYER DATA
@st.cache_data(show_spinner=False)
def get_all_players():
    all_players = players.get_players()

    player_names = []
    for player in all_players:
        player_names.append(player['full_name'])
    return player_names


@st.cache_data(show_spinner=False)
def get_api_dataframe(player_id):
    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    return career.get_data_frames()[0]


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


@st.cache_resource(show_spinner=False)
def common_player_details(player_id):
    player_common_details = commonplayerinfo.CommonPlayerInfo(player_id=player_id)

    with open("test_file.json", "w") as file:
        file.write(player_common_details.get_normalized_json())

    with open("test_file.json", "r") as file:
        player_json = json.load(file)

    # player_json = json.load(player_common_details.get_normalized_json())
    return player_json['CommonPlayerInfo'][0]


def player_stats():
        
    player_choice = st.sidebar.selectbox('Select a player:', options=get_all_players(), index=None, placeholder="Select an option...")

    if player_choice is not None:
        player_id = players.find_players_by_full_name(player_choice)[0]['id']
        st.header(f"{player_choice}")

        column1, column2 = st.columns([1,1.8])

        with column1:
            photo_link = f'https://cdn.nba.com/headshots/nba/latest/1040x760/{player_id}.png'
            request = requests.get(photo_link)
            if request.status_code > 300:
                st.image("placeholder.png", width=180)
            else:
                st.image(photo_link, width=240) 
               

        with column2:
            details = common_player_details(player_id)
            output = f"Birthday:  \t{details['BIRTHDATE'][:10]}  \nOrigin:  \t{details['SCHOOL']}  \nHeight:  \t{details['HEIGHT'][:1]}' {details['HEIGHT'][2:]}\'\'  \nWeight:  \t{details['WEIGHT']} lb  \nPosition: {details['POSITION']}  \nJersey Number: {details['JERSEY']}  \nStatus:  \t{details['ROSTERSTATUS']}  \nTeam:  \t{details['TEAM_CITY']} {details['TEAM_NAME']}  \nPlaying Between:  \t{details['FROM_YEAR']} - {details['TO_YEAR']}"
            st.caption(output)

        player_details(player_id)
    else:
        st.info("Select a player in the search bar in the left sidebar.")


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



# Display the data that the user wants. If you want to give more options,
# add the option in the parameters variable and also add the conversion in the
# match() method, so that you can convert from the syntax used in the dataframe
# provided by the api.

def dataframe(player_id, df):

    parameters = st.multiselect(
        "Select the data you want to see.",
        options=[
            "Points",
            "Games Played",
            "Minutes Played",
            "Field Goals Made (FGM)",
            "Field Goals Attempted (FGA)",
            "Field Goals Percentage (FGP in %)"
        ]
    )   
    
    button = st.button("Display Stats")
    if button:
        dataFrame = get_custom_dataframe(parameters=parameters, df=df)
        st.dataframe(dataFrame)
        
def dataframe2(parameters, df):
    temp_list = []
    options = [
        "Points",
        "Games Played",
        "Minutes Played",
        "Field Goals Made (FGM)",
        "Field Goals Attempted (FGA)",
        "Field Goals Percentage (FGP in %)"
    ]

    for i, element in enumerate(parameters):
        if element:
            temp_list.append(options[i])
    dataFrame = get_custom_dataframe(parameters=temp_list, df=df)
    st.dataframe(dataFrame)

# Add the new name of the index in the data frame you want to display here

def match(val):

    match val:
        case 'Points':
            return 'PTS'
        case 'Games Played':
            return 'GP'
        case 'Minutes Played':
            return 'MIN'
        case 'Field Goals Made (FGM)':
            return 'FGM'
        case 'Field Goals Attempted (FGA)':
            return 'FGA'
        case 'Field Goals Percentage (FGP in %)':
            return 'FG_PCT'


############################################################

###################### MATCHUPS TODAY ######################

# This method generates the latitude and longtitude of the 
# stadium the game will be played in. Be careful, there is a
# 3000 calls per day limit!
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
    m = folium.Map(location=[latitude, longitude], zoom_start=10)

    # add marker for the station
    folium.Marker([latitude, longitude], popup="Station", tooltip="Station").add_to(m)

    # call to render Folium map in Streamlit
    folium_static(m)


@st.cache_data(show_spinner=False)
def get_scoreboard(gameday):
    score = scoreboardv2.ScoreboardV2(game_date=gameday)
    
    with open("scoreboard.json", "w") as file:
        file.write(score.get_json())

    with open("scoreboard.json", "r") as file:
        score_json = json.load(file)

    return score_json

@st.cache_data(show_spinner=False)
def get_team_details(team_id):
    team_details = teamdetails.TeamDetails(team_id=team_id)

    with open("temp.json", "w") as file:
       file.write(team_details.get_json())

    with open("temp.json", "r") as file:
       details_json = json.load(file)

    return details_json

# Get the league teams and store them in a json file
@st.cache_data(show_spinner=False)
def get_league_teams():

    league_standings = leaguestandings.LeagueStandings()

    with open("league.json", "w") as file:
        file.write(league_standings.get_json())


# Get team nave given the team id
@st.cache_data(show_spinner=False)
def get_team_name(team_id):

    with open("league.json", "r") as file:
        team_json = json.load(file)

    teams = team_json['resultSets'][0]['rowSet']

    for entry in teams:
        if team_id == entry[2]:
            team_name = entry[3] + " " + entry[4]

    return team_name


def display_match_details(team_id, day):

    score_board = get_scoreboard(day)
    teams = score_board['resultSets'][0]['rowSet']
    # st.caption(teams)
    
    for entry in teams:
        if entry[6] == team_id:
            team_1_details = get_team_details(team_id=entry[6])
            team_2_details = get_team_details(team_id=entry[7])

            team_1_full_name = get_team_name(team_id=entry[6]) + " (" + team_1_details['resultSets'][0]['rowSet'][0][1] + ")"
            team_2_full_name = get_team_name(team_id=entry[7]) + " (" + team_2_details['resultSets'][0]['rowSet'][0][1] + ")"

            st.subheader(team_1_full_name + " vs. " + team_2_full_name)
            st.text(f"Start Time: {entry[4]}")
            st.text(f"Stadium Name: {entry[15]}")
            map_creator(entry[15])

    _, col2 = st.columns([7,1])

    with col2:
        button = st.button("Go Back")
        if button:
            todays_matchups()


def display_matchups(matchups, day):
    
    global match_team_ids
    global index
    global button_list
    global days
    get_league_teams()

    st.subheader(f"Game Day: {day}")
        
    for entry in matchups:
        col1, col2 = st.columns([3,1])

        with col1:
            
            team_1_name = get_team_name(team_id=entry[6])
            team_2_name = get_team_name(team_id=entry[7])

            st.text(f"{team_1_name} vs. {team_2_name}")
            
        # with col2:
        #     temp_button = st.button("Check More Details", key=index)
        #     button_list.append(temp_button)
        #     index += 1

        # st.markdown("""---""")
        # match_team_ids.append(entry[6])
        # days.append(day)

# Given a data frame and an index, return the 
# index of that dataframe as an array.
def todays_matchups():

    placeholder = st.empty()

    with placeholder:
        tab1, tab2, tab3 = st.tabs(['Yesterday', 'Today', 'Tomorrow'])
        
        with tab1:
            yesterday = date.today() - timedelta(days=1)
            board_json = get_scoreboard(yesterday)
            
            day = yesterday

            matchups = board_json['resultSets'][0]['rowSet']
            if len(matchups) == 0:
                st.warning(f"There were no matchups for Game Day {yesterday}!")
            else:
                display_matchups(matchups=matchups, day=yesterday)

        with tab2:
            today = date.today()
            board_json = get_scoreboard(today)

            day = today

            matchups = board_json['resultSets'][0]['rowSet']
            if len(matchups) == 0:
                st.warning(f"There were no matchups for Game Day {today}!")
            else:
                display_matchups(matchups=matchups, day=today)
    
        with tab3:
            tomorrow = date.today() + timedelta(days=1)
            board_json = get_scoreboard(tomorrow)
        
            day = tomorrow

            matchups = board_json['resultSets'][0]['rowSet']
            if len(matchups) == 0:
                st.warning(f"There were no matchups for Game Day {tomorrow}!")
            else:
                display_matchups(matchups=matchups, day=tomorrow)

    if button_list:
        for i in range(len(button_list)):
            if button_list[i]:
                # st.info(get_team_name(match_team_ids[i]))
                placeholder.empty()
                display_match_details(match_team_ids[i], days[i])