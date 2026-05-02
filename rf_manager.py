import streamlit as st
import pandas as pd
import os
import subprocess

# 1. DATABASE LOADED FROM YOUR NAUSORI.XLSX FILE
# I've mapped these exactly from the document you provided.
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

DATA_FILE = "work_log.csv"

# Load/Create local file
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["Location", "Site ID", "Work Done", "Status", "Timestamp"])

st.set_page_config(page_title="RF Field Log", layout="wide")
st.title("📡 RF Field Work Manager")

# --- SIDEBAR ---
mode = st.sidebar.radio("Navigation", ["Add New Work", "Edit/Update Log"])

if mode == "Add New Work":
    st.sidebar.header("Log Entry")
    with st.sidebar.form("entry", clear_on_submit=True):
        site = st.selectbox("Site Name", sorted(list(SITE_MAP.keys())))
        work = st.text_area("What was done?")
        status = st.selectbox("Status", ["Planned", "In Progress", "Completed"])
        save = st.form_submit_button("Save to CSV")

    if save and work:
        ts = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
        new_row = pd.DataFrame([[site, SITE_MAP[site], work, status, ts]], columns=df.columns)
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.rerun()

else:
    st.sidebar.header("Edit Entry")
    if not df.empty:
        idx = st.sidebar.selectbox("Select Row", df.index, format_func=lambda x: f"{df.at[x, 'Location']} ({df.at[x, 'Timestamp']})")
        with st.sidebar.form("edit"):
            e_work = st.text_area("Update Work", value=df.at[idx, "Work Done"])
            e_stat = st.selectbox("Update Status", ["Planned", "In Progress", "Completed"], 
                                  index=["Planned", "In Progress", "Completed"].index(df.at[idx, "Status"]))
            if st.form_submit_button("Update"):
                df.at[idx, "Work Done"] = e_work
                df.at[idx, "Status"] = e_stat
                df.to_csv(DATA_FILE, index=False)
                st.rerun()

# --- MAIN TABLE ---
st.subheader("📋 Activity Log")
if not df.empty:
    st.dataframe(df.iloc[::-1], use_container_width=True, hide_index=True)
else:
    st.info("No work logged yet. Use the sidebar to start.")

if st.button("📁 Open Folder"):
    subprocess.Popen(f'explorer "{os.getcwd()}"')