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
    layout="wide"
)

# --- CUSTOM CSS (Warna Krem & Oranye) ---
st.markdown("""
<style>
    .stApp {
        background-color: #FAF4E6;
        color: #1E1E1E;
    }
    .orange-divider {
        height: 3px;
        background-color: #FF7A2F;
        border: none;
        margin-top: -10px;
        margin-bottom: 20px;
    }
    div.stButton > button {
        background-color: #FF7A2F;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        width: 100%;
        padding: 10px 0;
        transition: background-color 0.2s ease;
    }
    div.stButton > button:hover {
        background-color: #E5651C;
        color: white;
    }
    .profile-card {
        background-color: #FFFFFF;
        padding: 24px 20px;
        border-radius: 16px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
        text-align: center;
        border-top: 5px solid #FF7A2F;
        margin-top: 10px;
    }
    .role-badge {
        background-color: #FF7A2F;
        color: white;
        padding: 7px 14px;
        border-radius: 20px;
        font-size: 12.5px;
        font-weight: bold;
        display: inline-block;
        margin: 10px 0 14px 0;
    }
    .contrib-list {
        text-align: left;
        font-size: 14px;
        color: #333333;
        margin-top: 8px;
    }
    .contrib-list ul {
        padding-left: 18px;
        margin-top: 6px;
    }
    .footer {
        text-align: center;
        font-size: 12px;
        font-weight: bold;
        color: #444;
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid #D8CFC0;
    }
</style>
""", unsafe_allow_html=True)

# --- NAVIGASI SIDEBAR ---
st.sidebar.title("🧭 Navigasi Aplikasi")
menu = st.sidebar.radio(
    "Pilih Halaman:",
    ["Team Member Profiles", "Graph Matrix Application", "Java Island Route Planner"]
)

# =====================================================================
# HALAMAN 1: TEAM MEMBER PROFILES
# =====================================================================
if menu == "Team Member Profiles":
    st.markdown("<h1 style='text-align: center;'>TEAM MEMBER PROFILES</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center; font-size: 18px; font-weight: 600;'>"
        "Meet the talented team behind Graph Matrix Pro"
        "</p>",
        unsafe_allow_html=True
    )
    st.write("")

    team_members = [
        {
            "name": "Samuel",
            "nim": "02120200017",
            "role": "⚙️ DevOps & Project Manager / Team Leader",
            "photo": "https://via.placeholder.com/200x200.png?text=Samuel",
            "contributions": [
                "Mengatur alur kerja tim & timeline proyek",
                "Mengelola struktur repository & deployment aplikasi",
                "Koordinasi integrasi antar modul"
            ]
        },
        {
            "name": "Meysya",
            "nim": "021202600026",
            "role": "🪄 Quality Assurance (QA) & Finalizer",
            "photo": "https://via.placeholder.com/200x200.png?text=Meysya",
            "contributions": [
                "Pengujian fungsionalitas graf & rute peta",
                "Pengecekan tampilan UI/UX & validasi input"
            ]
        },
        {
            "name": "Abdi",
            "nim": "021202600026",
            "role": "💻 Back-End Developer & Full-Stack Developer",
            "photo": "https://via.placeholder.com/200x200.png?text=Abdi",
            "contributions": [
                "Implementasi logika graf (NetworkX) & integrasi OSRM",
                "Pengembangan antarmuka interaktif Streamlit"
            ]
        }
    ]

    cols = st.columns(3)
    for col, member in zip(cols, team_members):
        with col:
            st.markdown('<div class="profile-card">', unsafe_allow_html=
