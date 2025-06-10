import streamlit as st
import google.generativeai as genai  # Import the genai module
import os

# Configure the Gemini API key
genai.configure(api_key='AIzaSyCaAF8nMeqTfcbcNPPMG6RDiUht5N8sJZs')  # Set it using configure

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-2.0-flash')  # Ensure this model name is valid

st.title("✨ Social Media Content Generator with Gemini")

# --- Input Section ---
platform = st.selectbox("Select Platform:", ["Instagram", "Twitter", "LinkedIn"])
mood = st.selectbox("Select Mood:", ["Funny", "Formal"])
topic = st.text_input("Enter Topic:")
add_emoji = st.checkbox("Add Emojis", value=True)
styling = st.checkbox("Add Styling (hashtags, punctuation flair)", value=True)

# Function to create the prompt
def create_prompt():
    prompt = f"""
    Generate a {mood.lower()} caption for {platform}.
    Topic: {topic if topic else "general"}.
    Include emojis: {'yes' if add_emoji else 'no'}.
    Add styling like hashtags and punctuation flair: {'yes' if styling else 'no'}.
    """
    return prompt.strip()

# --- Generate Caption ---
if st.button("Generate Caption"):
    prompt = create_prompt()
    st.info("Generating your caption... Please wait.")
    
    response = model.generate_content(prompt)
    caption = response.text.strip() if hasattr(response, "text") and response.text else "⚠️ No caption generated."
    
    st.subheader("Generated Caption:")
    st.write(caption)
    
    if st.button("Regenerate Caption"):
        st.info("Generating a new version...")
        response = model.generate_content(prompt)
        new_caption = response.text.strip() if hasattr(response, "text") and response.text else "⚠️ No caption generated."
        st.write(new_caption)
    
    st.download_button("Download Caption", caption, file_name="caption.txt")

# Sidebar: instructions
st.sidebar.title("ℹ️ How to Use")
st.sidebar.markdown("""
✅ **Choose your platform, mood, and topic**.  
✅ **Select emoji/styling options** to customize the style.  
✅ **Click "Generate Caption"** and wait a few seconds!  
✅ Use **"Regenerate Caption"** for variations.  
✅ **Download** your caption for easy use.  
""")
