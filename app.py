import streamlit as st
import numpy as np

st.set_page_config(page_title="Smart Sports Bet Finder", page_icon="🪙", layout="wide")

def calculate_bet_value(true_prob, best_odds, bankroll, risk_mult=0.25):
    implied = 1.0 / best_odds
    edge_pct = (true_prob - implied) * 100
    b = best_odds - 1
    p = true_prob
    q = 1.0 - p
    raw_kelly = (b * p - q) / b if b > 0 else 0
    adj_kelly = max(0, raw_kelly * risk_mult)
    recommended_bet = bankroll * adj_kelly
    return edge_pct, recommended_bet

def to_american_odds(dec):
    if dec <= 1.0:
        return "N/A"
    if dec >= 2.0:
        val = int(round((dec - 1.0) * 100))
        return "+" + str(val)
    val = int(round(100.0 / (dec - 1.0)))
    return "-" + str(val)

PRIZEPICKS_FIXED_ODDS = 1.84
DABBLE_FIXED_ODDS = 1.82

st.sidebar.title("Settings")
bankroll = st.sidebar.number_input("Total bankroll (USD)", min_value=20.0, value=1000.0, step=50.0)
style_choice = st.sidebar.radio("Bet sizing preference:", ["Conservative", "Moderate", "Aggressive"], index=0)
risk_mult = {"Conservative": 0.20, "Moderate": 0.35, "Aggressive": 0.50}[style_choice]

available_books = ["DraftKings", "FanDuel", "PrizePicks (DFS)", "Dabble (DFS)"]
selected_books = st.sidebar.multiselect("Active apps:", options=available_books, default=available_books)

st.title("🪙 Smart Sports Bet & Prop Finder")

# =========================================================================
# 1. POPULAR PLAYER PROPS CAROUSEL
# =========================================================================
st.subheader("⭐ Popular Player Picks Carousel")
st.caption("Trending high-value player and driver props across all leagues.")

popular_players = [
    {"player": "Patrick Mahomes", "team": "KC Chiefs", "sport": "NFL", "logo": "https://a.espncdn.com/i/teamlogos/nfl/500/kc.png", "line": "Over 265.5 Pass Yds", "best_app": "PrizePicks", "edge": "+7.1%"},
    {"player": "Luka Doncic", "team": "Dallas Mavericks", "sport": "NBA", "logo": "https://a.espncdn.com/i/teamlogos/nba/500/dal.png", "line": "Over 31.5 Points", "best_app": "Dabble", "edge": "+6.4%"},
    {"player": "Max Verstappen", "team": "Red Bull F1", "sport": "F1", "logo": "https://media.formula1.com/d_team_car_fallback_image.png/content/dam/fom-website/teams/2024/red-bull-racing-logo.png", "line": "Podium Finish (Top 3)", "best_app": "PrizePicks", "edge": "+8.2%"},
    {"player": "Connor McDavid", "team": "EDM Oilers", "sport": "NHL", "logo": "https://a.espncdn.com/i/teamlogos/nhl/500/edm.png", "line": "Over 3.5 Shots on Goal", "best_app": "PrizePicks", "edge": "+8.5%"},
    {"player": "Virat Kohli", "team": "India Cricket", "sport": "Cricket", "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/8/8d/Cricket_India_Crest.svg/1200px-Cricket_India_Crest.svg.png", "line": "Over 32.5 Runs", "best_app": "Dabble", "edge": "+6.8%"},
    {"player": "Erling Haaland", "team": "Manchester City", "sport": "Soccer", "logo": "https://a.espncdn.com/i/teamlogos/soccer/500/382.png", "line": "Over 1.5 Shots on Target", "best_app": "PrizePicks", "edge": "+9.0%"}
]

if "p_car_idx" not in st.session_state:
    st.session_state.p_car_idx = 0

col_c1, col_c2, col_c3 = st.columns([1, 10, 1])
with col_c1:
    st.write("")
    st.write("")
    if st.button("◀", key="prev_player"):
        st.session_state.p_car_idx = (st.session_state.p_car_idx - 1) % len(popular_players)

with col_c3:
    st.write("")
    st.write("")
    if st.button("▶", key="next_player"):
        st.session_state.p_car_idx = (st.session_state.p_car_idx + 1) % len(popular_players)

with col_c2:
    p_cols = st.columns(3)
    for i in range(3):
        curr_p = popular_players[(st.session_state.p_car_idx + i) % len(popular_players)]
        with p_cols[i]:
            with st.container():
                st.image(curr_p["logo"], width=55)
                st.markdown(f"**{curr_p['player']}** ({curr_p['sport']})")
                st.caption(f"{curr_p['team']}")
                st.success(f"🎯 {curr_p['line']}")
                st.info(f"App: **{curr_p['best_app']}** | Edge: **{curr_p['edge']}**")

st.markdown("---")

# =========================================================================
# 2. POPULAR TEAMS & MATCHUPS CAROUSEL
# =========================================================================
st.subheader("🏆 Popular Team Picks Carousel")
st.caption("Trending team moneylines and head-to-head race matchups.")

popular_teams = [
    {"team": "Kansas City Chiefs", "matchup": "vs. Buffalo Bills", "sport": "NFL", "logo": "https://a.espncdn.com/i/teamlogos/nfl/500/kc.png", "best_book": "FanDuel (+105)", "edge": "+4.1%"},
    {"team": "Dallas Mavericks", "matchup": "vs. Phoenix Suns", "sport": "NBA", "logo": "https://a.espncdn.com/i/teamlogos/nba/500/dal.png", "best_book": "DraftKings (+115)", "edge": "+3.4%"},
    {"team": "Max Verstappen", "matchup": "vs. Lando Norris (F1 H2H)", "sport": "F1", "logo": "https://media.formula1.com/d_team_car_fallback_image.png/content/dam/fom-website/teams/2024/red-bull-racing-logo.png", "best_book": "DraftKings (-118)", "edge": "+3.9%"},
    {"team": "Kyle Larson", "matchup": "vs. Denny Hamlin (NASCAR)", "sport": "NASCAR", "logo": "https://images.seeklogo.com/logo-png/43/1/hendrick-motorsports-logo-png_seeklogo-437537.png", "best_book": "FanDuel (-105)", "edge": "+3.4%"},
    {"team": "India National Team", "matchup": "vs. Australia (T20)", "sport": "Cricket", "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/8/8d/Cricket_India_Crest.svg/1200px-Cricket_India_Crest.svg.png", "best_book": "DraftKings (-125)", "edge": "+4.2%"},
    {"team": "Edmonton Oilers", "matchup": "vs. Vegas Golden Knights", "sport": "NHL", "logo": "https://a.espncdn.com/i/teamlogos/nhl/500/edm.png", "best_book": "DraftKings (-105)", "edge": "+3.8%"}
]

if "t_car_idx" not in st.session_state:
    st.session_state.t_car_idx = 0

col_t1, col_t2, col_t3 = st.columns([1, 10, 1])
with col_t1:
    st.write("")
    st.write("")
    if st.button("◀", key="prev_team"):
        st.session_state.t_car_idx = (st.session_state.t_car_idx - 1) % len(popular_teams)

with col_t3:
    st.write("")
    st.write("")
    if st.button("▶", key="next_team"):
        st.session_state.t_car_idx = (st.session_state.t_car_idx + 1) % len(popular_teams)

with col_t2:
    t_cols = st.columns(3)
    for i in range(3):
        curr_t = popular_teams[(st.session_state.t_car_idx + i) % len(popular_teams)]
        with t_cols[i]:
            with st.container():
                st.image(curr_t["logo"], width=55)
                st.markdown(f"**{curr_t['team']}** ({curr_t['sport']})")
                st.caption(f"{curr_t['matchup']}")
                st.success("🎯 Recommended Winner")
                st.info(f"Line: **{curr_t['best_book']}** | Edge: **{curr_t['edge']}**")

st.markdown("---")

# =========================================================================
# 3. FULL DETAIL TABS (PROPS & PAYOUT CALCULATOR)
# =========================================================================
tab_props, tab_games = st.tabs(["🎯 All Player & Driver Props", "🏆 All Game Winners"])
odds_type = st.radio("Odds Format", ["American (+150 / -110)", "Decimal (2.50)"], horizontal=True)

with tab_props:
    st.subheader("All Player & Driver Props by League")
    prop_sport = st.selectbox("Choose Sport or League:", ["NFL Football", "NBA Basketball", "Formula 1 Racing", "NASCAR Racing", "Cricket (T20 / IPL)", "NHL Hockey", "Soccer (EPL / UCL)"])

    all_props_data = [
        {"id": "nfl_mahomes", "sport": "NFL Football", "player": "Patrick Mahomes", "team_name": "Kansas City Chiefs", "matchup": "KC vs. Buffalo Bills", "logo": "https://a.espncdn.com/i/teamlogos/nfl/500/kc.png", "category": "Passing Yards", "line": 265.5, "pick": "OVER", "fair_prob": 0.582, "best_app": "PrizePicks (DFS)", "payout_odds": PRIZEPICKS_FIXED_ODDS, "app_rates": {"PrizePicks": 3.0, "Dabble": 3.1, "DraftKings": 1.69, "FanDuel": 1.71}, "notes": "Books juice this over. Flat payout on PrizePicks offers +7.1% edge."},
        {"id": "nba_luka", "sport": "NBA Basketball", "player": "Luka Doncic", "team_name": "Dallas Mavericks", "matchup": "DAL vs. Phoenix Suns", "logo": "https://a.espncdn.com/i/teamlogos/nba/500/dal.png", "category": "Points", "line": 31.5, "pick": "OVER", "fair_prob": 0.565, "best_app": "Dabble (DFS)", "payout_odds": DABBLE_FIXED_ODDS, "app_rates": {"PrizePicks": 3.0, "Dabble": 3.1, "DraftKings": 1.72, "FanDuel": 1.74}, "notes": "Consensus favorite to clear 31.5. Great leg for Dabble entries."},
        {"id": "f1_max", "sport": "Formula 1 Racing", "player": "Max Verstappen", "team_name": "Red Bull Racing", "matchup": "Grand Prix Main Race", "logo": "https://media.formula1.com/d_team_car_fallback_image.png/content/dam/fom-website/teams/2024/red-bull-racing-logo.png", "category": "Podium Finish (Top 3)", "line": 1.5, "pick": "YES", "fair_prob": 0.615, "best_app": "PrizePicks (DFS)", "payout_odds": PRIZEPICKS_FIXED_ODDS, "app_rates": {"PrizePicks": 3.0, "Dabble": 3.1, "DraftKings": 1.65, "FanDuel": 1.67}, "notes": "Books juice podium finish. Flat rate offers +8.2% edge."},
        {"id": "nascar_larson", "sport": "NASCAR Racing", "player": "Kyle Larson", "team_name": "Hendrick Motorsports (#5)", "matchup": "NASCAR Cup Series Race", "logo": "https://images.seeklogo.com/logo-png/43/1/hendrick-motorsports-logo-png_seeklogo-437537.png", "category": "Top 5 Finish", "line": 4.5, "pick": "YES", "fair_prob": 0.575, "best_app": "Dabble (DFS)", "payout_odds": DABBLE_FIXED_ODDS, "app_rates": {"PrizePicks": 3.0, "Dabble": 3.1, "DraftKings": 1.71, "FanDuel": 1.74}, "notes": "High track history rating. Great leg on Dabble slips."},
        {"id": "cricket_kohli", "sport": "Cricket (T20 / IPL)", "player": "Virat Kohli", "team_name": "India National Team", "matchup": "India vs. Australia (T20)", "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/8/8d/Cricket_India_Crest.svg/1200px-Cricket_India_Crest.svg.png", "category": "Batter Total Runs", "line": 32.5, "pick": "OVER", "fair_prob": 0.584, "best_app": "PrizePicks (DFS)", "payout_odds": PRIZEPICKS_FIXED_ODDS, "app_rates": {"PrizePicks": 3.0, "Dabble": 3.1, "DraftKings": 1.69, "FanDuel": 1.71}, "notes": "Batting-friendly pitch. High value at flat payout."},
        {"id": "nhl_mcdavid", "sport": "NHL Hockey", "player": "Connor McDavid", "team_name": "Edmonton Oilers", "matchup": "EDM vs. Vegas Golden Knights", "logo": "https://a.espncdn.com/i/teamlogos/nhl/500/edm.png", "category": "Shots on Goal", "line": 3.5, "pick": "OVER", "fair_prob": 0.590, "best_app": "PrizePicks (DFS)", "payout_odds": PRIZEPICKS_FIXED_ODDS, "app_rates": {"PrizePicks": 3.0, "Dabble": 3.1, "DraftKings": 1.67, "FanDuel": 1.69}, "notes": "Favored over 3.5 shots. Flat payout offers +8.5% edge."},
        {"id": "soccer_haaland", "sport": "Soccer (EPL / UCL)", "player": "Erling Haaland", "team_name": "Manchester City", "matchup": "Man City vs. Arsenal", "logo": "https://a.espncdn.com/i/teamlogos/soccer/500/382.png", "category": "Shots on Target", "line": 1.5, "pick": "OVER", "fair_prob": 0.612, "best_app": "PrizePicks (DFS)", "payout_odds": PRIZEPICKS_FIXED_ODDS, "app_rates": {"PrizePicks": 3.0, "Dabble": 3.1, "DraftKings": 1.63, "FanDuel": 1.65}, "notes": "Books juice this line to -160. Great value on PrizePicks."}
    ]

    filtered_props = [p for p in all_props_data if p["sport"] == prop_sport]

    if filtered_props:
        for p in filtered_props:
            edge, default_bet = calculate_bet_value(p["fair_prob"], p["payout_odds"], bankroll, risk_mult)
            fmt_odds = to_american_odds(p["payout_odds"]) if "American" in odds_type else f"{p['payout_odds']:.2f}"

            with st.container():
                c_logo, c_info, c_pick = st.columns([1, 4, 3])
                with c_logo:
                    st.image(p["logo"], width=75)
                with c_info:
                    st.markdown(f"### {p['player']}")
                    st.markdown(f"**{p['team_name']}** ({p['matchup']})")
                    st.markdown(f"Target Stat: **{p['category']}** — Line: **{p['line']}**")
                with c_pick:
                    st.success(f"TAKE {p['pick']} {p['line']}")
                    st.caption(f"Best App: **{p['best_app']}** (+{edge:.2f}% Edge | Rate: {fmt_odds})")

                c_wager, c_payouts = st.columns([2, 5])
                with c_wager:
                    user_wager = st.number_input(f"Wager for {p['player']} (USD):", min_value=1.0, max_value=float(bankroll), value=max(5.0, round(float(default_bet), 2)), step=5.0, key=f"w_{p['id']}")
                    st.caption(f"AI Recommended: **{default_bet:.2f} USD**")

                with c_payouts:
                    st.write("Projected Total Payout and Net Profit by App:")
                    app_cols = st.columns(len(p["app_rates"]))
                    for i, (app_name, mult) in enumerate(p["app_rates"].items()):
                        payout = user_wager * mult
                        profit = payout - user_wager
                        with app_cols[i]:
                            st.metric(label=app_name, value=f"{payout:.2f} USD", delta=f"+{profit:.2f} USD")

                st.info(f"Notes: {p['notes']}")
                st.markdown("---")
    else:
        st.info(f"No active prop edges found for {prop_sport}.")

with tab_games:
    st.subheader("All Matchup and Race Winners")
    games_data = [
        {"id": "g1", "home": "Max Verstappen", "away": "Lando Norris", "sport": "Formula 1 H2H", "pick": {"team": "Max Verstappen", "book": "DraftKings", "odds": 1.85, "edge": 3.9, "amount": 27.00}},
        {"id": "g2", "home": "Kyle Larson", "away": "Denny Hamlin", "sport": "NASCAR H2H", "pick": {"team": "Kyle Larson", "book": "FanDuel", "odds": 1.95, "edge": 3.4, "amount": 23.50}},
        {"id": "g3", "home": "India", "away": "Australia", "sport": "Cricket T20", "pick": {"team": "India", "book": "DraftKings", "odds": 1.80, "edge": 4.2, "amount": 29.00}},
        {"id": "g4", "home": "Kansas City Chiefs", "away": "Buffalo Bills", "sport": "NFL", "pick": {"team": "Kansas City Chiefs", "book": "FanDuel", "odds": 2.05, "edge": 4.1, "amount": 28.50}}
    ]

    for g in games_data:
        p = g["pick"]
        fmt_odds = to_american_odds(p["odds"]) if "American" in odds_type else f"{p['odds']:.2f}"
        st.subheader(f"[{g['sport']}] {g['away']} vs. {g['home']}")
        c_pick, c_calc = st.columns([2, 2])
        with c_pick:
            st.success(f"TOP RECOMMENDED PLAY: {p['team'].upper()}\n\nWhere to Bet: Best on {p['book']} at {fmt_odds}\n\nAdvantage: +{p['edge']:.2f}% Edge")
        with c_calc:
            w = st.number_input(f"Bet Amount for {p['team']}:", min_value=1.0, value=float(p["amount"]), step=5.0, key=f"gw_{g['id']}")
            payout = w * p["odds"]
            profit = payout - w
            st.metric("Projected Total Payout", f"{payout:.2f} USD", delta=f"+{profit:.2f} USD Profit")
        st.markdown("---")