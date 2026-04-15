import os
import pandas as pd
import streamlit as st

# ── Configuration ─────────────────────────────────────────────────────────────
DATA_FILE = "bmtc_routes_with_stops.csv"
SEPARATOR = " -> "

# ── Theme Management ───────────────────────────────────────────────────────────
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

def toggle_theme():
    st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'
    st.rerun()

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SmartBus AI",
    page_icon="🚌",
    layout="centered",
)

# ── Minimal Theme Styling ─────────────────────────────────────────────────────
theme_colors = {
    'light': {
        'bg': '#ffffff',
        'text': '#1a1f2b',
        'card': '#f8f9fa',
        'border': '#dee2e6',
        'success': '#d4edda',
        'error': '#f8d7da'
    },
    'dark': {
        'bg': '#0c0f14',
        'text': '#e8eaf0',
        'card': '#1a1f2b',
        'border': '#252d3d',
        'success': '#1e3a2f',
        'error': '#3a1f23'
    }
}

current_theme = theme_colors[st.session_state.theme]

# Apply theme
st.markdown(f"""
<style>
    .stApp {{
        background-color: {current_theme['bg']};
        color: {current_theme['text']};
    }}
</style>
""", unsafe_allow_html=True)

# ── Data loading ──────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data(filepath: str) -> pd.DataFrame:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Data file not found: {filepath}")
    try:
        df = pd.read_excel(filepath)
    except Exception:
        df = pd.read_csv(filepath)
    df.columns = [c.strip() for c in df.columns]
    return df


# ── Core lookup ───────────────────────────────────────────────────────────────
def find_routes(df: pd.DataFrame, bus_number: str) -> list:
    query = bus_number.strip().upper()
    mask = df["Route"].astype(str).str.strip().str.upper() == query
    matches = df[mask]
    results = []
    for _, row in matches.iterrows():
        raw_stops = str(row["Stops (via)"]).strip()
        stops = [s.strip() for s in raw_stops.split(SEPARATOR) if s.strip()]
        results.append({
            "route": row["Route"],
            "stops": stops,
            "start": stops[0] if stops else "N/A",
            "destination": stops[-1] if stops else "N/A",
            "total": len(stops),
        })
    return results


# ── Header Section ────────────────────────────────────────────────────────────
# Prominent App Header with Theme Toggle
header_col1, header_col2 = st.columns([4, 1])
with header_col1:
    st.markdown(f"""
    <h1 style='margin-bottom: 0px; color: {current_theme["text"]};'>
        🚌 SmartBus AI
    </h1>
    <p style='margin-top: 5px; color: gray; font-size: 1.1rem;'>
        BMTC Route Finder · Bengaluru
    </p>
    """, unsafe_allow_html=True)

with header_col2:
    st.write("")  # Spacing
    theme_icon = "🌙 Dark" if st.session_state.theme == 'light' else "☀️ Light"
    if st.button(theme_icon, key="theme_toggle", use_container_width=True):
        toggle_theme()

st.divider()

# ── Hero Section ───────────────────────────────────────────────────────────────
st.subheader("Find your route, stop by stop.")
st.write("Enter a BMTC bus number to see the full route and all intermediate stops.")

# Load data
try:
    df = load_data(DATA_FILE)
    data_ok = True
except FileNotFoundError as e:
    st.error(f"⚠️ {e}")
    data_ok = False

# Search form
if data_ok:
    col1, col2 = st.columns([4, 1])
    with col1:
        bus_input = st.text_input(
            label="Bus number",
            placeholder="e.g. 242-LA, 500C, D35G-BVRH…",
            label_visibility="collapsed",
            key="bus_input",
        )
    with col2:
        search_clicked = st.button("Search", key="search_btn", use_container_width=True, type="primary")

    query = bus_input.strip()
    
    if not query:
        st.info("👆 Type a bus number above to view its route.")
    else:
        results = find_routes(df, query)

        if not results:
            st.error(f"❌ No route found for **{query.upper()}**. Check the bus number and try again.")
        else:
            st.success(f"Found {len(results)} route variant(s) for bus **{query.upper()}**")
            
            for idx, r in enumerate(results):
                # Route card
                with st.container(border=True):
                    # Header: Route number and metadata
                    c1, c2 = st.columns([3, 1])
                    with c1:
                        st.markdown(f"### 🚍 {r['route']}")
                    with c2:
                        if len(results) > 1:
                            st.caption(f"Variant {idx + 1} of {len(results)}")
                        st.markdown(f"**🚏 {r['total']} stops**")
                    
                    st.divider()
                    
                    # Quick Summary
                    sum_col1, sum_col2 = st.columns(2)
                    with sum_col1:
                        st.markdown("**Origin**")
                        st.markdown(f"🟢 {r['start']}")
                    with sum_col2:
                        st.markdown("**Destination**")
                        st.markdown(f"🔴 {r['destination']}")
                    
                    st.divider()
                    
                    # VERTICAL ROUTE FLOW
                    st.markdown("#### 🗺️ Route Flow")
                    
                    stops = r['stops']
                    total_stops = len(stops)
                    
                    for i, stop in enumerate(stops):
                        # Determine styling based on position
                        if i == 0:
                            # First stop: Green circle + location pin + bold + Start label
                            st.markdown(f"""
                            <div style='display: flex; align-items: center; gap: 8px; margin: 8px 0;'>
                                <span style='font-size: 1.2rem;'>🟢</span>
                                <span style='font-size: 1.2rem;'>📍</span>
                                <span style='font-weight: bold; font-size: 1.1rem;'>{stop}</span>
                                <span style='color: gray; font-size: 0.9rem; margin-left: 8px;'>(Start)</span>
                            </div>
                            """, unsafe_allow_html=True)
                        elif i == total_stops - 1:
                            # Last stop: Red circle + location pin + bold + End label
                            st.markdown(f"""
                            <div style='display: flex; align-items: center; gap: 8px; margin: 8px 0;'>
                                <span style='font-size: 1.2rem;'>🔴</span>
                                <span style='font-size: 1.2rem;'>📍</span>
                                <span style='font-weight: bold; font-size: 1.1rem;'>{stop}</span>
                                <span style='color: gray; font-size: 0.9rem; margin-left: 8px;'>(End)</span>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            # Middle stops: Location pin only
                            st.markdown(f"""
                            <div style='display: flex; align-items: center; gap: 8px; margin: 8px 0; padding-left: 4px;'>
                                <span style='font-size: 1.1rem;'>📍</span>
                                <span style='font-size: 1.05rem;'>{stop}</span>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Arrow down (between stops, not after last)
                        if i < total_stops - 1:
                            st.markdown("""
                            <div style='text-align: left; padding-left: 24px; color: gray; font-size: 1.2rem; margin: 4px 0;'>
                                ⬇️
                            </div>
                            """, unsafe_allow_html=True)
                
                st.write("")  # Spacing between cards
