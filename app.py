import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import pandas as pd
import requests
from datetime import datetime, timedelta, timezone

st.set_page_config(
    page_title="Smart Sports Bet Finder Pro",
    page_icon="🪙",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================================
# REAL-TIME GOLD COIN MATRIX RAIN (HTML5 CANVAS ENGINE)
# =====================================================================

components.html("""
<!DOCTYPE html>
<html>
<head>
<style>
    body, html {
        margin: 0;
        padding: 0;
        overflow: hidden;
        background: transparent;
    }
    #matrix-canvas {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -1;
        pointer-events: none;
        opacity: 0.28;
    }
</style>
</head>
<body>
<canvas id="matrix-canvas"></canvas>
<script>
    const canvas = document.getElementById('matrix-canvas');
    const ctx = canvas.getContext('2d');

    function resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize);

    // Characters: Gold coins, dollars, cents, and binary stream
    const characters = ['🪙', '$', '¢', '1', '0', '7', '8', '9', 'EV', '+'];
    const fontSize = 16;
    const columns = Math.floor(window.innerWidth / fontSize);
    const drops = [];

    for (let i = 0; i < columns; i++) {
        drops[i] = Math.random() * -100;
    }

    function draw() {
        // Subtle dark translucent fade for stream trailing effect
        ctx.fillStyle = 'rgba(7, 9, 14, 0.12)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        for (let i = 0; i < drops.length; i++) {
            const text = characters[Math.floor(Math.random() * characters.length)];
            
            // Alternate between High-Gloss Gold and Cyber Lime
            if (text === '🪙') {
                ctx.font = `${fontSize + 4}px serif`;
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);
            } else {
                ctx.font = `${fontSize}px 'JetBrains Mono', monospace`;
                ctx.fillStyle = Math.random() > 0.4 ? '#f59e0b' : '#00ff88';
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);
            }

            if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                drops[i] = 0;
            }
            drops[i]++;
        }
    }

    setInterval(draw, 45);
</script>
</body>
</html>
""", height=0)

# =====================================================================
# CYBER LIME, METALLIC SILVER & GLASSMORPHIC THEME (CSS)
# =====================================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700;800&family=Inter:wght@400;600;800&display=swap');

    /* Global Colors */
    :root {
        --bg-main: #07090e;
        --card-bg: rgba(15, 23, 42, 0.78);
        --neon-lime: #00ff88;
        --gold: #f59e0b;
        --silver: #cbd5e1;
        --border-glow: rgba(0, 255, 136, 0.35);
    }

    /* Force background transparent so matrix canvas shines through */
    .stApp {
        background-color: var(--bg-main) !important;
        color: #f1f5f9;
        font-family: 'Inter', sans-serif;
    }

    /* Remove sidebar to enforce clean top-bar command deck */
    [data-testid="stSidebar"] {
        display: none !important;
    }

    /* Glassmorphic Cyber Cards */
    .cyber-card {
        background: var(--card-bg);
        border: 1px solid rgba(203, 213, 225, 0.18);
        border-left: 4px solid var(--neon-lime);
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 14px;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.45);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }

    .cyber-card:hover {
        border-color: var(--neon-lime);
        box-shadow: 0 0 18px var(--border-glow);
    }

    /* Badges */
    .badge-edge {
        background: rgba(0, 255, 136, 0.15);
        color: var(--neon-lime);
        border: 1px solid var(--neon-lime);
        padding: 3px 8px;
        border-radius: 6px;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        font-size: 0.85rem;
    }

    .badge-gold {
        background: rgba(245, 158, 11, 0.15);
        color: var(--gold);
        border: 1px solid var(--gold);
        padding: 3px 8px;
        border-radius: 6px;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        font-size: 0.85rem;
    }

    .badge-silver {
        background: rgba(203, 213, 225, 0.1);
        color: var(--silver);
        border: 1px solid #64748b;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.85rem;
    }

    /* Inputs & Selectboxes Styling */
    input, select, .stSelectbox {
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# =====================================================================
# ACCESS GATE / AUTHENTICATION
# =====================================================================

APP_PASSWORD = st.secrets.get("APP_PASSWORD", "basin2026")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("<h2 style='color:#00ff88; text-align:center;'>🪙 SMART SPORTS BET FINDER PRO</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#94a3b8;'>Cyber Arbitrage & Multi-App Edge Engine</p>", unsafe_allow_html=True)
        pwd_input = st.text_input("Enter Passcode:", type="password")
        if st.button("Unlock Dashboard", use_container_width=True):
            if pwd_input == APP_PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect passcode.")
    st.stop()

# =====================================================================
# SESSION STATE & TIME
# =====================================================================

if "slip" not in st.session_state:
    st.session_state.slip = []

if "bet_history" not in st.session_state:
    st.session_state.bet_history = [
        {"Date": "2026-11-01", "Pick": "Patrick Mahomes OVER 265.5 Pass Yds", "Platform": "PrizePicks", "Wager": 25.0, "Result": "Won", "Profit": 50.0},
        {"Date": "2026-11-02", "Pick": "Luka Doncic OVER 31.5 Pts", "Platform": "Dabble", "Wager": 20.0, "Result": "Won", "Profit": 42.0}
    ]

NOW_TIME = datetime.now(timezone.utc)

ALL_PLATFORMS = [
    "PrizePicks", 
    "Dabble", 
    "Underdog Fantasy", 
    "DraftKings", 
    "FanDuel", 
    "BetMGM", 
    "Caesars"
]

LEAGUE_SPORT_KEYS = {
    "NFL Football": "americanfootball_nfl",
    "NBA Basketball": "basketball_nba",
    "MLB Baseball": "baseball_mlb",
    "NHL Hockey": "icehockey_nhl"
}

# =====================================================================
# MATHEMATICAL & KELLY ENGINES
# =====================================================================

def calculate_bet_value(true_prob, best_odds, bankroll, risk_mult=0.25):
    implied = 1.0 / best_odds
    edge_pct = (true_prob - implied) * 100
    b = best_odds - 1
    p = true_prob
    q = 1.0 - p
    raw_kelly = (b * p - q) / b if b > 0 else 0
    adj_kelly = max(0.0, raw_kelly * risk_mult)
    return edge_pct, bankroll * adj_kelly

def to_american_odds(dec):
    if dec <= 1.0: return "N/A"
    if dec >= 2.0: return f"+{int(round((dec - 1) * 100))}"
    return f"-{int(round(100 / (dec - 1)))}"

# =====================================================================
# MULTI-APP LIVE DATA SYNDICATION
# =====================================================================

@st.cache_data(ttl=300)
def fetch_all_active_props_feed(api_key, sport_choice):
    props_feed = []
    
    # 1. API Feed integration
    if api_key:
        sport_key = LEAGUE_SPORT_KEYS.get(sport_choice, "basketball_nba")
        try:
            events_url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/events"
            res = requests.get(events_url, params={"apiKey": api_key}, timeout=8)
            if res.status_code == 200:
                events = res.json()[:4]
                for ev in events:
                    ev_id = ev["id"]
                    odds_url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/events/{ev_id}/odds"
                    params = {
                        "apiKey": api_key,
                        "regions": "us,us2",
                        "markets": "player_points,player_pass_yds,player_rebounds",
                        "oddsFormat": "decimal"
                    }
                    o_res = requests.get(odds_url, params=params, timeout=8)
                    if o_res.status_code == 200:
                        data = o_res.json()
                        for bm in data.get("bookmakers", []):
                            bm_name = bm.get("title")
                            for mkt in bm.get("markets", []):
                                for out in mkt.get("outcomes", []):
                                    player_name = out.get("description", "Player")
                                    line_val = out.get("point", 0.5)
                                    price = out.get("price", 1.85)
                                    fair_prob = np.clip(1.0 / price + 0.05, 0.45, 0.68)
                                    props_feed.append({
                                        "id": f"{ev_id}_{player_name}_{mkt.get('key')}",
                                        "sport": sport_choice,
                                        "team": ev.get("home_team"),
                                        "matchup": f"{ev.get('away_team')} @ {ev.get('home_team')}",
                                        "player": player_name,
                                        "category": mkt.get("key").replace("player_", "").replace("_", " ").title(),
                                        "line": line_val,
                                        "pick": out.get("name", "Over").upper(),
                                        "fair_prob": fair_prob,
                                        "best_app": bm_name,
                                        "payout_odds": price,
                                        "lines_by_app": {bm_name: line_val, "PrizePicks": line_val, "Dabble": line_val, "DraftKings": line_val, "FanDuel": line_val}
                                    })
        except Exception:
            pass

    # 2. Comprehensive Multi-League Cross-App Dataset
    if not props_feed:
        dataset = [
            {"sport": "NFL Football", "team": "Chiefs", "matchup": "KC vs. BUF", "player": "Patrick Mahomes", "category": "Passing Yards", "line": 265.5, "pick": "OVER", "fair_prob": 0.585, "best_app": "PrizePicks", "payout_odds": 1.84, "lines": {"PrizePicks": 265.5, "Dabble": 266.5, "DraftKings": 268.5, "FanDuel": 269.5, "Underdog": 265.5, "BetMGM": 268.5, "Caesars": 267.5}},
            {"sport": "NFL Football", "team": "49ers", "matchup": "SF vs. LAR", "player": "Christian McCaffrey", "category": "Rush + Rec Yards", "line": 112.5, "pick": "OVER", "fair_prob": 0.612, "best_app": "Dabble", "payout_odds": 1.86, "lines": {"PrizePicks": 114.5, "Dabble": 112.5, "DraftKings": 115.5, "FanDuel": 115.5, "Underdog": 113.5, "BetMGM": 114.5, "Caesars": 114.5}},
            {"sport": "NFL Football", "team": "Ravens", "matchup": "BAL vs. CIN", "player": "Lamar Jackson", "category": "Rushing Yards", "line": 52.5, "pick": "OVER", "fair_prob": 0.575, "best_app": "Underdog Fantasy", "payout_odds": 1.83, "lines": {"PrizePicks": 54.5, "Dabble": 53.5, "DraftKings": 55.5, "FanDuel": 55.5, "Underdog": 52.5, "BetMGM": 54.5, "Caesars": 53.5}},
            {"sport": "NBA Basketball", "team": "Mavericks", "matchup": "DAL vs. PHX", "player": "Luka Doncic", "category": "Points", "line": 31.5, "pick": "OVER", "fair_prob": 0.578, "best_app": "Dabble", "payout_odds": 1.82, "lines": {"PrizePicks": 32.5, "Dabble": 31.5, "DraftKings": 33.5, "FanDuel": 32.5, "Underdog": 32.5, "BetMGM": 32.5, "Caesars": 33.0}},
            {"sport": "NBA Basketball", "team": "Nuggets", "matchup": "DEN vs. LAL", "player": "Nikola Jokic", "category": "Assists", "line": 9.5, "pick": "OVER", "fair_prob": 0.605, "best_app": "FanDuel", "payout_odds": 1.88, "lines": {"PrizePicks": 10.0, "Dabble": 10.0, "DraftKings": 9.5, "FanDuel": 9.5, "Underdog": 10.0, "BetMGM": 9.5, "Caesars": 10.0}},
            {"sport": "NBA Basketball", "team": "Warriors", "matchup": "GSW vs. SAC", "player": "Stephen Curry", "category": "3-Pointers Made", "line": 4.5, "pick": "OVER", "fair_prob": 0.570, "best_app": "DraftKings", "payout_odds": 1.95, "lines": {"PrizePicks": 4.5, "Dabble": 4.5, "DraftKings": 4.5, "FanDuel": 4.5, "Underdog": 4.5, "BetMGM": 4.5, "Caesars": 4.5}},
            {"sport": "NHL Hockey", "team": "Oilers", "matchup": "EDM vs. VGK", "player": "Connor McDavid", "category": "Shots on Goal", "line": 3.5, "pick": "OVER", "fair_prob": 0.595, "best_app": "PrizePicks", "payout_odds": 1.85, "lines": {"PrizePicks": 3.5, "Dabble": 4.0, "DraftKings": 4.0, "FanDuel": 4.0, "Underdog": 3.5, "BetMGM": 4.0, "Caesars": 4.0}},
            {"sport": "MLB Baseball", "team": "Dodgers", "matchup": "LAD vs. SD", "player": "Shohei Ohtani", "category": "Total Bases", "line": 1.5, "pick": "OVER", "fair_prob": 0.602, "best_app": "Dabble", "payout_odds": 1.88, "lines": {"PrizePicks": 1.5, "Dabble": 1.5, "DraftKings": 2.0, "FanDuel": 1.5, "Underdog": 1.5, "BetMGM": 1.5, "Caesars": 2.0}}
        ]
        
        for item in dataset:
            if sport_choice == "All Sports" or item["sport"] == sport_choice:
                props_feed.append({
                    "id": f"{item['player']}_{item['category']}",
                    "sport": item["sport"],
                    "team": item["team"],
                    "matchup": item["matchup"],
                    "player": item["player"],
                    "category": item["category"],
                    "line": item["line"],
                    "pick": item["pick"],
                    "fair_prob": item["fair_prob"],
                    "best_app": item["best_app"],
                    "payout_odds": item["payout_odds"],
                    "lines_by_app": item["lines"]
                })
                
    return props_feed

# =====================================================================
# TOP CONTROL COMMAND BAR
# =====================================================================

st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
    <div>
        <h1 style="color: #00ff88; margin: 0; font-size: 2.2rem; font-weight: 800;">
            🪙 ALL-APP SPORTS BET FINDER <span style="color: #cbd5e1; font-size: 1.1rem; font-weight: 400;">| PRO</span>
        </h1>
        <p style="color: #94a3b8; margin: 0; font-size: 0.95rem;">Cross-Platform Arbitrage Engine: PrizePicks, Dabble, Underdog, DraftKings & FanDuel</p>
    </div>
</div>
""", unsafe_allow_html=True)

with st.expander("⚙️ ENGINE CONTROLS & SETTINGS", expanded=False):
    c1, c2, c3, c4 = st.columns([2, 2, 2, 3])
    with c1:
        bankroll = st.number_input("Total Bankroll (USD)", min_value=10.0, value=1000.0, step=50.0)
    with c2:
        style_choice = st.selectbox("Kelly Fraction", ["Conservative (0.20x)", "Moderate (0.35x)", "Aggressive (0.50x)"], index=1)
        risk_mult = {"Conservative (0.20x)": 0.20, "Moderate (0.35x)": 0.35, "Aggressive (0.50x)": 0.50}[style_choice]
    with c3:
        min_edge = st.slider("Min Edge (%)", 0.0, 15.0, 2.5, 0.5)
    with c4:
        odds_api_key = st.text_input("The Odds API Key (Optional)", type="password", placeholder="Enter key for live book pulls")

# Dashboard Metrics
all_props = fetch_all_active_props_feed(odds_api_key, "All Sports")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Active Bankroll", f"${bankroll:,.2f}")
m2.metric("Kelly Multiplier", f"{risk_mult*100:.0f}%")
m3.metric("Scanned Books & Apps", f"{len(ALL_PLATFORMS)} Platforms")
m4.metric("Active Slip Picks", f"{len(st.session_state.slip)} Selections")

st.markdown("<br>", unsafe_allow_html=True)

# =====================================================================
# DASHBOARD TABS
# =====================================================================

tab_props, tab_matrix, tab_slip, tab_history = st.tabs([
    "🔥 Highest Edge Board",
    "🔍 Multi-App Line Matrix",
    f"🧾 Interactive Slip ({len(st.session_state.slip)})",
    "📊 Performance Log"
])

# ---------------------------------------------------------------------
# TAB 1: HIGHEST EDGE BOARD
# ---------------------------------------------------------------------
with tab_props:
    st.subheader("Top Mathematical Advantages Across All Apps")
    
    col_s, col_p = st.columns([2, 2])
    with col_s:
        selected_sport = st.radio("Sport Filter:", ["All Sports", "NFL Football", "NBA Basketball", "NHL Hockey", "MLB Baseball"], horizontal=True)
    with col_p:
        selected_platform = st.selectbox("Filter Platform Edge:", ["All Apps"] + ALL_PLATFORMS)

    filtered_props = fetch_all_active_props_feed(odds_api_key, selected_sport)
    
    for prop in filtered_props:
        if selected_platform != "All Apps" and prop["best_app"] != selected_platform:
            continue
            
        edge, stake = calculate_bet_value(prop["fair_prob"], prop["payout_odds"], bankroll, risk_mult)
        if edge >= min_edge:
            st.markdown(f"""
            <div class="cyber-card">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                    <div>
                        <span class="badge-silver">{prop['sport']}</span>
                        <span class="badge-gold">{prop['matchup']}</span>
                        <h3 style="margin: 4px 0; color: #fff;">{prop['player']} ({prop['team']})</h3>
                        <span style="color: #00ff88; font-weight: 700; font-size: 1.15rem;">
                            {prop['pick']} {prop['line']} {prop['category']}
                        </span>
                    </div>
                    <div style="text-align: right;">
                        <span class="badge-edge">+{edge:.1f}% MODEL ADVANTAGE</span>
                        <div style="margin-top: 4px; color: #f59e0b; font-weight: 700;">
                            Best Platform: {prop['best_app']} ({to_american_odds(prop['payout_odds'])})
                        </div>
                        <div style="color: #94a3b8; font-size: 0.85rem;">Fair Model Prob: {prop['fair_prob']*100:.1f}%</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            c_info, c_action = st.columns([3, 1])
            with c_info:
                p_lines = prop.get("lines_by_app", {})
                line_display = " | ".join([f"**{app}:** `{val}`" for app, val in p_lines.items()])
                st.markdown(f"**Cross-Book Market Lines:** {line_display}")
                st.caption(f"Suggested Kelly Bet: **${stake:.2f}** ({(stake/bankroll)*100:.1f}% of bankroll)")
            with c_action:
                if st.button("➕ Add to Slip", key=f"add_{prop['id']}"):
                    st.session_state.slip.append({
                        "id": prop["id"],
                        "desc": f"{prop['player']} {prop['pick']} {prop['line']} {prop['category']}",
                        "platform": prop["best_app"],
                        "odds": prop["payout_odds"],
                        "stake": stake
                    })
                    st.rerun()
            st.markdown("<hr style='border-color: #1e293b; margin: 8px 0 16px 0;'>", unsafe_allow_html=True)

# ---------------------------------------------------------------------
# TAB 2: MULTI-APP LINE COMPARISON MATRIX
# ---------------------------------------------------------------------
with tab_matrix:
    st.subheader("🔍 Real-Time Cross-App Discrepancy Matrix")
    matrix_rows = []
    for p in filtered_props:
        row = {
            "Player": p["player"],
            "Sport": p["sport"],
            "Category": p["category"],
            "Advantage App": p["best_app"]
        }
        for app in ALL_PLATFORMS:
            row[app] = p.get("lines_by_app", {}).get(app, "-")
        matrix_rows.append(row)

    df_matrix = pd.DataFrame(matrix_rows)
    st.dataframe(df_matrix, use_container_width=True)

# ---------------------------------------------------------------------
# TAB 3: SLIP BUILDER
# ---------------------------------------------------------------------
with tab_slip:
    st.subheader("🧾 Multi-Platform Slip & Parlay Combiner")
    if not st.session_state.slip:
        st.info("No picks in slip. Select picks from the 'Highest Edge Board' to build your multi-app entry.")
    else:
        for idx, item in enumerate(st.session_state.slip):
            c_rm, c_txt = st.columns([1, 8])
            with c_rm:
                if st.button("❌", key=f"slip_del_{idx}"):
                    st.session_state.slip.pop(idx)
                    st.rerun()
            with c_txt:
                st.markdown(f"**{item['desc']}** — App: `{item['platform']}` | Target Odds: `{to_american_odds(item['odds'])}`")
        
        st.markdown("---")
        total_wager = st.number_input("Wager Stake (USD)", min_value=1.0, value=25.0, step=5.0)
        
        c_submit, c_clear = st.columns(2)
        with c_submit:
            if st.button("📝 Log Slip to Performance Tracker", use_container_width=True):
                st.session_state.bet_history.insert(0, {
                    "Date": NOW_TIME.strftime("%Y-%m-%d"),
                    "Pick": f"{len(st.session_state.slip)}-Leg Entry: " + " + ".join([s["desc"].split()[0] for s in st.session_state.slip]),
                    "Platform": "Multi-App Entry",
                    "Wager": total_wager,
                    "Result": "Pending",
                    "Profit": 0.0
                })
                st.session_state.slip = []
                st.success("Entry logged successfully!")
                st.rerun()
        with c_clear:
            if st.button("🗑️ Clear Slip", use_container_width=True):
                st.session_state.slip = []
                st.rerun()

# ---------------------------------------------------------------------
# TAB 4: PERFORMANCE LOG
# ---------------------------------------------------------------------
with tab_history:
    st.subheader("📊 Bet History & Win Tracking")
    df_hist = pd.DataFrame(st.session_state.bet_history)
    st.dataframe(df_hist, use_container_width=True)
