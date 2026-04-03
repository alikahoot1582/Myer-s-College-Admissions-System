import streamlit as st
import sqlite3
import os
import pandas as pd
from groq import Groq
from datetime import date, datetime

# --- 1. CONFIGURATION ---
LIVE_API_KEY = "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" # Best practice: use st.secrets["GROQ_API_KEY"]
client = Groq(api_key=LIVE_API_KEY)

DB_FILE = 'myers_college_admissions.db'
SCHOOL_NAME = "Myer's College Chakwal"

# --- 2. DATABASE HELPER FUNCTIONS ---
def run_query(query, params=()):
    with sqlite3.connect(DB_FILE) as conn:
        return pd.read_sql_query(query, conn, params=params)

def get_db_schema():
    return """
    Table: registrations
    Columns: id, submission_date, student_name, applied_class, dob, 
             hospital_born, father_name, father_cnic, mother_name, 
             medical_history, emergency_instructions, undertaking_accepted
    """

# --- 3. AI ASSISTANT LOGIC ---
def ask_ai(user_prompt):
    # This system prompt tells the AI how to behave and what data it has access to
    schema = get_db_schema()
    context_data = run_query("SELECT * FROM registrations").to_string()
    
    system_message = f"""
    You are the {SCHOOL_NAME} Admission Assistant. 
    You have access to the current registration database.
    
    DATABASE SCHEMA:
    {schema}
    
    CURRENT DATA:
    {context_data}
    
    INSTRUCTIONS:
    1. Answer questions based ONLY on the data provided above.
    2. If asked to summarize, be concise.
    3. If no data exists for a query, politely inform the user.
    4. Do not reveal sensitive ID card numbers (CNIC) unless explicitly asked.
    """
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2 # Lower temperature for factual accuracy
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"I'm having trouble accessing my brain right now: {str(e)}"

# --- 4. UI SETUP ---
st.set_page_config(page_title=f"{SCHOOL_NAME} Portal", layout="wide", page_icon="🎓")

tab1, tab2, tab3 = st.tabs(["📝 Admission Form", "🤖 AI Assistant", "📊 Admin View"])

# --- TAB 1: REGISTRATION FORM (Existing Logic) ---
with tab1:
    st.header("Student Registration")
    # ... (Keep your existing form code here) ...

# --- TAB 2: AI ASSISTANT (New Feature) ---
with tab2:
    st.header("💬 Admission AI Chat")
    st.info("Ask me about current applications, student counts, or medical summaries.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ex: 'Summarize all applicants for class K-1'"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = ask_ai(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# --- TAB 3: ADMIN VIEW ---
with tab3:
    st.header("Database Overview")
    df = run_query("SELECT * FROM registrations")
    st.dataframe(df, use_container_width=True)
    
    if st.button("Refresh Data"):
        st.rerun()
