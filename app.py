import streamlit as st
import pandas as pd
from datetime import datetime

# --- बिजनेस की जानकारी ---
ST_NAME = "BABA FAKIRA SUMIT PANDIT JAN SEVA KENDRA"
OWNER = "SUMIT SHARMA"

st.set_page_config(page_title=ST_NAME, layout="wide")

# डेटा स्टोरेज (जब तक ब्राउज़र खुला है)
if 'db' not in st.session_state:
    st.session_state.db = []

st.title(f"🛡️ {ST_NAME}")
st.write(f"**संचालक:** {OWNER} | **CSC ID:** 473614450018")

# --- बिलिंग फॉर्म ---
with st.form("billing_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        c_name = st.text_input("ग्राहक का नाम")
        c_mob = st.text_input("मोबाइल नंबर")
        service = st.selectbox("सर्विस", ["Photocopy", "PAN Card", "Income/Caste Cert", "Pension", "RTI", "Other"])
    with col2:
        g_fee = st.number_input("सरकारी फीस (Govt Fee)", min_value=0)
        s_fee = st.number_input("आपका चार्ज (Service Charge)", min_value=0)
        mode = st.radio("पेमेंट मोड", ["Cash", "Online", "Udhaar"])
    
    if st.form_submit_button("बिल सेव करें"):
        st.session_state.db.append({
            "Date": datetime.now().strftime("%d-%m-%Y %H:%M"),
            "Customer": c_name, "Mobile": c_mob, "Service": service,
            "Total": g_fee + s_fee, "Mode": mode
        })
        st.success("डाटा सेव हो गया!")

# --- हिसाब किताब ---
if st.session_state.db:
    df = pd.DataFrame(st.session_state.db)
    st.divider()
    st.subheader("आज का हिसाब")
    st.table(df)
    
    # उधार का हिसाब
    udhaar_total = df[df['Mode'] == 'Udhaar']['Total'].sum()
    st.error(f"कुल बकाया उधार: ₹{udhaar_total}")
