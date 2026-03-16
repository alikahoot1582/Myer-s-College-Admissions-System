import streamlit as st
import sqlite3
import os
from groq import Groq
from datetime import date, datetime

# --- 1. LIVE API CONFIGURATION ---
# PASTE YOUR LIVE GROQ API KEY HERE
LIVE_API_KEY = "PASTE_YOUR_GROQ_API_KEY_HERE"

client = Groq(api_key=LIVE_API_KEY)

DB_FILE = 'myers_college_admissions.db'
SCHOOL_NAME = "Myer's College Chakwal"

# --- 2. DATABASE INITIALIZATION ---
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # Schema built specifically from PDF sources [cite: 1, 36, 67, 72, 86]
    c.execute('''
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            submission_date TEXT,
            student_name TEXT,
            applied_class TEXT,
            dob TEXT,
            father_name TEXT,
            father_cnic TEXT,
            mother_name TEXT,
            medical_history TEXT,
            emergency_instructions TEXT,
            undertaking_accepted INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def save_to_db(data):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    query = '''
        INSERT INTO registrations 
        (submission_date, student_name, applied_class, dob, father_name, father_cnic, mother_name, medical_history, emergency_instructions, undertaking_accepted)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    c.execute(query, data)
    conn.commit()
    conn.close()

init_db()

# --- 3. UI SETUP ---
st.set_page_config(page_title=f"{SCHOOL_NAME} Admission", layout="wide", page_icon="🎓")

st.title(f"{SCHOOL_NAME} Admission Portal")
st.info("Note: Registration fee Rs. 300/- is non-refundable whether child joins or not[cite: 42, 68].")

# --- 4. INTEGRATED FORM (Data from PDF) ---
with st.form("myers_registration"):
    # Section: The Student [cite: 72]
    st.header("Student Information")
    col1, col2 = st.columns(2)
    with col1:
        s_name = st.text_input("Student's Name (Block Letters) [cite: 68, 73]")
        dob = st.date_input("Date of Birth [cite: 75]", value=date(2018, 1, 1))
        hospital = st.text_input("Hospital where born [cite: 76]")
    with col2:
        # Age-to-Class mapping extracted from PDF 
        class_list = [
            "K-1 (Age 5+)", "K-2 (Age 6+)", "K-3 (Age 7+)", "K-4 (Age 8+)",
            "E-1 (Age 9+)", "E-2 (Age 10+)", "E-3 (Age 11+)",
            "M-1/C-1 (Age 12+)", "M-2/C-2 (Age 13+)", "M-3/C-3 (Age 14+)"
        ]
        applied_class = st.selectbox("Applying for Class [cite: 74]", class_list)
        religion = st.text_input("Religion [cite: 77]")

    # Section: The Parents [cite: 86]
    st.header("Parental Details")
    col3, col4 = st.columns(2)
    with col3:
        f_name = st.text_input("Father's Name [cite: 82]")
        f_cnic = st.text_input("Father's Identity Card No [cite: 83]")
    with col4:
        m_name = st.text_input("Mother's Name [cite: 84]")
        address = st.text_input("Present Address [cite: 91]")

    # Section: Compulsory Medical Questionnaire [cite: 1]
    st.header("Medical Questionnaire")
    st.write("This helps us look after your child; we do not reject based on this document[cite: 2, 3].")
    
    col5, col6 = st.columns(2)
    with col5:
        physician = st.text_input("Family Physician's Name [cite: 4]")
        emergency_instr = st.text_area("Emergency Instructions [cite: 6]")
    with col6:
        st.write("Past Diseases[cite: 21]:")
        m_measles = st.checkbox("Measles [cite: 22]")
        m_mumps = st.checkbox("Mumps [cite: 26]")
        m_rubella = st.checkbox("Rubella [cite: 29]")
        m_pox = st.checkbox("Chicken Pox [cite: 34]")

    # Section: Undertaking [cite: 38]
    st.header("Undertaking")
    st.write("I understand the academic/financial year is August to July and fees are payable till July[cite: 40, 125].")
    agree = st.checkbox("I agree to conform to the rules and regulations of Myer's College[cite: 39].")

    if st.form_submit_button("Submit Application"):
        if agree and s_name and f_name:
            med_summary = f"Measles: {m_measles}, Mumps: {m_mumps}, Rubella: {m_rubella}, Pox: {m_pox}"
            submission_data = (
                datetime.now().strftime("%Y-%m-%d %H:%M"),
                s_name, applied_class, str(dob), f_name, f_cnic, m_name, med_summary, emergency_instr, 1
            )
            save_to_db(submission_data)
            st.success("✅ Application successfully submitted to the database!")
        else:
            st.error("Please complete required fields and accept the undertaking.")

st.markdown("---")
st.markdown("<center>Myer's College Chakwal Admission Portal</center>", unsafe_allow_html=True)
