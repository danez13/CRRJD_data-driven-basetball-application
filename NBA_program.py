# NBA Stats
import nba_api.library
import nba_api.stats
import nba_api.stats.static
import nba_api.stats.static.teams as teams
from streamlit_option_menu import option_menu
from helpers import display_detailedPlayer, search_for_player,get_all_players
import redi_helpers
import streamlit as st
import nba_api
from nba_api.stats.static import players
from nba_api.stats.static import teams
from datetime import date, timedelta
from streamlit_folium import folium_static
import folium

# NAVIGATION MENU
menu = option_menu(
    menu_title=None,
    options=["Player","Matches","Teams", "Else"],
    icons=["person-bounding-box", "calendar-event", "list"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal"
)


# Start running the program from here
if menu == "Player":
    # textSearch = st.text_input("search for player",value=None)
    textSearch = st.multiselect("select a player:",get_all_players())
    filter = st.radio("filters",options=["active","all-time"],horizontal=True)
    if len(textSearch)!=0:
        display_detailedPlayer(textSearch)
    else:
        st.empty()
        search_for_player(filter)
elif menu == "Matches":
    redi_helpers.todays_matchups()

elif menu=="Teams":
    for item in teams.teams:
        st.write(f"{item}")
        

elif menu == "Else":
    print("hello")