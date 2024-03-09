import time
from streamlit_option_menu import option_menu
import streamlit as st
import importlib.util
import About, Home, Contact

st.set_page_config(layout="wide")


def render_About_page():
    About.main()


def render_home_page():
    Home.main()


def render_contact_page():
    Contact.main()


# TO remove streamlit branding and other running animation
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# Spinners
bar = st.progress(0)
for i in range(101):
    bar.progress(i)
    time.sleep(0.07)  # Adjust the sleep time for the desired speed

st.balloons()

# Web content starts
# Navbar starts
col9, col10 = st.columns([1, 10])
col9.image('popcon.png')
col10.write('Movie mind')

selected = option_menu(
    menu_title="",
    options=["Home", "About", "Contact"],
    icons=['house', 'kanban', 'envelope'],
    menu_icon="",
    default_index=0,
    orientation="horizontal",
    styles="height: {300px;}, padding: {0px;}, margin: {0px;}, background-color: {white;}"
)

if selected == "About":
    render_About_page()
elif selected == "Contact":
    render_contact_page()
else:
    render_home_page()

# Navbar ends
