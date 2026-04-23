"""
🎮 ARCADE GALAXY — ספריית משחקים
=====================================
קובץ יחיד | Python + Streamlit
הפעלה: streamlit run arcade_galaxy.py

משחקים: נחש | פלאפי | זיכרון | איקס-עיגול | קליקר | מכונת מזל
"""

import streamlit as st
import streamlit.components.v1 as components
import random
import time

# ─────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────
st.set_page_config(
    page_title="🎮 Arcade Galaxy",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────
# SHOP DATA
# ─────────────────────────────────────────
SHOP_ITEMS = {
    "snake_speed_up":    {"name": "⚡ מהירות נחש+",       "game": "snake",     "price": 150, "desc": "הנחש זז מהר יותר",          "icon": "⚡"},
    "snake_extra_life":  {"name": "💚 חיים נוספים",        "game": "snake",     "price": 300, "desc": "התחל עם 3 חיים",             "icon": "💚"},
    "snake_wall_pass":   {"name": "🌀 מעבר קירות",         "game": "snake",     "price": 500, "desc": "הנחש עובר דרך קירות",        "icon": "🌀"},
    "flappy_shield":     {"name": "🛡️ מגן פלאפי",         "game": "flappy",    "price": 200, "desc": "מגן חד-פעמי",                "icon": "🛡️"},
    "flappy_slow_pipes": {"name": "🐌 צינורות איטיים",     "game": "flappy",    "price": 250, "desc": "הצינורות זזים לאט יותר",     "icon": "🐌"},
    "flappy_big_gap":    {"name": "🔓 פתח גדול",           "game": "flappy",    "price": 400, "desc": "פתח גדול יותר בצינורות",     "icon": "🔓"},
    "memory_hint":       {"name": "💡 רמזים בזיכרון",      "game": "memory",    "price": 100, "desc": "3 רמזים לכל משחק",           "icon": "💡"},
    "memory_extra_time": {"name": "⏰ זמן נוסף",           "game": "memory",    "price": 200, "desc": "+10 שניות לכל פנייה",        "icon": "⏰"},
    "memory_x2":         {"name": "✨ כפל ניקוד",          "game": "memory",    "price": 350, "desc": "פי 2 נקודות",                "icon": "✨"},
    "slot_luck":         {"name": "🍀 מזל מוגבר",          "game": "slot",      "price": 300, "desc": "סיכויי זכייה גבוהים יותר",  "icon": "🍀"},
    "slot_jackpot":      {"name": "💰 ג'קפוט מוגדל",       "game": "slot",      "price": 500, "desc": "פרס ג'קפוט כפול",           "icon": "💰"},
    "clicker_auto":      {"name": "🤖 קליקר אוטומטי",      "game": "clicker",   "price": 200, "desc": "קליק אוטומטי כל 2 שניות",   "icon": "🤖"},
    "clicker_multiplier":{"name": "🔢 כפל קליקים",         "game": "clicker",   "price": 400, "desc": "כל קליק שווה 3",            "icon": "🔢"},
    "ttt_undo":          {"name": "↩️ ביטול מהלך",         "game": "tictactoe", "price": 150, "desc": "אפשר לבטל מהלך אחד",        "icon": "↩️"},
    "ttt_preview":       {"name": "🔮 צפייה במהלך AI",     "game": "tictactoe", "price": 300, "desc": "ראה מה AI מתכנן",            "icon": "🔮"},
    "coin_boost":        {"name": "🪙 בוסט מטבעות",        "game": "global",    "price": 600, "desc": "20% יותר מטבעות מכל משחק",  "icon": "🪙"},
    "xp_boost":          {"name": "⭐ בוסט ניסיון",        "game": "global",    "price": 800, "desc": "50% יותר XP",               "icon": "⭐"},
}

# ─────────────────────────────────────────
# STATE HELPERS
# ─────────────────────────────────────────
def init_state():
    defaults = {
        "coins": 100, "player_level": 1, "player_xp": 0,
        "achievements": [], "owned_upgrades": [],
        "snake_high_score": 0,   "snake_games_played": 0,
        "flappy_high_score": 0,  "flappy_games_played": 0,
        "memory_high_score": 0,  "memory_games_played": 0,
        "ttt_wins": 0, "ttt_losses": 0, "ttt_draws": 0, "ttt_games_played": 0,
        "clicker_total_clicks": 0, "clicker_sessions": 0, "clicker_best": 0,
        "slot_spins": 0, "slot_wins": 0, "slot_total_won": 0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def add_coins(amount):
    mul = 1.2 if "coin_boost" in st.session_state.get("owned_upgrades", []) else 1.0
    actual = int(amount * mul)
    st.session_state["coins"] = st.session_state.get("coins", 0) + actual
    return actual

def add_xp(amount):
    mul = 1.5 if "xp_boost" in st.session_state.get("owned_upgrades", []) else 1.0
    actual = int(amount * mul)
    st.session_state["player_xp"] = st.session_state.get("player_xp", 0) + actual
    level = st.session_state.get("player_level", 1)
    while st.session_state["player_xp"] >= level * 100:
        st.session_state["player_xp"] -= level * 100
        level += 1
        st.session_state["player_level"] = level
        add_achievement(f"⬆️ הגעת לרמה {level}!")
    return actual

def add_achievement(name):
    achs = st.session_state.get("achievements", [])
    if name not in achs:
        achs.append(name)
        st.session_state["achievements"] = achs
        return True
    return False

def has_upgrade(uid):
    return uid in st.session_state.get("owned_upgrades", [])

def buy_upgrade(uid):
    item = SHOP_ITEMS.get(uid)
    if not item:              return False, "פריט לא קיים"
    if has_upgrade(uid):      return False, "כבר קנית את זה!"
    if st.session_state.get("coins", 0) < item["price"]:
        return False, f"אין מספיק מטבעות! צריך {item['price']} 🪙"
    st.session_state["coins"] -= item["price"]
    st.session_state["owned_upgrades"] = st.session_state.get("owned_upgrades", []) + [uid]
    return True, f"קנית {item['name']} בהצלחה! 🎉"

# ─────────────────────────────────────────
# GLOBAL STYLES
# ─────────────────────────────────────────
def inject_styles():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;600;800&display=swap');
:root {
    --bg: #0a0a1a; --bg2: #0f0f2e; --card: #12122a;
    --cyan: #00f5ff; --pink: #ff006e; --yellow: #ffd60a;
    --green: #39ff14; --purple: #bf5fff; --orange: #ff7c00;
    --dim: #8888aa; --text: #e8e8ff;
}
.stApp {
    background: var(--bg) !important;
    background-image:
        radial-gradient(ellipse at 20% 50%, rgba(0,245,255,.04) 0%, transparent 60%),
        radial-gradient(ellipse at 80% 20%, rgba(255,0,110,.04)  0%, transparent 60%),
        url("data:image/svg+xml,%3Csvg width='60' height='60' xmlns='http://www.w3.org/2000/svg'%3E%3Cdefs%3E%3Cpattern id='g' width='60' height='60' patternUnits='userSpaceOnUse'%3E%3Cpath d='M60 0L0 0 0 60' fill='none' stroke='rgba(0,245,255,.03)' stroke-width='1'/%3E%3C/pattern%3E%3C/defs%3E%3Crect width='60' height='60' fill='url(%23g)'/%3E%3C/svg%3E") !important;
    font-family: 'Exo 2', sans-serif !important;
    color: var(--text) !important;
}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#060618,#0a0a24) !important;
    border-right: 1px solid rgba(0,245,255,.15) !important;
}
.sb-header { padding:24px 20px 16px; text-align:center; border-bottom:1px solid rgba(0,245,255,.1); background:linear-gradient(180deg,rgba(0,245,255,.05),transparent); }
.sb-logo   { font-size:48px; filter:drop-shadow(0 0 20px rgba(0,245,255,.8)); animation:pulseG 2s ease-in-out infinite; }
.sb-title  { font-family:Orbitron,sans-serif!important; font-size:22px!important; font-weight:900!important; color:var(--cyan)!important; letter-spacing:4px!important; text-shadow:0 0 20px rgba(0,245,255,.8),0 0 40px rgba(0,245,255,.4)!important; margin:8px 0 0!important; line-height:1.2!important; }
@keyframes pulseG { 0%,100%{filter:drop-shadow(0 0 20px rgba(0,245,255,.8))} 50%{filter:drop-shadow(0 0 35px rgba(0,245,255,1)) drop-shadow(0 0 60px rgba(0,245,255,.4))} }
.coin-box  { margin:16px; padding:14px; background:linear-gradient(135deg,rgba(255,214,10,.1),rgba(255,214,10,.05)); border:1px solid rgba(255,214,10,.4); border-radius:12px; display:flex; align-items:center; gap:10px; box-shadow:0 0 20px rgba(255,214,10,.1),inset 0 1px 0 rgba(255,255,255,.05); }
.coin-icon { font-size:24px; filter:drop-shadow(0 0 8px rgba(255,214,10,.8)); }
.coin-amt  { font-family:Orbitron,sans-serif; font-size:22px; font-weight:700; color:var(--yellow); text-shadow:0 0 10px rgba(255,214,10,.8); }
.coin-lbl  { font-size:11px; color:var(--dim); }
.sb-div    { border:none; border-top:1px solid rgba(0,245,255,.08); margin:8px 16px; }
.stat-panel{ margin:8px 12px; padding:12px; background:rgba(255,255,255,.02); border-radius:10px; border:1px solid rgba(255,255,255,.05); }
.stat-row  { display:flex; justify-content:space-between; font-size:12px; color:var(--dim); padding:4px 0; }
.stat-row span:last-child { color:var(--text); font-weight:600; }
.main .block-container { padding:24px 32px!important; max-width:100%!important; }
h1,h2,h3 { font-family:Orbitron,sans-serif!important; color:var(--cyan)!important; text-shadow:0 0 20px rgba(0,245,255,.5)!important; }
.stButton>button { background:linear-gradient(135deg,rgba(0,245,255,.15),rgba(0,245,255,.05))!important; color:var(--cyan)!important; border:1px solid rgba(0,245,255,.4)!important; border-radius:10px!important; font-family:'Exo 2',sans-serif!important; font-weight:700!important; font-size:14px!important; letter-spacing:1px!important; transition:all .2s!important; text-transform:uppercase!important; box-shadow:0 0 15px rgba(0,245,255,.1)!important; }
.stButton>button:hover { background:linear-gradient(135deg,rgba(0,245,255,.3),rgba(0,245,255,.1))!important; border-color:var(--cyan)!important; box-shadow:0 0 25px rgba(0,245,255,.3),0 0 50px rgba(0,245,255,.1)!important; transform:translateY(-2px)!important; }
.btn-primary .stButton>button { background:linear-gradient(135deg,var(--cyan),#0088aa)!important; color:#000!important; border-color:var(--cyan)!important; box-shadow:0 0 25px rgba(0,245,255,.4)!important; }
.btn-danger  .stButton>button { background:linear-gradient(135deg,rgba(255,0,110,.2),rgba(255,0,110,.05))!important; color:var(--pink)!important; border-color:rgba(255,0,110,.5)!important; }
.btn-success .stButton>button { background:linear-gradient(135deg,rgba(57,255,20,.2),rgba(57,255,20,.05))!important; color:var(--green)!important; border-color:rgba(57,255,20,.5)!important; }
.btn-gold    .stButton>button { background:linear-gradient(135deg,rgba(255,214,10,.2),rgba(255,214,10,.05))!important; color:var(--yellow)!important; border-color:rgba(255,214,10,.5)!important; }
.card { background:var(--card); border:1px solid rgba(0,245,255,.3); border-radius:16px; padding:24px; margin:8px 0; transition:all .3s; position:relative; overflow:hidden; }
.card::before { content:''; position:absolute; top:0; left:0; right:0; height:2px; background:linear-gradient(90deg,transparent,var(--cyan),transparent); opacity:.6; }
.card:hover { border-color:var(--cyan); box-shadow:0 0 30px rgba(0,245,255,.2); transform:translateY(-3px); }
[data-testid="metric-container"] { background:var(--card)!important; border:1px solid rgba(0,245,255,.3)!important; border-radius:12px!important; padding:16px!important; }
[data-testid="metric-container"] label { color:var(--dim)!important; font-family:'Exo 2',sans-serif!important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { color:var(--cyan)!important; font-family:Orbitron,sans-serif!important; text-shadow:0 0 10px rgba(0,245,255,.5)!important; }
.ok  { padding:16px; background:linear-gradient(135deg,rgba(57,255,20,.1),rgba(57,255,20,.03)); border:1px solid rgba(57,255,20,.4); border-radius:12px; color:var(--green); font-weight:600; text-align:center; animation:fadeUp .3s ease; }
.err { padding:16px; background:linear-gradient(135deg,rgba(255,0,110,.1),rgba(255,0,110,.03)); border:1px solid rgba(255,0,110,.4); border-radius:12px; color:var(--pink); font-weight:600; text-align:center; animation:fadeUp .3s ease; }
.inf { padding:16px; background:linear-gradient(135deg,rgba(0,245,255,.1),rgba(0,245,255,.03)); border:1px solid rgba(0,245,255,.3); border-radius:12px; color:var(--cyan); text-align:center; }
@keyframes fadeUp { from{opacity:0;transform:translateY(10px)} to{opacity:1;transform:translateY(0)} }
.ach { display:inline-flex; align-items:center; gap:8px; padding:8px 14px; background:linear-gradient(135deg,rgba(255,214,10,.15),rgba(255,214,10,.05)); border:1px solid rgba(255,214,10,.4); border-radius:20px; font-size:12px; font-weight:700; color:var(--yellow); margin:4px; animation:achIn .5s cubic-bezier(.34,1.56,.64,1); }
@keyframes achIn { from{transform:scale(0) rotate(-10deg);opacity:0} to{transform:scale(1) rotate(0);opacity:1} }
.stProgress>div>div>div { background:linear-gradient(90deg,var(--cyan),var(--purple))!important; box-shadow:0 0 10px rgba(0,245,255,.5)!important; border-radius:4px!important; }
.stProgress>div>div { background:rgba(255,255,255,.05)!important; border-radius:4px!important; }
div[role="radiogroup"] { display:flex!important; flex-direction:column!important; gap:4px!important; padding:8px 12px!important; }
div[role="radiogroup"] label { display:flex!important; align-items:center!important; padding:10px 14px!important; border-radius:10px!important; cursor:pointer!important; transition:all .2s!important; font-family:'Exo 2',sans-serif!important; font-size:14px!important; font-weight:600!important; color:var(--dim)!important; border:1px solid transparent!important; }
div[role="radiogroup"] label:hover { background:rgba(0,245,255,.07)!important; color:var(--cyan)!important; border-color:rgba(0,245,255,.2)!important; }
div[role="radiogroup"] label input { display:none!important; }
.stRadio>label { display:none!important; }
hr { border-color:rgba(0,245,255,.1)!important; }
::-webkit-scrollbar { width:6px; } ::-webkit-scrollbar-track { background:var(--bg); } ::-webkit-scrollbar-thumb { background:rgba(0,245,255,.3); border-radius:3px; }
#MainMenu,footer,.stDeployButton { display:none!important; }
header[data-testid="stHeader"] { background:transparent!important; }
.stTabs [data-baseweb="tab-list"] { background:rgba(255,255,255,.02)!important; border-radius:10px!important; gap:4px!important; }
.stTabs [data-baseweb="tab"] { font-family:'Exo 2',sans-serif!important; font-weight:700!important; color:var(--dim)!important; border-radius:8px!important; }
.stTabs [aria-selected="true"] { background:rgba(0,245,255,.15)!important; color:var(--cyan)!important; }
[data-testid="column"] { padding:0 8px!important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div class='sb-header'>
            <div class='sb-logo'>🎮</div>
            <h1 class='sb-title'>ARCADE<br>GALAXY</h1>
        </div>""", unsafe_allow_html=True)

        coins = st.session_state.get("coins", 0)
        st.markdown(f"""
        <div class='coin-box'>
            <span class='coin-icon'>🪙</span>
            <span class='coin-amt'>{coins:,}</span>
            <span class='coin-lbl'>מטבעות</span>
        </div>""", unsafe_allow_html=True)

        st.markdown("<hr class='sb-div'>", unsafe_allow_html=True)

        pages = ["🏠 לובי", "🐍 נחש", "🐦 פלאפי בירד", "🧠 זיכרון",
                 "❌ איקס עיגול", "👆 קליקר", "🎰 מכונת מזל", "🛒 חנות"]
        selected = st.radio("nav", pages, label_visibility="collapsed", key="nav_sel")

        st.markdown("<hr class='sb-div'>", unsafe_allow_html=True)
        total = sum(st.session_state.get(k, 0) for k in [
            "snake_games_played","flappy_games_played","memory_games_played",
            "ttt_games_played","clicker_sessions","slot_spins"])
        st.markdown(f"""
        <div class='stat-panel'>
            <div class='stat-row'><span>🎮 משחקים:</span><span>{total}</span></div>
            <div class='stat-row'><span>🏆 הישגים:</span><span>{len(st.session_state.get("achievements",[]))}</span></div>
            <div class='stat-row'><span>💎 רמה:</span><span>{st.session_state.get("player_level",1)}</span></div>
        </div>""", unsafe_allow_html=True)

    return selected

# ─────────────────────────────────────────
# PAGE: LOBBY
# ─────────────────────────────────────────
def page_lobby():
    st.markdown("""
    <div style='text-align:center;padding:20px 0 30px'>
        <div style='font-size:72px;filter:drop-shadow(0 0 30px rgba(0,245,255,.8));animation:flt 3s ease-in-out infinite'>🎮</div>
        <h1 style='font-family:Orbitron,sans-serif;font-size:40px;font-weight:900;
            background:linear-gradient(90deg,#00f5ff,#bf5fff,#ff006e,#00f5ff);
            background-size:300%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;
            animation:shim 3s linear infinite;margin:12px 0 4px'>ARCADE GALAXY</h1>
        <p style='color:#8888aa;font-size:16px;letter-spacing:3px'>בחר משחק וצא למסע הגלקסי</p>
    </div>
    <style>
    @keyframes flt{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}
    @keyframes shim{0%{background-position:0%}100%{background-position:300%}}
    </style>""", unsafe_allow_html=True)

    lv = st.session_state.get("player_level", 1)
    xp = st.session_state.get("player_xp", 0)
    xp_need = lv * 100

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.metric("💎 רמה",  lv)
    with c2: st.metric("🪙 מטבעות", f"{st.session_state.get('coins',0):,}")
    with c3: st.metric("🏆 הישגים", len(st.session_state.get("achievements",[])))
    with c4:
        total = sum(st.session_state.get(k,0) for k in [
            "snake_games_played","flappy_games_played","memory_games_played",
            "ttt_games_played","clicker_sessions","slot_spins"])
        st.metric("🎮 משחקים", total)

    st.markdown(f"""
    <div style='margin:8px 0 4px;display:flex;justify-content:space-between;font-size:12px'>
        <span style='color:#8888aa'>XP: {xp}/{xp_need}</span>
        <span style='color:#00f5ff'>רמה {lv+1}</span>
    </div>""", unsafe_allow_html=True)
    st.progress(min(xp / xp_need, 1.0))
    st.markdown("<br>", unsafe_allow_html=True)

    games = [
        ("🐍","נחש","#39ff14","rgba(57,255,20,.3)","שלוט בנחש, אכול אוכל, הימנע מקירות!",f"שיא: {st.session_state.get('snake_high_score',0)}",st.session_state.get("snake_games_played",0)),
        ("🐦","פלאפי בירד","#ffd60a","rgba(255,214,10,.3)","עוף בין הצינורות ואל תיפול!",f"שיא: {st.session_state.get('flappy_high_score',0)}",st.session_state.get("flappy_games_played",0)),
        ("🧠","זיכרון","#bf5fff","rgba(191,95,255,.3)","מצא זוגות קלפים תוך הכי פחות מהלכים!",f"שיא: {st.session_state.get('memory_high_score',0)}",st.session_state.get("memory_games_played",0)),
        ("❌","איקס עיגול","#00f5ff","rgba(0,245,255,.3)","שחק נגד AI חכם ונסה לנצח!",f"נצחונות: {st.session_state.get('ttt_wins',0)}",st.session_state.get("ttt_games_played",0)),
        ("👆","קליקר","#ff006e","rgba(255,0,110,.3)","לחץ מהר ככל האפשר תוך 10 שניות!",f"קליקים: {st.session_state.get('clicker_total_clicks',0)}",st.session_state.get("clicker_sessions",0)),
        ("🎰","מכונת מזל","#ff7c00","rgba(255,124,0,.3)","סובב ונסה לפגוע בג'קפוט!",f"זכיות: {st.session_state.get('slot_wins',0)}",st.session_state.get("slot_spins",0)),
    ]
    cols = st.columns(3)
    for i,(ico,name,col,glow,desc,best,played) in enumerate(games):
        with cols[i%3]:
            st.markdown(f"""
            <div class='card' style='border-color:{col}40;background:linear-gradient(135deg,{glow.replace(".3","0.05")} 0%,var(--card) 100%);text-align:center;padding:28px 20px;'>
                <div style='font-size:52px;filter:drop-shadow(0 0 15px {glow});animation:flt {1.5+i*.3:.1f}s ease-in-out infinite'>{ico}</div>
                <h3 style='font-family:Orbitron,sans-serif;font-size:15px;color:{col};text-shadow:0 0 15px {glow};margin:12px 0 8px'>{name}</h3>
                <p style='color:#8888aa;font-size:12px;margin:0 0 12px;line-height:1.5'>{desc}</p>
                <div style='display:flex;justify-content:space-between;font-size:11px'>
                    <span style='color:{col}'>🏆 {best}</span>
                    <span style='color:#666'>🎮 {played}</span>
                </div>
            </div><br>""", unsafe_allow_html=True)

    achs = st.session_state.get("achievements",[])
    if achs:
        st.markdown("<hr>### 🏆 הישגים", unsafe_allow_html=False)
        badges = "".join(f"<span class='ach'>🏅 {a}</span>" for a in achs[-10:])
        st.markdown(f"<div style='display:flex;flex-wrap:wrap'>{badges}</div>", unsafe_allow_html=True)

    if "daily_claimed" not in st.session_state:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<div class='inf'>🎁 יש לך בונוס יומי! לחץ למטה לקבל 50 מטבעות</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        _,c2,_ = st.columns([1,2,1])
        with c2:
            st.markdown('<div class="btn-gold">', unsafe_allow_html=True)
            if st.button("🎁 קבל בונוס יומי — 50 מטבעות!", use_container_width=True):
                add_coins(50); add_xp(10)
                st.session_state["daily_claimed"] = True
                add_achievement("🎁 בונוס יומי ראשון!")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────
# PAGE: SNAKE
# ─────────────────────────────────────────
def page_snake():
    st.markdown("<h1 style='text-align:center'>🐍 נחש</h1><p style='text-align:center;color:#8888aa'>חצים / WASD לשליטה</p>", unsafe_allow_html=True)

    ups=[]
    if has_upgrade("snake_wall_pass"):  ups.append("🌀 מעבר קירות")
    if has_upgrade("snake_extra_life"): ups.append("💚 3 חיים")
    if has_upgrade("snake_speed_up"):   ups.append("⚡ מהירות+")
    if ups: st.markdown(f"<div class='inf'>✅ שדרוגים: {' | '.join(ups)}</div>", unsafe_allow_html=True)

    wall_pass   = "true"  if has_upgrade("snake_wall_pass")   else "false"
    extra_lives = "3"     if has_upgrade("snake_extra_life")  else "1"
    speed_boost = "true"  if has_upgrade("snake_speed_up")    else "false"
    high = st.session_state.get("snake_high_score", 0)

    _,col2,_ = st.columns([1,3,1])
    with col2:
        components.html(f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0a0a1a;display:flex;flex-direction:column;align-items:center;font-family:Orbitron,monospace;padding:8px;color:#e8e8ff}}
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');
.hud{{display:flex;gap:14px;margin-bottom:8px;font-size:13px;font-weight:700}}
.hud-i{{background:rgba(0,245,255,.1);border:1px solid rgba(0,245,255,.3);border-radius:8px;padding:5px 12px;color:#00f5ff}}
canvas{{border:2px solid rgba(0,245,255,.4);border-radius:12px;box-shadow:0 0 40px rgba(0,245,255,.15);display:block}}
.ov{{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);background:rgba(0,0,0,.9);border:2px solid #00f5ff;border-radius:14px;padding:22px 30px;text-align:center}}
.ov h2{{color:#00f5ff;font-size:20px;margin-bottom:10px}}
.ov p{{color:#8888aa;font-size:13px;margin-bottom:14px}}
.ov button{{background:linear-gradient(135deg,rgba(0,245,255,.3),rgba(0,245,255,.1));color:#00f5ff;border:1px solid #00f5ff;padding:9px 22px;border-radius:8px;cursor:pointer;font-family:Orbitron;font-size:13px;font-weight:700}}
.ov button:hover{{background:rgba(0,245,255,.4)}}
.wrap{{position:relative}}
</style></head><body>
<div class="hud">
  <div class="hud-i">ניקוד: <span id="sc">0</span></div>
  <div class="hud-i">שיא: <span id="hi">{high}</span></div>
  <div class="hud-i">חיים: <span id="lv">{extra_lives}</span></div>
  <div class="hud-i">מהירות: <span id="sp">1</span></div>
</div>
<div class="wrap">
<canvas id="c" width="400" height="400"></canvas>
<div class="ov" id="ov">
  <h2 id="ot">🐍 נחש</h2><p id="ob">לחץ שחק להתחיל</p>
  <button onclick="startGame()">▶ שחק</button>
</div>
</div>
<script>
const G=20,C=20,WP={wall_pass},SB={speed_boost},ML={extra_lives};
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
let sn,dir,nd,food,bon,score,lives,speed,loop,run,parts;
function startGame(){{
  document.getElementById('ov').style.display='none';
  sn=[{{x:10,y:10}},{{x:9,y:10}},{{x:8,y:10}}];
  dir={{x:1,y:0}};nd={{x:1,y:0}};
  score=0;lives=ML;speed=1;parts=[];bon=null;run=true;
  document.getElementById('sc').textContent='0';
  document.getElementById('lv').textContent=lives;
  document.getElementById('sp').textContent='1';
  placeFood();
  if(loop)clearInterval(loop);
  loop=setInterval(update,SB?120:150);
}}
let ndir={{x:1,y:0}};
document.addEventListener('keydown',e=>{{
  const k={{ArrowUp:{{x:0,y:-1}},ArrowDown:{{x:0,y:1}},ArrowLeft:{{x:-1,y:0}},ArrowRight:{{x:1,y:0}},
            w:{{x:0,y:-1}},s:{{x:0,y:1}},a:{{x:-1,y:0}},d:{{x:1,y:0}},
            W:{{x:0,y:-1}},S:{{x:0,y:1}},A:{{x:-1,y:0}},D:{{x:1,y:0}}}};
  if(k[e.key]){{const n=k[e.key];if(n.x!=-dir.x||n.y!=-dir.y)ndir=n;e.preventDefault();}}
}});
function placeFood(){{
  let p;do{{p={{x:Math.floor(Math.random()*G),y:Math.floor(Math.random()*G)}}}}while(sn.some(s=>s.x==p.x&&s.y==p.y));
  food=p;
  if(score>0&&score%50==0&&!bon){{
    let b;do{{b={{x:Math.floor(Math.random()*G),y:Math.floor(Math.random()*G)}}}}while(sn.some(s=>s.x==b.x&&s.y==b.y));
    bon={{...b,t:80}};
  }}
}}
function spark(x,y,col){{for(let i=0;i<8;i++)parts.push({{x:x*C+C/2,y:y*C+C/2,vx:(Math.random()-.5)*4,vy:(Math.random()-.5)*4,l:30,c:col}});}}
function update(){{
  if(!run)return;dir={{...ndir}};
  let h={{x:sn[0].x+dir.x,y:sn[0].y+dir.y}};
  if(WP){{h.x=(h.x+G)%G;h.y=(h.y+G)%G;}}
  else if(h.x<0||h.x>=G||h.y<0||h.y>=G){{die();return;}}
  if(sn.slice(1).some(s=>s.x==h.x&&s.y==h.y)){{die();return;}}
  sn.unshift(h);
  let grew=false;
  if(h.x==food.x&&h.y==food.y){{
    score+=10;grew=true;spark(food.x,food.y,'#39ff14');placeFood();
    let ns=1+Math.floor(score/50);
    if(ns>speed){{speed=ns;clearInterval(loop);loop=setInterval(update,Math.max(60,(SB?120:150)-speed*15));document.getElementById('sp').textContent=speed;}}
    document.getElementById('sc').textContent=score;
  }}
  if(bon&&h.x==bon.x&&h.y==bon.y){{score+=50;grew=true;spark(bon.x,bon.y,'#ffd60a');bon=null;document.getElementById('sc').textContent=score;}}
  if(!grew)sn.pop();
  if(bon)bon.t--;if(bon&&bon.t<=0)bon=null;
  parts=parts.filter(p=>p.l>0);parts.forEach(p=>{{p.x+=p.vx;p.y+=p.vy;p.l--;}});
  draw();
}}
function die(){{
  lives--;document.getElementById('lv').textContent=lives;
  if(lives<=0){{
    run=false;clearInterval(loop);
    let hs=parseInt(document.getElementById('hi').textContent)||0;
    if(score>hs)document.getElementById('hi').textContent=score;
    document.getElementById('ot').textContent='💀 משחק הסתיים!';
    document.getElementById('ob').textContent='ניקוד: '+score;
    document.getElementById('ov').style.display='block';
  }}else{{sn=[{{x:10,y:10}},{{x:9,y:10}},{{x:8,y:10}}];dir={{x:1,y:0}};ndir={{x:1,y:0}};}}
}}
function rr(ctx,x,y,w,h,r){{ctx.beginPath();ctx.moveTo(x+r,y);ctx.lineTo(x+w-r,y);ctx.quadraticCurveTo(x+w,y,x+w,y+r);ctx.lineTo(x+w,y+h-r);ctx.quadraticCurveTo(x+w,y+h,x+w-r,y+h);ctx.lineTo(x+r,y+h);ctx.quadraticCurveTo(x,y+h,x,y+h-r);ctx.lineTo(x,y+r);ctx.quadraticCurveTo(x,y,x+r,y);ctx.closePath();}}
function draw(){{
  ctx.fillStyle='#0a0a14';ctx.fillRect(0,0,400,400);
  ctx.strokeStyle='rgba(0,245,255,.04)';ctx.lineWidth=.5;
  for(let i=0;i<=G;i++){{ctx.beginPath();ctx.moveTo(i*C,0);ctx.lineTo(i*C,400);ctx.stroke();ctx.beginPath();ctx.moveTo(0,i*C);ctx.lineTo(400,i*C);ctx.stroke();}}
  parts.forEach(p=>{{ctx.globalAlpha=p.l/30;ctx.fillStyle=p.c;ctx.beginPath();ctx.arc(p.x,p.y,3,0,Math.PI*2);ctx.fill();}});
  ctx.globalAlpha=1;
  let t=Date.now()/300;
  ctx.save();ctx.translate(food.x*C+C/2,food.y*C+C/2);ctx.scale(1+Math.sin(t)*.15,1+Math.sin(t)*.15);
  ctx.shadowBlur=20;ctx.shadowColor='#39ff14';ctx.fillStyle='#39ff14';
  ctx.beginPath();ctx.arc(0,0,C/2-2,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;ctx.restore();
  if(bon){{
    ctx.save();ctx.translate(bon.x*C+C/2,bon.y*C+C/2);let p=Math.sin(Date.now()/150);
    ctx.scale(1+p*.2,1+p*.2);ctx.shadowBlur=25;ctx.shadowColor='#ffd60a';
    ctx.font=(C-2)+'px serif';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('⭐',0,0);
    ctx.restore();ctx.fillStyle='rgba(255,214,10,'+bon.t/80+')';ctx.fillRect(bon.x*C,bon.y*C-3,C*(bon.t/80),2);
  }}
  sn.forEach((seg,i)=>{{
    let rat=i/sn.length;
    ctx.save();
    if(i==0){{ctx.shadowBlur=15;ctx.shadowColor='rgba(0,245,255,.8)';}}
    ctx.fillStyle=i==0?'#ffffff':`rgba(${{Math.floor(0+rat*0)}},${{Math.floor(245-rat*100)}},255,.9)`;
    let pd=i==0?1:2,rd=i==0?6:4;rr(ctx,seg.x*C+pd,seg.y*C+pd,C-pd*2,C-pd*2,rd);ctx.fill();
    ctx.restore();
    if(i==0){{
      ctx.fillStyle='#0a0a14';
      ctx.beginPath();ctx.arc(seg.x*C+C*.3+dir.y*C*.2,seg.y*C+C*.3-dir.x*C*.2,2.5,0,Math.PI*2);ctx.fill();
      ctx.beginPath();ctx.arc(seg.x*C+C*.7-dir.y*C*.2,seg.y*C+C*.3-dir.x*C*.2,2.5,0,Math.PI*2);ctx.fill();
    }}
  }});
}}
ctx.fillStyle='#0a0a14';ctx.fillRect(0,0,400,400);
</script></body></html>""", height=510, scrolling=False)

    _,c2,_ = st.columns([1,2,1])
    with c2:
        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        if st.button("▶ התחל משחק חדש", use_container_width=True, key="sn_start"):
            st.session_state["snake_games_played"] += 1
            e = add_coins(5); add_xp(5)
            st.toast(f"🐍 +{e} 🪙")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 🏆 דווח ניקוד")
    c1,c2 = st.columns([3,1])
    with c1: sc = st.number_input("ניקוד", 0, 9999, 0, key="sn_sc", label_visibility="collapsed")
    with c2:
        st.markdown('<div class="btn-gold">', unsafe_allow_html=True)
        if st.button("✔", key="sn_ok"):
            if sc > 0:
                e = add_coins(sc//2); add_xp(sc//5)
                if sc > st.session_state.get("snake_high_score",0):
                    st.session_state["snake_high_score"] = sc
                    add_achievement(f"🐍 שיא נחש: {sc}!")
                st.markdown(f"<div class='ok'>+{e} 🪙 על {sc} ניקוד!</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    c1,c2 = st.columns(2)
    with c1: st.metric("🏆 שיא", st.session_state.get("snake_high_score",0))
    with c2: st.metric("🎮 משחקים", st.session_state.get("snake_games_played",0))

# ─────────────────────────────────────────
# PAGE: FLAPPY
# ─────────────────────────────────────────
def page_flappy():
    st.markdown("<h1 style='text-align:center'>🐦 פלאפי בירד</h1><p style='text-align:center;color:#8888aa'>SPACE / לחיצה לעוף</p>", unsafe_allow_html=True)

    slow    = "true" if has_upgrade("flappy_slow_pipes") else "false"
    big_gap = "true" if has_upgrade("flappy_big_gap")   else "false"
    shield  = "true" if has_upgrade("flappy_shield")    else "false"
    high = st.session_state.get("flappy_high_score", 0)

    _,c2,_ = st.columns([1,3,1])
    with c2:
        components.html(f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0a0a1a;display:flex;flex-direction:column;align-items:center;padding:8px;font-family:Orbitron,monospace;color:#e8e8ff}}
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');
.hud{{display:flex;gap:14px;margin-bottom:8px;font-size:13px;font-weight:700}}
.hud-i{{background:rgba(255,214,10,.1);border:1px solid rgba(255,214,10,.3);border-radius:8px;padding:5px 12px;color:#ffd60a}}
canvas{{border:2px solid rgba(255,214,10,.4);border-radius:12px;box-shadow:0 0 40px rgba(255,214,10,.15);cursor:pointer;display:block}}
.ov{{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);background:rgba(0,0,0,.9);border:2px solid #ffd60a;border-radius:14px;padding:22px 30px;text-align:center;min-width:190px}}
.ov h2{{color:#ffd60a;font-size:19px;margin-bottom:10px}}.ov p{{color:#8888aa;font-size:12px;margin-bottom:14px}}
.ov button{{background:linear-gradient(135deg,rgba(255,214,10,.3),rgba(255,214,10,.1));color:#ffd60a;border:1px solid #ffd60a;padding:9px 22px;border-radius:8px;cursor:pointer;font-family:Orbitron;font-size:13px;font-weight:700}}
.wrap{{position:relative}}
</style></head><body>
<div class="hud">
  <div class="hud-i">ניקוד: <span id="sc">0</span></div>
  <div class="hud-i">שיא: <span id="hi">{high}</span></div>
  <div class="hud-i" id="sh-hud" style="display:{('flex' if has_upgrade('flappy_shield') else 'none')}">🛡️ <span id="sh">1</span></div>
</div>
<div class="wrap">
<canvas id="c" width="360" height="480"></canvas>
<div class="ov" id="ov">
  <h2 id="ot">🐦 פלאפי בירד</h2><p id="ob">לחץ SPACE או לחץ להתחיל</p>
  <button onclick="startGame()">▶ שחק</button>
</div>
</div>
<script>
const W=360,H=480,BR=14;
const SLOW={slow},BIG={big_gap};
let SHIELD={shield};
const PS=SLOW?1.8:2.5,GAP=BIG?160:120;
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
let bird,pipes,score,frame,run,raf,shUsed,parts,stars,gOff;
function mkStars(){{stars=[];for(let i=0;i<60;i++)stars.push({{x:Math.random()*W,y:Math.random()*H*.8,r:Math.random()*1.5+.5,s:Math.random()*.3+.1}});}}
function startGame(){{
  document.getElementById('ov').style.display='none';
  bird={{x:80,y:H/2,vy:0,rot:0,sh:SHIELD?1:0}};
  pipes=[];score=0;frame=0;run=true;shUsed=false;parts=[];gOff=0;
  document.getElementById('sc').textContent='0';
  if(raf)cancelAnimationFrame(raf);mkStars();loop();
}}
function flap(){{if(run)bird.vy=-7;}}
cv.addEventListener('click',flap);
document.addEventListener('keydown',e=>{{if(e.code=='Space'){{flap();e.preventDefault();}}}});
function loop(){{if(!run)return;update();draw();raf=requestAnimationFrame(loop);}}
function update(){{
  frame++;gOff=(gOff+PS)%(W*2);
  bird.vy+=.35;bird.y+=bird.vy;bird.rot=Math.min(Math.max(bird.vy*3,-30),90);
  parts=parts.filter(p=>p.l>0);parts.forEach(p=>{{p.x+=p.vx;p.y+=p.vy;p.l--;p.vy+=.1;}});
  stars.forEach(s=>{{s.x-=s.s;if(s.x<0)s.x=W;}});
  if(frame%80==0){{let th=60+Math.random()*(H-GAP-120);pipes.push({{x:W,th,ok:false}});}}
  pipes.forEach(p=>p.x-=PS);pipes=pipes.filter(p=>p.x>-80);
  pipes.forEach(p=>{{
    if(!p.ok&&p.x+40<bird.x){{p.ok=true;score++;document.getElementById('sc').textContent=score;for(let i=0;i<6;i++)parts.push({{x:bird.x,y:bird.y,vx:(Math.random()-.5)*4,vy:-Math.random()*4,l:25,c:'#ffd60a'}});}}
    if(bird.x+BR>p.x&&bird.x-BR<p.x+52){{
      if(bird.y-BR<p.th||bird.y+BR>p.th+GAP){{
        if(bird.sh>0&&!shUsed){{shUsed=true;bird.sh=0;document.getElementById('sh').textContent='0';for(let i=0;i<15;i++)parts.push({{x:bird.x,y:bird.y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,l:30,c:'#00f5ff'}});}}
        else die();
      }}
    }}
  }});
  if(bird.y+BR>H-30||bird.y-BR<0)die();
}}
function die(){{
  run=false;cancelAnimationFrame(raf);
  let hs=parseInt(document.getElementById('hi').textContent)||0;
  if(score>hs)document.getElementById('hi').textContent=score;
  document.getElementById('ot').textContent='💥 נפלת!';
  document.getElementById('ob').textContent='ניקוד: '+score+' | שיא: '+Math.max(score,hs);
  document.getElementById('ov').style.display='block';
}}
function pipe(x,th){{
  let g=ctx.createLinearGradient(x,0,x+52,0);g.addColorStop(0,'#1a5c1a');g.addColorStop(.5,'#2d8f2d');g.addColorStop(1,'#1a5c1a');
  ctx.fillStyle=g;ctx.fillRect(x,0,52,th);ctx.fillStyle='#3aaf3a';ctx.fillRect(x-4,th-20,60,20);
  let bot=th+GAP;ctx.fillStyle=g;ctx.fillRect(x,bot,52,H-bot);ctx.fillStyle='#3aaf3a';ctx.fillRect(x-4,bot,60,20);
  ctx.shadowBlur=10;ctx.shadowColor='rgba(57,255,20,.4)';ctx.strokeStyle='rgba(57,255,20,.3)';ctx.lineWidth=1;
  ctx.strokeRect(x,0,52,th);ctx.strokeRect(x,bot,52,H-bot);ctx.shadowBlur=0;
}}
function draw(){{
  let sky=ctx.createLinearGradient(0,0,0,H);sky.addColorStop(0,'#050510');sky.addColorStop(.7,'#0a0a2a');sky.addColorStop(1,'#0d1a0d');
  ctx.fillStyle=sky;ctx.fillRect(0,0,W,H);
  stars.forEach(s=>{{ctx.globalAlpha=.6+Math.sin(frame*.05+s.x)*.4;ctx.fillStyle='#fff';ctx.beginPath();ctx.arc(s.x,s.y,s.r,0,Math.PI*2);ctx.fill();}});
  ctx.globalAlpha=1;
  parts.forEach(p=>{{ctx.globalAlpha=p.l/30;ctx.fillStyle=p.c;ctx.beginPath();ctx.arc(p.x,p.y,3,0,Math.PI*2);ctx.fill();}});
  ctx.globalAlpha=1;
  pipes.forEach(p=>pipe(p.x,p.th));
  ctx.fillStyle='#1a3a0a';ctx.fillRect(0,H-30,W,30);ctx.fillStyle='#2d5c14';ctx.fillRect(0,H-30,W,8);
  ctx.save();ctx.translate(bird.x,bird.y);ctx.rotate(bird.rot*Math.PI/180);
  if(SHIELD&&!shUsed){{ctx.beginPath();ctx.arc(0,0,BR+8,0,Math.PI*2);ctx.strokeStyle='rgba(0,245,255,'+(0.4+Math.sin(frame*.15)*.3)+')';ctx.lineWidth=2;ctx.stroke();}}
  ctx.shadowBlur=12;ctx.shadowColor='#ffd60a';ctx.fillStyle='#ffd60a';ctx.beginPath();ctx.ellipse(0,0,BR,BR-2,0,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='#ff9500';ctx.beginPath();ctx.ellipse(-4,2,8,5,Math.PI/4+Math.sin(frame*.3)*.4,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='white';ctx.beginPath();ctx.arc(6,-2,4,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='#1a1a2e';ctx.beginPath();ctx.arc(7,-2,2.5,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='white';ctx.beginPath();ctx.arc(8,-3,1,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='#ff6600';ctx.beginPath();ctx.moveTo(BR,0);ctx.lineTo(BR+7,2);ctx.lineTo(BR,-2);ctx.fill();
  ctx.shadowBlur=0;ctx.restore();
  ctx.fillStyle='rgba(255,214,10,.9)';ctx.font='700 28px Orbitron,monospace';ctx.textAlign='center';
  ctx.shadowBlur=15;ctx.shadowColor='#ffd60a';ctx.fillText(score,W/2,50);ctx.shadowBlur=0;
}}
mkStars();
let sk=ctx.createLinearGradient(0,0,0,H);sk.addColorStop(0,'#050510');sk.addColorStop(1,'#0a0a2a');ctx.fillStyle=sk;ctx.fillRect(0,0,W,H);
</script></body></html>""", height=550, scrolling=False)

    _,c2,_ = st.columns([1,2,1])
    with c2:
        st.markdown('<div class="btn-gold">', unsafe_allow_html=True)
        if st.button("▶ התחל", use_container_width=True, key="fl_start"):
            st.session_state["flappy_games_played"] += 1
            add_coins(5); add_xp(5); st.toast("🐦 +5 🪙")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 🏆 דווח ניקוד")
    c1,c2 = st.columns([3,1])
    with c1: sc = st.number_input("ניקוד", 0, 999, 0, key="fl_sc", label_visibility="collapsed")
    with c2:
        st.markdown('<div class="btn-gold">', unsafe_allow_html=True)
        if st.button("✔", key="fl_ok"):
            if sc > 0:
                e = add_coins(sc*5); add_xp(sc*2)
                if sc > st.session_state.get("flappy_high_score",0):
                    st.session_state["flappy_high_score"] = sc
                    add_achievement(f"🐦 שיא פלאפי: {sc}!")
                st.markdown(f"<div class='ok'>+{e} 🪙!</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    c1,c2 = st.columns(2)
    with c1: st.metric("🏆 שיא", st.session_state.get("flappy_high_score",0))
    with c2: st.metric("🎮 משחקים", st.session_state.get("flappy_games_played",0))

# ─────────────────────────────────────────
# PAGE: MEMORY
# ─────────────────────────────────────────
MEM_EMOJIS = ["🐉","🦄","🔥","⚡","🌟","💎","🎭","🚀","🌊","🎸","🦋","🍄","🎯","🏆","🌈","🎪"]

def _mem_reset():
    chosen = random.sample(MEM_EMOJIS, 8)
    board  = chosen * 2; random.shuffle(board)
    st.session_state["mb"]  = board
    st.session_state["mf"]  = []
    st.session_state["mm"]  = set()
    st.session_state["mov"] = 0
    st.session_state["mcp"] = False
    st.session_state["mh"]  = 3 if has_upgrade("memory_hint") else 0

def page_memory():
    st.markdown("<h1 style='text-align:center'>🧠 משחק זיכרון</h1><p style='text-align:center;color:#8888aa'>מצא את כל הזוגות!</p>", unsafe_allow_html=True)
    if has_upgrade("memory_x2"): st.markdown("<div class='inf'>✨ כפל ניקוד פעיל!</div>", unsafe_allow_html=True)
    if "mb" not in st.session_state: _mem_reset()

    board   = st.session_state["mb"]
    flipped = st.session_state["mf"]
    matched = st.session_state["mm"]
    moves   = st.session_state["mov"]
    hints   = st.session_state["mh"]

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.metric("🎯 מהלכים", moves)
    with c2: st.metric("✅ זוגות",   len(matched)//2)
    with c3: st.metric("🃏 נותרו",   8 - len(matched)//2)
    with c4: st.metric("💡 רמזים",   hints)
    st.markdown("<br>", unsafe_allow_html=True)

    # Win
    if len(matched) == len(board):
        sc = max(100 - moves*3, 10) * (2 if has_upgrade("memory_x2") else 1)
        e  = add_coins(sc); add_xp(sc//2)
        st.session_state["memory_games_played"] = st.session_state.get("memory_games_played",0) + 1
        if sc > st.session_state.get("memory_high_score",0):
            st.session_state["memory_high_score"] = sc
            add_achievement(f"🧠 שיא זיכרון: {sc}!")
        st.markdown(f"<div class='ok' style='font-size:18px;padding:24px'>🎉 סיימת ב-{moves} מהלכים! +{e} 🪙</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        _,c2,_ = st.columns([1,2,1])
        with c2:
            st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
            if st.button("🔄 משחק חדש", use_container_width=True, key="mr"):
                _mem_reset(); st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        return

    # Pending reveal
    if st.session_state.get("mcp"):
        time.sleep(0.4)
        f = st.session_state["mf"]
        if len(f) == 2:
            i1,i2 = f
            if board[i1] == board[i2]: matched.add(i1); matched.add(i2); st.session_state["mm"] = matched
        st.session_state["mf"] = []; st.session_state["mcp"] = False; st.rerun()

    # Grid
    for row in range(4):
        cols = st.columns(4)
        for ci in range(4):
            idx = row*4+ci
            with cols[ci]:
                is_flip = idx in flipped or idx in matched
                is_mat  = idx in matched
                if is_flip:
                    color = "rgba(57,255,20,.2)" if is_mat else "rgba(0,245,255,.12)"
                    border= "rgba(57,255,20,.6)"  if is_mat else "rgba(0,245,255,.5)"
                    anim  = "matchP .4s ease" if is_mat else "flipIn .25s ease"
                    st.markdown(f"""
                    <div style='aspect-ratio:1;min-height:80px;background:{color};border:2px solid {border};
                         border-radius:12px;display:flex;align-items:center;justify-content:center;
                         font-size:36px;animation:{anim};'>{board[idx]}</div>
                    <style>
                    @keyframes matchP{{0%{{transform:scale(1)}}50%{{transform:scale(1.12)}}100%{{transform:scale(1)}}}}
                    @keyframes flipIn{{from{{transform:rotateY(90deg);opacity:0}}to{{transform:rotateY(0);opacity:1}}}}
                    </style>""", unsafe_allow_html=True)
                else:
                    if st.button("❓", key=f"mc_{idx}", use_container_width=True):
                        if idx not in matched and idx not in flipped and len(flipped) < 2:
                            flipped.append(idx); st.session_state["mf"] = flipped
                            if len(flipped) == 2:
                                st.session_state["mov"] = moves + 1
                                st.session_state["mcp"] = True
                            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    with c1:
        st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
        if st.button("🔄 איפוס", use_container_width=True, key="mem_rst"): _mem_reset(); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        if hints > 0:
            st.markdown('<div class="btn-gold">', unsafe_allow_html=True)
            if st.button(f"💡 רמז ({hints})", use_container_width=True, key="mem_ht"):
                un = [i for i in range(len(board)) if i not in matched]
                seen = {}
                for i in un:
                    e = board[i]
                    if e in seen:
                        st.session_state["mf"] = [seen[e], i]
                        st.session_state["mcp"] = True
                        st.session_state["mh"] -= 1
                        st.rerun(); break
                    seen[e] = i
            st.markdown('</div>', unsafe_allow_html=True)
    with c3: st.metric("🏆 שיא", st.session_state.get("memory_high_score",0))

# ─────────────────────────────────────────
# PAGE: TIC TAC TOE
# ─────────────────────────────────────────
def _ttt_reset():
    st.session_state["tb"] = [""]*9
    st.session_state["to"] = False
    st.session_state["ts"] = ""
    st.session_state["tp"] = None

def _ttt_winner(b):
    for a,bx,c in [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]:
        if b[a] and b[a]==b[bx]==b[c]: return b[a]
    return None

def _minimax(b, is_max, depth):
    w = _ttt_winner(b)
    if w=="O": return 10-depth
    if w=="X": return depth-10
    emp = [i for i,v in enumerate(b) if v==""]
    if not emp: return 0
    if is_max:
        best=-1000
        for i in emp: b[i]="O"; best=max(best,_minimax(b,False,depth+1)); b[i]=""
        return best
    else:
        best=1000
        for i in emp: b[i]="X"; best=min(best,_minimax(b,True,depth+1)); b[i]=""
        return best

def _ai_move(b):
    diff = st.session_state.get("ttt_diff","בינוני")
    emp  = [i for i,v in enumerate(b) if v==""]
    if not emp: return None
    if diff=="קל": return random.choice(emp)
    if diff=="בינוני" and random.random()<.3: return random.choice(emp)
    bst=-1000; mv=None
    for i in emp:
        b[i]="O"; s=_minimax(b,False,0); b[i]=""
        if s>bst: bst=s; mv=i
    return mv

def page_tictactoe():
    st.markdown("<h1 style='text-align:center'>❌ איקס עיגול</h1><p style='text-align:center;color:#8888aa'>אתה X, המחשב O</p>", unsafe_allow_html=True)

    ups=[]
    if has_upgrade("ttt_undo"):    ups.append("↩️ ביטול")
    if has_upgrade("ttt_preview"): ups.append("🔮 תצוגה מקדימה")
    if ups: st.markdown(f"<div class='inf'>✅ {' | '.join(ups)}</div>", unsafe_allow_html=True)

    if "tb" not in st.session_state: _ttt_reset()
    b  = st.session_state["tb"]
    ov = st.session_state["to"]
    st_ = st.session_state["ts"]
    prev = st.session_state.get("tp")

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.metric("✅ נצחונות", st.session_state.get("ttt_wins",0))
    with c2: st.metric("❌ הפסדים",  st.session_state.get("ttt_losses",0))
    with c3: st.metric("🤝 תיקו",    st.session_state.get("ttt_draws",0))
    with c4: st.metric("🎮 משחקים",  st.session_state.get("ttt_games_played",0))
    st.markdown("<br>", unsafe_allow_html=True)

    if st_:
        css = "ok" if "ניצחת" in st_ else ("err" if "הפסדת" in st_ else "inf")
        st.markdown(f"<div class='{css}' style='font-size:17px;padding:18px'>{st_}</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    if has_upgrade("ttt_preview") and not ov:
        am = _ai_move(b[:])
        if am is not None:
            st.markdown(f"<div style='color:#bf5fff;font-size:12px;text-align:center;margin-bottom:8px'>🔮 AI מתכנן מיקום {am+1}</div>", unsafe_allow_html=True)

    _,mc,_ = st.columns([1,2,1])
    with mc:
        for row in range(3):
            rcols = st.columns(3)
            for ci in range(3):
                idx = row*3+ci
                with rcols[ci]:
                    cell = b[idx]
                    if cell=="X":
                        st.markdown("""<div style='min-height:90px;background:linear-gradient(135deg,rgba(0,245,255,.15),rgba(0,245,255,.03));
                            border:2px solid rgba(0,245,255,.5);border-radius:14px;display:flex;align-items:center;justify-content:center;
                            font-size:44px;font-weight:900;color:#00f5ff;text-shadow:0 0 20px rgba(0,245,255,.8);
                            animation:pop .2s cubic-bezier(.34,1.56,.64,1);'>✕</div>
                            <style>@keyframes pop{from{transform:scale(.3);opacity:0}to{transform:scale(1);opacity:1}}</style>""",
                            unsafe_allow_html=True)
                    elif cell=="O":
                        st.markdown("""<div style='min-height:90px;background:linear-gradient(135deg,rgba(255,0,110,.15),rgba(255,0,110,.03));
                            border:2px solid rgba(255,0,110,.5);border-radius:14px;display:flex;align-items:center;justify-content:center;
                            font-size:44px;font-weight:900;color:#ff006e;text-shadow:0 0 20px rgba(255,0,110,.8);'>○</div>""",
                            unsafe_allow_html=True)
                    else:
                        if not ov and st.button(" ", key=f"tt_{idx}", use_container_width=True):
                            st.session_state["tp"] = b[:]
                            b[idx] = "X"
                            w = _ttt_winner(b)
                            if w: _ttt_end(w, b); return
                            if "" not in b: _ttt_end("draw", b); return
                            ai = _ai_move(b)
                            if ai is not None:
                                b[ai] = "O"
                                w = _ttt_winner(b)
                                if w: _ttt_end(w, b); return
                                if "" not in b: _ttt_end("draw", b); return
                            st.session_state["tb"] = b
                            st.rerun()
                        elif ov:
                            st.markdown("""<div style='min-height:90px;background:rgba(255,255,255,.01);
                                border:2px solid rgba(255,255,255,.05);border-radius:14px;'></div>""",
                                unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    with c1:
        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        if st.button("🔄 חדש", use_container_width=True, key="ttt_new"): _ttt_reset(); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        if has_upgrade("ttt_undo") and prev and not ov:
            st.markdown('<div class="btn-gold">', unsafe_allow_html=True)
            if st.button("↩️ ביטול", use_container_width=True, key="ttt_undo_btn"):
                st.session_state["tb"] = prev; st.session_state["tp"] = None; st.session_state["ts"] = ""; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    with c3:
        st.selectbox("קושי", ["קל","בינוני","קשה"], key="ttt_diff")

def _ttt_end(result, b):
    st.session_state["ttt_games_played"] = st.session_state.get("ttt_games_played",0) + 1
    st.session_state["to"] = True; st.session_state["tb"] = b
    if result=="X":
        st.session_state["ttt_wins"] = st.session_state.get("ttt_wins",0) + 1
        e = add_coins(50); add_xp(25); st.session_state["ts"] = f"🎉 ניצחת! +{e} 🪙"
        add_achievement("❌ ניצחת את ה-AI!")
    elif result=="O":
        st.session_state["ttt_losses"] = st.session_state.get("ttt_losses",0) + 1
        e = add_coins(10); st.session_state["ts"] = f"😅 הפסדת... +{e} 🪙"
    else:
        st.session_state["ttt_draws"] = st.session_state.get("ttt_draws",0) + 1
        e = add_coins(20); add_xp(10); st.session_state["ts"] = f"🤝 תיקו! +{e} 🪙"
    st.rerun()

# ─────────────────────────────────────────
# PAGE: CLICKER
# ─────────────────────────────────────────
def page_clicker():
    st.markdown("<h1 style='text-align:center'>👆 קליקר</h1><p style='text-align:center;color:#8888aa'>לחץ כמה שיותר ב-10 שניות!</p>", unsafe_allow_html=True)

    mul  = 3 if has_upgrade("clicker_multiplier") else 1
    auto = has_upgrade("clicker_auto")
    ups  = []
    if mul>1: ups.append("🔢 x3")
    if auto:  ups.append("🤖 אוטו")
    if ups: st.markdown(f"<div class='inf'>✅ {' | '.join(ups)}</div>", unsafe_allow_html=True)

    if "ck_state" not in st.session_state:
        st.session_state["ck_state"] = "idle"
        st.session_state["ck_cnt"]   = 0
        st.session_state["ck_start"] = 0

    state = st.session_state["ck_state"]
    count = st.session_state["ck_cnt"]
    best  = st.session_state.get("clicker_best", 0)

    if state == "playing":
        elapsed   = time.time() - st.session_state["ck_start"]
        remaining = max(0, 10 - elapsed)
        if auto and int(elapsed*2) > int((elapsed - 0.05)*2):
            st.session_state["ck_cnt"] += mul; count = st.session_state["ck_cnt"]
        col = "#ff006e"
        anim = "flashR .2s infinite" if remaining < 3 else "none"
        st.markdown(f"""
        <div style='text-align:center;margin-bottom:14px'>
            <div style='font-family:Orbitron,sans-serif;font-size:60px;font-weight:900;color:{col};
                 text-shadow:0 0 30px {col}cc;animation:{anim};'>{remaining:.1f}</div>
            <div style='color:#8888aa;font-size:12px'>שניות</div>
        </div>
        <style>@keyframes flashR{{0%,100%{{color:#ff006e}}50%{{color:#ff4444}}}}</style>""",
        unsafe_allow_html=True)
        st.progress(remaining/10)
        if remaining <= 0: st.session_state["ck_state"] = "done"; st.rerun()

    click_color = "#ff006e" if state=="playing" else ("#39ff14" if state=="done" else "#8888aa")
    st.markdown(f"""
    <div style='text-align:center;margin:14px 0'>
        <div style='font-family:Orbitron,sans-serif;font-size:80px;font-weight:900;
             color:{click_color};text-shadow:0 0 40px {click_color}80;'>{count}</div>
        <div style='color:#8888aa;font-size:13px'>קליקים</div>
    </div>""", unsafe_allow_html=True)

    _,c2,_ = st.columns([1,2,1])
    with c2:
        if state == "idle":
            st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
            if st.button("🚀 התחל!", use_container_width=True, key="ck_go"):
                st.session_state["ck_state"] = "playing"
                st.session_state["ck_cnt"]   = 0
                st.session_state["ck_start"] = time.time()
                st.session_state["clicker_sessions"] = st.session_state.get("clicker_sessions",0) + 1
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        elif state == "playing":
            st.markdown("""<style>div.cbtn button{background:linear-gradient(135deg,rgba(255,0,110,.4),rgba(255,0,110,.15))!important;
                border:2px solid rgba(255,0,110,.8)!important;color:#ff006e!important;font-size:22px!important;
                height:100px!important;font-weight:900!important;box-shadow:0 0 30px rgba(255,0,110,.3)!important;}
                div.cbtn button:hover{box-shadow:0 0 50px rgba(255,0,110,.6)!important;transform:scale(1.04)!important;}
                div.cbtn button:active{transform:scale(.96)!important;}</style>""", unsafe_allow_html=True)
            st.markdown('<div class="cbtn">', unsafe_allow_html=True)
            if st.button("👆 לחץ!", use_container_width=True, key="ck_click"):
                st.session_state["ck_cnt"] += mul
                st.session_state["clicker_total_clicks"] = st.session_state.get("clicker_total_clicks",0) + mul
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        elif state == "done":
            final = st.session_state["ck_cnt"]
            e = add_coins(final*2); add_xp(final)
            if final > best:
                st.session_state["clicker_best"] = final
                add_achievement(f"👆 שיא קליקר: {final}!")
                st.markdown(f"<div class='ok' style='font-size:17px;margin-bottom:14px'>🏆 שיא חדש! {final} קליקים! +{e} 🪙</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='inf' style='margin-bottom:14px'>{final} קליקים! +{e} 🪙 | שיא: {st.session_state.get('clicker_best',0)}</div>", unsafe_allow_html=True)
            st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
            if st.button("🔄 נסה שוב", use_container_width=True, key="ck_re"):
                st.session_state["ck_state"]="idle"; st.session_state["ck_cnt"]=0; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    if state == "playing": time.sleep(0.05); st.rerun()

    st.markdown("---")
    c1,c2,c3 = st.columns(3)
    with c1: st.metric("🏆 שיא",         st.session_state.get("clicker_best",0))
    with c2: st.metric("👆 סה\"כ קליקים", st.session_state.get("clicker_total_clicks",0))
    with c3: st.metric("🎮 סבבים",       st.session_state.get("clicker_sessions",0))

# ─────────────────────────────────────────
# PAGE: SLOT MACHINE
# ─────────────────────────────────────────
SL_SYM  = ["🍒","🍋","🍊","🍇","⭐","💎","🎰","🃏"]
SL_W    = [20,18,15,12,10,8,5,12]
SL_PAY  = {"🍒🍒🍒":5,"🍋🍋🍋":8,"🍊🍊🍊":10,"🍇🍇🍇":15,"⭐⭐⭐":20,"💎💎💎":50,"🎰🎰🎰":100,"🃏🃏🃏":30}

def page_slot():
    st.markdown("<h1 style='text-align:center'>🎰 מכונת מזל</h1><p style='text-align:center;color:#8888aa'>סובב ונסה לפגוע בג'קפוט!</p>", unsafe_allow_html=True)

    luck   = has_upgrade("slot_luck")
    jp2    = has_upgrade("slot_jackpot")
    ups    = []
    if luck: ups.append("🍀 מזל")
    if jp2:  ups.append("💰 ג'קפוט x2")
    if ups: st.markdown(f"<div class='inf'>✅ {' | '.join(ups)}</div>", unsafe_allow_html=True)

    if "sl_reels" not in st.session_state:
        st.session_state["sl_reels"]  = ["🎰","🎰","🎰"]
        st.session_state["sl_result"] = ""
        st.session_state["sl_bet"]    = 10

    reels  = st.session_state["sl_reels"]
    result = st.session_state.get("sl_result","")
    coins  = st.session_state.get("coins",0)
    is_win = "ניצחת" in result or "ג'קפוט" in result

    brd   = "rgba(255,214,10,.8)" if is_win else "rgba(255,124,0,.4)"
    glow  = "rgba(255,214,10,.35)" if is_win else "rgba(255,124,0,.1)"
    panim = "animation:jpFlash .3s infinite;" if is_win else ""
    reels_html = "".join(f"""
        <div style='flex:1;aspect-ratio:1;background:linear-gradient(180deg,#1a0a00,#0d0500);
             border:2px solid rgba(255,124,0,.4);border-radius:10px;display:flex;
             align-items:center;justify-content:center;font-size:52px;
             box-shadow:inset 0 0 20px rgba(0,0,0,.8);'>{r}</div>""" for r in reels)

    st.markdown(f"""
    <div style='max-width:420px;margin:0 auto;padding:22px;
         background:linear-gradient(135deg,#1a0d00,#2a1500,#1a0d00);
         border:3px solid {brd};border-radius:20px;
         box-shadow:0 0 40px {glow},inset 0 0 30px rgba(0,0,0,.5);{panim}'>
      <div style='text-align:center;margin-bottom:14px'>
        <span style='font-family:Orbitron,sans-serif;font-size:18px;font-weight:900;
              color:#ff7c00;text-shadow:0 0 15px rgba(255,124,0,.8);letter-spacing:3px;'>🎰 ARCADE SLOTS</span>
      </div>
      <div style='display:flex;gap:10px;justify-content:center;margin:14px 0;padding:14px;
           background:rgba(0,0,0,.5);border-radius:14px;border:1px solid rgba(255,124,0,.2);'>
        {reels_html}
      </div>
      <div style='height:3px;background:linear-gradient(90deg,transparent,{"#ffd60a" if is_win else "rgba(255,124,0,.3)"},transparent);
           {"box-shadow:0 0 10px #ffd60a;" if is_win else ""}'>
      </div>
    </div>
    <style>@keyframes jpFlash{{0%,100%{{border-color:rgba(255,214,10,.8)}}50%{{border-color:rgba(255,214,10,.2)}}}}</style>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if result:
        st.markdown(f"<div class='{'ok' if is_win else 'err'}' style='font-size:15px'>{result}</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    c1,c2 = st.columns([3,1])
    with c1:
        bet = st.slider("הימור 🪙", 5, min(100,max(coins,5)), st.session_state.get("sl_bet",10), 5, key="sl_bet_sl")
        st.session_state["sl_bet"] = bet
    with c2: st.metric("יתרה", f"{coins} 🪙")

    _,c2,_ = st.columns([1,2,1])
    with c2:
        st.markdown("""<style>div.spbtn button{background:linear-gradient(135deg,rgba(255,124,0,.4),rgba(255,124,0,.15))!important;
            border:2px solid rgba(255,124,0,.7)!important;color:#ff7c00!important;font-size:17px!important;
            height:58px!important;font-weight:900!important;box-shadow:0 0 25px rgba(255,124,0,.3)!important;}
            div.spbtn button:hover{box-shadow:0 0 40px rgba(255,124,0,.5)!important;}</style>""", unsafe_allow_html=True)
        can = coins >= bet
        st.markdown('<div class="spbtn">', unsafe_allow_html=True)
        if st.button("🎰 סובב!", use_container_width=True, key="sl_spin", disabled=not can):
            _do_spin(bet, luck, jp2)
        st.markdown('</div>', unsafe_allow_html=True)

    if not can: st.markdown("<div class='err'>אין מספיק מטבעות!</div>", unsafe_allow_html=True)

    st.markdown("---")
    with st.expander("📋 טבלת תשלומים"):
        for combo,mult in SL_PAY.items():
            am = mult*(2 if jp2 and mult>=50 else 1)
            st.markdown(f"""<div style='display:flex;justify-content:space-between;padding:5px 12px;
                background:rgba(255,124,0,.05);border-radius:8px;margin-bottom:3px'>
                <span style='font-size:20px'>{combo}</span>
                <span style='color:#ff7c00;font-weight:700;font-family:Orbitron'>x{am}</span></div>""", unsafe_allow_html=True)

    st.markdown("---")
    c1,c2,c3 = st.columns(3)
    with c1: st.metric("🎰 סיבובים", st.session_state.get("slot_spins",0))
    with c2: st.metric("🏆 זכיות",   st.session_state.get("slot_wins",0))
    with c3: st.metric("💰 סה\"כ זכה", f"{st.session_state.get('slot_total_won',0)} 🪙")

def _do_spin(bet, luck, jp2):
    if st.session_state.get("coins",0) < bet: return
    st.session_state["coins"] -= bet
    st.session_state["slot_spins"] = st.session_state.get("slot_spins",0) + 1
    w = SL_W[:]
    if luck: w[4]=int(w[4]*1.5); w[5]=int(w[5]*1.5); w[6]=int(w[6]*1.5)
    reels = [random.choices(SL_SYM, weights=w, k=1)[0] for _ in range(3)]
    st.session_state["sl_reels"] = reels
    combo = "".join(reels)
    pay   = SL_PAY.get(combo, 0)
    if pay==0 and (reels[0]==reels[1] or reels[1]==reels[2] or reels[0]==reels[2]): pay=2
    if pay > 0:
        if jp2 and pay>=50: pay*=2
        won = bet*pay; e = add_coins(won); add_xp(won//5)
        st.session_state["slot_wins"]      = st.session_state.get("slot_wins",0) + 1
        st.session_state["slot_total_won"] = st.session_state.get("slot_total_won",0) + e
        if pay>=100:
            st.session_state["sl_result"] = f"🎉 ג'קפוט!!! +{e} 🪙!"; add_achievement("🎰 ג'קפוט!")
        elif pay>=20: st.session_state["sl_result"] = f"⭐ ניצחת! +{e} 🪙 (x{pay})"
        else:         st.session_state["sl_result"] = f"✅ ניצחת! +{e} 🪙 (x{pay})"
    else:
        st.session_state["sl_result"] = f"😔 הפסדת {bet} 🪙..."
    st.rerun()

# ─────────────────────────────────────────
# PAGE: SHOP
# ─────────────────────────────────────────
GAME_LBL = {"snake":"🐍 נחש","flappy":"🐦 פלאפי","memory":"🧠 זיכרון",
            "slot":"🎰 מכונת מזל","clicker":"👆 קליקר","tictactoe":"❌ איקס עיגול","global":"🌐 גלובלי"}

def page_shop():
    coins = st.session_state.get("coins",0)
    st.markdown(f"""
    <div style='text-align:center;margin-bottom:22px'>
        <h1>🛒 חנות שדרוגים</h1>
        <div style='display:inline-flex;align-items:center;gap:10px;padding:12px 24px;
             background:linear-gradient(135deg,rgba(255,214,10,.15),rgba(255,214,10,.05));
             border:1px solid rgba(255,214,10,.4);border-radius:12px;margin-top:8px'>
            <span style='font-size:28px;filter:drop-shadow(0 0 10px rgba(255,214,10,.8))'>🪙</span>
            <span style='font-family:Orbitron,sans-serif;font-size:26px;font-weight:900;
                  color:#ffd60a;text-shadow:0 0 15px rgba(255,214,10,.8)'>{coins:,}</span>
            <span style='color:#8888aa;font-size:13px'>מטבעות</span>
        </div>
    </div>""", unsafe_allow_html=True)

    by_game = {}
    for uid,item in SHOP_ITEMS.items():
        by_game.setdefault(item["game"],[]).append((uid,item))

    for game in ["global"] + [g for g in by_game if g!="global"]:
        if game not in by_game: continue
        items = by_game[game]
        st.markdown(f"""<div style='margin:14px 0 8px'>
            <h3 style='font-size:15px;color:#8888aa;font-family:Orbitron,sans-serif;
                 text-transform:uppercase;letter-spacing:2px;border-bottom:1px solid rgba(255,255,255,.05);
                 padding-bottom:8px'>{GAME_LBL.get(game,game)}</h3></div>""", unsafe_allow_html=True)

        cols = st.columns(min(len(items),3))
        for i,(uid,item) in enumerate(items):
            with cols[i%3]:
                owned   = has_upgrade(uid)
                can_buy = coins >= item["price"] and not owned
                col_   = "#39ff14" if owned else ("#ffd60a" if can_buy else "#8888aa")
                bg_    = "rgba(57,255,20,.08)" if owned else "rgba(255,255,255,.02)"
                brd_   = "rgba(57,255,20,.4)"  if owned else ("rgba(255,214,10,.3)" if can_buy else "rgba(255,255,255,.06)")
                badge  = "<div style='position:absolute;top:8px;right:8px;background:rgba(57,255,20,.2);border:1px solid rgba(57,255,20,.5);border-radius:6px;padding:2px 8px;font-size:10px;color:#39ff14;font-weight:700'>✓ נקנה</div>" if owned else ""
                st.markdown(f"""
                <div style='background:{bg_};border:1px solid {brd_};border-radius:14px;padding:18px;
                     text-align:center;margin-bottom:8px;min-height:130px;position:relative;'>
                    {badge}
                    <div style='font-size:34px;margin-bottom:6px;filter:drop-shadow(0 0 8px {col_}80)'>{item["icon"]}</div>
                    <div style='font-weight:700;font-size:12px;color:{col_};margin-bottom:4px'>{item["name"]}</div>
                    <div style='color:#8888aa;font-size:11px;margin-bottom:10px;line-height:1.4'>{item["desc"]}</div>
                    <div style='font-family:Orbitron,sans-serif;font-size:15px;font-weight:900;
                         color:{"#39ff14" if owned else "#ffd60a"}'>
                         {"✅ בבעלותך" if owned else f"🪙 {item['price']:,}"}</div>
                </div>""", unsafe_allow_html=True)

                if not owned:
                    st.markdown(f'<div class="{"btn-gold" if can_buy else ""}">', unsafe_allow_html=True)
                    if st.button("🛒 קנה" if can_buy else "🔒 חסר", key=f"sh_{uid}", use_container_width=True, disabled=not can_buy):
                        ok,msg = buy_upgrade(uid)
                        if ok: st.rerun()
                        else: st.markdown(f"<div class='err'>{msg}</div>", unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.markdown("<br>", unsafe_allow_html=True)

    owned_list = st.session_state.get("owned_upgrades",[])
    if owned_list:
        st.markdown("---\n### 🎒 השדרוגים שלך")
        b = "".join(f"<span class='ach'>{SHOP_ITEMS[u]['icon']} {SHOP_ITEMS[u]['name']}</span>" for u in owned_list if u in SHOP_ITEMS)
        st.markdown(f"<div style='display:flex;flex-wrap:wrap'>{b}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🪙 איך להרוויח מטבעות?")
    st.markdown("""
    <div style='display:grid;grid-template-columns:1fr 1fr;gap:10px'>
      <div style='background:rgba(0,245,255,.05);border:1px solid rgba(0,245,255,.15);border-radius:10px;padding:12px'><div style='color:#00f5ff;font-weight:700;margin-bottom:4px'>🐍 נחש</div><div style='color:#8888aa;font-size:12px'>ניקוד ÷ 2 מטבעות</div></div>
      <div style='background:rgba(255,214,10,.05);border:1px solid rgba(255,214,10,.15);border-radius:10px;padding:12px'><div style='color:#ffd60a;font-weight:700;margin-bottom:4px'>🐦 פלאפי</div><div style='color:#8888aa;font-size:12px'>ניקוד × 5 מטבעות</div></div>
      <div style='background:rgba(191,95,255,.05);border:1px solid rgba(191,95,255,.15);border-radius:10px;padding:12px'><div style='color:#bf5fff;font-weight:700;margin-bottom:4px'>🧠 זיכרון</div><div style='color:#8888aa;font-size:12px'>עד 100 מטבעות</div></div>
      <div style='background:rgba(255,0,110,.05);border:1px solid rgba(255,0,110,.15);border-radius:10px;padding:12px'><div style='color:#ff006e;font-weight:700;margin-bottom:4px'>👆 קליקר</div><div style='color:#8888aa;font-size:12px'>קליקים × 2 מטבעות</div></div>
      <div style='background:rgba(255,124,0,.05);border:1px solid rgba(255,124,0,.15);border-radius:10px;padding:12px'><div style='color:#ff7c00;font-weight:700;margin-bottom:4px'>🎰 מכונת מזל</div><div style='color:#8888aa;font-size:12px'>הימור × כפל</div></div>
      <div style='background:rgba(0,245,255,.05);border:1px solid rgba(0,245,255,.15);border-radius:10px;padding:12px'><div style='color:#00f5ff;font-weight:700;margin-bottom:4px'>❌ איקס עיגול</div><div style='color:#8888aa;font-size:12px'>ניצחון = 50 מטבעות</div></div>
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# ROUTER
# ─────────────────────────────────────────
def main():
    inject_styles()
    init_state()
    selected = render_sidebar()

    routes = {
        "🏠 לובי":          page_lobby,
        "🐍 נחש":           page_snake,
        "🐦 פלאפי בירד":   page_flappy,
        "🧠 זיכרון":        page_memory,
        "❌ איקס עיגול":    page_tictactoe,
        "👆 קליקר":         page_clicker,
        "🎰 מכונת מזל":    page_slot,
        "🛒 חנות":          page_shop,
    }
    routes.get(selected, page_lobby)()

if __name__ == "__main__":
    main()
