# navigation_bar.py

import streamlit as st

def navigation_bar():
    st.sidebar.title("Navigation")

    # Add links to different sections of the website
    st.session_state.page = st.sidebar.radio("Go to", ["Home", "Courses", "Profile", "Login"])

if __name__ == "__main__":
    navigation_bar()
