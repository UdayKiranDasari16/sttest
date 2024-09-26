import streamlit as st # type: ignore

from random import randint

import utils.SupabaseClient as sc
from utils.OpenAI import ask_gpt, basic_ask_gpt

sc.create_connection()
data = sc.fetch_all()
# TODO: Create types for data
total_questions = len(data)
print("Total number of questions: " + str(total_questions))


def clear_session_storage():
    st.session_state["Row"] = None
    st.session_state["Response"] = None
    st.session_state["Reprompt"] = False
    st.session_state["Re_Response"] = None


# List of all variables used in session state

def pick_random_question():
    clear_session_storage()
    ran_int = randint(0, total_questions - 1)
    picked_row = data[ran_int]
    print(picked_row["task_id"])
    return picked_row


if "Row" not in st.session_state:
    st.session_state["Row"] = None
if "Response" not in st.session_state:
    st.session_state["Response"] = None
if "Reprompt" not in st.session_state:
    st.session_state["Reprompt"] = False
if "Re_Response" not in st.session_state:
    st.session_state["Re_Response"] = None


# Title and random number picker
st.title("OpenAI Prompting")
if st.button("Pick a random question 🎲"):
    row = pick_random_question()
    st.session_state["Row"] = row

# Question Info
if st.session_state["Row"]:
    row = st.session_state["Row"]
    st.text_area(label="Question", value=row["Question"])
    st.text_input(label="Expected Answer", value=row["Final answer"])

# Prompt LLM First time and ask gpt
if st.session_state["Response"] is None and st.session_state["Row"] is not None:
    if st.button("Prompt LLM", type="primary"):
        row = st.session_state["Row"]
        with st.spinner("Generating Response..."):
            st.session_state["Response"] = basic_ask_gpt(row["Question"])

# Annotate text box and further controls
if st.session_state["Reprompt"] == True:
    row = st.session_state["Row"]
    st.text_area("Annotator Metadata",row["Annotator Metadata"])
    if st.button("Re-Prompt GPT"):
        with st.spinner("Generating Response..."):
            st.session_state["Re_Response"] = basic_ask_gpt(row["Question"] + "\n" + row["Annotator Metadata"])

# This is being triggered cz of the rerun logic in ask_gpt
if st.session_state["Response"] and st.session_state["Reprompt"] is False:
    row = st.session_state["Row"]
    st.success(st.session_state["Response"])
    # TODO: Use columns to view it side by side
    if st.button("Answer is As Is", type="primary"):
        st.session_state["Reprompt"] = True
        st.success("Great")
    if st.button("Annotate & Re-Prompt"):
        st.session_state["Reprompt"] = True
        st.rerun()

if "Re_Response" in st.session_state and st.session_state["Re_Response"]:
    st.success(st.session_state["Re_Response"])
    if st.button("Mark as failed to answer"):
        st.success("Marked as Failed")
    if st.button("Mark as succeeded on annotating"):
        st.success("Marked as success on annotating")
