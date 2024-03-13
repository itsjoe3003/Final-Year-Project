import streamlit as st

def user_authentication():
    st.title("Login")
    
    # Define a dictionary of predefined usernames and passwords
    users = {
        "user1": "password1",
        "user2": "password2"
    }
    
    # Create input fields for username and password
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Create a login button
    if st.button("Login"):
        # Check if the entered username and password match any user in the dictionary
        if username in users and users[username] == password:
            st.success("Login successful!")
            # Set session state variable to indicate successful login
            st.session_state.logged_in = True
        else:
            st.error("Invalid username or password")

    # Optionally, you can provide a link to register for new users
    st.write("Don't have an account? [Register here](#)")

