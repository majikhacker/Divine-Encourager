import openai
import streamlit as st

st.title("🎚️🙏🏽 Divine Encourager 🙏🏽🎚️")

openai.api_key=st.secrets["OPENAI_API_KEY"]

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4-0125-preview"

if "messages" not in st.session_state:
    st.session_state.messages = []

chatbot_tone = {'role': 'system', 'content': 'You are a chatbot that encourages users with Bible verses and words of encouragement depending on what they input, if they ask anything other than for words of encouragement or bible verses politely decline them and redirect them towards our app and our functionalities.'}
st.session_state.messages.append(chatbot_tone)

for message in st.session_state.messages:
    if message["role"] in ["user", "assistant"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Input anything you would like encouragement with, like strength, courage, protection, etc."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = openai.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
