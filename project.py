"""
🎮 ARCADE GALAXY v2
הפעלה: streamlit run arcade_galaxy_v2.py
"""
import streamlit as st
import streamlit.components.v1 as components
import random, time, math

st.set_page_config(page_title="🎮 Arcade Galaxy", page_icon="🎮", layout="wide", initial_sidebar_state="expanded")

# ══════════════════════════════════════════════════════════
# SHOP CATALOGUE  (max_owned > 1 = ניתן לקנות כמה פעמים)
# ══════════════════════════════════════════════════════════
SHOP = {
    # ── SNAKE
    "snake_speed":   {"name":"מהירות נחש +1",   "game":"snake",     "price":120, "max":3, "icon":"⚡", "desc":"כל רכישה מגבירה מהירות"},
    "snake_life":    {"name":"חיים נוספים",      "game":"snake",     "price":250, "max":3, "icon":"💚", "desc":"כל רכישה מוסיפה חיים"},
    "snake_wall":    {"name":"מעבר קירות",        "game":"snake",     "price":500, "max":1, "icon":"🌀", "desc":"הנחש עובר דרך קירות"},
    "snake_magnet":  {"name":"מגנט אוכל",         "game":"snake",     "price":400, "max":1, "icon":"🧲", "desc":"האוכל נמשך לנחש"},
    # ── FLAPPY
    "flappy_shield": {"name":"מגן פלאפי",         "game":"flappy",    "price":200, "max":3, "icon":"🛡", "desc":"כל רכישה מוסיפה מגן"},
    "flappy_slow":   {"name":"צינורות איטיים",    "game":"flappy",    "price":300, "max":2, "icon":"🐌", "desc":"צינורות איטיים יותר"},
    "flappy_gap":    {"name":"פתח גדול",           "game":"flappy",    "price":400, "max":2, "icon":"🔓", "desc":"פתח רחב יותר בכל רכישה"},
    # ── MEMORY
    "mem_hint":      {"name":"רמזים",              "game":"memory",    "price": 80, "max":5, "icon":"💡", "desc":"כל רכישה מוסיפה 2 רמזים"},
    "mem_x2":        {"name":"כפל ניקוד",          "game":"memory",    "price":350, "max":1, "icon":"×2", "desc":"פי 2 מטבעות בסיום"},
    "mem_flip_time": {"name":"זמן חשיפה +",        "game":"memory",    "price":200, "max":3, "icon":"⏱", "desc":"קלפים נשארים גלויים יותר"},
    # ── SLOT
    "slot_luck":     {"name":"מזל מוגבר",          "game":"slot",      "price":300, "max":3, "icon":"🍀", "desc":"כל רכישה מגדילה סיכוי"},
    "slot_jackpot":  {"name":"ג'קפוט x2",          "game":"slot",      "price":500, "max":2, "icon":"💰", "desc":"כפל את הג'קפוט"},
    "slot_refund":   {"name":"החזר הפסד 10%",      "game":"slot",      "price":600, "max":1, "icon":"↩", "desc":"10% החזר על הפסדים"},
    # ── CLICKER
    "clicker_mul":   {"name":"כפל קליקים",         "game":"clicker",   "price":300, "max":3, "icon":"×2", "desc":"כל רכישה מכפילה קליקים"},
    "clicker_time":  {"name":"זמן נוסף",            "game":"clicker",   "price":400, "max":3, "icon":"⏰", "desc":"כל רכישה מוסיפה 3 שניות"},
    "clicker_auto":  {"name":"קליקר אוטו",          "game":"clicker",   "price":700, "max":1, "icon":"🤖", "desc":"1 קליק/שניה אוטומטי"},
    # ── TTT
    "ttt_undo":      {"name":"ביטול מהלך",         "game":"ttt",       "price":150, "max":3, "icon":"↩", "desc":"כל רכישה מוסיפה ביטול"},
    "ttt_easy":      {"name":"AI קל יותר",          "game":"ttt",       "price":200, "max":3, "icon":"🎯", "desc":"AI חלש יותר בכל רכישה"},
    # ── GLOBAL
    "coin_boost":    {"name":"בוסט מטבעות",        "game":"global",    "price":800, "max":3, "icon":"💫", "desc":"כל רכישה +15% מטבעות"},
    "xp_boost":      {"name":"בוסט XP",             "game":"global",    "price":600, "max":3, "icon":"⭐", "desc":"כל רכישה +20% XP"},
    "daily_coins":   {"name":"בונוס יומי +",        "game":"global",    "price":500, "max":5, "icon":"📅", "desc":"כל רכישה +30 לבונוס יומי"},
}

GAME_LBL = {"snake":"🐍 נחש","flappy":"🐦 פלאפי","memory":"🧠 זיכרון",
            "slot":"🎰 מכונת מזל","clicker":"👆 קליקר","ttt":"❌ איקס עיגול","global":"🌐 גלובלי"}

# ══════════════════════════════════════════════════════════
# STATE
# ══════════════════════════════════════════════════════════
def init():
    D = {
        "coins":0, "level":1, "xp":0,
        "achievements":[], "owned":{},      # owned: {uid: count}
        "snake_hi":0,  "snake_played":0,
        "flappy_hi":0, "flappy_played":0,
        "mem_hi":0,    "mem_played":0,
        "ttt_w":0, "ttt_l":0, "ttt_d":0, "ttt_played":0,
        "click_hi":0,  "click_total":0, "click_sessions":0,
        "slot_spins":0,"slot_wins":0,   "slot_total_won":0,
        "daily_last": 0,
    }
    for k,v in D.items():
        if k not in st.session_state: st.session_state[k]=v

def S(k, default=None):
    return st.session_state.get(k, default)

def owned_count(uid):
    return S("owned",{}).get(uid,0)

def has(uid):
    return owned_count(uid) > 0

def buy(uid):
    item = SHOP.get(uid)
    if not item: return False,"?"
    cnt = owned_count(uid)
    if cnt >= item["max"]: return False,"הגעת למקסימום!"
    if S("coins",0) < item["price"]: return False,f"חסר {item['price']-S('coins',0)} מטבעות"
    st.session_state["coins"] -= item["price"]
    owned = dict(S("owned",{})); owned[uid] = cnt+1
    st.session_state["owned"] = owned
    return True, f"קנית {item['name']}! ({cnt+1}/{item['max']})"

def earn_coins(base):
    mul = 1.0 + owned_count("coin_boost")*0.15
    amt = max(1, int(base*mul))
    st.session_state["coins"] = S("coins",0) + amt
    return amt

def earn_xp(base):
    mul = 1.0 + owned_count("xp_boost")*0.20
    amt = max(1, int(base*mul))
    st.session_state["xp"] = S("xp",0) + amt
    lv = S("level",1)
    while S("xp",0) >= lv*120:
        st.session_state["xp"] -= lv*120
        lv += 1
        st.session_state["level"] = lv
        # milestone achievements only
        if lv in (5,10,20,50):
            _ach(f"רמה {lv}! ⬆️")
    return amt

def _ach(name):
    a = list(S("achievements",[]))
    if name not in a:
        a.append(name)
        st.session_state["achievements"] = a

# ══════════════════════════════════════════════════════════
# STYLES
# ══════════════════════════════════════════════════════════
def inject_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Exo+2:wght@400;600;700&display=swap');
:root{--bg:#0a0a1a;--card:#11112a;--cyan:#00f5ff;--pink:#ff006e;--gold:#ffd60a;
      --green:#39ff14;--purple:#bf5fff;--orange:#ff7c00;--dim:#7777aa;--fg:#dde0ff;}
.stApp{background:var(--bg)!important;
  background-image:radial-gradient(ellipse at 15% 50%,rgba(0,245,255,.05) 0%,transparent 55%),
    radial-gradient(ellipse at 85% 20%,rgba(255,0,110,.04) 0%,transparent 55%)!important;
  font-family:'Exo 2',sans-serif!important;color:var(--fg)!important;}
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#040414,#08081e)!important;
  border-right:1px solid rgba(0,245,255,.12)!important;}
.main .block-container{padding:20px 28px!important;max-width:100%!important;}
/* Headings */
h1,h2,h3{font-family:Orbitron,sans-serif!important;color:var(--cyan)!important;
  text-shadow:0 0 18px rgba(0,245,255,.5)!important;}
/* Buttons */
.stButton>button{background:linear-gradient(135deg,rgba(0,245,255,.12),rgba(0,245,255,.04))!important;
  color:var(--cyan)!important;border:1px solid rgba(0,245,255,.35)!important;
  border-radius:9px!important;font-family:'Exo 2',sans-serif!important;font-weight:700!important;
  transition:all .18s!important;}
.stButton>button:hover{background:linear-gradient(135deg,rgba(0,245,255,.25),rgba(0,245,255,.1))!important;
  border-color:var(--cyan)!important;box-shadow:0 0 20px rgba(0,245,255,.25)!important;transform:translateY(-1px)!important;}
.btn-gold .stButton>button{background:linear-gradient(135deg,rgba(255,214,10,.2),rgba(255,214,10,.06))!important;
  color:var(--gold)!important;border-color:rgba(255,214,10,.45)!important;}
.btn-gold .stButton>button:hover{box-shadow:0 0 20px rgba(255,214,10,.3)!important;}
.btn-red .stButton>button{background:linear-gradient(135deg,rgba(255,0,110,.2),rgba(255,0,110,.05))!important;
  color:var(--pink)!important;border-color:rgba(255,0,110,.45)!important;}
.btn-green .stButton>button{background:linear-gradient(135deg,rgba(57,255,20,.2),rgba(57,255,20,.05))!important;
  color:var(--green)!important;border-color:rgba(57,255,20,.45)!important;}
.btn-big .stButton>button{font-size:20px!important;padding:14px!important;height:64px!important;
  letter-spacing:2px!important;}
/* Metrics */
[data-testid="metric-container"]{background:var(--card)!important;
  border:1px solid rgba(0,245,255,.2)!important;border-radius:10px!important;padding:12px!important;}
[data-testid="metric-container"] label{color:var(--dim)!important;font-size:12px!important;}
[data-testid="metric-container"] [data-testid="stMetricValue"]{color:var(--cyan)!important;
  font-family:Orbitron,sans-serif!important;font-size:22px!important;}
/* Alerts */
.ok{padding:12px 16px;background:rgba(57,255,20,.08);border:1px solid rgba(57,255,20,.4);
  border-radius:10px;color:var(--green);font-weight:600;text-align:center;}
.err{padding:12px 16px;background:rgba(255,0,110,.08);border:1px solid rgba(255,0,110,.4);
  border-radius:10px;color:var(--pink);font-weight:600;text-align:center;}
.inf{padding:12px 16px;background:rgba(0,245,255,.07);border:1px solid rgba(0,245,255,.3);
  border-radius:10px;color:var(--cyan);text-align:center;}
.warn{padding:12px 16px;background:rgba(255,214,10,.07);border:1px solid rgba(255,214,10,.35);
  border-radius:10px;color:var(--gold);text-align:center;}
/* Cards */
.gcard{background:var(--card);border:1px solid rgba(0,245,255,.18);border-radius:14px;
  padding:20px;transition:all .25s;position:relative;overflow:hidden;}
.gcard:hover{border-color:rgba(0,245,255,.5);box-shadow:0 0 28px rgba(0,245,255,.15);transform:translateY(-2px);}
/* Progress */
.stProgress>div>div>div{background:linear-gradient(90deg,var(--cyan),var(--purple))!important;border-radius:4px!important;}
.stProgress>div>div{background:rgba(255,255,255,.06)!important;border-radius:4px!important;}
/* Radio */
div[role="radiogroup"]{display:flex!important;flex-direction:column!important;gap:3px!important;padding:6px 10px!important;}
div[role="radiogroup"] label{padding:9px 13px!important;border-radius:9px!important;
  color:var(--dim)!important;border:1px solid transparent!important;font-weight:600!important;transition:all .15s!important;}
div[role="radiogroup"] label:hover{background:rgba(0,245,255,.06)!important;color:var(--cyan)!important;}
div[role="radiogroup"] label input{display:none!important;}
.stRadio>label{display:none!important;}
/* Misc */
hr{border-color:rgba(0,245,255,.09)!important;}
::-webkit-scrollbar{width:5px;}::-webkit-scrollbar-track{background:var(--bg);}
::-webkit-scrollbar-thumb{background:rgba(0,245,255,.25);border-radius:3px;}
#MainMenu,footer,.stDeployButton{display:none!important;}
header[data-testid="stHeader"]{background:transparent!important;}
.stTabs [data-baseweb="tab-list"]{background:rgba(255,255,255,.02)!important;border-radius:8px!important;}
.stTabs [data-baseweb="tab"]{font-family:'Exo 2',sans-serif!important;font-weight:700!important;color:var(--dim)!important;}
.stTabs [aria-selected="true"]{background:rgba(0,245,255,.12)!important;color:var(--cyan)!important;}
[data-testid="column"]{padding:0 6px!important;}
</style>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════
PAGES = ["🏠 לובי","🐍 נחש","🐦 פלאפי","🧠 זיכרון","❌ איקס-עיגול","👆 קליקר","🎰 מכונת מזל","🛒 חנות"]

def sidebar():
    with st.sidebar:
        coins = S("coins",0)
        lv    = S("level",1)
        st.markdown(f"""
<div style="padding:20px 16px 14px;text-align:center;border-bottom:1px solid rgba(0,245,255,.1)">
  <div style="font-size:52px;filter:drop-shadow(0 0 18px rgba(0,245,255,.9));
       animation:pg 2.5s ease-in-out infinite">&#127918;</div>
  <div style="font-family:Orbitron,sans-serif;font-size:20px;font-weight:900;color:#00f5ff;
       text-shadow:0 0 18px rgba(0,245,255,.8);letter-spacing:4px;margin-top:6px">ARCADE<br>GALAXY</div>
</div>
<div style="margin:14px 12px;padding:12px 14px;background:rgba(255,214,10,.07);
     border:1px solid rgba(255,214,10,.35);border-radius:10px;display:flex;align-items:center;gap:10px">
  <span style="font-size:22px">&#128170;</span>
  <div>
    <div style="font-family:Orbitron,sans-serif;font-size:20px;font-weight:900;color:#ffd60a;
         text-shadow:0 0 10px rgba(255,214,10,.7)">{coins:,}</div>
    <div style="font-size:10px;color:#7777aa">מטבעות | רמה {lv}</div>
  </div>
</div>
<div style="margin:0 12px 12px;height:4px;background:rgba(255,255,255,.05);border-radius:2px">
  <div style="height:100%;width:{min(S('xp',0)/(lv*120)*100,100):.0f}%;
       background:linear-gradient(90deg,#00f5ff,#bf5fff);border-radius:2px"></div>
</div>
<style>@keyframes pg{{0%,100%{{filter:drop-shadow(0 0 18px rgba(0,245,255,.9))}}
  50%{{filter:drop-shadow(0 0 32px rgba(0,245,255,1)) drop-shadow(0 0 55px rgba(0,245,255,.4))}}}}</style>
""", unsafe_allow_html=True)

        sel = st.radio("nav", PAGES, label_visibility="collapsed", key="nav_sel")

        total = sum(S(k,0) for k in ["snake_played","flappy_played","mem_played","ttt_played","click_sessions","slot_spins"])
        st.markdown(f"""
<div style="margin:10px 12px;padding:10px;background:rgba(255,255,255,.02);border-radius:9px;
     border:1px solid rgba(255,255,255,.04)">
  <div style="display:flex;justify-content:space-between;font-size:11px;color:#7777aa;padding:2px 0">
    <span>&#127918; משחקים</span><span style="color:#dde0ff">{total}</span></div>
  <div style="display:flex;justify-content:space-between;font-size:11px;color:#7777aa;padding:2px 0">
    <span>&#127942; הישגים</span><span style="color:#dde0ff">{len(S("achievements",[]))}</span></div>
  <div style="display:flex;justify-content:space-between;font-size:11px;color:#7777aa;padding:2px 0">
    <span>&#128142; שדרוגים</span><span style="color:#dde0ff">{sum(S("owned",{}).values())}</span></div>
</div>""", unsafe_allow_html=True)
    return sel

# ══════════════════════════════════════════════════════════
# LOBBY
# ══════════════════════════════════════════════════════════
def page_lobby():
    st.markdown("""
<div style="text-align:center;padding:16px 0 24px">
  <div style="font-size:64px;animation:flt 3s ease-in-out infinite;display:inline-block">&#127918;</div>
  <h1 style="font-family:Orbitron,sans-serif;font-size:36px;font-weight:900;margin:10px 0 4px;
     background:linear-gradient(90deg,#00f5ff,#bf5fff,#ff006e,#00f5ff);background-size:300%;
     -webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:shim 4s linear infinite">
     ARCADE GALAXY</h1>
  <p style="color:#7777aa;letter-spacing:3px;font-size:14px">בחר משחק מהרשימה בצד שמאל</p>
</div>
<style>
@keyframes flt{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
@keyframes shim{0%{background-position:0%}100%{background-position:300%}}
</style>""", unsafe_allow_html=True)

    lv   = S("level",1)
    xp   = S("xp",0)
    need = lv*120
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.metric("&#127922; רמה",   lv)
    with c2: st.metric("&#128170; מטבעות", f"{S('coins',0):,}")
    with c3: st.metric("&#127942; הישגים", len(S("achievements",[])))
    with c4:
        total = sum(S(k,0) for k in ["snake_played","flappy_played","mem_played","ttt_played","click_sessions","slot_spins"])
        st.metric("&#127918; משחקים", total)

    st.markdown(f"<div style='font-size:11px;color:#7777aa;text-align:right;margin:4px 0'>XP: {xp}/{need}</div>",unsafe_allow_html=True)
    st.progress(min(xp/need,1.0))
    st.markdown("<br>",unsafe_allow_html=True)

    rows = [
        ("&#128013;","נחש","#39ff14","שלוט בנחש, אכול אוכל",f"שיא: {S('snake_hi',0)}",S("snake_played",0)),
        ("&#128054;","פלאפי","#ffd60a","עוף בין הצינורות",f"שיא: {S('flappy_hi',0)}",S("flappy_played",0)),
        ("&#129504;","זיכרון","#bf5fff","מצא זוגות קלפים",f"שיא: {S('mem_hi',0)}",S("mem_played",0)),
        ("&#10060;","איקס-עיגול","#00f5ff","שחק נגד AI",f"ניצחונות: {S('ttt_w',0)}",S("ttt_played",0)),
        ("&#128070;","קליקר","#ff006e","לחץ הכי מהר!",f"שיא: {S('click_hi',0)}",S("click_sessions",0)),
        ("&#127920;","מכונת מזל","#ff7c00","סובב ונסה לזכות",f"זכיות: {S('slot_wins',0)}",S("slot_spins",0)),
    ]
    c = st.columns(3)
    for i,(ico,name,col,desc,best,played) in enumerate(rows):
        with c[i%3]:
            st.markdown(f"""
<div class="gcard" style="border-color:{col}30;text-align:center;padding:22px 16px;
     background:linear-gradient(135deg,{col}08,var(--card))">
  <div style="font-size:44px;margin-bottom:8px">{ico}</div>
  <div style="font-family:Orbitron,sans-serif;font-size:14px;color:{col};
       text-shadow:0 0 12px {col}80;margin-bottom:6px">{name}</div>
  <div style="color:#7777aa;font-size:12px;margin-bottom:10px">{desc}</div>
  <div style="display:flex;justify-content:space-between;font-size:11px">
    <span style="color:{col}">&#127942; {best}</span>
    <span style="color:#555">&#127918; {played}</span>
  </div>
</div><br>""", unsafe_allow_html=True)

    # Daily bonus
    now = int(time.time())
    last = S("daily_last",0)
    if now - last > 86400:
        st.markdown("<hr>",unsafe_allow_html=True)
        base = 50 + owned_count("daily_coins")*30
        st.markdown(f"<div class='warn'>&#127873; בונוס יומי זמין! קבל {base} מטבעות</div>",unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
        _,mc,_ = st.columns([1,2,1])
        with mc:
            st.markdown('<div class="btn-gold">',unsafe_allow_html=True)
            if st.button(f"&#127873; קבל {base} מטבעות!", use_container_width=True, key="daily_btn"):
                earn_coins(base); earn_xp(15)
                st.session_state["daily_last"] = now
                _ach("&#127873; בונוס יומי!")
                st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)

    # Achievements
    achs = S("achievements",[])
    if achs:
        st.markdown("<hr>",unsafe_allow_html=True)
        st.markdown("### &#127942; הישגים")
        b = "".join(f"<span style='display:inline-flex;align-items:center;gap:6px;padding:6px 12px;"
                    f"background:rgba(255,214,10,.08);border:1px solid rgba(255,214,10,.35);"
                    f"border-radius:16px;font-size:12px;font-weight:700;color:#ffd60a;margin:3px'>{a}</span>"
                    for a in achs[-12:])
        st.markdown(f"<div style='display:flex;flex-wrap:wrap'>{b}</div>",unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# SNAKE
# ══════════════════════════════════════════════════════════
def page_snake():
    st.markdown("<h1 style='text-align:center'>&#128013; נחש</h1><p style='text-align:center;color:#7777aa'>חצים / WASD לשליטה</p>",unsafe_allow_html=True)
    wp  = "true" if has("snake_wall")  else "false"
    spd = owned_count("snake_speed")
    lfs = 1 + owned_count("snake_life")
    mag = "true" if has("snake_magnet") else "false"
    hi  = S("snake_hi",0)

    ups=[]
    if has("snake_wall"):   ups.append("🌀 מעבר קירות")
    if lfs>1:               ups.append(f"💚 {lfs} חיים")
    if spd:                 ups.append(f"⚡ מהירות +{spd}")
    if has("snake_magnet"): ups.append("🧲 מגנט")
    if ups: st.markdown(f"<div class='inf'>{'  |  '.join(ups)}</div>",unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)

    _,col,_ = st.columns([1,6,1])
    with col:
        components.html(f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#070712;display:flex;flex-direction:column;align-items:center;
     font-family:'Orbitron',monospace;padding:6px;user-select:none}}
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');
.hud{{display:flex;gap:10px;margin-bottom:6px;font-size:12px;flex-wrap:wrap;justify-content:center}}
.hi{{background:rgba(0,245,255,.09);border:1px solid rgba(0,245,255,.28);border-radius:7px;
     padding:4px 10px;color:#00f5ff;white-space:nowrap}}
canvas{{border:2px solid rgba(0,245,255,.35);border-radius:10px;
        box-shadow:0 0 30px rgba(0,245,255,.12);display:block;max-width:100%}}
.ov{{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
     background:rgba(5,5,20,.93);border:2px solid #00f5ff;border-radius:12px;
     padding:20px 28px;text-align:center;min-width:180px}}
.ov h2{{color:#00f5ff;font-size:18px;margin-bottom:8px}}
.ov p{{color:#8888aa;font-size:12px;margin-bottom:12px}}
.ov button{{background:rgba(0,245,255,.18);color:#00f5ff;border:1px solid #00f5ff;
            padding:8px 20px;border-radius:7px;cursor:pointer;font-family:Orbitron;
            font-size:12px;font-weight:700;transition:all .18s}}
.ov button:hover{{background:rgba(0,245,255,.35);box-shadow:0 0 14px rgba(0,245,255,.4)}}
.wrap{{position:relative}}
</style></head><body>
<div class="hud">
  <div class="hi">ניקוד: <span id="sc">0</span></div>
  <div class="hi">שיא: <span id="hi">{hi}</span></div>
  <div class="hi">חיים: <span id="lv">{lfs}</span></div>
  <div class="hi">מהירות: <span id="sp">1</span></div>
</div>
<div class="wrap">
<canvas id="c"></canvas>
<div class="ov" id="ov">
  <h2 id="ot">&#128013; נחש</h2><p id="ob">לחץ שחק להתחיל</p>
  <button onclick="startGame()">&#9654; שחק</button>
</div></div>
<script>
const GRID=20,CELL=20,CANVAS_S=GRID*CELL;
const WP={wp},MAG={mag},INIT_SPD={max(1,spd)},INIT_LIVES={lfs};
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
cv.width=CANVAS_S; cv.height=CANVAS_S;
let sn,dir,nd,food,bon,score,lives,spd,loop,run,parts;

function startGame(){{
  document.getElementById('ov').style.display='none';
  sn=[{{x:10,y:10}},{{x:9,y:10}},{{x:8,y:10}}];
  dir={{x:1,y:0}};nd={{x:1,y:0}};
  score=0;lives=INIT_LIVES;spd=INIT_SPD;parts=[];bon=null;run=true;
  document.getElementById('sc').textContent='0';
  document.getElementById('lv').textContent=lives;
  document.getElementById('sp').textContent=spd;
  placeFood();
  if(loop)clearInterval(loop);
  let iv=Math.max(65,160-spd*18);
  loop=setInterval(update,iv);
}}
document.addEventListener('keydown',e=>{{
  const k={{ArrowUp:{{x:0,y:-1}},ArrowDown:{{x:0,y:1}},ArrowLeft:{{x:-1,y:0}},ArrowRight:{{x:1,y:0}},
    KeyW:{{x:0,y:-1}},KeyS:{{x:0,y:1}},KeyA:{{x:-1,y:0}},KeyD:{{x:1,y:0}}}};
  const n=k[e.code];
  if(n&&(n.x!==-dir.x||n.y!==-dir.y)){{nd=n;e.preventDefault();}}
}});
function placeFood(){{
  let p;do{{p={{x:Math.floor(Math.random()*GRID),y:Math.floor(Math.random()*GRID)}}}}
  while(sn.some(s=>s.x===p.x&&s.y===p.y));food=p;
  if(score>0&&score%60===0&&!bon){{
    let b;do{{b={{x:Math.floor(Math.random()*GRID),y:Math.floor(Math.random()*GRID)}}}}
    while(sn.some(s=>s.x===b.x&&s.y===b.y)||(food.x===b.x&&food.y===b.y));bon={{...b,t:90}};
  }}
}}
function spark(x,y,c){{for(let i=0;i<8;i++)parts.push({{x:x*CELL+CELL/2,y:y*CELL+CELL/2,
  vx:(Math.random()-.5)*4.5,vy:(Math.random()-.5)*4.5,l:28,c}});}}
function update(){{
  if(!run)return;dir={{...nd}};
  let h={{x:sn[0].x+dir.x,y:sn[0].y+dir.y}};
  if(WP){{h.x=(h.x+GRID)%GRID;h.y=(h.y+GRID)%GRID;}}
  else if(h.x<0||h.x>=GRID||h.y<0||h.y>=GRID){{die();return;}}
  if(sn.slice(1).some(s=>s.x===h.x&&s.y===h.y)){{die();return;}}
  // Magnet: if food is adjacent pull it closer
  if(MAG){{
    let dx=food.x-h.x,dy=food.y-h.y,dist=Math.abs(dx)+Math.abs(dy);
    if(dist<=4){{
      if(dx!==0)food.x+=dx>0?-1:1;
      else if(dy!==0)food.y+=dy>0?-1:1;
    }}
  }}
  sn.unshift(h);
  let grew=false;
  if(h.x===food.x&&h.y===food.y){{
    score+=10;grew=true;spark(food.x,food.y,'#39ff14');placeFood();
    document.getElementById('sc').textContent=score;
    let ns=INIT_SPD+Math.floor(score/60);
    if(ns>spd){{spd=ns;clearInterval(loop);loop=setInterval(update,Math.max(65,160-spd*18));
      document.getElementById('sp').textContent=spd;}}
  }}
  if(bon&&h.x===bon.x&&h.y===bon.y){{score+=50;grew=true;spark(bon.x,bon.y,'#ffd60a');
    bon=null;document.getElementById('sc').textContent=score;}}
  if(!grew)sn.pop();
  if(bon){{bon.t--;if(bon.t<=0)bon=null;}}
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
    document.getElementById('ob').textContent='ניקוד: '+score+'  |  שיא: '+Math.max(score,hs);
    document.getElementById('ov').style.display='block';
    window.parent.postMessage({{type:'snake_done',score}},'*');
  }}else{{sn=[{{x:10,y:10}},{{x:9,y:10}},{{x:8,y:10}}];dir={{x:1,y:0}};nd={{x:1,y:0}};}}
}}
function rr(x,y,w,h,r){{
  ctx.beginPath();ctx.moveTo(x+r,y);ctx.lineTo(x+w-r,y);ctx.quadraticCurveTo(x+w,y,x+w,y+r);
  ctx.lineTo(x+w,y+h-r);ctx.quadraticCurveTo(x+w,y+h,x+w-r,y+h);ctx.lineTo(x+r,y+h);
  ctx.quadraticCurveTo(x,y+h,x,y+h-r);ctx.lineTo(x,y+r);ctx.quadraticCurveTo(x,y,x+r,y);ctx.closePath();
}}
function draw(){{
  ctx.fillStyle='#070712';ctx.fillRect(0,0,CANVAS_S,CANVAS_S);
  ctx.strokeStyle='rgba(0,245,255,.04)';ctx.lineWidth=.5;
  for(let i=0;i<=GRID;i++){{ctx.beginPath();ctx.moveTo(i*CELL,0);ctx.lineTo(i*CELL,CANVAS_S);ctx.stroke();
    ctx.beginPath();ctx.moveTo(0,i*CELL);ctx.lineTo(CANVAS_S,i*CELL);ctx.stroke();}}
  // particles
  parts.forEach(p=>{{ctx.globalAlpha=p.l/28;ctx.fillStyle=p.c;
    ctx.beginPath();ctx.arc(p.x,p.y,3,0,Math.PI*2);ctx.fill();}});
  ctx.globalAlpha=1;
  // food pulse
  let t=Date.now()/350;
  ctx.save();ctx.translate(food.x*CELL+CELL/2,food.y*CELL+CELL/2);
  ctx.scale(1+Math.sin(t)*.16,1+Math.sin(t)*.16);
  ctx.shadowBlur=18;ctx.shadowColor='#39ff14';ctx.fillStyle='#39ff14';
  ctx.beginPath();ctx.arc(0,0,CELL/2-2,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;ctx.restore();
  // bonus
  if(bon){{
    ctx.save();ctx.translate(bon.x*CELL+CELL/2,bon.y*CELL+CELL/2);
    ctx.scale(1+Math.sin(Date.now()/140)*.22,1+Math.sin(Date.now()/140)*.22);
    ctx.shadowBlur=22;ctx.shadowColor='#ffd60a';
    ctx.fillStyle='#ffd60a';ctx.font=(CELL-2)+'px serif';
    ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('*',0,0);ctx.restore();
    ctx.fillStyle='rgba(255,214,10,'+bon.t/90+')';ctx.fillRect(bon.x*CELL,bon.y*CELL-3,CELL*(bon.t/90),2);
  }}
  // snake
  sn.forEach((seg,i)=>{{
    ctx.save();
    if(i===0){{ctx.shadowBlur=14;ctx.shadowColor='rgba(0,245,255,.8)';}}
    let ratio=i/sn.length;
    ctx.fillStyle=i===0?'#fff':`rgba(0,${{Math.round(220-ratio*90)}},255,.9)`;
    let pd=i===0?1:2,rd=i===0?5:3;rr(seg.x*CELL+pd,seg.y*CELL+pd,CELL-pd*2,CELL-pd*2,rd);ctx.fill();
    ctx.restore();
    if(i===0){{
      ctx.fillStyle='#0a0a1a';
      ctx.beginPath();ctx.arc(seg.x*CELL+CELL*.32+dir.y*CELL*.18,seg.y*CELL+CELL*.3-dir.x*CELL*.18,2.2,0,Math.PI*2);ctx.fill();
      ctx.beginPath();ctx.arc(seg.x*CELL+CELL*.68-dir.y*CELL*.18,seg.y*CELL+CELL*.3-dir.x*CELL*.18,2.2,0,Math.PI*2);ctx.fill();
    }}
  }});
}}
ctx.fillStyle='#070712';ctx.fillRect(0,0,CANVAS_S,CANVAS_S);
</script></body></html>""", height=GRID*CELL+90, scrolling=False)

    st.markdown("<br>",unsafe_allow_html=True)
    _,c2,_ = st.columns([1,2,1])
    with c2:
        st.markdown('<div class="btn-green">',unsafe_allow_html=True)
        if st.button("&#9654; משחק חדש", use_container_width=True, key="sn_new"):
            st.session_state["snake_played"] = S("snake_played",0)+1
            earn_coins(3); earn_xp(3)
            st.toast("&#128013; בהצלחה!")
        st.markdown('</div>',unsafe_allow_html=True)

    st.markdown("---")
    c1,c2 = st.columns(2)
    with c1: st.metric("&#127942; שיא", S("snake_hi",0))
    with c2: st.metric("&#127918; משחקים", S("snake_played",0))
    st.markdown("---")
    _score_report("snake", multiplier=0.4)

# ══════════════════════════════════════════════════════════
# FLAPPY
# ══════════════════════════════════════════════════════════
def page_flappy():
    st.markdown("<h1 style='text-align:center'>&#128054; פלאפי בירד</h1><p style='text-align:center;color:#7777aa'>SPACE / לחיצה לעוף</p>",unsafe_allow_html=True)

    slow   = "true" if has("flappy_slow") else "false"
    gap_b  = owned_count("flappy_gap")
    sh_cnt = owned_count("flappy_shield")
    hi     = S("flappy_hi",0)

    ups=[]
    if sh_cnt: ups.append(f"&#128737; {sh_cnt} מגנים")
    if has("flappy_slow"): ups.append("&#128012; איטי")
    if gap_b:  ups.append(f"&#128275; פתח +{gap_b}")
    if ups: st.markdown(f"<div class='inf'>{'  |  '.join(ups)}</div>",unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)

    _,col,_ = st.columns([1,5,1])
    with col:
        components.html(f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#050510;display:flex;flex-direction:column;align-items:center;
     padding:6px;font-family:Orbitron,monospace;user-select:none}}
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');
.hud{{display:flex;gap:10px;margin-bottom:6px;font-size:12px}}
.hi{{background:rgba(255,214,10,.09);border:1px solid rgba(255,214,10,.28);
     border-radius:7px;padding:4px 10px;color:#ffd60a}}
canvas{{border:2px solid rgba(255,214,10,.35);border-radius:10px;
        box-shadow:0 0 28px rgba(255,214,10,.12);cursor:pointer;display:block;max-width:100%}}
.ov{{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
     background:rgba(5,5,18,.93);border:2px solid #ffd60a;border-radius:12px;
     padding:18px 26px;text-align:center;min-width:175px}}
.ov h2{{color:#ffd60a;font-size:17px;margin-bottom:8px}}
.ov p{{color:#8888aa;font-size:11px;margin-bottom:12px}}
.ov button{{background:rgba(255,214,10,.18);color:#ffd60a;border:1px solid #ffd60a;
            padding:8px 20px;border-radius:7px;cursor:pointer;font-family:Orbitron;font-size:12px;font-weight:700}}
.ov button:hover{{background:rgba(255,214,10,.35)}}
.wrap{{position:relative}}
</style></head><body>
<div class="hud">
  <div class="hi">ניקוד: <span id="sc">0</span></div>
  <div class="hi">שיא: <span id="hi">{hi}</span></div>
  <div class="hi" id="sh_hud">&#128737;: <span id="sh">{sh_cnt}</span></div>
</div>
<div class="wrap">
<canvas id="c" width="340" height="460"></canvas>
<div class="ov" id="ov">
  <h2 id="ot">&#128054; פלאפי בירד</h2>
  <p id="ob">לחץ SPACE או לחץ להתחיל</p>
  <button onclick="startGame()">&#9654; שחק</button>
</div></div>
<script>
const W=340,H=460,BR=13;
const SLOW={slow},GAP_BONUS={gap_b}*12,INIT_SH={sh_cnt};
const PS=SLOW?1.7:2.4,GAP=115+GAP_BONUS;
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
let bird,pipes,score,frame,run,raf,shLeft,parts,stars,gOff;
function mkStars(){{stars=[];for(let i=0;i<55;i++)stars.push({{x:Math.random()*W,y:Math.random()*H*.78,r:Math.random()*1.4+.4,s:Math.random()*.28+.08}});}}
function startGame(){{
  document.getElementById('ov').style.display='none';
  bird={{x:75,y:H/2,vy:0,rot:0}};
  pipes=[];score=0;frame=0;run=true;shLeft=INIT_SH;parts=[];gOff=0;
  document.getElementById('sc').textContent='0';
  document.getElementById('sh').textContent=shLeft;
  if(raf)cancelAnimationFrame(raf);mkStars();loop();
}}
function flap(){{if(run)bird.vy=-7;}}
cv.addEventListener('click',flap);
document.addEventListener('keydown',e=>{{if(e.code==='Space'){{flap();e.preventDefault();}}}});
function loop(){{if(!run)return;update();draw();raf=requestAnimationFrame(loop);}}
function update(){{
  frame++;gOff=(gOff+PS)%(W*2);
  bird.vy+=.34;bird.y+=bird.vy;bird.rot=Math.min(Math.max(bird.vy*3,-30),90);
  parts=parts.filter(p=>p.l>0);parts.forEach(p=>{{p.x+=p.vx;p.y+=p.vy;p.l--;p.vy+=.1;}});
  stars.forEach(s=>{{s.x-=s.s;if(s.x<0)s.x=W;}});
  if(frame%82===0){{let th=55+Math.random()*(H-GAP-110);pipes.push({{x:W,th,ok:false}});}}
  pipes.forEach(p=>p.x-=PS);pipes=pipes.filter(p=>p.x>-70);
  pipes.forEach(p=>{{
    if(!p.ok&&p.x+38<bird.x){{p.ok=true;score++;document.getElementById('sc').textContent=score;
      for(let i=0;i<6;i++)parts.push({{x:bird.x,y:bird.y,vx:(Math.random()-.5)*4,vy:-Math.random()*4,l:22,c:'#ffd60a'}});}}
    if(bird.x+BR>p.x&&bird.x-BR<p.x+48){{
      if(bird.y-BR<p.th||bird.y+BR>p.th+GAP){{
        if(shLeft>0){{shLeft--;document.getElementById('sh').textContent=shLeft;
          for(let i=0;i<12;i++)parts.push({{x:bird.x,y:bird.y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,l:28,c:'#00f5ff'}});}}
        else die();
      }}
    }}
  }});
  if(bird.y+BR>H-28||bird.y-BR<0)die();
}}
function die(){{
  run=false;cancelAnimationFrame(raf);
  let hs=parseInt(document.getElementById('hi').textContent)||0;
  if(score>hs)document.getElementById('hi').textContent=score;
  document.getElementById('ot').textContent='&#128165; נפלת!';
  document.getElementById('ob').textContent='ניקוד: '+score+'  שיא: '+Math.max(score,hs);
  document.getElementById('ov').style.display='block';
  window.parent.postMessage({{type:'flappy_done',score}},'*');
}}
function dpipe(x,th){{
  let g=ctx.createLinearGradient(x,0,x+48,0);g.addColorStop(0,'#165016');g.addColorStop(.5,'#268926');g.addColorStop(1,'#165016');
  ctx.fillStyle=g;ctx.fillRect(x,0,48,th);ctx.fillStyle='#30a030';ctx.fillRect(x-4,th-18,56,18);
  let bot=th+GAP;ctx.fillStyle=g;ctx.fillRect(x,bot,48,H-bot);ctx.fillStyle='#30a030';ctx.fillRect(x-4,bot,56,18);
  ctx.shadowBlur=9;ctx.shadowColor='rgba(57,255,20,.35)';ctx.strokeStyle='rgba(57,255,20,.28)';
  ctx.lineWidth=1;ctx.strokeRect(x,0,48,th);ctx.strokeRect(x,bot,48,H-bot);ctx.shadowBlur=0;
}}
function draw(){{
  let sky=ctx.createLinearGradient(0,0,0,H);sky.addColorStop(0,'#040410');sky.addColorStop(.7,'#09092a');sky.addColorStop(1,'#0c180c');
  ctx.fillStyle=sky;ctx.fillRect(0,0,W,H);
  stars.forEach(s=>{{ctx.globalAlpha=.5+Math.sin(frame*.05+s.x)*.4;ctx.fillStyle='#fff';
    ctx.beginPath();ctx.arc(s.x,s.y,s.r,0,Math.PI*2);ctx.fill();}});ctx.globalAlpha=1;
  parts.forEach(p=>{{ctx.globalAlpha=p.l/28;ctx.fillStyle=p.c;
    ctx.beginPath();ctx.arc(p.x,p.y,2.5,0,Math.PI*2);ctx.fill();}});ctx.globalAlpha=1;
  pipes.forEach(p=>dpipe(p.x,p.th));
  ctx.fillStyle='#162a10';ctx.fillRect(0,H-28,W,28);ctx.fillStyle='#245018';ctx.fillRect(0,H-28,W,7);
  ctx.save();ctx.translate(bird.x,bird.y);ctx.rotate(bird.rot*Math.PI/180);
  if(shLeft>0){{ctx.beginPath();ctx.arc(0,0,BR+8,0,Math.PI*2);
    ctx.strokeStyle='rgba(0,245,255,'+(0.38+Math.sin(frame*.14)*.28)+')';ctx.lineWidth=2;ctx.stroke();}}
  ctx.shadowBlur=11;ctx.shadowColor='#ffd60a';ctx.fillStyle='#ffd60a';
  ctx.beginPath();ctx.ellipse(0,0,BR,BR-2,0,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='#ff9200';ctx.beginPath();ctx.ellipse(-4,2,7,4,Math.PI/4+Math.sin(frame*.28)*.4,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='#fff';ctx.beginPath();ctx.arc(5,-2,3.5,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='#1a1a3a';ctx.beginPath();ctx.arc(6,-2,2.2,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='#ff5500';ctx.beginPath();ctx.moveTo(BR-.5,0);ctx.lineTo(BR+6,1.5);ctx.lineTo(BR-.5,-1.5);ctx.fill();
  ctx.shadowBlur=0;ctx.restore();
  ctx.fillStyle='rgba(255,214,10,.92)';ctx.font='bold 26px Orbitron,monospace';
  ctx.textAlign='center';ctx.shadowBlur=14;ctx.shadowColor='#ffd60a';ctx.fillText(score,W/2,46);ctx.shadowBlur=0;
}}
mkStars();ctx.fillStyle='#040410';ctx.fillRect(0,0,W,H);
</script></body></html>""", height=510, scrolling=False)

    st.markdown("<br>",unsafe_allow_html=True)
    _,c2,_ = st.columns([1,2,1])
    with c2:
        st.markdown('<div class="btn-gold">',unsafe_allow_html=True)
        if st.button("&#9654; משחק חדש", use_container_width=True, key="fl_new"):
            st.session_state["flappy_played"] = S("flappy_played",0)+1
            earn_coins(3); earn_xp(3); st.toast("&#128054; בהצלחה!")
        st.markdown('</div>',unsafe_allow_html=True)

    st.markdown("---")
    c1,c2 = st.columns(2)
    with c1: st.metric("&#127942; שיא", S("flappy_hi",0))
    with c2: st.metric("&#127918; משחקים", S("flappy_played",0))
    st.markdown("---")
    _score_report("flappy", multiplier=3)

# ══════════════════════════════════════════════════════════
# MEMORY  — with flip animation + correct 2-card reveal
# ══════════════════════════════════════════════════════════
EMOJIS = ["&#127987;","&#127775;","&#128293;","&#9889;","&#128142;","&#128640;","&#127754;","&#127925;",
          "&#128150;","&#128140;","&#127939;","&#127808;","&#127774;","&#127752;","&#127963;","&#127881;"]

def _mem_reset():
    chosen = random.sample(range(len(EMOJIS)), 8)
    board  = chosen * 2; random.shuffle(board)
    st.session_state.update({
        "mb": board, "mf": [], "mm": set(), "mov": 0,
        "mcp": False, "mcp_time": 0,
        "mh": owned_count("mem_hint")*2,
        "mft": 0.6 + owned_count("mem_flip_time")*0.4,
    })

def page_memory():
    st.markdown("<h1 style='text-align:center'>&#129504; זיכרון</h1><p style='text-align:center;color:#7777aa'>מצא זוגות — לחץ על קלף לגלות</p>",unsafe_allow_html=True)
    if has("mem_x2"): st.markdown("<div class='inf'>&#10006;2 ניקוד פעיל!</div>",unsafe_allow_html=True)
    if "mb" not in st.session_state: _mem_reset()

    board   = st.session_state["mb"]
    flipped = list(st.session_state["mf"])
    matched = set(st.session_state["mm"])
    moves   = S("mov",0)
    hints   = S("mh",0)

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.metric("&#127919; מהלכים", moves)
    with c2: st.metric("&#9989; זוגות",    len(matched)//2)
    with c3: st.metric("&#127183; נותרו",   8-len(matched)//2)
    with c4: st.metric("&#128161; רמזים",   hints)
    st.markdown("<br>",unsafe_allow_html=True)

    # Win check
    if len(matched)==16:
        sc = max(80-moves*2,10)*(2 if has("mem_x2") else 1)
        e  = earn_coins(sc); earn_xp(sc//2)
        st.session_state["mem_played"] = S("mem_played",0)+1
        if sc > S("mem_hi",0):
            st.session_state["mem_hi"] = sc
            _ach("&#129504; שיא זיכרון!")
        if moves <= 10: _ach("&#129504; מוח של זהב!")
        st.markdown(f"<div class='ok' style='font-size:18px;padding:20px'>&#127881; סיימת ב-{moves} מהלכים! +{e} &#128170;</div>",unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
        _,mc,_ = st.columns([1,2,1])
        with mc:
            st.markdown('<div class="btn-green">',unsafe_allow_html=True)
            if st.button("&#128260; משחק חדש", use_container_width=True, key="mr"):
                _mem_reset(); st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)
        return

    # Pending mismatch delay
    if S("mcp") and time.time()-S("mcp_time",0) >= S("mft",0.6):
        f = list(S("mf",[]))
        if len(f)==2:
            i1,i2=f[0],f[1]
            if board[i1]==board[i2]: matched.add(i1); matched.add(i2); st.session_state["mm"]=matched
        st.session_state["mf"]=[]; st.session_state["mcp"]=False; st.rerun()
    if S("mcp"):
        st.rerun()

    # Build HTML board — all in one iframe for smooth flip animation
    # We pass state as JSON and render entirely in JS
    import json
    board_json = json.dumps(board)
    emojis_json = json.dumps(EMOJIS)
    flipped_json = json.dumps(flipped)
    matched_list = sorted(matched)
    matched_json = json.dumps(matched_list)
    can_flip = len(flipped)<2 and not S("mcp")

    board_html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:transparent;padding:4px;font-family:sans-serif}}
.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;max-width:380px;margin:0 auto}}
.cell{{position:relative;width:100%;padding-top:100%;cursor:pointer;perspective:600px}}
.inner{{position:absolute;inset:0;transform-style:preserve-3d;transition:transform .45s ease;border-radius:10px}}
.inner.flipped{{transform:rotateY(180deg)}}
.front,.back{{position:absolute;inset:0;border-radius:10px;display:flex;align-items:center;justify-content:center;
              backface-visibility:hidden;-webkit-backface-visibility:hidden;font-size:28px;font-weight:700}}
.front{{background:linear-gradient(135deg,rgba(191,95,255,.18),rgba(191,95,255,.06));
        border:2px solid rgba(191,95,255,.4);color:#bf5fff}}
.back{{background:linear-gradient(135deg,rgba(0,245,255,.15),rgba(0,245,255,.04));
       border:2px solid rgba(0,245,255,.45);transform:rotateY(180deg);color:#fff;font-size:28px}}
.cell.matched .inner{{transform:rotateY(180deg)}}
.cell.matched .back{{background:linear-gradient(135deg,rgba(57,255,20,.18),rgba(57,255,20,.06));
  border-color:rgba(57,255,20,.55);box-shadow:0 0 18px rgba(57,255,20,.25)}}
.cell:not(.matched):not(.no-click) .front:hover{{background:rgba(191,95,255,.3);border-color:rgba(191,95,255,.7)}}
</style></head><body>
<div class="grid" id="grid"></div>
<script>
const BOARD  = {board_json};
const EMOJIS = {emojis_json};
const FLIPPED= new Set({flipped_json});
const MATCHED= new Set({matched_json});
const CAN    = {'true' if can_flip else 'false'};

function build(){{
  const g=document.getElementById('grid');
  BOARD.forEach((eIdx,i)=>{{
    const isMatch=MATCHED.has(i);
    const isFlip=FLIPPED.has(i)||isMatch;
    const cell=document.createElement('div');
    cell.className='cell'+(isMatch?' matched':'')+((!CAN&&!isFlip)?' no-click':'');
    cell.innerHTML=`<div class="inner ${{isFlip?'flipped':''}}">
      <div class="front">?</div>
      <div class="back">${{EMOJIS[eIdx]}}</div></div>`;
    if(!isMatch&&!isFlip&&CAN)
      cell.addEventListener('click',()=>window.parent.postMessage({{type:'mem_flip',idx:i}},'*'));
    g.appendChild(cell);
  }});
}}
build();
</script></body></html>"""

    components.html(board_html, height=440, scrolling=False)

    # Listen for flip messages via a hack: use session_state + rerun via button
    st.markdown("<br>",unsafe_allow_html=True)

    # Manual flip buttons (hidden below, triggered by clicking labeled buttons)
    # We use a more reliable approach: show clickable placeholder styled as cards
    st.markdown("**בחר קלף — לחץ על המספר:**", unsafe_allow_html=False)
    available = [i for i in range(16) if i not in matched and i not in flipped and not S("mcp")]
    if available and can_flip:
        btn_cols = st.columns(8)
        for j, i in enumerate(available[:8]):
            with btn_cols[j % 8]:
                if st.button(f"{i+1}", key=f"mc_{i}_{moves}"):
                    flipped.append(i)
                    st.session_state["mf"] = flipped
                    if len(flipped)==2:
                        st.session_state["mov"] = moves+1
                        st.session_state["mcp"] = True
                        st.session_state["mcp_time"] = time.time()
                    st.rerun()
        if len(available) > 8:
            btn_cols2 = st.columns(8)
            for j, i in enumerate(available[8:]):
                with btn_cols2[j % 8]:
                    if st.button(f"{i+1}", key=f"mc2_{i}_{moves}"):
                        flipped.append(i)
                        st.session_state["mf"] = flipped
                        if len(flipped)==2:
                            st.session_state["mov"] = moves+1
                            st.session_state["mcp"] = True
                            st.session_state["mcp_time"] = time.time()
                        st.rerun()

    # Show what's currently revealed
    if flipped or matched:
        visible = []
        for i in sorted(set(flipped)|matched):
            visible.append(f"קלף {i+1}: {EMOJIS[board[i]]}")
        st.markdown(f"<div class='inf' style='font-size:12px'>&#128065; גלויים: {' | '.join(visible[:6])}</div>",unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    with c1:
        st.markdown('<div class="btn-red">',unsafe_allow_html=True)
        if st.button("&#128260; איפוס", use_container_width=True, key="mem_rst"):
            _mem_reset(); st.rerun()
        st.markdown('</div>',unsafe_allow_html=True)
    with c2:
        if hints>0:
            st.markdown('<div class="btn-gold">',unsafe_allow_html=True)
            if st.button(f"&#128161; רמז ({hints})", use_container_width=True, key="mem_hint_btn"):
                un=[i for i in range(16) if i not in matched and i not in flipped]
                seen={}
                for i in un:
                    e=board[i]
                    if e in seen:
                        st.session_state["mf"]=[seen[e],i]
                        st.session_state["mov"]=moves+1
                        st.session_state["mcp"]=True
                        st.session_state["mcp_time"]=time.time()
                        st.session_state["mh"]=hints-1
                        st.rerun(); break
                    seen[e]=i
            st.markdown('</div>',unsafe_allow_html=True)
    with c3: st.metric("&#127942; שיא", S("mem_hi",0))

# ══════════════════════════════════════════════════════════
# TIC TAC TOE
# ══════════════════════════════════════════════════════════
def _tw(b):
    for a,bx,c in [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]:
        if b[a] and b[a]==b[bx]==b[c]: return b[a]
    return None

def _mm(b,is_max,d,ai_weakness):
    w=_tw(b)
    if w=="O": return 10-d
    if w=="X": return d-10
    emp=[i for i,v in enumerate(b) if v==""]
    if not emp: return 0
    # weakness: occasionally skip optimal
    if ai_weakness>0 and random.random()<ai_weakness*0.12 and d==0:
        return random.choice([-1,0,1])
    if is_max:
        bst=-99
        for i in emp: b[i]="O";bst=max(bst,_mm(b,False,d+1,ai_weakness));b[i]=""
        return bst
    else:
        bst=99
        for i in emp: b[i]="X";bst=min(bst,_mm(b,True,d+1,ai_weakness));b[i]=""
        return bst

def _ai(b):
    weakness = owned_count("ttt_easy")
    if weakness>=3 and random.random()<0.5:
        emp=[i for i,v in enumerate(b) if v==""]
        return random.choice(emp) if emp else None
    bst=-99;mv=None
    for i in [j for j,v in enumerate(b) if v==""]:
        b[i]="O";s=_mm(b,False,0,weakness);b[i]=""
        if s>bst: bst=s;mv=i
    return mv

def _ttt_reset():
    st.session_state.update({"tb":[""]*9,"to":False,"ts":"","tp":None})

def page_tictactoe():
    st.markdown("<h1 style='text-align:center'>&#10060; איקס-עיגול</h1><p style='text-align:center;color:#7777aa'>אתה X, המחשב O</p>",unsafe_allow_html=True)

    undo_cnt = owned_count("ttt_undo")
    if has("ttt_preview"): st.markdown("<div class='inf'>&#128302; תצוגה מקדימה פעילה</div>",unsafe_allow_html=True)
    if "tb" not in st.session_state: _ttt_reset()

    b=st.session_state["tb"]; ov=S("to"); ts=S("ts",""); prev=S("tp")

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.metric("&#9989; נצחונות", S("ttt_w",0))
    with c2: st.metric("&#10060; הפסדים", S("ttt_l",0))
    with c3: st.metric("&#129309; תיקו",  S("ttt_d",0))
    with c4: st.metric("&#127918; משחקים",S("ttt_played",0))
    st.markdown("<br>",unsafe_allow_html=True)

    if ts:
        cls="ok" if "ניצחת" in ts else ("err" if "הפסדת" in ts else "inf")
        st.markdown(f"<div class='{cls}' style='font-size:16px;padding:16px'>{ts}</div>",unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)

    if has("ttt_preview") and not ov:
        am=_ai(b[:])
        if am is not None:
            st.markdown(f"<div style='color:#bf5fff;font-size:12px;text-align:center;margin-bottom:8px'>&#128302; AI מתכנן: מיקום {am+1}</div>",unsafe_allow_html=True)

    # Board — 3 cols centered, fixed small size
    _,mc,_ = st.columns([1,3,1])
    with mc:
        # CSS to fix button heights
        st.markdown("""<style>
div[data-testid="column"] button{min-height:70px!important;max-height:70px!important;
  font-size:32px!important;font-weight:900!important;border-radius:12px!important;}
</style>""",unsafe_allow_html=True)
        for row in range(3):
            rc = st.columns(3)
            for ci in range(3):
                idx=row*3+ci
                with rc[ci]:
                    cell=b[idx]
                    if cell=="X":
                        st.markdown(f"""<div style="height:70px;background:rgba(0,245,255,.12);
                            border:2px solid rgba(0,245,255,.5);border-radius:12px;display:flex;
                            align-items:center;justify-content:center;font-size:36px;font-weight:900;
                            color:#00f5ff;text-shadow:0 0 16px rgba(0,245,255,.8);
                            animation:pp .22s cubic-bezier(.34,1.56,.64,1)">&#10005;</div>
                            <style>@keyframes pp{{from{{transform:scale(.25);opacity:0}}to{{transform:scale(1);opacity:1}}}}</style>""",
                            unsafe_allow_html=True)
                    elif cell=="O":
                        st.markdown(f"""<div style="height:70px;background:rgba(255,0,110,.12);
                            border:2px solid rgba(255,0,110,.5);border-radius:12px;display:flex;
                            align-items:center;justify-content:center;font-size:36px;font-weight:900;
                            color:#ff006e;text-shadow:0 0 16px rgba(255,0,110,.8);
                            animation:pp .22s cubic-bezier(.34,1.56,.64,1)">&#9711;</div>""",
                            unsafe_allow_html=True)
                    elif not ov:
                        if st.button(" ", key=f"tt_{idx}_{sum(1 for x in b if x)}", use_container_width=True):
                            st.session_state["tp"]=b[:]
                            b[idx]="X"
                            w=_tw(b)
                            if w: _ttt_end(w,b); return
                            if "" not in b: _ttt_end("draw",b); return
                            ai=_ai(b)
                            if ai is not None:
                                b[ai]="O"
                                w=_tw(b)
                                if w: _ttt_end(w,b); return
                                if "" not in b: _ttt_end("draw",b); return
                            st.session_state["tb"]=b; st.rerun()
                    else:
                        st.markdown("""<div style="height:70px;background:rgba(255,255,255,.02);
                            border:2px solid rgba(255,255,255,.06);border-radius:12px"></div>""",
                            unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    with c1:
        st.markdown('<div class="btn-green">',unsafe_allow_html=True)
        if st.button("&#128260; חדש", use_container_width=True, key="ttt_new"):
            _ttt_reset(); st.rerun()
        st.markdown('</div>',unsafe_allow_html=True)
    with c2:
        if undo_cnt>0 and prev and not ov:
            st.markdown('<div class="btn-gold">',unsafe_allow_html=True)
            if st.button(f"&#8617; ביטול ({undo_cnt})", use_container_width=True, key="ttt_undo"):
                st.session_state["tb"]=prev; st.session_state["tp"]=None
                st.session_state["ts"]=""; st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)
    with c3:
        st.selectbox("קושי AI", ["רגיל","קל","ילד"], key="ttt_diff_sel", label_visibility="visible")
    with c4:
        st.metric("&#127942; שיא", S("ttt_w",0))

def _ttt_end(result,b):
    st.session_state["ttt_played"]=S("ttt_played",0)+1
    st.session_state["to"]=True; st.session_state["tb"]=b
    if result=="X":
        st.session_state["ttt_w"]=S("ttt_w",0)+1
        e=earn_coins(50); earn_xp(25); st.session_state["ts"]=f"&#127881; ניצחת! +{e} &#128170;"
        w=S("ttt_w",0)
        if w in (1,5,10,25,50): _ach(f"&#10060; {w} נצחונות!")
    elif result=="O":
        st.session_state["ttt_l"]=S("ttt_l",0)+1
        e=earn_coins(5); st.session_state["ts"]=f"&#128533; הפסדת... +{e} &#128170;"
    else:
        st.session_state["ttt_d"]=S("ttt_d",0)+1
        e=earn_coins(15); earn_xp(8); st.session_state["ts"]=f"&#129309; תיקו! +{e} &#128170;"
    st.rerun()

# ══════════════════════════════════════════════════════════
# CLICKER
# ══════════════════════════════════════════════════════════
def page_clicker():
    st.markdown("<h1 style='text-align:center'>&#128070; קליקר</h1>",unsafe_allow_html=True)

    mul      = 1 + owned_count("clicker_mul")
    duration = 10 + owned_count("clicker_time")*3
    auto     = has("clicker_auto")
    ups=[]
    if mul>1: ups.append(f"&#215;{mul} קליקים")
    if duration>10: ups.append(f"&#9201; {duration}s")
    if auto: ups.append("&#129302; אוטו")
    if ups: st.markdown(f"<div class='inf'>{'  |  '.join(ups)}</div>",unsafe_allow_html=True)

    if "ck_st" not in st.session_state:
        st.session_state.update({"ck_st":"idle","ck_cnt":0,"ck_start":0})

    state=S("ck_st"); count=S("ck_cnt",0); best=S("click_hi",0)

    if state=="playing":
        elapsed=time.time()-S("ck_start",0)
        remain=max(0,duration-elapsed)
        if auto: st.session_state["ck_cnt"]=count+mul; count=S("ck_cnt",0)
        col="#ff006e"
        anim="clkFlash .18s infinite" if remain<3 else "none"
        st.markdown(f"""<div style="text-align:center;margin-bottom:12px">
<div style="font-family:Orbitron,sans-serif;font-size:56px;font-weight:900;color:{col};
     text-shadow:0 0 28px {col}cc;animation:{anim}">{remain:.1f}</div>
<div style="color:#7777aa;font-size:12px">שניות נשארו</div></div>
<style>@keyframes clkFlash{{0%,100%{{color:#ff006e}}50%{{color:#ff5555}}}}</style>""",unsafe_allow_html=True)
        st.progress(remain/duration)
        if remain<=0: st.session_state["ck_st"]="done"; st.rerun()

    click_col="#ff006e" if state=="playing" else ("#39ff14" if state=="done" else "#7777aa")
    st.markdown(f"""<div style="text-align:center;margin:12px 0">
<div style="font-family:Orbitron,sans-serif;font-size:76px;font-weight:900;
     color:{click_col};text-shadow:0 0 36px {click_col}80">{count}</div>
<div style="color:#7777aa;font-size:13px">קליקים</div></div>""",unsafe_allow_html=True)

    _,c2,_ = st.columns([1,2,1])
    with c2:
        if state=="idle":
            st.markdown('<div class="btn-red btn-big">',unsafe_allow_html=True)
            if st.button("&#128640; התחל!", use_container_width=True, key="ck_go"):
                st.session_state.update({"ck_st":"playing","ck_cnt":0,"ck_start":time.time()})
                st.session_state["click_sessions"]=S("click_sessions",0)+1
                st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)
        elif state=="playing":
            st.markdown("""<style>
div.ck_big .stButton>button{background:linear-gradient(135deg,rgba(255,0,110,.38),rgba(255,0,110,.14))!important;
  border:2px solid rgba(255,0,110,.75)!important;color:#ff006e!important;font-size:24px!important;
  height:110px!important;font-weight:900!important;box-shadow:0 0 28px rgba(255,0,110,.28)!important;}
div.ck_big .stButton>button:active{transform:scale(.93)!important;}</style>""",unsafe_allow_html=True)
            st.markdown('<div class="ck_big">',unsafe_allow_html=True)
            if st.button("&#128070; לחץ!", use_container_width=True, key="ck_click"):
                st.session_state["ck_cnt"]=count+mul
                st.session_state["click_total"]=S("click_total",0)+mul
                st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)
        elif state=="done":
            final=S("ck_cnt",0)
            e=earn_coins(final*2); earn_xp(final)
            if final>best:
                st.session_state["click_hi"]=final
                _ach(f"&#128070; שיא קליקר: {final}!")
                st.markdown(f"<div class='ok' style='font-size:17px;margin-bottom:12px'>&#127942; שיא! {final} קליקים! +{e} &#128170;</div>",unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='inf' style='margin-bottom:12px'>{final} קליקים! +{e} &#128170;</div>",unsafe_allow_html=True)
            st.markdown('<div class="btn-green">',unsafe_allow_html=True)
            if st.button("&#128260; שוב", use_container_width=True, key="ck_re"):
                st.session_state["ck_st"]="idle"; st.session_state["ck_cnt"]=0; st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)

    if state=="playing": time.sleep(0.05); st.rerun()

    st.markdown("---")
    c1,c2,c3=st.columns(3)
    with c1: st.metric("&#127942; שיא",           S("click_hi",0))
    with c2: st.metric("&#128070; סה\"כ",         S("click_total",0))
    with c3: st.metric("&#127918; סבבים",         S("click_sessions",0))

# ══════════════════════════════════════════════════════════
# SLOT MACHINE — rendered as styled HTML to avoid raw code
# ══════════════════════════════════════════════════════════
SL_SYM = ["&#127826;","&#127819;","&#127818;","&#127815;","&#11088;","&#128142;","&#127920;","&#127183;"]
SL_W   = [20,18,15,12,10,7,4,14]
SL_PAY = {0:5,1:8,2:10,3:15,4:20,5:50,6:100,7:35}  # index -> multiplier

def page_slot():
    st.markdown("<h1 style='text-align:center'>&#127920; מכונת מזל</h1><p style='text-align:center;color:#7777aa'>הימר וסובב!</p>",unsafe_allow_html=True)

    luck_lv  = owned_count("slot_luck")
    jackpot_lv = owned_count("slot_jackpot")
    refund   = has("slot_refund")
    ups=[]
    if luck_lv:    ups.append(f"&#127808; מזל +{luck_lv}")
    if jackpot_lv: ups.append(f"&#128176; ג'קפוט x{2**jackpot_lv}")
    if refund:     ups.append("&#8617; החזר 10%")
    if ups: st.markdown(f"<div class='inf'>{'  |  '.join(ups)}</div>",unsafe_allow_html=True)

    if "sl_r" not in st.session_state:
        st.session_state.update({"sl_r":[6,6,6],"sl_res":"","sl_bet":10})

    reels  = st.session_state["sl_r"]
    result = S("sl_res","")
    coins  = S("coins",0)
    is_win = "ניצחת" in result or "קפוט" in result
    is_jp  = "קפוט" in result

    # Machine rendered as pure HTML
    r_html = "".join(f"""
<div style="flex:1;max-width:110px;aspect-ratio:1;
     background:linear-gradient(160deg,#1e0e00,#120800);
     border:2px solid rgba(255,124,0,.45);border-radius:12px;
     display:flex;align-items:center;justify-content:center;
     font-size:56px;box-shadow:inset 0 0 18px rgba(0,0,0,.7);
     {'animation:spinA .08s linear infinite;' if S('sl_spinning') else ''}">
  {SL_SYM[r]}
</div>""" for r in reels)

    border = "rgba(255,214,10,.85)" if is_jp else ("rgba(255,214,10,.5)" if is_win else "rgba(255,124,0,.4)")
    glow   = "0 0 35px rgba(255,214,10,.45)" if is_win else "0 0 20px rgba(255,124,0,.1)"
    pulse  = "animation:slFlash .28s infinite;" if is_jp else ""

    st.markdown(f"""
<div style="max-width:430px;margin:0 auto;padding:20px;
     background:linear-gradient(145deg,#180a00,#220e00,#180a00);
     border:3px solid {border};border-radius:18px;
     box-shadow:{glow},inset 0 0 28px rgba(0,0,0,.55);{pulse}">
  <div style="text-align:center;margin-bottom:14px">
    <span style="font-family:Orbitron,sans-serif;font-size:17px;font-weight:900;
          color:#ff7c00;text-shadow:0 0 12px rgba(255,124,0,.75);letter-spacing:3px">
      &#127920; ARCADE SLOTS</span>
  </div>
  <div style="display:flex;gap:12px;justify-content:center;padding:14px 10px;
       background:rgba(0,0,0,.55);border-radius:12px;border:1px solid rgba(255,124,0,.18)">
    {r_html}
  </div>
  <div style="margin-top:10px;height:3px;
       background:linear-gradient(90deg,transparent,{'#ffd60a' if is_win else 'rgba(255,124,0,.3)'},transparent);
       {'box-shadow:0 0 8px #ffd60a;' if is_win else ''}"></div>
</div>
<style>
@keyframes slFlash{{0%,100%{{border-color:rgba(255,214,10,.85)}}50%{{border-color:rgba(255,214,10,.1)}}}}
@keyframes spinA{{0%{{opacity:.4}}50%{{opacity:1}}100%{{opacity:.4}}}}
</style>""", unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)

    if result:
        cls = "ok" if is_win else "err"
        st.markdown(f"<div class='{cls}' style='font-size:15px'>{result}</div>",unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)

    c1,c2 = st.columns([3,1])
    with c1:
        max_bet = max(5, min(200, coins)) if coins>=5 else 5
        bet=st.slider("הימור &#128170;", 5, max_bet, min(S("sl_bet",10), max_bet), 5, key="sl_sl")
        st.session_state["sl_bet"]=bet
    with c2: st.metric("יתרה", f"{coins}")

    _,c2,_ = st.columns([1,2,1])
    with c2:
        st.markdown("""<style>div.spbtn .stButton>button{
          background:linear-gradient(135deg,rgba(255,124,0,.38),rgba(255,124,0,.14))!important;
          border:2px solid rgba(255,124,0,.65)!important;color:#ff7c00!important;
          font-size:18px!important;height:58px!important;font-weight:900!important;}</style>""",unsafe_allow_html=True)
        can=coins>=bet
        st.markdown('<div class="spbtn">',unsafe_allow_html=True)
        if st.button("&#127920; סובב!", use_container_width=True, key="sl_spin", disabled=not can):
            _spin(bet, luck_lv, jackpot_lv, refund)
        st.markdown('</div>',unsafe_allow_html=True)
    if not can: st.markdown("<div class='err'>אין מספיק מטבעות!</div>",unsafe_allow_html=True)

    st.markdown("---")
    with st.expander("&#128203; טבלת תשלומים"):
        names = ["&#127826; דובדבן","&#127819; לימון","&#127818; תפוז","&#127815; ענבים",
                 "&#11088; כוכב","&#128142; יהלום","&#127920; ג'קפוט","&#127183; ג'וקר"]
        for idx,mul in SL_PAY.items():
            am = mul * (2**jackpot_lv if mul>=50 else 1)
            bar=idx
            st.markdown(f"""<div style="display:flex;justify-content:space-between;padding:5px 10px;
              background:rgba(255,124,0,.05);border-radius:7px;margin-bottom:3px">
              <span style="font-size:18px">{names[idx]} {names[idx]} {names[idx]}</span>
              <span style="color:#ff7c00;font-weight:700;font-family:Orbitron">x{am}</span></div>""",
              unsafe_allow_html=True)

    st.markdown("---")
    c1,c2,c3=st.columns(3)
    with c1: st.metric("&#127920; סיבובים",  S("slot_spins",0))
    with c2: st.metric("&#127942; זכיות",    S("slot_wins",0))
    with c3: st.metric("&#128176; סה\"כ",    S("slot_total_won",0))

def _spin(bet, luck_lv, jackpot_lv, refund):
    if S("coins",0)<bet: return
    st.session_state["coins"]-=bet
    st.session_state["slot_spins"]=S("slot_spins",0)+1
    w=SL_W[:]
    for i in [4,5,6]: w[i]=int(w[i]*(1+luck_lv*0.3))
    reels=[random.choices(range(8),weights=w,k=1)[0] for _ in range(3)]
    st.session_state["sl_r"]=reels
    pay=0
    if reels[0]==reels[1]==reels[2]:
        pay=SL_PAY[reels[0]]
        if jackpot_lv and reels[0]>=4: pay*=(2**jackpot_lv)
    elif reels[0]==reels[1] or reels[1]==reels[2] or reels[0]==reels[2]:
        pay=2
    if pay>0:
        won=bet*pay; e=earn_coins(won); earn_xp(won//5)
        st.session_state["slot_wins"]=S("slot_wins",0)+1
        st.session_state["slot_total_won"]=S("slot_total_won",0)+e
        if pay>=100: st.session_state["sl_res"]=f"&#127881; &#127920; ג'קפוט!!! +{e} &#128170;"; _ach("&#127920; ג'קפוט!")
        elif pay>=20: st.session_state["sl_res"]=f"&#11088; ניצחת! +{e} &#128170; (x{pay})"
        else: st.session_state["sl_res"]=f"&#9989; ניצחת! +{e} &#128170; (x{pay})"
    else:
        if refund:
            rb=max(1,int(bet*0.1)); earn_coins(rb)
            st.session_state["sl_res"]=f"&#128533; הפסדת {bet} &#128170;... החזר: {rb}"
        else:
            st.session_state["sl_res"]=f"&#128533; הפסדת {bet} &#128170;... נסה שוב!"
    st.rerun()

# ══════════════════════════════════════════════════════════
# SHOP
# ══════════════════════════════════════════════════════════
def page_shop():
    coins=S("coins",0)
    st.markdown(f"""<div style="text-align:center;margin-bottom:20px">
<h1>&#128722; חנות שדרוגים</h1>
<div style="display:inline-flex;align-items:center;gap:10px;padding:10px 22px;
     background:rgba(255,214,10,.07);border:1px solid rgba(255,214,10,.35);border-radius:10px;margin-top:6px">
  <span style="font-size:24px">&#128170;</span>
  <span style="font-family:Orbitron,sans-serif;font-size:24px;font-weight:900;color:#ffd60a;
       text-shadow:0 0 12px rgba(255,214,10,.7)">{coins:,}</span>
  <span style="color:#7777aa;font-size:12px">מטבעות</span>
</div></div>""", unsafe_allow_html=True)

    by_game={}
    for uid,item in SHOP.items(): by_game.setdefault(item["game"],[]).append((uid,item))

    tabs_order=["global","snake","flappy","memory","clicker","slot","ttt"]
    tab_labels=[GAME_LBL.get(g,g) for g in tabs_order if g in by_game]
    tab_games =[g for g in tabs_order if g in by_game]

    tabs=st.tabs(tab_labels)
    for ti,(tab,game) in enumerate(zip(tabs,tab_games)):
        with tab:
            items=by_game[game]
            cols=st.columns(min(len(items),3))
            for i,(uid,item) in enumerate(items):
                cnt=owned_count(uid)
                mx=item["max"]
                maxed=cnt>=mx
                can=(coins>=item["price"] and not maxed)
                col_="#39ff14" if maxed else ("#ffd60a" if can else "#7777aa")
                bg_="rgba(57,255,20,.07)" if maxed else "rgba(255,255,255,.02)"
                brd_="rgba(57,255,20,.4)" if maxed else ("rgba(255,214,10,.35)" if can else "rgba(255,255,255,.06)")
                badge=(f"<div style='position:absolute;top:7px;right:7px;background:rgba(57,255,20,.18);"
                       f"border:1px solid rgba(57,255,20,.5);border-radius:5px;padding:1px 7px;"
                       f"font-size:10px;color:#39ff14;font-weight:700'>&#10003; MAX</div>") if maxed else \
                      (f"<div style='position:absolute;top:7px;right:7px;background:rgba(255,214,10,.12);"
                       f"border:1px solid rgba(255,214,10,.4);border-radius:5px;padding:1px 7px;"
                       f"font-size:10px;color:#ffd60a;font-weight:700'>{cnt}/{mx}</div>") if cnt else ""
                with cols[i%3]:
                    st.markdown(f"""<div style="background:{bg_};border:1px solid {brd_};border-radius:12px;
                         padding:16px;text-align:center;margin-bottom:8px;min-height:140px;position:relative;">
                      {badge}
                      <div style="font-size:32px;margin-bottom:6px">{item["icon"]}</div>
                      <div style="font-weight:700;font-size:12px;color:{col_};margin-bottom:4px">{item["name"]}</div>
                      <div style="color:#7777aa;font-size:11px;margin-bottom:10px;line-height:1.4">{item["desc"]}</div>
                      <div style="font-family:Orbitron,sans-serif;font-size:14px;font-weight:900;
                           color:{'#39ff14' if maxed else '#ffd60a'}">
                           {'MAX ✓' if maxed else f'&#128170; {item["price"]:,}'}</div>
                    </div>""", unsafe_allow_html=True)
                    if not maxed:
                        st.markdown(f'<div class="{"btn-gold" if can else ""}">',unsafe_allow_html=True)
                        if st.button("&#128722; קנה" if can else "&#128274; חסר",
                                     key=f"sh_{uid}_{cnt}", use_container_width=True, disabled=not can):
                            ok,msg=buy(uid)
                            if ok: st.rerun()
                            else: st.markdown(f"<div class='err'>{msg}</div>",unsafe_allow_html=True)
                        st.markdown('</div>',unsafe_allow_html=True)

    st.markdown("---")
    owned={k:v for k,v in S("owned",{}).items() if v>0}
    if owned:
        st.markdown("### &#127890; השדרוגים שלך")
        b="".join(f"<span style='display:inline-flex;align-items:center;gap:5px;padding:5px 11px;"
                  f"background:rgba(57,255,20,.07);border:1px solid rgba(57,255,20,.3);border-radius:14px;"
                  f"font-size:11px;font-weight:700;color:#39ff14;margin:3px'>"
                  f"{SHOP[uid]['icon']} {SHOP[uid]['name']}"
                  f"{'x'+str(cnt) if cnt>1 else ''}</span>"
                  for uid,cnt in owned.items() if uid in SHOP)
        st.markdown(f"<div style='display:flex;flex-wrap:wrap'>{b}</div>",unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# SCORE REPORT HELPER  (only for snake + flappy, limited)
# ══════════════════════════════════════════════════════════
def _score_report(game, multiplier=1.0):
    hi_key = f"{game}_hi"
    played_key = f"{game}_played"
    st.markdown(f"<p style='color:#7777aa;font-size:12px'>הזן ניקוד לקבל מטבעות (ניתן פעם אחת בין משחקים):</p>",unsafe_allow_html=True)
    lock_key = f"{game}_sc_locked"
    if S(lock_key):
        st.markdown("<div class='warn'>&#128274; כבר דווח ניקוד — שחק שוב כדי לדווח</div>",unsafe_allow_html=True)
        return
    c1,c2=st.columns([3,1])
    with c1:
        sc=st.number_input("ניקוד",0,9999,0,key=f"{game}_sc_in",label_visibility="collapsed")
    with c2:
        st.markdown('<div class="btn-gold">',unsafe_allow_html=True)
        if st.button("&#10004;",key=f"{game}_sc_ok"):
            if sc>0:
                e=earn_coins(int(sc*multiplier)); earn_xp(int(sc*0.1))
                st.session_state[lock_key]=True
                if sc>S(hi_key,0):
                    st.session_state[hi_key]=sc
                    if sc>=50: _ach(f"{'&#128013;' if game=='snake' else '&#128054;'} שיא {sc}!")
                st.markdown(f"<div class='ok'>+{e} &#128170; נרשם!</div>",unsafe_allow_html=True)
                st.rerun()
        st.markdown('</div>',unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════
def main():
    inject_css()
    init()
    sel=sidebar()

    # Unlock score lock when new game started (tracked by played count changing)
    # This is handled in each page's "new game" button by resetting the lock

    routes={
        "🏠 לובי":        page_lobby,
        "🐍 נחש":         page_snake,
        "🐦 פלאפי":       page_flappy,
        "🧠 זיכרון":      page_memory,
        "❌ איקס-עיגול":  page_tictactoe,
        "👆 קליקר":       page_clicker,
        "🎰 מכונת מזל":   page_slot,
        "🛒 חנות":        page_shop,
    }
    routes.get(sel, page_lobby)()

if __name__=="__main__":
    main()
