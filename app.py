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

# --- CUSTOM CSS (Warna Krem & Oranye sesuai gambar) ---
st.markdown("""
<style>
    /* Latar belakang utama warna krem lembut */
    .stApp {
        background-color: #FAF4E6;
        color: #1E1E1E;
    }
    /* Garis pembatas oranye di bawah judul utama */
    .orange-divider {
        height: 3px;
        background-color: #FF7A2F;
        border: none;
        margin-top: -10px;
        margin-bottom: 20px;
    }
    /* Tombol oranye */
    div.stButton > button {
        background-color: #FF7A2F;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        width: 100%;
        padding: 10px 0;
    }
    div.stButton > button:hover {
        background-color: #E5651C;
        color: white;
    }
    /* Kartu Profil Tim */
    .profile-card {
        background-color: #FFFFFF;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        text-align: center;
        height: 100%;
    }
    .role-badge {
        background-color: #FF7A2F;
        color: white;
        padding: 8px 15px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: bold;
        display: inline-block;
        margin: 12px 0;
    }
    .contrib-list {
        text-align: left;
        font-size: 14px;
        color: #333333;
    }
    /* Footer */
    .footer {
        text-align: center;
        font-size: 12px;
        font-weight: bold;
        color: #333;
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid #CCC;
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
    st.markdown("<p style='font-size: 18px; font-weight: 600;'>Meet the talented team behind Graph Matrix Pro</p>", unsafe_allow_html=True)
    st.write("")

    col1, col2, col3 = st.columns(3)

    # Anggota 1
    with col1:
        # Ganti URL dengan path foto lokal Anda, misal: "foto1.jpg"
        st.image("https://via.placeholder.com/200x240.png?text=Foto+Anggota+1", width=180)
        st.markdown("""
        <div class="profile-card">
            <h3>Samuel Juan Trisna Manurung</h3>
            <p style="font-weight: bold; font-size: 13px;">NIM: 021202600017</p>
            <div class="role-badge">⚙️ DevOps & Project Manager / Team Leader</div>
            <div class="contrib-list">
                <b>Contributions:</b>
                <ul>
                    <li>.</li>
                    <li>.</li>
                    <li>.</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Anggota 2
    with col2:
        st.image("https://via.placeholder.com/200x240.png?text=Foto+Anggota+2", width=180)
        st.markdown("""
        <div class="profile-card">
            <h3>Meysya Rahmadiyah</h3>
            <p style="font-weight: bold; font-size: 13px;">NIM: 021202600016</p>
            <div class="role-badge">🪄 Quality Assurance (QA) & Finalizer</div>
            <div class="contrib-list">
                <b>Contributions:</b>
                <ul>
                    <li>.</li>
                    <li>.</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Anggota 3
    with col3:
        st.image("https://via.placeholder.com/200x240.png?text=Foto+Anggota+3", width=180)
        st.markdown("""
        <div class="profile-card">
            <h3>abdi</h3>
            <p style="font-weight: bold; font-size: 13px;">NIM: 021202600026</p>
            <div class="role-badge">💻 Back-End Developer & Full-Stack Developer</div>
            <div class="contrib-list">
                <b>Contributions:</b>
                <ul>
                    <li>.</li>
                    <li>.</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

# =====================================================================
# HALAMAN 2: GRAPH MATRIX APPLICATION
# =====================================================================
elif menu == "Graph Matrix Application":
st.markdown("<h1>📊 GRAPH MATRIX APPLICATION</h1>", unsafe_allow_html=True)
