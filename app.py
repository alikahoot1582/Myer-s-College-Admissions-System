import streamlit as st
import pandas as pd
import os
import requests
from datetime import date, datetime

# --- 1. PURE API & CHATBOT CONFIGURATION ---
# Your Groq API Key is used here for the AI Chatbot
API_KEY = st.secrets["GROQ_API_KEY"]
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def get_ai_response(user_query):
    """Fetches a response from Groq AI acting as a Myer's College assistant."""
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    
    # Context given to the AI so it knows about Myer's College
    system_prompt = f"""
    You are the Myer's College Chakwal Admissions Assistant. 
    School Info: 
    - Classes: Pre-school (P1-P3), Junior (K1-K4), Prep (E1-E3), Senior (C1-C4, AS/A2).
    - Policy: 1. Get Prospectus, 2. Register at office, 3. Interview/Test, 4. Pay fee if passed.
    - Contact: (0543) 541610. 
    - Hours: Summer (7am-1pm), Winter (8am-2pm).
    Be professional, helpful, and concise.
    """
    
    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ]
    }
    try:
        response = requests.post(GROQ_API_URL, json=payload, headers=headers)
        return response.json()['choices'][0]['message']['content']
    except:
        return "I'm sorry, I'm having trouble connecting to the school's server. Please call (0543) 541610."

def send_to_school_api(data):
    """Sends the admission data to the school's central database (Placeholder)."""
    return True 

# --- 2. LOCAL FILE CONFIGURATION ---
CSV_FILE = 'admissions_data.csv'
UPLOAD_DIR = "uploads"
LOGO_PATH = "logo.png"  
SCHOOL_NAME = "Myer's College Chakwal"

# Resource Links
HANDBOOK_URL = "https://myers.edu.pk/stdhbk.pdf" 
NEWSLETTER_URL = "https://myers.edu.pk/newsletterdec25.pdf"
WEBSITE_URL = "https://myers.edu.pk"
MAP_LINK = "https://www.google.com/maps/search/?api=1&query=Myer%27s+College+Chakwal"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

if not os.path.exists(CSV_FILE):
    columns = [
        "Submission Date", "Full Name", "Applied Class", "DOB", "Guardian Name", 
        "Email", "Financial History", "Join Reason", "ID Path", "Grades Path"
    ]
    pd.DataFrame(columns=columns).to_csv(CSV_FILE, index=False)

def save_to_csv(data):
    df = pd.read_csv(CSV_FILE)
    new_entry = pd.DataFrame([data])
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

# --- 3. PAGE SETUP ---
st.set_page_config(page_title=f"{SCHOOL_NAME} Admission", layout="wide", page_icon="🎓")

# --- 4. SIDEBAR (RESOURCES & AI CHAT) ---
with st.sidebar:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=150)
    
    st.markdown(f"## [🌐 Official Website]({WEBSITE_URL})")
    
    # AI CHATBOT SECTION
    st.divider()
    st.subheader("🤖 Admissions AI Assistant")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if chat_input := st.chat_input("Ask me about admissions..."):
        st.session_state.messages.append({"role": "user", "content": chat_input})
        with st.chat_message("user"):
            st.markdown(chat_input)
        
        with st.chat_message("assistant"):
            ai_res = get_ai_response(chat_input)
            st.markdown(ai_res)
            st.session_state.messages.append({"role": "assistant", "content": ai_res})

    st.divider()
    st.subheader("📚 Quick Resources")
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.link_button("📘 Handbook", HANDBOOK_URL, use_container_width=True)
    with col_r2:
        st.link_button("📰 Newsletter", NEWSLETTER_URL, use_container_width=True)
    
    st.divider()
    st.markdown(f"📍 [**Open Google Maps**]({MAP_LINK})")
    st.markdown(f"""
        <a href="tel:0543541610" style="text-decoration: none;">
            <div style="background-color: #1e3d59; color: white; padding: 10px; text-align: center; border-radius: 5px; font-weight: bold;">
                📞 Click to Call Office
            </div>
        </a>
    """, unsafe_allow_html=True)

# --- 5. MAIN HEADER ---
col_h1, col_h2 = st.columns([1, 5])
with col_h1:
    if os.path.exists(LOGO_PATH): st.image(LOGO_PATH, width=110)
with col_h2:
    st.title(SCHOOL_NAME)
    st.subheader("Student Admission Portal")

# CONTACT BAR
st.divider()
c1, c2, c3 = st.columns(3)
with c1: st.markdown("📞 **Phone:** (0543) 541610")
with c2: 
    timing = "7-1 Summer" if 4 <= datetime.now().month <= 9 else "8-2 Winter"
    st.markdown(f"🕒 **Hours:** {timing}")
with c3: st.markdown(f"📧 **Email:** [admissions@myers.edu.pk](mailto:admissions@myers.edu.pk)")
st.divider()

# --- 6. ADMISSION FORM ---
with st.form("admission_form", clear_on_submit=True):
    st.header("1. Student Details")
    col_a, col_b = st.columns(2)
    with col_a:
        name = st.text_input("Full Name")
        dob = st.date_input("Date of Birth", value=date(2015,1,1))
    with col_b:
        class_options = [
            "Pre-School: P1-P3", "Junior: K1-K4", 
            "Prep: E1-E3", "Senior: C1-C4 (O-Level)", 
            "Senior: AS/A2 (A-Level)"
        ]
        selected_class = st.selectbox("Applying for Class", class_options)

    st.header("2. Guardian & Contact")
    col_c, col_d = st.columns(2)
    with col_c:
        g_name = st.text_input("Guardian's Name")
        email = st.text_input("Contact Email")
    with col_d:
        prev_school = st.text_input("Previous School")
        scholarship = st.checkbox("Apply for Scholarship?")

    st.header("3. Background & Statement")
    fin_history = st.text_area("Financial History (e.g., previous school fee status)")
    join_reason = st.text_area("Why do you want to join Myer's College?")

    st.header("4. Document Uploads")
    col_e, col_f = st.columns(2)
    with col_e:
        id_file = st.file_uploader("Birth Certificate / ID Card", type=['jpg', 'png', 'pdf'])
    with col_f:
        grades_file = st.file_uploader("Proof of Grades (Last Result Card)", type=['jpg', 'png', 'pdf'])
    
    if st.form_submit_button("Submit Online Application"):
        if name and email:
            ts = datetime.now().strftime('%Y%m%d_%H%M')
            safe_name = name.replace(' ','_')
            id_path = os.path.join(UPLOAD_DIR, f"{safe_name}_ID_{ts}.pdf")
            grade_path = os.path.join(UPLOAD_DIR, f"{safe_name}_Grades_{ts}.pdf")
            
            if id_file:
                with open(id_path, "wb") as f: f.write(id_file.getbuffer())
            if grades_file:
                with open(grade_path, "wb") as f: f.write(grades_file.getbuffer())

            data = {
                "Submission Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Full Name": name, "Applied Class": selected_class, "DOB": str(dob),
                "Guardian Name": g_name, "Email": email, "Financial History": fin_history,
                "Join Reason": join_reason, "ID Path": id_path if id_file else "N/A",
                "Grades Path": grade_path if grades_file else "N/A"
            }
            save_to_csv(data)
            send_to_school_api(data)
            st.success("✅ Application Submitted Successfully!")
            st.balloons()
        else:
            st.error("Student Name and Contact Email are required.")

st.markdown("---")
st.markdown(f"<center>Myer's College Chakwal | <a href='{WEBSITE_URL}'>myers.edu.pk</a></center>", unsafe_allow_html=True)