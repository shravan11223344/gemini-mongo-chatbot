import streamlit as st

from services.get_model_list import get_ollama_model_list
from services.get_title import get_chat_title
from services.chat_utilities import get_answer
from db.conversations import (
    create_new_conversation,
    add_message,
    get_conversation,
    get_all_conversations,
)

# ---- Page Config ----
st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 Gemini Chatbot")

# ---- Models ----
if "MODEL_LIST" not in st.session_state:
    st.session_state.MODEL_LIST = get_ollama_model_list()

selected_model = st.selectbox("Select Model", st.session_state.MODEL_LIST)

# ---- Session State ----
st.session_state.setdefault("conversation_id", None)
st.session_state.setdefault("conversation_title", None)
st.session_state.setdefault("chat_history", [])

# ---- Sidebar Chat History ----
with st.sidebar:
    st.header("💬 Chat History")

    conversations = get_all_conversations()

    if st.button("➕ New Chat"):
        st.session_state.conversation_id = None
        st.session_state.conversation_title = None
        st.session_state.chat_history = []

    for cid, title in conversations.items():

        is_current = cid == st.session_state.conversation_id
        label = f"**{title}**" if is_current else title

        if st.button(label, key=f"conv_{cid}"):

            doc = get_conversation(cid) or {}

            st.session_state.conversation_id = cid
            st.session_state.conversation_title = doc.get("title", "Untitled")

            st.session_state.chat_history = [
                {"role": m["role"], "content": m["content"]}
                for m in doc.get("messages", [])
            ]

# ---- Display Chat ----
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---- Chat Input ----
user_query = st.chat_input("Ask AI...")

if user_query:

    # Show user message
    st.chat_message("user").markdown(user_query)

    # Save to session
    st.session_state.chat_history.append(
        {"role": "user", "content": user_query}
    )

    # ---- Create new conversation if needed ----
    if st.session_state.conversation_id is None:

        try:
            title = get_chat_title(selected_model, user_query)
        except Exception:
            title = "New Chat"

        conv_id = create_new_conversation(
            title=title,
            role="user",
            content=user_query,
        )

        st.session_state.conversation_id = conv_id
        st.session_state.conversation_title = title

    else:
        add_message(
            st.session_state.conversation_id,
            "user",
            user_query,
        )

    # ---- Get AI Response ----
    try:
        assistant_text = get_answer(
            selected_model,
            st.session_state.chat_history
        )
    except Exception as e:
        assistant_text = f"[Error getting response: {e}]"

    # ---- Show AI Response ----
    with st.chat_message("assistant"):
        st.markdown(assistant_text)

    # ---- Save AI Response ----
    st.session_state.chat_history.append(
        {"role": "assistant", "content": assistant_text}
    )

    if st.session_state.conversation_id:
        add_message(
            st.session_state.conversation_id,
            "assistant",
            assistant_text,
        )