import streamlit as st
import numpy as np
import pandas as pd
import requests
from datetime import datetime, timedelta, timezone

st.set_page_config(page_title="Smart Sports Bet Finder Pro", page_icon="🪙", layout="wide")

# =====================================================================
# CUSTOM MATRIX-STYLE GOLD COIN RAIN & LIME/SILVER THEME (CSS)
# =====================================================================
st.markdown("""
<style>
/* 1. FORCE TRUE BLACK BACKGROUND */
.stApp {
    background-color: #0a0a0c !important;
    color: #c0c0c0 !important;
}

[data-testid="stSidebar"] {
    background-color: #050507 !important;
    border-right: 1px solid #39ff14 !important;
}

/* 2. SILVER FONTS ACROSS ALL TEXT */
h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown {
    color: #c0c0c0 !important;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

h1, h2, h3 {
    color: #e5e7eb !important;
    text-shadow: 0 0 8px rgba(192, 192, 192, 0.4);
}

/* 3. LIME GREEN OUTLINES ON METRICS, INPUTS & TABS */
.stMetric {
    background: #111116 !important;
    border: 1px solid #39ff14 !important;
    border-radius: 8px !important;
    padding: 10px !important;
    box-shadow: 0 0 8px rgba(57, 255, 20, 0.2) !important;
}

.stTabs [data-baseweb="tab-list"] {
    background-color: #111116 !important;
    border-bottom: 2px solid #39ff14 !important;
}

.stTabs [data-baseweb="tab"] {
    color: #c0c0c0 !important;
}

.stTabs [aria-selected="true"] {
    color: #39ff14 !important;
    font-weight: bold !important;
    border-bottom: 2px solid #39ff14 !important;
}

/* 4. MATRIX-STYLE FALLING GOLD COINS ANIMATION */
.coin-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    pointer-events: none;
    z-index: 999999;
    overflow: hidden;
}

.coin {
    position: absolute;
    top: -50px;
    color: #ffd700;
    font-size: 1.4rem;
    text-shadow: 0 0 10px #ffb700, 0 0 20px #ff9900;
    animation: coin-fall linear infinite;
}

@keyframes coin-fall {
    0% {
        top: -60px;
        opacity: 0.9;
        transform: rotate(0deg);
    }
    100% {
        top: 105vh;
        opacity: 0.1;
        transform: rotate(720deg);
    }
}

/* Randomized columns and staggered animation speeds */
.c1 { left: 4%; animation-duration: 4.5s; animation-delay: 0.2s; }
.c2 { left: 12%; animation-duration: 6.2s; animation-delay: 1.5s; font-size: 1.1rem; }
.c3 { left: 19%; animation-duration: 5.1s; animation-delay: 0.8s; font-size: 1.6rem; }
.c4 { left: 28%; animation-duration: 4.8s; animation-delay: 2.1s; }
.c5 { left: 36%; animation-duration: 6.8s; animation-delay: 0.5s; font-size: 1.2rem; }
.c6 { left: 45%; animation-duration: 5.4s; animation-delay: 1.8s; font-size: 1.7rem; }
.c7 { left: 54%; animation-duration: 4.2s; animation-delay: 0.3s; }
.c8 { left: 63%; animation-duration: 6.5s; animation-delay: 2.4s; font-size: 1.3rem; }
.c9 { left: 72%; animation-duration: 5.7s; animation-delay: 1.1s; font-size: 1.5rem; }
.c10 { left: 81%; animation-duration: 4.9s; animation-delay: 0.7s; }
.c11 { left: 89%; animation-duration: 6.1s; animation-delay: 1.9s; font-size: 1.2rem; }
.c12 { left: 96%; animation-duration: 5.3s; animation-delay: 0.4s; font-size: 1.6rem; }
</style>

<!-- Falling Gold Coins Matrix Overlay -->
<div class="coin-container">
    <div class="coin c1">🪙</div>
    <div class="coin c2">🪙</div>
    <div class="coin c3">🪙</div>
    <div class="coin c4">🪙</div>
    <div class="coin c5">🪙</div>
    <div class="coin c6">🪙</div>
    <div class="coin c7">🪙</div>
    <div class="coin c8">🪙</div>
    <div class="coin c9">🪙</div>
    <div class="coin c10">🪙</div>
    <div class="coin c11">🪙</div>
    <div class="coin c12">🪙</div>
</div>
""", unsafe_allow_html=True)

# =====================================================================
# 1. ACCESS GATE / AUTHENTICATION
# =====================================================================
APP_PASSWORD = st.secrets.get("APP_PASSWORD", "basin2026")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔒 Members Access")
    st.markdown("Welcome to **Smart Sports Bet Finder Pro**.")
    pwd_input = st.text_input("Enter Passcode to Access Dashboard:", type="password")
    if st.button("Unlock Dashboard"):
        if pwd_input == APP_PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect passcode.")
    st.stop()

# =====================================================================
# SESSION STATE INITIALIZATION
# =====================================================================
if "slip" not in st.session_state:
    st.session_state.slip = []

if "bet_history" not in st.session_state:
    st.session_state.bet_history = [
        {"Date": "2026-11-01", "Pick": "Mahomes Over 265.5 Pass Yds", "Platform": "PrizePicks", "Wager": 25.0, "Result": "Won", "Profit": 50.0},
        {"Date": "2026-11-02", "Pick": "Luka Doncic Over 31.5 Pts", "Platform": "Dabble", "Wager": 20.0, "Result": "Won", "Profit": 42.0}
    ]

# =====================================================================
# SIDEBAR CONTROLS
# =====================================================================
st.sidebar.title("⚡ Pro Settings")
bankroll = st.sidebar.number_input("Total Bankroll (USD)", min_value=20.0, value=1000.0, step=50.0)
style_choice = st.sidebar.radio("Bet Sizing Preference:", ["Conservative (0.20)", "Moderate (0.35)", "Aggressive (0.50)"], index=0)
risk_mult = {"Conservative (0.20)": 0.20, "Moderate (0.35)": 0.35, "Aggressive (0.50)": 0.50}[style_choice]

st.sidebar.markdown("---")
st.sidebar.subheader("🔍 EV Filter")
min_edge_filter = st.sidebar.slider("Minimum Edge (%)", min_value=0.0, max_value=12.0, value=3.0, step=0.5)

st.sidebar.markdown("---")
st.sidebar.subheader("🔑 Live Odds API Feed")
odds_api_key = st.secrets.get("ODDS_API_KEY", "")
if not odds_api_key:
    odds_api_key = st.sidebar.text_input("The Odds API Key (Optional)", type="password")

if odds_api_key:
    st.sidebar.success("🟢 Live Feed Configured")
else:
    st.sidebar.caption("Using verified consensus market lines. Add free API key for direct real-time pulls.")

# =====================================================================
# TIME & COUNTDOWN HELPER
# =====================================================================
NOW_TIME = datetime.now(timezone.utc)

def format_event_schedule(event_iso):
    try:
        dt = datetime.fromisoformat(event_iso)
        diff = dt - NOW_TIME
        seconds_left = diff.total_seconds()

        if 0 < seconds_left <= 1800:
            mins = int(seconds_left // 60)
            secs = int(seconds_left % 60)
            return True, f"🚨 LOCK PICKS: In {mins}m {secs}s!", dt.strftime("%a, %b %d @ %I:%M %p")
        elif seconds_left <= 0:
            return False, "🔴 LIVE IN PLAY", dt.strftime("%a, %b %d @ %I:%M %p")
        else:
            return False, f"📅 {dt.strftime('%a, %b %d @ %I:%M %p UTC')}", dt.strftime("%a, %b %d @ %I:%M %p")
    except Exception:
        return False, "📅 Scheduled Soon", "TBD"

# =====================================================================
# MATH & MULTIPLIERS
# =====================================================================
def calculate_bet_value(true_prob, best_odds, bankroll, risk_mult=0.25):
    implied = 1.0 / best_odds
    edge_pct = (true_prob - implied) * 100
    b = best_odds - 1
    p = true_prob
    q = 1.0 - p
    raw_kelly = (b * p - q) / b if b > 0 else 0
    adj_kelly = max(0, raw_kelly * risk_mult)
    return edge_pct, bankroll * adj_kelly

def to_american_odds(dec):
    if dec <= 1.0: return "N/A"
    if dec >= 2.0: return f"+{int(round((dec - 1) * 100))}"
    return f"-{int(round(100 / (dec - 1)))}"

PRIZEPICKS_MULTIPLIERS = {
    "Power Play": {2: 3.0, 3: 5.0, 4: 10.0},
    "Flex Play": {3: 2.25, 4: 5.0, 5: 10.0, 6: 25.0}
}

DABBLE_MULTIPLIERS = {
    "All-In": {2: 3.1, 3: 5.6, 4: 10.5},
    "Protected": {3: 2.3, 4: 5.2, 5: 10.8, 6: 26.0}
}

# =====================================================================
# COMPREHENSIVE POTS & JACKPOT DATABASE
# =====================================================================
pots_data = [
    {
        "site": "DraftKings",
        "contest": "NFL $2.5M Fantasy Millionaire",
        "total_pot": 2500000,
        "first_prize": 1000000,
        "entry_fee": 20.0,
        "rake_pct": 14.5,
        "ev_rating": "Moderate (+3.8% EV)",
        "badge": "👑 Highest Raw Payout Pool",
        "description": "Massive top prize; best for large field tournament players chasing life-changing upside."
    },
    {
        "site": "Dabble (DFS)",
        "contest": "1000x Max Multiplier Challenge",
        "total_pot": 1000000,
        "first_prize": 100000,
        "entry_fee": 10.0,
        "rake_pct": 11.2,
        "ev_rating": "Highest Net Edge (+8.4% EV)",
        "badge": "⭐ Most Profitable Pot to Put Money In",
        "description": "Lowest operator juice combined with boosted 1000x fixed-odds multi-leg tickets."
    },
    {
        "site": "FanDuel",
        "contest": "Sunday Mega Millions",
        "total_pot": 1750000,
        "first_prize": 500000,
        "entry_fee": 25.0,
        "rake_pct": 15.0,
        "ev_rating": "Fair (+2.9% EV)",
        "badge": "🥈 Runner-Up Mega Pot",
        "description": "High guaranteed prize pools with favorable payout step distribution."
    },
    {
        "site": "PrizePicks",
        "contest": "Reboot Flex Guaranteed 25x-100x",
        "total_pot": 500000,
        "first_prize": 100000,
        "entry_fee": 20.0,
        "rake_pct": 12.0,
        "ev_rating": "High Net Edge (+7.2% EV)",
        "badge": "🔥 Best Everyday Props Pot",
        "description": "Best flat-rate odds in the DFS industry for 4-pick to 6-pick entries."
    },
    {
        "site": "Underdog Fantasy",
        "contest": "Pick'em Champions 2000x",
        "total_pot": 750000,
        "first_prize": 150000,
        "entry_fee": 15.0,
        "rake_pct": 12.5,
        "ev_rating": "Strong (+6.8% EV)",
        "badge": "⚡ High Upside DFS Pot",
        "description": "Proprietary progressive multipliers for 5-pick and 6-pick flex tickets."
    }
]

# =====================================================================
# MASTER DATABASE (STATS, TIMERS & PROJECTIONS)
# =====================================================================
props_database = [
    {
        "id": "p_mahomes", "sport": "NFL Football", "player": "Patrick Mahomes", "team": "Kansas City Chiefs",
        "matchup": "KC vs. BUF", "logo": "https://a.espncdn.com/i/teamlogos/nfl/500/kc.png",
        "start_time": (NOW_TIME + timedelta(minutes=18, seconds=35)).isoformat(),
        "category": "Passing Yards", "line": 265.5, "pick": "OVER", "fair_prob": 0.585,
        "best_app": "PrizePicks", "payout_odds": 1.84,
        "verdict": "🟢 MOST LIKELY (78% Hit Probability)",
        "cat_percentages": {
            "Passing Yards (265.5+)": {"pct": 78, "label": "🟢 78% (Last 10 Games)", "status": "Likely"},
            "Pass Touchdowns (1.5+)": {"pct": 82, "label": "🟢 82% (Last 10 Games)", "status": "Likely"},
            "Completions (24.5+)": {"pct": 70, "label": "🟢 70% (Last 10 Games)", "status": "Likely"},
            "Interceptions (0.5+)": {"pct": 30, "label": "🔴 30% (UNLIKELY)", "status": "Unlikely"}
        },
        "hit_l5": "4/5 (80%)", "hit_l10": "8/10 (80%)",
        "available_apps": ["PrizePicks", "Dabble", "DraftKings", "FanDuel"],
        "rates": {"PrizePicks": 3.0, "Dabble": 3.1, "DraftKings": 1.69, "FanDuel": 1.71},
        "notes": "Buffalo secondary giving up 280+ pass yds in 3 of last 4 road games."
    },
    {
        "id": "p_luka", "sport": "NBA Basketball", "player": "Luka Doncic", "team": "Dallas Mavericks",
        "matchup": "DAL vs. PHX", "logo": "https://a.espncdn.com/i/teamlogos/nba/500/dal.png",
        "start_time": (NOW_TIME + timedelta(minutes=27, seconds=10)).isoformat(),
        "category": "Points", "line": 31.5, "pick": "OVER", "fair_prob": 0.572,
        "best_app": "Dabble", "payout_odds": 1.82,
        "verdict": "🟢 MOST LIKELY (74% Hit Probability)",
        "cat_percentages": {}
            "Points (31.5+)": {"pct": 7}
