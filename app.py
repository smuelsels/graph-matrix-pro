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
            "photo": "https://via.placeholder.com/220x260.png?text=Meysya",
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
            "photo": "https://via.placeholder.com/220x260.png?text=Abdi",
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
                st.image(member["photo"], width=185)

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

    st.markdown("<hr style='border-color:#D5CBB8; margin:32px 0 20px 0;'>", unsafe_allow_html=True)
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
elif page == "Graph Matrix App":
    st.markdown("<h1>📊 GRAPH MATRIX APPLICATION</h1>", unsafe_allow_html=True)
    st.markdown('<div class="orange-divider"></div>', unsafe_allow_html=True)
    st.write("This application demonstrates graph theory concepts including graph visualization, node degree calculation, and adjacency matrix representation.")

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
                # Beri bobot acak untuk variasi matriks jika diinginkan
                for u, v in G.edges():
                    G[u][v]["weight"] = int(np.random.randint(1, 20))
                st.session_state.graph = G

        with col_right:
            st.subheader("👁️ GRAPH VISUALIZATION")
            G = st.session_state.graph
            if G is None:
                st.info("👆 Please generate a random graph using the controls on the left to see the visualization here.")
            else:
                fig, ax = plt.subplots(figsize=(6.5, 4.2))
                fig.patch.set_facecolor("#FAF4E6")
                ax.set_facecolor("#FAF4E6")
                pos = nx.spring_layout(G, seed=42)
                labels = {n: str(n + 1) for n in G.nodes()}
                nx.draw(
                    G, pos,
                    labels=labels,
                    with_labels=True,
                    node_color="#FF7A2F",
                    node_size=750,
                    font_color="white",
                    font_weight="bold",
                    edge_color="#444444",
                    width=1.8,
                    ax=ax
                )
                plt.tight_layout()
                st.pyplot(fig, use_container_width=True)
                plt.close(fig)

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
                st.subheader("📊 NODE DEGREES CALCULATION")
                fig, ax = plt.subplots(figsize=(6.5, 4.4))
                fig.patch.set_facecolor("#FAF4E6")
                ax.set_facecolor("#FAF4E6")

                colors = []
                for d in degrees:
                    if d == max_deg and max_deg > min_deg:
                        colors.append("#FF6A1A")
                    elif d == min_deg and max_deg > min_deg:
                        colors.append("#1E1E1E")
                    else:
                        colors.append("#F3E5C8")

                bars = ax.bar(node_labels, degrees, color=colors, edgecolor="#1E1E1E", linewidth=1.2)
                for bar, d in zip(bars, degrees):
                    ax.text(
                        bar.get_x() + bar.get_width() / 2,
                        bar.get_height() + 0.06,
                        str(d),
                        ha="center", va="bottom", fontweight="bold", fontsize=9.5, color="#1E1E1E"
                    )

                ax.set_title("Node Degrees Distribution", fontweight="bold", fontsize=12)
                ax.set_xlabel("Nodes", fontweight="bold")
                ax.set_ylabel("Degree", fontweight="bold")
                ax.grid(axis="y", linestyle="--", alpha=0.35)
                plt.tight_layout()
                st.pyplot(fig, use_container_width=True)
                plt.close(fig)

            with c_right:
                st.subheader("📈 DEGREE STATISTICS")
                st.markdown("**Degree of Each Node:**")
                for lbl, d in zip(node_labels, degrees):
                    st.markdown(f"Node {lbl}: {d} connection(s)")

                st.markdown("<hr style='border-color:#D5CBB8;'>", unsafe_allow_html=True)
                avg_deg = float(np.mean(degrees)) if degrees else 0.0
                tot_deg = int(np.sum(degrees)) if degrees else 0

                s1, s2, s3, s4 = st.columns(4)
                s1.metric("Maximum Degree", max_deg)
                s2.metric("Minimum Degree", min_deg)
                s3.metric("Average Degree", f"{avg_deg:.2f}")
                s4.metric("Total Degree", tot_deg)

                st.markdown("<hr style='border-color:#D5CBB8;'>", unsafe_allow_html=True)
                st.subheader("📋 GRAPH PROPERTIES")
                is_conn = "Yes" if nx.is_connected(G) else "No"
                num_comp = nx.number_connected_components(G)
                gp1, gp2 = st.columns(2)
                gp1.markdown(f"**Is Connected:** {is_conn}")
                gp2.markdown(f"**Number of Components:** {num_comp}")

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
                st.subheader("🔢 ADJACENCY MATRIX")
                st.dataframe(df_adj, use_container_width=True)

            with c_right:
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

                st.markdown("<hr style='border-color:#D5CBB8;'>", unsafe_allow_html=True)
                st.subheader("🎨 MATRIX HEATMAP")
                fig_h, ax_h = plt.subplots(figsize=(6, 3.6))
                fig_h.patch.set_facecolor("#FAF4E6")
                im = ax_h.imshow(adj, cmap="Oranges")
                ax_h.set_xticks(range(len(labels)))
                ax_h.set_yticks(range(len(labels)))
                ax_h.set_xticklabels(labels)
                ax_h.set_yticklabels(labels)
                ax_h.set_title("Adjacency Matrix Heatmap", fontweight="bold")
                fig_h.colorbar(im, ax=ax_h)
                plt.tight_layout()
                st.pyplot(fig_h, use_container_width=True)
                plt.close(fig_h)

File "/mount/src/graph-matrix-pro/app.py", line 656
  st.markdown("""
             ^
SyntaxError: '(' was never closed
