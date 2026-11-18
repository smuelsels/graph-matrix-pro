import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import requests

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
            <h3>Samuel</h3>
            <p style="font-weight: bold; font-size: 13px;">NIM: 02120200017</p>
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
            <h3>Meysya</h3>
            <p style="font-weight: bold; font-size: 13px;">NIM: 021202600026</p>
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
    st.markdown('<div class="orange-divider"></div>', unsafe_allow_html=True)
    st.write("This application demonstrates graph theory concepts including graph visualization, node degree calculation, and adjacency matrix representation.")

    tab1, tab2, tab3 = st.tabs(["🎲 GRAPH VISUALIZATION", "📈 NODE DEGREES", "🔢 ADJACENCY MATRIX"])

    # Inisialisasi session state untuk graf
    if "graph" not in st.session_state:
        st.session_state.graph = None

    with tab1:
        col_left, col_right = st.columns([1, 1.3])

        with col_left:
            st.subheader("⚙️ GRAPH CONFIGURATION")
            st.markdown("**Create a Random Graph**")
            num_nodes = st.slider("Number of Nodes", min_value=2, max_value=20, value=6)
            max_edges = int(num_nodes * (num_nodes - 1) / 2)
            num_edges = st.slider("Number of Edges", min_value=1, max_value=max(1, max_edges), value=min(8, max_edges))

            if st.button("🎲 GENERATE RANDOM GRAPH"):
                st.session_state.graph = nx.gnm_random_graph(num_nodes, num_edges)

        with col_right:
            st.subheader("👁️ GRAPH VISUALIZATION")
            if st.session_state.graph is None:
                st.info("👆 Please generate a random graph using the controls on the left to see the visualization here.")
            else:
                fig, ax = plt.subplots(figsize=(6, 4))
                fig.patch.set_facecolor('#FAF4E6')
                ax.set_facecolor('#FAF4E6')
                pos = nx.spring_layout(st.session_state.graph, seed=42)
                nx.draw(
                    st.session_state.graph, pos, with_labels=True,
                    node_color="#FF7A2F", node_size=700,
                    font_color="white", font_weight="bold", edge_color="#555555", ax=ax
                )
                st.pyplot(fig)

    with tab2:
        st.subheader("📈 NODE DEGREES")
        if st.session_state.graph is not None:
            degrees = dict(st.session_state.graph.degree())
            df_deg = pd.DataFrame(list(degrees.items()), columns=["Node", "Degree (Derajat)"])
            st.dataframe(df_deg, use_container_width=True)
        else:
            st.warning("Silakan buat graf terlebih dahulu di tab GRAPH VISUALIZATION.")

    with tab3:
        st.subheader("🔢 ADJACENCY MATRIX")
        if st.session_state.graph is not None:
            adj_matrix = nx.to_numpy_array(st.session_state.graph, dtype=int)
            df_adj = pd.DataFrame(adj_matrix)
            st.dataframe(df_adj, use_container_width=True)
        else:
            st.warning("Silakan buat graf terlebih dahulu di tab GRAPH VISUALIZATION.")

# =====================================================================
# HALAMAN 3: JAVA ISLAND ROUTE PLANNER
# =====================================================================
elif menu == "Java Island Route Planner":
    st.markdown("<h1>🗺️ JAVA ISLAND ROUTE PLANNER</h1>", unsafe_allow_html=True)
    st.markdown('<div class="orange-divider"></div>', unsafe_allow_html=True)

    # Koordinat kota-kota utama di Pulau Jawa
    cities = {
        "Jakarta": (-6.2088, 106.8456),
        "Bandung": (-6.9175, 107.6191),
        "Semarang": (-6.9667, 110.4167),
        "Yogyakarta": (-7.7956, 110.3695),
        "Surakarta (Solo)": (-7.5755, 110.8243),
        "Surabaya": (-7.2575, 112.7521),
        "Malang": (-7.9666, 112.6326)
    }

    col_ctrl, col_map = st.columns([1, 1.4])

    with col_ctrl:
        st.subheader("📍 SELECT YOUR ROUTE")
        origin = st.selectbox("🚗 Origin City", list(cities.keys()), index=0)
        destination = st.selectbox("🎯 Destination City", list(cities.keys()), index=4)

        st.subheader("🛠️ Routing Options")
        use_osrm = st.checkbox("Use OSRM for accurate routing (recommended)", value=True)
        show_alt = st.checkbox("Show alternative routes", value=True)

        find_btn = st.button("🔍 FIND ROUTES")

    with col_map:
        st.subheader("🗺️ INTERACTIVE JAVA MAP")
        m = folium.Map(location=[-7.3, 110.0], zoom_start=7)

        lat1, lon1 = cities[origin]
        lat2, lon2 = cities[destination]

        folium.Marker([lat1, lon1], tooltip=f"Asal: {origin}", icon=folium.Icon(color="green")).add_to(m)
        folium.Marker([lat2, lon2], tooltip=f"Tujuan: {destination}", icon=folium.Icon(color="red")).add_to(m)

        if find_btn and origin != destination:
            if use_osrm:
                # Mengambil rute jalan raya asli dari API publik OSRM
                url = f"http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=full&geometries=geojson"
                res = requests.get(url).json()
                if "routes" in res and len(res["routes"]) > 0:
                    coords = res["routes"][0]["geometry"]["coordinates"]
                    route_points = [(c[1], c[0]) for c in coords]
                    dist_km = res["routes"][0]["distance"] / 1000
                    dur_hr = res["routes"][0]["duration"] / 3600

                    folium.PolyLine(route_points, color="#FF7A2F", weight=5, opacity=0.8).add_to(m)
                    st.success(f"Jarak: **{dist_km:.1f} km** | Estimasi Waktu: **{dur_hr:.1f} jam**")
            else:
                # Garis lurus jika OSRM tidak dicentang
                folium.PolyLine([(lat1, lon1), (lat2, lon2)], color="blue", weight=4).add_to(m)

        st_folium(m, width=700, height=450)

# --- FOOTER ---
st.markdown("""
<div class="footer">
    🌐 GRAPH MATRIX PRO - FINAL PROJECT © 2024 | COMPREHENSIVE GRAPH ANALYSIS & JAVA ROUTE PLANNING | DEVELOPED WITH STREAMLIT & NETWORKX
</div>
""", unsafe_allow_html=True)