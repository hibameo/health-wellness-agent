# main.py
import os
import asyncio
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.responses import ResponseTextDeltaEvent
from context import UserSessionContext
from hooks import LoggingRunHooks
from agent_utils import Runner, health_wellness_agent  # make sure it's correctly imported

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Health & Wellness Assistant", page_icon="💬")

st.title("💬 Health & Wellness Assistant")
st.caption("Ask me anything related to health, wellness, injuries, or nutrition.")

# Initialize session history
if "history" not in st.session_state:
    st.session_state.history = []

# Display previous chat
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

query = st.chat_input("What's your health/wellness question?")

if query:
    st.chat_message("user").markdown(query)
    st.session_state.history.append({"role": "user", "content": query})

    hooks = LoggingRunHooks()

    # ✅ Create agent instance correctly
    agent_instance = health_wellness_agent(
        history=st.session_state.history,
        query=query
    ).triage_agent

    # Container for assistant response
    with st.chat_message("assistant"):
        placeholder = st.empty()

        async def get_response():
            try:
                result = Runner.run_streamed(
                    agent_instance,
                    input=query,
                    context=UserSessionContext(name="TestUser", uid=12345),
                    hooks=hooks,
                )

                full_response = ""
                async for event in result.stream_events():
                    if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                        full_response += event.data.delta
                        placeholder.markdown(full_response)

                # Try extracting JSON response
                try:
                    from json import loads
                    data = loads(full_response)
                    final_message = data.get("response", "")
                except:
                    final_message = full_response.strip()

                st.session_state.history.append({"role": "assistant", "content": final_message})

            except Exception as e:
                placeholder.error(f"❌ Error: {str(e)}")

        asyncio.run(get_response())
