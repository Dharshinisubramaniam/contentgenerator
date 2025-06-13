import streamlit as st
import requests
from datetime import datetime

# ----------------- CONFIGURATION -------------------
N8N_WEBHOOK_URL = "https://dharshini2212.app.n8n.cloud/webhook-test/80467156-bf4c-40d1-9194-d2eafcd8cd60"  # 🔁 Replace with your real URL

# Example hardcoded user credentials
USER_CREDENTIALS = {
    "dharshini": "dharshini@123",
    "sowmiya": "sowmi@456",
    "stephy": "stephy@satler"
}

# ----------------- SESSION INITIALIZATION -------------------
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False
    st.session_state.username = ""

# ----------------- FUNCTIONS -------------------

def validate_login(username, password):
    """Validate credentials from dictionary"""
    return USER_CREDENTIALS.get(username) == password

def show_login():
    st.title("🔐 Employee Login")
    st.markdown("Please enter your credentials to access the portal.")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if validate_login(username, password):
            st.session_state.is_logged_in = True
            st.session_state.username = username
            st.success("Login successful!")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password.")

def logout():
    st.session_state.is_logged_in = False
    st.session_state.username = ""
    st.experimental_rerun()

def submit_action_item(data):
    try:
        response = requests.post(N8N_WEBHOOK_URL, json=data)
        if response.status_code == 200:
            st.success("✅ Action item submitted successfully!")
        else:
            st.error(f"❌ Submission failed. Status Code: {response.status_code}")
    except Exception as e:
        st.error(f"🚨 Error: {str(e)}")

def show_portal():
    st.title("📋 Meeting Action Item Submission")

    st.markdown(f"Welcome, **{st.session_state.username}**! Use the form below to submit your action items.")

    with st.form("action_form"):
        meeting_title = st.text_input("Meeting Title", placeholder="Weekly Sync-up")
        meeting_date = st.date_input("Meeting Date", value=datetime.today())
        attendees = st.text_area("Attendees", placeholder="Alice, Bob, Carol")
        email = st.text_input("Email", placeholder="you@example.com")  # ✅ Added email field here
        action_items = st.text_area("Action Items", placeholder="List all decisions, responsibilities, or tasks...")
        submit = st.form_submit_button("Submit")

    if submit:
        form_data = {
            "username": st.session_state.username,
            "meeting_title": meeting_title,
            "meeting_date": meeting_date.strftime("%Y-%m-%d"),
            "attendees": attendees,
            "email": email,  # ✅ Include email in payload
            "action_items": action_items,
            "submitted_at": datetime.now().isoformat()
        }
        submit_action_item(form_data)

    st.sidebar.markdown(f"👤 **User:** {st.session_state.username}")
    if st.sidebar.button("🚪 Logout"):
        logout()

# ----------------- APP ENTRY POINT -------------------
def main():
    st.set_page_config(page_title="Employee Portal", layout="centered")
    
    if st.session_state.is_logged_in:
        show_portal()
    else:
        show_login()

if __name__ == "__main__":
    main()
