import streamlit as st
import requests
from streamlit_option_menu import option_menu
import time

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Auth Chat App", page_icon="🤖")

if "token" not in st.session_state:
    st.session_state["token"] = None
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Sidebar menu
with st.sidebar:
    choice = option_menu(
        "Navigation",
        ["Home", "Signup", "Login", "Chat", "Logout"],
        icons=["house", "person-plus", "box-arrow-in-right", "chat-dots", "box-arrow-right"],
        menu_icon="list",
        default_index=0,
    )

# Home Page
if choice == "Home":
    st.title("Welcome to Auth Chat App 🤖")
    st.write("Login or Signup to continue.")

# Signup Page
elif choice == "Signup":
    st.subheader("Create New Account")
    username = st.text_input("Username", key="signup_user")
    password = st.text_input("Password", type="password", key="signup_pass")
    if st.button("Signup"):
        res = requests.post(f"{API_URL}/signup", json={"username": username, "password": password})
        if res.status_code == 200:
            st.success("Signup successful! Go to Login.")
        else:
            st.error(res.json()["detail"])

# Login Page
elif choice == "Login":
    st.subheader("Login to Your Account")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")
    if st.button("Login"):
        res = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
        if res.status_code == 200:
            st.session_state["token"] = res.json()["access_token"]
            st.success("Login successful!")
        else:
            st.error(res.json()["detail"])

# Chat Page
elif choice == "Chat":
    if st.session_state["token"]:
        st.subheader("Chat with Bot 🤖")
        user_input = st.text_input("You:", key="chat_input")
        if st.button("Send"):
            bot_reply = f"Echo: {user_input}"  # Dummy bot logic
            st.session_state["chat_history"].append(("You", user_input))
            st.session_state["chat_history"].append(("Bot", bot_reply))

        for role, msg in st.session_state["chat_history"]:
            st.write(f"**{role}:** {msg}")
    else:
        st.warning("Please login first.")

# Logout Page
elif choice == "Logout":
    st.session_state["token"] = None
    st.success("Logged out successfully!")
