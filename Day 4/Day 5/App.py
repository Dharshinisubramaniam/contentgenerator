import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.schema.runnable import Runnable

# ---------------------------
# Step 1: Set Gemini API Key
# ---------------------------
# Replace with your actual Gemini API key
GOOGLE_API_KEY = "AIzaSyCaAF8nMeqTfcbcNPPMG6RDiUht5N8sJZs"
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# ---------------------------
# Step 2: Initialize Gemini LLM
# ---------------------------
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3)

# ---------------------------
# Step 3: Create Prompt Template
# ---------------------------
prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        "You are a helpful assistant that translates English to French."
    ),
    HumanMessagePromptTemplate.from_template(
        "Translate this sentence to French:\n{sentence}"
    )
])

# ---------------------------
# Step 4: Create Runnable Chain
# ---------------------------
chain: Runnable = prompt | llm

# ---------------------------
# Step 5: Build Streamlit UI
# ---------------------------
st.set_page_config(page_title="English to French Translator", page_icon="🌍")
st.title("🌍 English to French Translator")
st.markdown("Enter an English sentence below and click **Translate** to see the French translation.")

# Input field
sentence = st.text_input("Your English sentence:")

# Translate button
if st.button("Translate"):
    if not sentence.strip():
        st.warning("Please enter a sentence to translate.")
    else:
        try:
            # Run the chain
            response = chain.invoke({"sentence": sentence})
            french = response.content

            # Display result
            st.success("✅ Translation successful!")
            st.markdown(f"**French Translation:**\n\n> {french}")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
