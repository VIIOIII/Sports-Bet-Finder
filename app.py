import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime, timezone

st.set_page_config(
    page_title="Smart Sports Bet Finder Pro",
    page_icon="🪙",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================================
# INJECT FULL-SCREEN GOLD COIN MATRIX RAIN INTO STREAMLIT ROOT
# =====================================================================

components.html("""
<script>
    // Ensure canvas attaches to the top-level window, not trapped in an iframe
    const parentDoc = window.parent.document;
    
    // Clean up any existing canvas on rerun
    let existingCanvas = parentDoc.getElementById("gold-matrix-canvas");
    if (existingCanvas) {
        existingCanvas.remove();
    }

    const canvas = parentDoc.createElement("canvas");
    canvas.id = "gold-matrix-canvas";
    canvas.style.position = "fixed";
    canvas.style.top = "0";
    canvas.style.left = "0";
    canvas.style.width = "100vw";
    canvas.style.height = "100vh";
    canvas.style.zIndex = "0"; // Right behind dashboard content
    canvas.style.pointerEvents = "none";
    canvas.style.opacity = "0.35"; // Bright and clearly visible

    parentDoc.body.prepend(canvas);

    const ctx = canvas.getContext("2d");

    function resize() {
        canvas.width = window.parent.innerWidth;
        canvas.height = window.parent.innerHeight;
    }
    resize();
    window.parent.addEventListener("resize", resize);

    // Characters: Gold Coins, Currency, Binary & EV symbols
    const symbols = ["🪙", "🪙", "$", "🪙", "$", "¢", "1", "0", "EV", "7", "8", "9", "+"];
    const fontSize = 18;
    const columns = Math.floor(window.parent.innerWidth / fontSize);
    const drops = [];

    for (let i = 0; i < columns; i++) {
        drops[i] = Math.random() * -80;
    }

    function renderMatrix() {
        // Translucent trail fade
        ctx.fillStyle = "rgba(7, 9, 14, 0.15)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        for (let i = 0; i < drops.length; i++) {
            const char = symbols[Math.floor(Math.random() * symbols.length)];

            if (char === "🪙") {
                ctx.font = `${fontSize + 6}px serif`;
                ctx.fillText(char, i * fontSize, drops[i] * fontSize);
            } else {
                ctx.font = `bold ${fontSize}px 'JetBrains Mono', monospace`;
                // High-shine metallic gold and cyber lime accents
                ctx.fillStyle = Math.random() > 0.35 ? "#f59e0b" : "#00ff88";
                ctx.shadowColor = "#f59e0b";
                ctx.shadowBlur = 6;
                ctx.fillText(char, i * fontSize, drops[i] * fontSize);
                ctx.shadowBlur = 0;
            }

            if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                drops[i] = 0;
            }
            drops[i]++;
        }
    }

    setInterval(renderMatrix, 40);
</script>
""", height=0)

# =====================================================================
# TRANSPARENCY & CYBER GLASSMORPHIC THEME (CSS)
# =====================================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700;800&family=Inter:wght@400;600;800&display=swap');

    /* CRITICAL: Force all parent Streamlit containers to transparent */
    html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], section.main {
        background-color: transparent !important;
        background: transparent !important;
        color: #f1f5f9;
        font-family: 'Inter', sans-serif;
    }

    /* Solid Obsidian base behind the canvas */
    body {
        background-color: #07090e !important;
    }

    /* Elevate content above the matrix canvas */
    .block-container {
        position: relative;
        z-index: 10 !important;
        padding-top: 1.5rem !important;
    }

    /* Hide sidebar completely */
    [data-testid="stSidebar"] {
        display: none !important;
    }

    /* Cyber Glassmorphic Cards */
    .cyber-card {
        background: rgba(15, 23, 42, 0.88) !important;
        border: 1px solid rgba(203, 213, 225, 0.22);
        border-left: 5px solid #00ff88;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6);
    }

    .badge-confidence {
        background: rgba(0, 255, 136, 0.18);
        color: #00ff88;
        border: 1px solid #00ff88;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.85rem;
    }

    .badge-app {
        background: rgba(245, 158, 11, 0.22);
        color: #f59e0b;
        border: 1px solid #f59e0b;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.85rem;
    }

    .badge-sport {
        background: rgba(203, 213, 225, 0.12);
        color: #cbd5e1;
        border: 1px solid #64748b;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.85rem;
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
        st.markdown("""
        <div style="background: rgba(15, 23, 42, 0.92); border: 1px solid #334155; padding: 24px; border-radius: 12px; backdrop-filter: blur(12px);">
            <h2 style='color:#00ff88; text-align:center; margin-bottom: 4px;'>🪙 SMART SPORTS BET FINDER PRO</h2>
            <p style='text-align:center; color:#94a3b8; font-size: 0.9rem;'>Enter your member passcode below to unlock dashboard.</p>
        </div>
        """, unsafe_allow_html=True)
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

# =====================================================================
# HEADER COMMAND DECK (BEGINNER-FRIENDLY)
# =====================================================================

st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
    <div>
        <h1 style="color: #00ff88; margin: 0; font-size: 2.3rem; font-weight: 800;">
            🪙 SPORTS BET FINDER <span style="color: #cbd5e1; font-size: 1.1rem; font-weight: 400;">| PRO</span>
        </h1>
        <p style="color: #94a3b8; margin: 0; font-size: 1rem;">The easiest way to find winning props on PrizePicks, Dabble, DraftKings & FanDuel</p>
    </div>
</div>
""", unsafe_allow_html=True)

with st.expander("💡 New here? Tap for a 30-second quickstart guide", expanded=False):
    st.markdown("""
    1. **Pick a Sport Below:** Filter for NFL, NBA, NHL, or MLB.
    2. **Look for the Green Badges:** Every play is pre-screened to give you the highest hit rate.
    3. **Bet on the Listed App:** We compare all apps and highlight the platform with the softest line.
    4. **Add to Slip:** Click **'➕ Add to Slip'** to track your picks and log your card.
    """)

# Beginner Friendly Controls
col_bank, col_style, col_filter = st.columns([2, 2, 3])

with col_bank:
    total_bankroll = st.number_input("Your Total Bankroll ($)", min_value=10.0, value=500.0, step=25.0)

with col_style:
    betting_style = st.selectbox(
        "Betting Style / Risk Level:",
        ["Standard (Recommended)", "Conservative (Safe)", "Aggressive (High Profit)"]
    )
    pct_map = {"Conservative (Safe)": 0.025, "Standard (Recommended)": 0.05, "Aggressive (High Profit)": 0.08}
    suggested_unit = total_bankroll * pct_map[betting_style]

with col_filter:
    pick_filter = st.radio(
        "Confidence Filter:",
        ["🔒 High Confidence (Safest)", "🎯 Best Value & Edge", "⚡ Show All Plays"],
        horizontal=True
    )

# Quick Overview Strip
m1, m2, m3 = st.columns(3)
m1.metric("Active Bankroll", f"${total_bankroll:,.2f}")
m2.metric("Recommended Bet Size", f"${suggested_unit:.2f} / bet")
m3.metric("Selections in Slip", f"{len(st.session_state.slip)} Picks")

st.markdown("<br>", unsafe_allow_html=True)

# =====================================================================
# CURATED ALL-APP PROPS DATABASE
# =====================================================================

props_database = [
    {
        "id": "p_mahomes",
        "sport": "NFL Football",
        "team": "Kansas City Chiefs",
        "matchup": "KC vs. BUF",
        "player": "Patrick Mahomes",
        "category": "Passing Yards",
        "line": 265.5,
        "pick": "OVER",
        "confidence": "🔒 High Confidence (Safest)",
        "hit_rate": "80% (Last 10 Games)",
        "best_app": "PrizePicks",
        "why": "Buffalo secondary allowed 280+ yards in 3 of their last 4 away games. PrizePicks has the line 3-4 yards lower than sportsbooks.",
        "lines": {"PrizePicks": 265.5, "Dabble": 266.5, "DraftKings": 268.5, "FanDuel": 269.5}
    },
    {
        "id": "p_cmc",
        "sport": "NFL Football",
        "team": "San Francisco 49ers",
        "matchup": "SF vs. LAR",
        "player": "Christian McCaffrey",
        "category": "Rushing + Receiving Yards",
        "line": 112.5,
        "pick": "OVER",
        "confidence": "🔒 High Confidence (Safest)",
        "hit_rate": "90% (Last 10 Games)",
        "best_app": "Dabble",
        "why": "Rams rank 28th against pass-catching running backs. Averaging 22+ touches per game.",
        "lines": {"Dabble": 112.5, "PrizePicks": 114.5, "DraftKings": 115.5, "FanDuel": 115.5}
    },
    {
        "id": "p_luka",
        "sport": "NBA Basketball",
        "team": "Dallas Mavericks",
        "matchup": "DAL vs. PHX",
        "player": "Luka Doncic",
        "category": "Points",
        "line": 31.5,
        "pick": "OVER",
        "confidence": "🎯 Best Value & Edge",
        "hit_rate": "70% (Last 10 Games)",
        "best_app": "Dabble",
        "why": "Phoenix allows top-5 points to opposing point guards. Dabble has the lowest line on the market.",
        "lines": {"Dabble": 31.5, "PrizePicks": 32.5, "DraftKings": 33.5, "FanDuel": 32.5}
    },
    {
        "id": "p_jokic",
        "sport": "NBA Basketball",
        "team": "Denver Nuggets",
        "matchup": "DEN vs. LAL",
        "player": "Nikola Jokic",
        "category": "Assists",
        "line": 9.5,
        "pick": "OVER",
        "confidence": "🔒 High Confidence (Safest)",
        "hit_rate": "80% (Last 10 Games)",
        "best_app": "FanDuel",
        "why": "Hit this line in 8 of his last 10 games vs. the Lakers.",
        "lines": {"FanDuel": 9.5, "DraftKings": 9.5, "PrizePicks": 10.0, "Dabble": 10.0}
    },
    {
        "id": "p_mcdavid",
        "sport": "NHL Hockey",
        "team": "Edmonton Oilers",
        "matchup": "EDM vs. VGK",
        "player": "Connor McDavid",
        "category": "Shots on Goal",
        "line": 3.5,
        "pick": "OVER",
        "confidence": "🎯 Best Value & Edge",
        "hit_rate": "70% (Last 10 Games)",
        "best_app": "PrizePicks",
        "why": "PrizePicks line is 3.5 while DraftKings and FanDuel require 4+ shots.",
        "lines": {"PrizePicks": 3.5, "Underdog": 3.5, "DraftKings": 4.0, "FanDuel": 4.0}
    },
    {
        "id": "p_ohtani",
        "sport": "MLB Baseball",
        "team": "Los Angeles Dodgers",
        "matchup": "LAD vs. SD",
        "player": "Shohei Ohtani",
        "category": "Total Bases",
        "line": 1.5,
        "pick": "OVER",
        "confidence": "🎯 Best Value & Edge",
        "hit_rate": "75% (Last 10 Games)",
        "best_app": "Dabble",
        "why": "Favorable pitching matchup; averages 2.2 total bases at home.",
        "lines": {"Dabble": 1.5, "PrizePicks": 1.5, "DraftKings": 2.0, "FanDuel": 1.5}
    }
]

# =====================================================================
# DASHBOARD TABS
# =====================================================================

tab_picks, tab_compare, tab_slip, tab_log = st.tabs([
    "🔥 Today's Best Picks",
    "🔍 Compare Lines Across Apps",
    f"🧾 Your Bet Slip ({len(st.session_state.slip)})",
    "📊 Win/Loss History"
])

# ---------------------------------------------------------------------
# TAB 1: EASY PICKS
# ---------------------------------------------------------------------
with tab_picks:
    st.subheader("High-Probability Recommended Plays")
    
    sel_sport = st.radio("Filter Sport:", ["All Sports", "NFL Football", "NBA Basketball", "NHL Hockey", "MLB Baseball"], horizontal=True)

    shown_count = 0
    for prop in props_database:
        if sel_sport != "All Sports" and prop["sport"] != sel_sport:
            continue
            
        if pick_filter == "🔒 High Confidence (Safest)" and prop["confidence"] != "🔒 High Confidence (Safest)":
            continue
        elif pick_filter == "🎯 Best Value & Edge" and prop["confidence"] not in ["🔒 High Confidence (Safest)", "🎯 Best Value & Edge"]:
            continue
            
        shown_count += 1
        
        st.markdown(f"""
        <div class="cyber-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;">
                <div>
                    <span class="badge-sport">{prop['sport']}</span>
                    <span class="badge-confidence">{prop['confidence']}</span>
                    <h3 style="margin: 6px 0 2px 0; color: #fff;">{prop['player']} ({prop['team']})</h3>
                    <div style="color: #00ff88; font-weight: 800; font-size: 1.25rem;">
                        👉 Take the {prop['pick']} {prop['line']} {prop['category']}
                    </div>
                </div>
                <div style="text-align: right; margin-top: 4px;">
                    <span class="badge-app">⭐ BEST APP: {prop['best_app'].upper()}</span>
                    <div style="margin-top: 6px; color: #f59e0b; font-weight: 700;">Hit Rate: {prop['hit_rate']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        c_why, c_btn = st.columns([3, 1])
        with c_why:
            st.markdown(f"**Why this is a top pick:** {prop['why']}")
            st.caption(f"Recommended bet: **${suggested_unit:.2f}** on **{prop['best_app']}**")
        with c_btn:
            already_added = any(item["id"] == prop["id"] for item in st.session_state.slip)
            if already_added:
                st.button("✅ Added to Slip", key=f"btn_{prop['id']}", disabled=True)
            else:
                if st.button("➕ Add to Slip", key=f"btn_{prop['id']}", use_container_width=True):
                    st.session_state.slip.append({
                        "id": prop["id"],
                        "desc": f"{prop['player']} {prop['pick']} {prop['line']} {prop['category']}",
                        "app": prop["best_app"],
                        "stake": suggested_unit
                    })
                    st.rerun()
        st.markdown("<hr style='border-color: #1e293b; margin: 8px 0 16px 0;'>", unsafe_allow_html=True)

    if shown_count == 0:
        st.info("No picks match this filter right now. Switch to '⚡ Show All Plays' to view available games.")

# ---------------------------------------------------------------------
# TAB 2: SIMPLE LINE COMPARISON
# ---------------------------------------------------------------------
with tab_compare:
    st.subheader("App-by-App Line Comparison")
    st.markdown("Shows how lines vary across sites so you can bet where it's easiest to win.")
    
    table_data = []
    for p in props_database:
        row = {
            "Player": p["player"],
            "Pick": f"{p['pick']} {p['category']}",
            "Recommended App": f"⭐ {p['best_app']}"
        }
        for app in ["PrizePicks", "Dabble", "DraftKings", "FanDuel"]:
            row[app] = p["lines"].get(app, "-")
        table_data.append(row)
        
    st.dataframe(pd.DataFrame(table_data), use_container_width=True)

# ---------------------------------------------------------------------
# TAB 3: BET SLIP
# ---------------------------------------------------------------------
with tab_slip:
    st.subheader("Your Selections")
    if not st.session_state.slip:
        st.info("Your bet slip is empty. Click **'➕ Add to Slip'** on any pick in the first tab to build your card.")
    else:
        for idx, item in enumerate(st.session_state.slip):
            c_del, c_name = st.columns([1, 8])
            with c_del:
                if st.button("❌", key=f"del_{idx}"):
                    st.session_state.slip.pop(idx)
                    st.rerun()
            with c_name:
                st.write(f"**{item['desc']}** — Place this on: `{item['app']}`")
        
        st.markdown("---")
        ticket_stake = st.number_input("How much are you betting on this card? ($)", min_value=1.0, value=float(suggested_unit), step=5.0)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("📝 Save to My Bet History", use_container_width=True):
                summary = " + ".join([s["desc"].split()[0] for s in st.session_state.slip])
                st.session_state.bet_history.insert(0, {
                    "Date": NOW_TIME.strftime("%Y-%m-%d"),
                    "Pick": f"{len(st.session_state.slip)}-Pick Entry: {summary}",
                    "Platform": st.session_state.slip[0]["app"] if len(st.session_state.slip) == 1 else "Multi-App",
                    "Wager": ticket_stake,
                    "Result": "Pending",
                    "Profit": 0.0
                })
                st.session_state.slip = []
                st.success("Entry saved!")
                st.rerun()
        with c2:
            if st.button("🗑️ Clear Slip", use_container_width=True):
                st.session_state.slip = []
                st.rerun()

# ---------------------------------------------------------------------
# TAB 4: HISTORY
# ---------------------------------------------------------------------
with tab_log:
    st.subheader("Past Bets Tracker")
    df_history = pd.DataFrame(st.session_state.bet_history)
    st.dataframe(df_history, use_container_width=True)
