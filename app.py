import folium
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import requests
import streamlit as st
from streamlit_folium import st_folium

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Graph Matrix Pro",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .stApp {
        background-color: #FAF4E6;
        color: #1E1E1E;
    }
    section[data-testid="stSidebar"] {
        background-color: #1E1E1E;
        color: #F5F5F5;
    }
    section[data-testid="stSidebar"] * {
        color: #F5F5F5;
    }
    .sidebar-brand {
        font-size: 20px;
        font-weight: 800;
        line-height: 1.25;
        margin-bottom: 4px;
    }
    .sidebar-sub {
        font-size: 12px;
        color: #BBBBBB !important;
        margin-bottom: 16px;
    }
    .orange-banner {
        background: linear-gradient(90deg, #FF7A2F 0%, #FF934F 100%);
        height: 46px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .orange-divider {
        height: 3px;
        background-color: #FF7A2F;
        border: none;
        margin-top: -8px;
        margin-bottom: 18px;
    }
    .top-pill-card {
        background-color: #FFFFFF;
        height: 42px;
        border-radius: 12px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.06);
        margin-bottom: 16px;
    }
    div.stButton > button {
        background-color: #FF7A2F;
        color: white !important;
        font-weight: 700;
        border-radius: 8px;
        border: none;
        width: 100%;
        padding: 10px 14px;
        text-align: center;
    }
    div.stButton > button:hover {
        background-color: #E5651C;
        color: white !important;
    }
    .profile-card {
        background-color: #FFFFFF;
        padding: 22px 20px;
        border-radius: 16px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.08);
        text-align: center;
        margin-top: 10px;
    }
    .profile-name {
        font-size: 20px;
        font-weight: 800;
        margin: 8px 0 4px 0;
        color: #1E1E1E;
    }
    .profile-nim {
        font-size: 13px;
        font-weight: 700;
        color: #444444;
        margin-bottom: 10px;
    }
    .role-badge {
        background-color: #FF7A2F;
        color: white;
        padding: 8px 14px;
        border-radius: 18px;
        font-size: 12.5px;
        font-weight: 700;
        display: inline-block;
        margin: 8px 0 14px 0;
    }
    .contrib-box {
        text-align: left;
        font-size: 13.5px;
        color: #2B2B2B;
    }
    .contrib-box ul {
        padding-left: 18px;
        margin-top: 6px;
    }
    .contrib-box li {
        margin-bottom: 6px;
    }
    .overview-card {
        background-color: #FFFFFF;
        padding: 22px 24px;
        border-radius: 14px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.07);
        height: 100%;
    }
    .overview-card ul {
        padding-left: 18px;
        margin-top: 10px;
        font-size: 14px;
        color: #2B2B2B;
    }
    .overview-card li {
        margin-bottom: 6px;
    }
    .legend-row {
        font-size: 12.5px;
        font-weight: 600;
        margin-top: 8px;
        color: #333333;
    }
    .footer {
        text-align: center;
        font-size: 12px;
        font-weight: 700;
        color: #333333;
        margin-top: 45px;
        padding-top: 16px;
        border-top: 1px solid #D5CBB8;
    }
</style>
""", unsafe_allow_html=True)

# --- DATA KOTA PULAU JAWA ---
CITIES = {
    "Jakarta": (-6.2088, 106.8456),
    "Tangerang": (-6.1783, 106.6319),
    "Bekasi": (-6.2383, 106.9756),
    "Bogor": (-6.5971, 106.8060),
    "Depok": (-6.4025, 106.7942),
    "Sukabumi": (-6.9278, 106.9300),
    "Bandung": (-6.9175, 107.6191),
    "Cimahi": (-6.8841, 107.5413),
    "Garut": (-7.2279, 107.9087),
    "Tasikmalaya": (-7.3274, 108.2207),
    "Cirebon": (-6.7320, 108.5523),
    "Purwokerto": (-7.4244, 109.2302),
    "Tegal": (-6.8694, 109.1402),
    "Pekalongan": (-6.8898, 109.6746),
    "Semarang": (-6.9667, 110.4167),
    "Salatiga": (-7.3305, 110.5084),
    "Magelang": (-7.4797, 110.2178),
    "Yogyakarta": (-7.7956, 110.3695),
    "Surakarta (Solo)": (-7.5755, 110.8243),
    "Kudus": (-6.8048, 110.8405),
    "Pati": (-6.7559, 111.0380),
    "Madiun": (-7.6298, 111.5239),
    "Kediri": (-7.8480, 112.0178),
    "Blitar": (-8.0983, 112.1681),
    "Malang": (-7.9666, 112.6326),
    "Surabaya": (-7.2575, 112.7521),
    "Sidoarjo": (-7.4478, 112.7183),
    "Mojokerto": (-7.4722, 112.4336),
    "Pasuruan": (-7.6453, 112.9075),
    "Probolinggo": (-7.7543, 113.2159),
    "Jember": (-8.1721, 113.7008),
    "Banyuwangi": (-8.2192, 114.3691)
}

# --- SESSION STATE ---
if "page" not in st.session_state:
    st.session_state.page = "Team Profiles"
if "graph" not in st.session_state:
    st.session_state.graph = None
if "route_data" not in st.session_state:
    st.session_state.route_data = None

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("""
        <div class="sidebar-brand">🌐 DISCRETE MATHEMATICS FINAL PROJECT</div>
        <div class="sidebar-sub">Advanced Graph Analysis Platform</div>
        <hr style="border-color:#383838;">
    """, unsafe_allow_html=True)

    if st.button("👥 TEAM PROFILES", key="nav_team"):
        st.session_state.page = "Team Profiles"
    if st.button("📊 GRAPH MATRIX APP", key="nav_graph"):
        st.session_state.page = "Graph Matrix App"
    if st.button("🗺️ JAVA ROUTE FINDER", key="nav_route"):
        st.session_state.page = "Java Route Finder"

    st.markdown("""
        <hr style="border-color:#383838; margin-top:20px;">
        <div style="font-size:12px; font-weight:700; margin-bottom:8px;">👥 DEVELOPMENT TEAM</div>
        <div style="font-size:12px; color:#D4D4D4; line-height:1.5;">
            - Samuel J. T. M. (021202600017)<br>
            - Meysya Rahmadiyah (021202600016)<br>
            - Abdi (021202600026)
        </div>
    """, unsafe_allow_html=True)

page = st.session_state.page

# =====================================================================
# HALAMAN 1: TEAM PROFILES + PROJECT OVERVIEW
# =====================================================================
if page == "Team Profiles":
    st.markdown('<div class="orange-banner"></div>', unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center; letter-spacing:1px;'>TEAM MEMBER PROFILES</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:18px; font-weight:600; margin-bottom:16px;'>Meet the talented team behind Graph Matrix Pro</p>", unsafe_allow_html=True)

    team = [
        {
            "name": "SAMUEL JUAN TRISNA MANURUNG",
            "nim": "021202600017",
            "role": "⚙️ DevOps & Project Manager / Team Leader",
            "photo": "https://via.placeholder.com/220x260.png?text=Samuel",
            "contributions": [
                "Led the team by coordinating tasks and managing timelines.",
                "Oversaw the entire development workflow.",
                "Handled deployment using GitHub and Streamlit Community Cloud.",
                "Managed version control and repository structure.",
                "Ensured final deployment met project requirements."
            ]
        },
        {
            "name": "MEYSYA RAHMADIYAH",
            "nim": "021202600016",
            "role": "🪄 Quality Assurance (QA) & Finalizer",