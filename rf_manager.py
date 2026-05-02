import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. SITE DATABASE (From your Nausori.xlsx)
SITE_MAP = {
    "Babavoce": "V0177", "Bau Island": "V0116", "Bau Landing": "V0575", "Bau Rd": "V0465",
    "Baulevu": "V0217", "Bureta": "V0552", "Buretu": "V0156", "Colo-I-Suva": "V0584",
    "Corbett": "V0136", "Dawasamu": "V0374", "Dilkusha": "V0217", "Forest Park": "V0072",
    "Kiuva": "V0369", "Koroqaqa": "V0559", "Korovou Deepwater": "V0557", "Korovou Ex": "V0051",
    "Lakeba": "V0102", "Lakena": "V0334", "Levuka": "V0080", "Logani": "V0490",
    "Lomaivuna": "V0499", "Lomanikoro": "V0245", "Manoca": "V0322", "Mokani": "V0267",
    "Muaniweni": "V0013", "Nabitu": "V0266", "Nabouva": "V0532", "Nabulini": "V0530",
    "Nadali": "V0542", "Naigani": "V0126", "Naiyala": "V0197", "Nakelo Landing": "V0579",
    "Nakobalevu": "V0377", "Nakorotubu": "V0338", "Namulomulo": "V0166", "Natovi": "V0528",
    "Nausori Airport": "V0091", "Nausori Ex": "V-NAU", "Nausori Market": "V0463",
    "Nausori Town": "V0265", "Navuso": "V0250", "Nayavu": "V0234", "Noco": "V0155",
    "Raralevu": "V0108", "Ross St": "V0464", "Rt Cakobau": "V0436", "Sawani": "V0137",
    "Taulevu": "V0233", "Tavuya": "V0246", "Tonia": "V0198", "Vione Gau": "V0222",
    "Viria": "V0495", "Visama": "V0479", "Vuci": "V0389", "Vuci South": "V0139",
    "Vunidawa": "V0111", "Vunikawai": "V0042", "Vunimono NFA": "V0358", "Vusuya": "V0312",
    "Waidalice": "V0472", "Waila Housing": "V0544", "Waimaro": "V0521", "Wainibokasi": "V0339",
    "Wakaya Island": "V0050", "Wakaya Resort": "V0076", "Tokou": "V0219"
}

st.set_page_config(page_title="RF Field Log (Cloud)", layout="wide")
st.title("📡 RF Field Work - Google Sheets Sync")

# --- CONNECTION ---
conn = st.connection("gsheets", type=GSheetsConnection)

# Read current data from Google Sheets
try:
    df = conn.read(ttl="0s")
except:
    df = pd.DataFrame(columns=["Location", "Site ID", "Work Done", "Status", "Timestamp"])

# --- NAVIGATION ---
mode = st.sidebar.radio("Navigation", ["Add Entry", "Edit Entry"])

if mode == "Add Entry":
    st.sidebar.header("Log New Work")
    with st.sidebar.form("entry", clear_on_submit=True):
        site = st.selectbox("Site Name", sorted(list(SITE_MAP.keys())))
        work = st.text_area("Work Description")
        status = st.selectbox("Status", ["Planned", "In Progress", "Completed"])
        submit = st.form_submit_button("Upload to Cloud")

    if submit and work:
        ts = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
        new_row = pd.DataFrame([[site, SITE_MAP[site], work, status, ts]], columns=df.columns)
        updated_df = pd.concat([df, new_row], ignore_index=True)
        conn.update(data=updated_df)
        st.success(f"Synced {site} to Google Sheets!")
        st.rerun()

else:
    st.sidebar.header("Edit Work")
    if not df.empty:
        idx = st.sidebar.selectbox("Select Entry", df.index, format_func=lambda x: f"{df.at[x, 'Location']} ({df.at[x, 'Timestamp']})")
        with st.sidebar.form("edit"):
            e_work = st.text_area("Update Work", value=df.at[idx, "Work Done"])
            e_stat = st.selectbox("Update Status", ["Planned", "In Progress", "Completed"], 
                                  index=["Planned", "In Progress", "Completed"].index(df.at[idx, "Status"]))
            if st.form_submit_button("Save Changes"):
                df.at[idx, "Work Done"] = e_work
                df.at[idx, "Status"] = e_stat
                conn.update(data=df)
                st.rerun()

# --- DISPLAY ---
st.subheader("📋 Live Activity Feed")
if not df.empty:
    st.dataframe(df.iloc[::-1], use_container_width=True, hide_index=True)
else:
    st.info("No data in Google Sheets yet.")
