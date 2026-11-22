import base64
import urllib.parse
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


def make_avatar_data_uri(name: str, accent: str = "#E86A2C") -> str:
    """Membuat avatar SVG bersih bertema hangat jika foto lokal belum tersedia."""
    parts = [p[0].upper() for p in name.strip().split() if p]
    initials = "".join(parts[:2]) or "GM"
    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="220" height="250" viewBox="0 0 220 250">
        <defs>
            <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stop-color="#1E2B37"/>
                <stop offset="100%" stop-color="#2F4152"/>
            </linearGradient>
        </defs>
        <rect width="220" height="250" rx="18" fill="url(#bg)"/>
        <circle cx="110" cy="96" r="44" fill="{accent}" opacity="0.92"/>
        <text x="110" y="110" text-anchor="middle" fill="#FFFFFF" font-family="Arial, sans-serif" font-size="34" font-weight="bold">{initials}</text>
        <rect x="34" y="162" width="152" height="6" rx="3" fill="{accent}" opacity="0.7"/>
        <text x="110" y="192" text-anchor="middle" fill="#F8F5EE" font-family="Arial, sans-serif" font-size="14" font-weight="bold">{urllib.parse.quote(name.split()[0])}</text>
        <text x="110" y="213" text-anchor="middle" fill="#B8C4D0" font-family="Arial, sans-serif" font-size="11">Graph Matrix Pro</text>
    </svg>
    """.strip()
    encoded = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    return f"data:image/svg+xml;base64,{encoded}"


# --- CUSTOM CSS (Palet Warm Ivory, Slate Navy & Terracotta Amber) ---
st.markdown("""
<style>
    .stApp {
        background-color: #F8F5EE;
        color: #16202A;
    }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #16202A 0%, #1E2C3A 100%);
        color: #F8F5EE;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    section[data-testid="stSidebar"] * {
        color: #F8F5EE;
    }
    .sidebar-brand {
        font-size: 19px;
        font-weight: 800;
        line-height: 1.25;
        margin-bottom: 4px;
        color: #FFFFFF !important;
    }
    .sidebar-sub {
        font-size: 12px;
        color: #B6C2CE !important;
        margin-bottom: 14px;
    }
    .orange-banner {
        background: linear-gradient(120deg, #16202A 0%, #273849 52%, #E86A2C 100%);
        padding: 14px 22px;
        border-radius: 14px;
        margin-bottom: 22px;
        color: #FFFFFF;
        box-shadow: 0 6px 18px rgba(22, 32, 42, 0.12);
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 10px;
    }
    .banner-pill {
        background: rgba(255, 255, 255, 0.14);
        border: 1px solid rgba(255, 255, 255, 0.25);
        color: #FFFFFF;
        font-size: 12px;
        font-weight: 700;
        padding: 5px 12px;
        border-radius: 999px;
    }
    .orange-divider {
        height: 3px;
        background: linear-gradient(90deg, #E86A2C 0%, #F39C6B 100%);
        border: none;
        border-radius: 999px;
        margin-top: -8px;
        margin-bottom: 18px;
    }
    .top-pill-card {
        background-color: #FFFFFF;
        height: 36px;
        border-radius: 12px;
        border-left: 4px solid #E86A2C;
        box-shadow: 0 3px 10px rgba(22, 32, 42, 0.05);
        margin-bottom: 16px;
    }
    div.stButton > button {
        background-color: #E86A2C;
        color: #FFFFFF !important;
        font-weight: 700;
        border-radius: 10px;
        border: none;
        width: 100%;
        padding: 10px 14px;
        text-align: center;
        box-shadow: 0 4px 10px rgba(232, 106, 44, 0.24);
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        background-color: #CF571D;
        color: #FFFFFF !important;
        transform: translateY(-1px);
    }
    .profile-card {
        background-color: #FFFFFF;
        padding: 22px 20px;
        border-radius: 16px;
        border: 1px solid #EAE2D3;
        box-shadow: 0 6px 18px rgba(22, 32, 42, 0.06);
        text-align: center;
        margin-top: 10px;
    }
    .profile-name {
        font-size: 18px;
        font-weight: 800;
        margin: 6px 0 4px 0;
        color: #16202A;
    }
    .profile-nim {
        font-size: 13px;
        font-weight: 700;
        color: #52606D;
        margin-bottom: 10px;
    }
    .role-badge {
        background-color: #FFF1EA;
        color: #C84F16;
        border: 1px solid #F6C3A8;
        padding: 7px 14px;
        border-radius: 18px;
        font-size: 12px;
        font-weight: 700;
        display: inline-block;
        margin: 6px 0 14px 0;
    }
    .contrib-box {
        text-align: left;
        font-size: 13.5px;
        color: #24303C;
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
        border-radius: 16px;
        border: 1px solid #EAE2D3;
        border-top: 4px solid #16202A;
        box-shadow: 0 6px 16px rgba(22, 32, 42, 0.06);
        height: 100%;
    }
    .overview-card ul {
        padding-left: 18px;
        margin-top: 10px;
        font-size: 14px;
        color: #24303C;
    }
    .overview-card li {
        margin-bottom: 6px;
    }
    .legend-row {
        background-color: #FFFFFF;
        border: 1px solid #EAE2D3;
        border-radius: 10px;
        padding: 8px 14px;
        font-size: 12.5px;
        font-weight: 600;
        margin-top: 8px;
        color: #16202A;
    }
    .footer {
        text-align: center;
        font-size: 12px;
        font-weight: 700;
        color: #52606D;
        margin-top: 45px;
        padding-top: 16px;
        border-top: 1px solid #DFD5C5;
    }
</style>
/* Memaksa ketiga tulisan tab menjadi hitam */
    button[data-baseweb="tab"],
    button[data-baseweb="tab"] p,
    button[data-baseweb="tab"] div,
    button[data-baseweb="tab"] span {
        color: #16202A !important;
        font-weight: 700 !important;
    }

    /* Tab yang sedang aktif tetap hitam dengan garis bawah oranye */
    button[data-baseweb="tab"][aria-selected="true"],
    button[data-baseweb="tab"][aria-selected="true"] p,
    button[data-baseweb="tab"][aria-selected="true"] div,
    button[data-baseweb="tab"][aria-selected="true"] span {
        color: #16202A !important;
        border-bottom-color: #E86A2C !important;
    }
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
        <hr style="border-color:rgba(255,255,255,0.12);">
    """, unsafe_allow_html=True)

    if st.button("👥 TEAM PROFILES", key="nav_team"):
        st.session_state.page = "Team Profiles"
    if st.button("📊 GRAPH MATRIX APP", key="nav_graph"):
        st.session_state.page = "Graph Matrix App"
    if st.button("🗺️ JAVA ROUTE FINDER", key="nav_route"):
        st.session_state.page = "Java Route Finder"

    st.markdown("""
        <hr style="border-color:rgba(255,255,255,0.12); margin-top:20px;">
        <div style="font-size:12px; font-weight:700; margin-bottom:8px; color:#F39C6B;">👥 DEVELOPMENT TEAM</div>
        <div style="font-size:12px; color:#D6E0EA; line-height:1.6;">
            • Samuel J. T. M. (021202600017)<br>
            • Meysya Rahmadiyah (021202600016)<br>
            • Abdi (021202600026)
        </div>
    """, unsafe_allow_html=True)

page = st.session_state.page

# =====================================================================
# HALAMAN 1: TEAM PROFILES + PROJECT OVERVIEW
# =====================================================================
if page == "Team Profiles":
    st.markdown("""
        <div class="orange-banner">
            <span style="font-weight:700; font-size:14px;">🌐 Graph Matrix Pro • Discrete Mathematics Final Project</span>
            <span class="banner-pill">Graph Theory • Adjacency Matrix • Java Routing</span>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center; letter-spacing:1px; color:#16202A;'>TEAM MEMBER PROFILES</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:17px; font-weight:600; color:#52606D; margin-bottom:20px;'>Meet the talented team behind Graph Matrix Pro</p>", unsafe_allow_html=True)

    team = [
        {
            "name": "SAMUEL JUAN TRISNA MANURUNG",
            "nim": "021202600017",
            "role": "⚙️ DevOps & Project Manager / Team Leader",
            "accent": "#E86A2C",
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
            "accent": "#D97706",
            "contributions": [
                "Conducted thorough testing of all features to detect bugs, UI inconsistencies, and functionality issues.",
                "Reported issues to the developers and verified fixes to ensure the system operated smoothly.",
                "Reviewed the entire web application for quality, completeness, and user experience before final submission.",
                "Finalized all project components, including documentation, formatting, and the submission file.",
                "Ensured that the deployed website and project report met academic standards and were error-free."
            ]
        },
        {
            "name": "ABDI",
            "nim": "021202600026",
            "role": "💻 Back-End Developer & Full-Stack Developer",
            "accent": "#2B6CB0",
            "contributions": [
                "Developed the server-side logic and built the core functionalities required for the web application.",
                "Designed and managed the data flow between the front-end and back-end components.",
                "Implemented APIs and ensured proper communication between the user interface and the database.",
                "Provided full-stack support by assisting with front-end integration and troubleshooting issues during development.",
                "Ensured the overall performance, stability, and functionality of the system."
            ]
        }
    ]

    cols = st.columns(3)
    for col, member in zip(cols, team):
        with col:
            _, img_c, _ = st.columns([1, 2, 1])
            with img_c:
                # Ganti make_avatar_data_uri(...) dengan path foto lokal (misal "assets/samuel.jpg") jika sudah ada
                st.image(make_avatar_data_uri(member["name"], member["accent"]), width=185)

            bullets = "".join(f"<li>{item}</li>" for item in member["contributions"])
            st.markdown(f"""
                <div class="profile-card">
                    <div class="profile-name">{member["name"]}</div>
                    <div class="profile-nim">NIM: {member["nim"]}</div>
                    <div class="role-badge">{member["role"]}</div>
                    <div class="contrib-box">
                        <b>Contributions:</b>
                        <ul>{bullets}</ul>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#DFD5C5; margin:34px 0 22px 0;'>", unsafe_allow_html=True)
    st.markdown("<h2>📋 PROJECT OVERVIEW</h2>", unsafe_allow_html=True)
    st.markdown('<div class="orange-divider"></div>', unsafe_allow_html=True)

    ov1, ov2 = st.columns(2)
    with ov1:
        st.markdown("""
            <div class="overview-card">
                <h3>🎯 Project Objectives</h3>
                <ul>
                    <li>Develop a comprehensive graph theory visualization and analysis tool</li>
                    <li>Create an interactive matrix application with adjacency matrix features</li>
                    <li>Build a Java city routing system with Dijkstra's algorithm</li>
                    <li>Deploy a fully functional web application using Streamlit</li>
                    <li>Document the entire development process and results</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    with ov2:
        st.markdown("""
            <div class="overview-card">
                <h3>🛠️ Technologies Used</h3>
                <ul>
                    <li><b>Frontend:</b> Streamlit, Folium, Matplotlib</li>
                    <li><b>Backend:</b> Python, NetworkX, NumPy, Pandas</li>
                    <li><b>Algorithms:</b> Dijkstra's Algorithm, Graph Theory</li>
                    <li><b>Deployment:</b> GitHub, Streamlit Community Cloud</li>
                    <li><b>Design:</b> Custom CSS, Google Fonts</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

# =====================================================================
# HALAMAN 2: GRAPH MATRIX APPLICATION
# =====================================================================
if page == "Graph Matrix App":
    st.markdown("""
        <div class="orange-banner">
            <span style="font-weight:700; font-size:14px;">📊 Graph Matrix Pro • Graph Theory & Adjacency Analysis</span>
            <span class="banner-pill">NetworkX • Degrees • Matrix Heatmap</span>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<h1 style='color:#16202A;'>📊 GRAPH MATRIX APPLICATION</h1>", unsafe_allow_html=True)
    st.markdown('<div class="orange-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#52606D; font-size:15px;'>"
        "This application demonstrates graph theory concepts including graph visualization, "
        "node degree calculation, and adjacency matrix representation."
        "</p>",
        unsafe_allow_html=True
    )

    tab1, tab2, tab3 = st.tabs(["🎲 GRAPH VISUALIZATION", "📈 NODE DEGREES", "🔢 ADJACENCY MATRIX"])

    # --- TAB 1 ---
    with tab1:
        p1, p2 = st.columns(2)
        with p1:
            st.markdown('<div class="top-pill-card"></div>', unsafe_allow_html=True)
        with p2:
            st.markdown('<div class="top-pill-card"></div>', unsafe_allow_html=True)

        col_left, col_right = st.columns([1, 1.35])
        with col_left:
            st.markdown('<div class="panel-card">', unsafe_allow_html=True)
            st.subheader("⚙️ GRAPH CONFIGURATION")
            st.markdown("**Create a Random Graph**")
            num_nodes = st.slider("Number of Nodes", min_value=2, max_value=20, value=6)
            max_edges = num_nodes * (num_nodes - 1) // 2
            num_edges = st.slider(
                "Number of Edges",
                min_value=1,
                max_value=max(1, max_edges),
                value=min(8, max(1, max_edges))
            )

            if st.button("🎲 GENERATE RANDOM GRAPH"):
                G = nx.gnm_random_graph(num_nodes, num_edges)
                for u, v in G.edges():
                    G[u][v]["weight"] = int(np.random.randint(1, 20))
                st.session_state.graph = G
            st.markdown("</div>", unsafe_allow_html=True)

        with col_right:
            st.markdown('<div class="panel-card">', unsafe_allow_html=True)
            st.subheader("👁️ GRAPH VISUALIZATION")
            G = st.session_state.graph
            if G is None:
                st.info("👆 Please generate a random graph using the controls on the left to see the visualization here.")
            else:
                fig, ax = plt.subplots(figsize=(6.5, 4.2))
                fig.patch.set_facecolor("#FFFFFF")
                ax.set_facecolor("#FAF7F2")
                pos = nx.spring_layout(G, seed=42)
                labels = {n: str(n + 1) for n in G.nodes()}
                nx.draw(
                    G, pos,
                    labels=labels,
                    with_labels=True,
                    node_color="#E86A2C",
                    node_size=760,
                    font_color="#FFFFFF",
                    font_weight="bold",
                    edge_color="#16202A",
                    edgecolors="#16202A",
                    linewidths=1.5,
                    width=1.8,
                    ax=ax
                )
                plt.tight_layout()
                st.pyplot(fig, use_container_width=True)
                plt.close(fig)
            st.markdown("</div>", unsafe_allow_html=True)

    # --- TAB 2 ---
    with tab2:
        p1, p2 = st.columns(2)
        with p1:
            st.markdown('<div class="top-pill-card"></div>', unsafe_allow_html=True)
        with p2:
            st.markdown('<div class="top-pill-card"></div>', unsafe_allow_html=True)

        G = st.session_state.graph
        if G is None:
            st.warning("Silakan buat graf terlebih dahulu di tab **GRAPH VISUALIZATION**.")
        else:
            c_left, c_right = st.columns([1.2, 1])

            degrees = [G.degree(n) for n in G.nodes()]
            node_labels = [str(n + 1) for n in G.nodes()]
            max_deg = max(degrees) if degrees else 0
            min_deg = min(degrees) if degrees else 0

            with c_left:
                st.markdown('<div class="panel-card">', unsafe_allow_html=True)
                st.subheader("📊 NODE DEGREES CALCULATION")
                fig, ax = plt.subplots(figsize=(6.5, 4.4))
                fig.patch.set_facecolor("#FFFFFF")
                ax.set_facecolor("#FAF7F2")

                colors = []
                for d in degrees:
                    if d == max_deg and max_deg > min_deg:
                        colors.append("#E86A2C")
                    elif d == min_deg and max_deg > min_deg:
                        colors.append("#16202A")
                    else:
                        colors.append("#F3E5D0")

                bars = ax.bar(node_labels, degrees, color=colors, edgecolor="#16202A", linewidth=1.2)
                for bar, d in zip(bars, degrees):
                    ax.text(
                        bar.get_x() + bar.get_width() / 2,
                        bar.get_height() + 0.06,
                        str(d),
                        ha="center", va="bottom", fontweight="bold", fontsize=9.5, color="#16202A"
                    )

                ax.set_title("Node Degrees Distribution", fontweight="bold", fontsize=12, color="#16202A")
                ax.set_xlabel("Nodes", fontweight="bold", color="#16202A")
                ax.set_ylabel("Degree", fontweight="bold", color="#16202A")
                ax.tick_params(colors="#16202A")
                ax.grid(axis="y", linestyle="--", alpha=0.35)
                plt.tight_layout()
                st.pyplot(fig, use_container_width=True)
                plt.close(fig)
                st.markdown("</div>", unsafe_allow_html=True)

            with c_right:
                st.markdown('<div class="panel-card">', unsafe_allow_html=True)
                st.subheader("📈 DEGREE STATISTICS")
                st.markdown("**Degree of Each Node:**")
                for lbl, d in zip(node_labels, degrees):
                    st.markdown(f"Node {lbl}: {d} connection(s)")

                st.markdown("<hr style='border-color:#EAE2D3;'>", unsafe_allow_html=True)
                avg_deg = float(np.mean(degrees)) if degrees else 0.0
                tot_deg = int(np.sum(degrees)) if degrees else 0

                s1, s2, s3, s4 = st.columns(4)
                s1.metric("Maximum Degree", max_deg)
                s2.metric("Minimum Degree", min_deg)
                s3.metric("Average Degree", f"{avg_deg:.2f}")
                s4.metric("Total Degree", tot_deg)

                st.markdown("<hr style='border-color:#EAE2D3;'>", unsafe_allow_html=True)
                st.subheader("📋 GRAPH PROPERTIES")
                is_conn = "Yes" if nx.is_connected(G) else "No"
                num_comp = nx.number_connected_components(G)
                gp1, gp2 = st.columns(2)
                gp1.markdown(f"**Is Connected:** {is_conn}")
                gp2.markdown(f"**Number of Components:** {num_comp}")
                st.markdown("</div>", unsafe_allow_html=True)

    # --- TAB 3 ---
    with tab3:
        p1, p2 = st.columns(2)
        with p1:
            st.markdown('<div class="top-pill-card"></div>', unsafe_allow_html=True)
        with p2:
            st.markdown('<div class="top-pill-card"></div>', unsafe_allow_html=True)

        G = st.session_state.graph
        if G is None:
            st.warning("Silakan buat graf terlebih dahulu di tab **GRAPH VISUALIZATION**.")
        else:
            c_left, c_right = st.columns([1.15, 1])
            labels = [str(n + 1) for n in G.nodes()]
            adj = nx.to_numpy_array(G, weight="weight", dtype=int)
            df_adj = pd.DataFrame(adj, index=labels, columns=labels)

            with c_left:
                st.markdown('<div class="panel-card">', unsafe_allow_html=True)
                st.subheader("🔢 ADJACENCY MATRIX")
                st.dataframe(df_adj, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

            with c_right:
                st.markdown('<div class="panel-card">', unsafe_allow_html=True)
                st.subheader("📊 MATRIX PROPERTIES")
                shape_val = adj.shape
                total_elem = int(adj.size)
                non_zero = int(np.count_nonzero(adj))
                density = non_zero / total_elem if total_elem > 0 else 0.0
                is_sym = bool(np.array_equal(adj, adj.T))
                trace_val = float(np.trace(adj))

                mp1, mp2 = st.columns(2)
                mp1.markdown(f"**Shape:** {shape_val}")
                mp1.markdown(f"**Total Elements:** {total_elem}")
                mp1.markdown(f"**Non-zero Elements:** {non_zero}")
                mp2.markdown(f"**Matrix Density:** {density:.3f}")
                mp2.markdown(f"**Symmetric:** {is_sym}")
                mp2.markdown(f"**Trace:** {trace_val:.1f}")

                st.markdown("<hr style='border-color:#EAE2D3;'>", unsafe_allow_html=True)
                st.subheader("🎨 MATRIX HEATMAP")
                fig_h, ax_h = plt.subplots(figsize=(6, 3.6))
                fig_h.patch.set_facecolor("#FFFFFF")
                im = ax_h.imshow(adj, cmap="Oranges")
                ax_h.set_xticks(range(len(labels)))
                ax_h.set_yticks(range(len(labels)))
                ax_h.set_xticklabels(labels, color="#16202A")
                ax_h.set_yticklabels(labels, color="#16202A")
                ax_h.set_title("Adjacency Matrix Heatmap", fontweight="bold", color="#16202A")
                fig_h.colorbar(im, ax=ax_h)
                plt.tight_layout()
                st.pyplot(fig_h, use_container_width=True)
                plt.close(fig_h)
                st.markdown("</div>", unsafe_allow_html=True)

# =====================================================================
# HALAMAN 3: JAVA ISLAND ROUTE PLANNER
# =====================================================================
elif page == "Java Route Finder":
    st.markdown("""
        <div class="orange-banner">
            <span style="font-weight:700; font-size:14px;">🗺️ Graph Matrix Pro • Java Island Route Planner</span>
            <span class="banner-pill">OSRM Road Routing • Alternative Paths</span>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<h1 style='color:#16202A;'>🗺️ JAVA ISLAND ROUTE PLANNER</h1>", unsafe_allow_html=True)
    st.markdown('<div class="orange-divider"></div>', unsafe_allow_html=True)

    p1, p2 = st.columns(2)
    with p1:
        st.markdown('<div class="top-pill-card"></div>', unsafe_allow_html=True)
    with p2:
        st.markdown('<div class="top-pill-card"></div>', unsafe_allow_html=True)

    col_ctrl, col_map = st.columns([1, 1.45])
    city_names = list(CITIES.keys())

    with col_ctrl:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        st.subheader("📍 SELECT YOUR ROUTE")
        origin = st.selectbox("🚗 Origin City", city_names, index=0)
        default_dest_idx = city_names.index("Surakarta (Solo)") if "Surakarta (Solo)" in city_names else 1
        destination = st.selectbox("🎯 Destination City", city_names, index=default_dest_idx)

        st.subheader("🛠️ Routing Options")
        use_osrm = st.checkbox("Use OSRM for accurate routing (recommended)", value=True)
        show_alt = st.checkbox("Show alternative routes", value=True)

        if st.button("🔍 FIND ROUTES"):
            if origin == destination:
                st.warning("Kota asal dan tujuan tidak boleh sama.")
            else:
                lat1, lon1 = CITIES[origin]
                lat2, lon2 = CITIES[destination]
                if use_osrm:
                    alt_str = "true" if show_alt else "false"
                    url = (
                        f"http://router.project-osrm.org/route/v1/driving/"
                        f"{lon1},{lat1};{lon2},{lat2}?overview=full&geometries=geojson&alternatives={alt_str}"
                    )
                    try:
                        res = requests.get(url, timeout=10).json()
                        routes_out = []
                        for idx, r in enumerate(res.get("routes", [])):
                            pts = [(c[1], c[0]) for c in r["geometry"]["coordinates"]]
                            routes_out.append({
                                "name": "Main Route" if idx == 0 else f"Alternative {idx}",
                                "points": pts,
                                "dist_km": r["distance"] / 1000,
                                "dur_hr": r["duration"] / 3600,
                                "is_main": idx == 0
                            })
                        st.session_state.route_data = {
                            "origin": origin,
                            "destination": destination,
                            "straight": False,
                            "routes": routes_out
                        }
                    except requests.RequestException:
                        st.error("Gagal terhubung ke server OSRM.")
                else:
                    st.session_state.route_data = {
                        "origin": origin,
                        "destination": destination,
                        "straight": True,
                        "routes": [{
                            "name": "Direct Line",
                            "points": [(lat1, lon1), (lat2, lon2)],
                            "dist_km": None,
                            "dur_hr": None,
                            "is_main": True
                        }]
                    }

        if st.session_state.route_data and not st.session_state.route_data["straight"]:
            for r in st.session_state.route_data["routes"]:
                if r["is_main"]:
                    st.success(f"**{r['name']}:** {r['dist_km']:.1f} km | ~{r['dur_hr']:.1f} jam")
                else:
                    st.info(f"**{r['name']}:** {r['dist_km']:.1f} km | ~{r['dur_hr']:.1f} jam")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_map:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        st.subheader("🗺️ INTERACTIVE JAVA MAP")
        m = folium.Map(location=[-7.35, 110.2], zoom_start=7, tiles="OpenStreetMap")

        for cname, (clat, clon) in CITIES.items():
            if cname == origin:
                folium.CircleMarker(
                    [clat, clon], radius=7.5, color="#15803D", fill=True, fill_color="#22C55E",
                    fill_opacity=0.95, tooltip=f"Start City: {cname}"
                ).add_to(m)
            elif cname == destination:
                folium.CircleMarker(
                    [clat, clon], radius=7.5, color="#B91C1C", fill=True, fill_color="#EF4444",
                    fill_opacity=0.95, tooltip=f"Destination: {cname}"
                ).add_to(m)
            else:
                folium.CircleMarker(
                    [clat, clon], radius=4.5, color="#16202A", fill=True, fill_color="#475569",
                    fill_opacity=0.85, tooltip=f"Other City: {cname}"
                ).add_to(m)

        rdata = st.session_state.route_data
        if rdata and rdata["origin"] == origin and rdata["destination"] == destination:
            all_pts = []
            for r in reversed(rdata["routes"]):
                all_pts.extend(r["points"])
                if r["is_main"]:
                    folium.PolyLine(
                        r["points"],
                        color="#E86A2C" if not rdata["straight"] else "#2563EB",
                        weight=5,
                        opacity=0.92,
                        tooltip=r["name"]
                    ).add_to(m)
                else:
                    folium.PolyLine(
                        r["points"],
                        color="#475569",
                        weight=3.5,
                        opacity=0.72,
                        dash_array="6",
                        tooltip=f"{r['name']} ({r['dist_km']:.1f} km)"
                    ).add_to(m)

            if all_pts:
                m.fit_bounds(all_pts, padding=(25, 25))

        st_folium(m, height=440, use_container_width=True, returned_objects=[])
        st.markdown("""
            <div class="legend-row">
                <b>Map Legend:</b> &nbsp;
                🟢 Start City &nbsp;|&nbsp;
                🔴 Destination &nbsp;|&nbsp;
                🔵 Route Stops &nbsp;|&nbsp;
                ⚫ Other Cities
            </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
<div class="footer">
    🌐 GRAPH MATRIX PRO - FINAL PROJECT © 2026 | COMPREHENSIVE GRAPH ANALYSIS & JAVA ROUTE PLANNING | DEVELOPED WITH STREAMLIT & NETWORKX
</div>
""", unsafe_allow_html=True)
