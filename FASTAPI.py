import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Auth Chat App", page_icon="🤖")

if "token" not in st.session_state:
    st.session_state["token"] = None
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Sidebar navigation (only main pages)
menu = st.sidebar.radio("Navigation", ["Home", "Auth", "Chat", "Logout"])

# Home
if menu == "Home":
    st.title("Welcome to Auth Chat App 🤖")
    st.write("Go to Auth tab to Login / Signup / Reset password.")

# Auth Page
elif menu == "Auth":
    st.title("Authentication 🔑")
    tab1, tab2, tab3 = st.tabs(["Login", "Signup", "Forgot Password"])

    # --- Login Tab ---
    with tab1:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            res = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
            if res.status_code == 200:
                st.session_state["token"] = res.json()["access_token"]
                st.success("Login successful!")
            else:
                st.error(res.json()["detail"])

    # --- Signup Tab ---
    with tab2:
        username = st.text_input("New Username", key="signup_user")
        password = st.text_input("New Password", type="password", key="signup_pass")
        if st.button("Signup"):
            res = requests.post(f"{API_URL}/signup", json={"username": username, "password": password})
            if res.status_code == 200:
                st.success("Signup successful! Go to Login.")
            else:
                st.error(res.json()["detail"])

    # --- Forgot Password Tab ---
    with tab3:
        username = st.text_input("Username", key="fp_user")
        new_password = st.text_input("New Password", type="password", key="fp_pass")
        if st.button("Reset Password"):
            res = requests.post(f"{API_URL}/forgot_password", json={"username": username, "password": new_password})
            if res.status_code == 200:
                st.success("Password reset successful! Please login again.")
            else:
                st.error(res.json()["detail"])

# Chat Page
elif menu == "Chat":
    if st.session_state["token"]:
        st.title("Chat with Bot 🤖")
        user_input = st.text_input("You:", key="chat_input")
        if st.button("Send"):
            bot_reply = f"Echo: {user_input}"  # Dummy bot
            st.session_state["chat_history"].append(("You", user_input))
            st.session_state["chat_history"].append(("Bot", bot_reply))

        for role, msg in st.session_state["chat_history"]:
            st.write(f"**{role}:** {msg}")
    else:
        st.warning("Please login first.")

# Logout Page
elif menu == "Logout":
    st.session_state["token"] = None
    st.success("Logged out successfully!")
