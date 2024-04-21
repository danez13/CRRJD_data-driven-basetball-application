# NBA Stats
import nba_api.library
import nba_api.stats
import nba_api.stats.static
import nba_api.stats.static.teams as teams
from streamlit_option_menu import option_menu
from helpers import display_detailedPlayer,get_all_players
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

# NAVIGATION MENU
menu = option_menu(
    menu_title=None,
    options=["Player","Matches","Teams", "Else"],
    icons=["person-bounding-box", "calendar-event", "list"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal"
)
def add(search:list):
    search.append(0)
    return search

# Start running the program from here
if menu == "Player":
    playerContainer = st.container(border=True)
    with playerContainer:
        textSearch=[]
        textSearch = playerContainer.multiselect("get detailed player info:",get_all_players())
        filter = playerContainer.radio("filters",options=["active","all-time"],horizontal=True)
        roster = playerContainer.container(border=True)
        with roster:
            if len(textSearch)!=0:
                roster.empty()
                display_detailedPlayer(textSearch,roster)
            else:
                if filter == "active":
                    roster.empty()
                    df=pd.read_json("activeRoster_file.json")
                    st.write("active league roster")
                    roster.dataframe(df,column_config={"Picture":st.column_config.ImageColumn(),"TeamPic":st.column_config.ImageColumn()},hide_index=True,use_container_width=True)
                else:
                    roster.empty()
                    df=pd.read_json("allRoster_file.json")
                    st.write("all time league roster")
                    roster.dataframe(df,column_config={"Picture":st.column_config.ImageColumn(),"TeamPic":st.column_config.ImageColumn()},hide_index=True,use_container_width=True)
        
elif menu == "Matches":
    redi_helpers.todays_matchups()

elif menu=="Teams":
    for item in teams.teams:
        st.write(f"{item}")
        

elif menu == "Else":
    print("hello")