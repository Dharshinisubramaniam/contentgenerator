import streamlit as st
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from duckduckgo_search import DDGS

# ------------------------------------------
# 🔐 Hardcoded Gemini API Key (not secure!)
# ------------------------------------------
GEMINI_API_KEY = "AIzaSyCaAF8nMeqTfcbcNPPMG6RDiUht5N8sJZs"  # Replace this with your real key

# ------------------------------------------
# 🔎 DuckDuckGo Search Tool
# ------------------------------------------
def duckduckgo_search(query: str) -> str:
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=3)
            return "\n".join([f"- {r['title']}: {r['body']}" for r in results])
    except Exception as e:
        return f"Search failed: {str(e)}"

search_tool = Tool(
    name="DuckDuckGoSearch",
    func=duckduckgo_search,
    description="Useful for answering real-world, recent, or factual questions."
)

# ------------------------------------------
# 🤖 Gemini LLM via LangChain
# ------------------------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.3
)

# ------------------------------------------
# 💬 Setup Conversational Memory
# ------------------------------------------
if "chat_memory" not in st.session_state:
    st.session_state.chat_memory = ConversationBufferMemory(memory_key="chat_history")

# ------------------------------------------
# 🧠 LangChain Agent Setup
# ------------------------------------------
agent = initialize_agent(
    tools=[search_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    memory=st.session_state.chat_memory,
    verbose=False,
    handle_parsing_errors=True
)

# ------------------------------------------
# 🎨 Streamlit UI
# ------------------------------------------
st.set_page_config(page_title="🌐 Real-Time Q&A with Gemini", page_icon="🧠")
st.title("🧠 Real-Time Q&A with Gemini + DuckDuckGo")
st.markdown("Ask questions about current events, news, or real-world facts.")

# Display chat history
if "chat_history_display" not in st.session_state:
    st.session_state.chat_history_display = []

for entry in st.session_state.chat_history_display:
    st.markdown(f"**You:** {entry['user']}")
    st.markdown(f"**Gemini:** {entry['bot']}")

# Input for new question
question = st.text_input("❓ Ask your question here:")

if st.button("🔍 Get Answer"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        try:
            with st.spinner("Thinking... 🤔"):
                answer = agent.run(question)

            # Save to chat history
            st.session_state.chat_history_display.append({
                "user": question,
                "bot": answer
            })

            st.markdown(f"**You:** {question}")
            st.markdown(f"**Gemini:** {answer}")

        except Exception as e:
            if "429" in str(e):
                st.error("❌ API quota exhausted. Please wait or check your billing settings.")
            else:
                st.error(f"❌ Unexpected error: {str(e)}")

