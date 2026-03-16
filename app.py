import streamlit as st
import sqlite3
import os
from groq import Groq
from datetime import date, datetime

# --- 1. LIVE API CONFIGURATION ---
LIVE_API_KEY = "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"
client = Groq(api_key=LIVE_API_KEY)

DB_FILE = 'myers_college_admissions.db'
SCHOOL_NAME = "Myer's College Chakwal"
LOGO_PATH = "logo.png"
HANDBOOK_PATH = "stdhbk (1).pdf"
NEWSLETTER_URL = "https://www.myers.edu.pk/newsletterdec25.pdf"

# --- 2. DATABASE INITIALIZATION ---
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # Added 'hospital_born' to the schema (making it 11 columns total)
    c.execute('''
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            submission_date TEXT,
            student_name TEXT,
            applied_class TEXT,
            dob TEXT,
            hospital_born TEXT,
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
    # Updated to match the 11 data points provided in the form
    query = '''
        INSERT INTO registrations 
        (submission_date, student_name, applied_class, dob, hospital_born, 
         father_name, father_cnic, mother_name, medical_history, 
         emergency_instructions, undertaking_accepted)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    c.execute(query, data)
    conn.commit()
    conn.close()

init_db()

# --- 3. UI SETUP ---
st.set_page_config(page_title=f"{SCHOOL_NAME} Admission", layout="wide", page_icon="🎓")

# Sidebar with Logo and Resources
with st.sidebar:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=250) # Fixed deprecated use_container_width
    
    st.title("Resources")
    
    if os.path.exists(HANDBOOK_PATH):
        with open(HANDBOOK_PATH, "rb") as f:
            st.download_button(
                label="📘 Download Student Handbook",
                data=f,
                file_name="Myers_Student_Handbook.pdf",
                mime="application/pdf",
                width="stretch"
            )
    
    st.link_button("📰 View December Newsletter", NEWSLETTER_URL, width="stretch")
    st.divider()
    st.info("Registration fee Rs. 300/- is non-refundable.")

# Main Header
col_header_1, col_header_2 = st.columns([1, 4])
with col_header_1:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=120)
with col_header_2:
    st.title(f"{SCHOOL_NAME}")
    st.subheader("Student Admission & Registration Portal")

# --- 4. REGISTRATION FORM ---
with st.form("myers_registration"):
    st.header("1. Student Information")
    col1, col2 = st.columns(2)
    with col1:
        s_name = st.text_input("Student's Name (Block Letters)")
        dob = st.date_input("Date of Birth", value=date(2018, 1, 1))
        hospital = st.text_input("Hospital where born")
    with col2:
        class_list = [
            "K-1 (Age 5+)", "K-2 (Age 6+)", "K-3 (Age 7+)", "K-4 (Age 8+)",
            "E-1 (Age 9+)", "E-2 (Age 10+)", "E-3 (Age 11+)",
            "M-1/C-1 (Age 12+)", "M-2/C-2 (Age 13+)", "M-3/C-3 (Age 14+)"
        ]
        applied_class = st.selectbox("Applying for Class", class_list)
        religion = st.text_input("Religion")

    st.header("2. Parental Details")
    col3, col4 = st.columns(2)
    with col3:
        f_name = st.text_input("Father's Name")
        f_cnic = st.text_input("Father's Identity Card No")
    with col4:
        m_name = st.text_input("Mother's Name")
        address = st.text_input("Present Address")

    st.header("3. Medical Questionnaire")
    st.write("This helps us look after your child; we do not reject based on this document.")
    
    col5, col6 = st.columns(2)
    with col5:
        physician = st.text_input("Family Physician's Name")
        emergency_instr = st.text_area("Emergency Instructions")
    with col6:
        st.write("Past Diseases:")
        m_measles = st.checkbox("Measles")
        m_mumps = st.checkbox("Mumps")
        m_rubella = st.checkbox("Rubella")
        m_pox = st.checkbox("Chicken Pox")

    st.header("4. Undertaking")
    st.write("I understand the academic/financial year is August to July and fees are payable till July.")
    agree = st.checkbox("I agree to conform to the rules and regulations of Myer's College.")

    if st.form_submit_button("Submit Application"):
        if agree and s_name and f_name:
            med_summary = f"Measles: {m_measles}, Mumps: {m_mumps}, Rubella: {m_rubella}, Pox: {m_pox}"
            # This list now contains exactly 11 items to match the 11 columns above
            submission_data = (
                datetime.now().strftime("%Y-%m-%d %H:%M"),
                s_name, applied_class, str(dob), hospital, f_name, f_cnic, m_name, med_summary, emergency_instr, 1
            )
            save_to_db(submission_data)
            st.success("✅ Application successfully submitted to the database!")
            st.balloons()
        else:
            st.error("Please complete required fields (Student Name, Father's Name) and accept the undertaking.")

st.markdown("---")
st.markdown("<center>© Myer's College Chakwal | Admission Portal</center>", unsafe_allow_html=True)
