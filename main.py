# NBA Stats
# from favicon import Icon
import nba_api.library
import nba_api.stats
import nba_api.stats.endpoints
import nba_api.stats.static
import nba_api.stats.static.teams as teams
from streamlit_option_menu import option_menu
from helpers import display_detailedPlayer,get_all_players,get_scoreboard,display_matchups,TeamRoster
import redi_helpers
import streamlit as st
import nba_api
from nba_api.stats.static import players
from nba_api.stats.static import teams
from datetime import date, timedelta
from streamlit_folium import folium_static
import folium
import pandas as pd
import json
from PIL import Image

image = Image.open("nba.jpg")
st.set_page_config(
    page_title="NBA Stats And Games", 
    page_icon=image,
    initial_sidebar_state="collapsed"
)

# NAVIGATION MENU
menu = option_menu(
    menu_title=None,
    options=["Player", "Matches", "Teams", "Else"],
    icons=["person-bounding-box", "calendar-event", "list"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal"
)

# Start running the program from here
if menu == "Player":
    playerContainer = st.container(border=True)
    with playerContainer:
        textSearch=[]
        textSearch = playerContainer.multiselect("get detailed player info:",get_all_players())
        filter = playerContainer.radio("filters",options=["active","all-time"],horizontal=True)
        roster = playerContainer.container()
        with roster:
            if len(textSearch)!=0:
                roster.empty()
                display_detailedPlayer(textSearch,roster)
            else:
                if filter == "active":
                    roster.empty()
                    df=pd.read_json("activeRoster_file.json")
                    roster.write("active league roster")
                    roster.dataframe(df,column_config={"Picture":st.column_config.ImageColumn(),"TeamPic":st.column_config.ImageColumn()},hide_index=True,use_container_width=True)
                else:
                    roster.empty()
                    df=pd.read_json("allRoster_file.json")
                    roster.write("all time league roster")
                    roster.dataframe(df,column_config={"Picture":st.column_config.ImageColumn(),"TeamPic":st.column_config.ImageColumn()},hide_index=True,use_container_width=True)
        
elif menu == "Matches":
    placeholder = st.empty()
    with placeholder:
        tab1, tab2, tab3 = placeholder.tabs(['Yesterday', 'Today', 'Tomorrow'])
        with tab1:
            yesterday = date.today() - timedelta(days=1)
            board_json = get_scoreboard(yesterday)
            day = yesterday

            matchups = board_json['resultSets'][0]['rowSet']
            if len(matchups) == 0:
                tab1.warning(f"There were no matchups for Game Day {yesterday}!")
            else:
                display_matchups(matchups=matchups, day=yesterday, _container=tab1)
        with tab2:
            today = date.today()
            board_json = get_scoreboard(today)

            day = today

            matchups = board_json['resultSets'][0]['rowSet']
            if len(matchups) == 0:
                st.warning(f"There were no matchups for Game Day {today}!")
            else:
                display_matchups(matchups=matchups, day=today, _container=tab2)
        with tab3:
            tomorrow = date.today() + timedelta(days=1)
            board_json = get_scoreboard(tomorrow)
        
            day = tomorrow

            matchups = board_json['resultSets'][0]['rowSet']
            if len(matchups) == 0:
                st.warning(f"There were no matchups for Game Day {tomorrow}!")
            else:
                display_matchups(matchups=matchups, day=tomorrow,_container=tab3)

elif menu=="Teams":
    placeholder = st.container()
    with placeholder:
        for team in teams.teams:
            col1,col2=placeholder.columns(2)
            with col1:
                col1.image(f"https://cdn.nba.com/logos/nba/{team[0]}/primary/L/logo.svg",width=100)
            with col2:
                col2.write(team[5])
                view_details = col2.button("View Details",team[0])
                if view_details:
                    with open("team_id.txt", "w") as file:
                        file.write(str(team[0]))
                    st.switch_page("pages/team_details.py")
                # st.write(len(TeamRoster(team[0])))
            placeholder.divider()
        

elif menu == "Else":
    st.info("New features will be comming soon!")