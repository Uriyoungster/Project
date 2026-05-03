"""
🎮 ARCADE GALAXY v3
הפעלה: pip install streamlit && streamlit run arcade_galaxy.py
"""
import streamlit as st, streamlit.components.v1 as components
import random, time, json, math

st.set_page_config(page_title="🎮 Arcade Galaxy", page_icon="🎮",
                   layout="wide", initial_sidebar_state="expanded")

# ═══════════════════════════════════════════════════════════════
#  SHOP
# ═══════════════════════════════════════════════════════════════
SHOP = {
    "snake_life":    {"name":"חיים נוספים",      "game":"snake",   "price":200,"max":4,"icon":"💚","desc":"כל רכישה: +1 חיים"},
    "snake_wall":    {"name":"מעבר קירות",        "game":"snake",   "price":500,"max":1,"icon":"🌀","desc":"עבור דרך קירות"},
    "snake_magnet":  {"name":"מגנט אוכל",         "game":"snake",   "price":350,"max":1,"icon":"🧲","desc":"האוכל נמשך אליך"},
    "flappy_shield": {"name":"מגן",               "game":"flappy",  "price":150,"max":5,"icon":"🛡","desc":"כל רכישה: +1 מגן"},
    "flappy_slow":   {"name":"צינורות איטיים",    "game":"flappy",  "price":300,"max":2,"icon":"🐌","desc":"צינורות איטיים יותר"},
    "flappy_gap":    {"name":"פתח גדול",           "game":"flappy",  "price":300,"max":3,"icon":"🔓","desc":"כל רכישה: פתח רחב"},
    "mem_hint":      {"name":"רמזים",              "game":"memory",  "price": 80,"max":6,"icon":"💡","desc":"כל רכישה: +2 רמזים"},
    "mem_x2":        {"name":"כפל ניקוד",          "game":"memory",  "price":400,"max":1,"icon":"×2","desc":"פי 2 מטבעות"},
    "slot_luck":     {"name":"מזל",               "game":"slot",    "price":250,"max":4,"icon":"🍀","desc":"כל רכישה: +סיכוי"},
    "slot_jackpot":  {"name":"ג'קפוט מוגדל",      "game":"slot",    "price":500,"max":2,"icon":"💰","desc":"כפל פרס גדול"},
    "slot_refund":   {"name":"החזר הפסד",          "game":"slot",    "price":600,"max":1,"icon":"↩","desc":"10% החזר"},
    "click_mul":     {"name":"כפל קליקים",         "game":"clicker", "price":300,"max":3,"icon":"×2","desc":"כל רכישה: x1 נוסף"},
    "click_time":    {"name":"זמן נוסף",            "game":"clicker", "price":350,"max":3,"icon":"⏰","desc":"כל רכישה: +3 שניות"},
    "ttt_undo":      {"name":"ביטול מהלך",         "game":"ttt",     "price":150,"max":3,"icon":"↩","desc":"כל רכישה: +1 ביטול"},
    "pong_speed":    {"name":"כדור מהיר",           "game":"pong",    "price":200,"max":3,"icon":"⚡","desc":"כל רכישה: כדור מהיר"},
    "coin_boost":    {"name":"בוסט מטבעות",        "game":"global",  "price":600,"max":4,"icon":"💫","desc":"כל רכישה: +15%"},
    "xp_boost":      {"name":"בוסט XP",             "game":"global",  "price":500,"max":4,"icon":"⭐","desc":"כל רכישה: +20%"},
    "daily_up":      {"name":"בונוס יומי+",         "game":"global",  "price":400,"max":5,"icon":"📅","desc":"כל רכישה: +25 בונוס"},
}
GAME_LBL={"snake":"🐍 נחש","flappy":"🐦 פלאפי","memory":"🧠 זיכרון",
           "slot":"🎰 מזל","clicker":"👆 קליקר","ttt":"❌ XO","pong":"🏓 פונג","global":"🌐 גלובלי"}

# ═══════════════════════════════════════════════════════════════
#  STATE
# ═══════════════════════════════════════════════════════════════
def init():
    D={"coins":150,"level":1,"xp":0,"ach":[],"owned":{},
       "snake_hi":0,"snake_pl":0,"flappy_hi":0,"flappy_pl":0,
       "mem_hi":0,"mem_pl":0,"ttt_w":0,"ttt_l":0,"ttt_d":0,"ttt_pl":0,
       "click_hi":0,"click_tot":0,"click_ses":0,
       "slot_sp":0,"slot_w":0,"slot_tot":0,
       "pong_hi":0,"pong_pl":0,"daily_last":0}
    for k,v in D.items():
        if k not in st.session_state: st.session_state[k]=v

def S(k,d=None): return st.session_state.get(k,d)
def oc(uid): return S("owned",{}).get(uid,0)
def has(uid): return oc(uid)>0

def earn(base):
    mul=1+oc("coin_boost")*0.15
    amt=max(1,int(base*mul))
    st.session_state["coins"]=S("coins",0)+amt
    return amt

def xp(base):
    mul=1+oc("xp_boost")*0.20
    amt=max(1,int(base*mul))
    st.session_state["xp"]=S("xp",0)+amt
    lv=S("level",1)
    while S("xp",0)>=lv*120:
        st.session_state["xp"]-=lv*120; lv+=1
        st.session_state["level"]=lv
        if lv in (5,10,20,50): ach(f"⬆️ רמה {lv}!")

def ach(name):
    a=list(S("ach",[]));
    if name not in a: a.append(name); st.session_state["ach"]=a

def buy(uid):
    item=SHOP.get(uid)
    if not item: return False,"?"
    cnt=oc(uid)
    if cnt>=item["max"]: return False,"מקסימום!"
    if S("coins",0)<item["price"]: return False,f"חסר {item['price']-S('coins',0)}"
    st.session_state["coins"]-=item["price"]
    owned=dict(S("owned",{})); owned[uid]=cnt+1
    st.session_state["owned"]=owned
    return True,f"קנית {item['name']}!"

# ═══════════════════════════════════════════════════════════════
#  CSS
# ═══════════════════════════════════════════════════════════════
def css():
    st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Exo+2:wght@400;600;700&display=swap');
:root{--bg:#080818;--card:#0e0e24;--cyan:#00f5ff;--pink:#ff006e;--gold:#ffd60a;
      --green:#39ff14;--purple:#bf5fff;--orange:#ff7c00;--dim:#6677aa;--fg:#dde0ff;}
.stApp{background:var(--bg)!important;font-family:'Exo 2',sans-serif!important;color:var(--fg)!important;
  background-image:radial-gradient(ellipse at 10% 40%,rgba(0,245,255,.04) 0%,transparent 50%),
    radial-gradient(ellipse at 90% 15%,rgba(255,0,110,.03) 0%,transparent 50%)!important;}
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#040412,#07071a)!important;
  border-right:1px solid rgba(0,245,255,.1)!important;}
.main .block-container{padding:18px 24px!important;max-width:100%!important;}
h1,h2,h3{font-family:Orbitron,sans-serif!important;color:var(--cyan)!important;
  text-shadow:0 0 16px rgba(0,245,255,.45)!important;}
.stButton>button{background:linear-gradient(135deg,rgba(0,245,255,.1),rgba(0,245,255,.03))!important;
  color:var(--cyan)!important;border:1px solid rgba(0,245,255,.3)!important;border-radius:8px!important;
  font-family:'Exo 2',sans-serif!important;font-weight:700!important;transition:all .16s!important;}
.stButton>button:hover{background:rgba(0,245,255,.18)!important;border-color:var(--cyan)!important;
  box-shadow:0 0 16px rgba(0,245,255,.22)!important;transform:translateY(-1px)!important;}
.stButton>button:disabled{opacity:.35!important;}
.btng .stButton>button{background:rgba(255,214,10,.12)!important;color:var(--gold)!important;
  border-color:rgba(255,214,10,.4)!important;}
.btng .stButton>button:hover{box-shadow:0 0 16px rgba(255,214,10,.28)!important;}
.btnr .stButton>button{background:rgba(255,0,110,.12)!important;color:var(--pink)!important;
  border-color:rgba(255,0,110,.4)!important;}
.btnG .stButton>button{background:rgba(57,255,20,.1)!important;color:var(--green)!important;
  border-color:rgba(57,255,20,.38)!important;}
.btnb .stButton>button{background:rgba(191,95,255,.1)!important;color:var(--purple)!important;
  border-color:rgba(191,95,255,.38)!important;}
[data-testid="metric-container"]{background:var(--card)!important;
  border:1px solid rgba(0,245,255,.18)!important;border-radius:9px!important;padding:10px!important;}
[data-testid="metric-container"] label{color:var(--dim)!important;font-size:11px!important;}
[data-testid="metric-container"] [data-testid="stMetricValue"]{color:var(--cyan)!important;
  font-family:Orbitron,sans-serif!important;font-size:20px!important;}
.ok{padding:10px 14px;background:rgba(57,255,20,.07);border:1px solid rgba(57,255,20,.35);
  border-radius:9px;color:var(--green);font-weight:600;text-align:center;}
.err{padding:10px 14px;background:rgba(255,0,110,.07);border:1px solid rgba(255,0,110,.35);
  border-radius:9px;color:var(--pink);font-weight:600;text-align:center;}
.inf{padding:10px 14px;background:rgba(0,245,255,.06);border:1px solid rgba(0,245,255,.25);
  border-radius:9px;color:var(--cyan);text-align:center;}
.warn{padding:10px 14px;background:rgba(255,214,10,.06);border:1px solid rgba(255,214,10,.3);
  border-radius:9px;color:var(--gold);text-align:center;}
.card{background:var(--card);border:1px solid rgba(0,245,255,.15);border-radius:12px;
  padding:16px;transition:all .22s;}
.card:hover{border-color:rgba(0,245,255,.4);box-shadow:0 0 22px rgba(0,245,255,.12);transform:translateY(-2px);}
.stProgress>div>div>div{background:linear-gradient(90deg,var(--cyan),var(--purple))!important;border-radius:3px!important;}
.stProgress>div>div{background:rgba(255,255,255,.05)!important;border-radius:3px!important;}
div[role="radiogroup"]{display:flex!important;flex-direction:column!important;gap:2px!important;padding:5px 9px!important;}
div[role="radiogroup"] label{padding:8px 12px!important;border-radius:8px!important;
  color:var(--dim)!important;border:1px solid transparent!important;font-weight:600!important;transition:all .14s!important;}
div[role="radiogroup"] label:hover{background:rgba(0,245,255,.06)!important;color:var(--cyan)!important;}
div[role="radiogroup"] label input{display:none!important;}
.stRadio>label{display:none!important;}
hr{border-color:rgba(0,245,255,.08)!important;}
::-webkit-scrollbar{width:4px;}::-webkit-scrollbar-track{background:var(--bg);}
::-webkit-scrollbar-thumb{background:rgba(0,245,255,.2);border-radius:2px;}
#MainMenu,footer,.stDeployButton{display:none!important;}
header[data-testid="stHeader"]{background:transparent!important;}
.stTabs [data-baseweb="tab-list"]{background:rgba(255,255,255,.02)!important;border-radius:7px!important;}
.stTabs [data-baseweb="tab"]{font-family:'Exo 2',sans-serif!important;font-weight:700!important;color:var(--dim)!important;}
.stTabs [aria-selected="true"]{background:rgba(0,245,255,.1)!important;color:var(--cyan)!important;}
[data-testid="column"]{padding:0 5px!important;}
</style>""",unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  SIDEBAR + PAGES LIST
# ═══════════════════════════════════════════════════════════════
PAGES=[
    "🏠 לובי",
    "── 1-PLAYER ──",
    "🐍 נחש",
    "🐦 פלאפי",
    "🧠 זיכרון",
    "❌ איקס-עיגול",
    "👆 קליקר",
    "🎰 מכונת מזל",
    "🏓 פונג (1P)",
    "💣 שדה מוקשים",
    "🔢 מספר חשאי",
    "🎯 ירי מטרות",
    "🐍 נחש מילים",
    "── 2-PLAYER ──",
    "🏓 פונג (2P)",
    "❌ איקס-עיגול (2P)",
    "🎲 קוביות - 2P",
    "💣 שדה מוקשים (2P)",
    "── ── ── ── ──",
    "🛒 חנות",
]

def sidebar():
    with st.sidebar:
        lv=S("level",1); coins=S("coins",0)
        st.markdown(f"""
<div style="padding:18px 14px 12px;text-align:center;border-bottom:1px solid rgba(0,245,255,.09)">
<div style="font-size:48px;animation:gp 2.5s ease-in-out infinite;display:inline-block">&#127918;</div>
<div style="font-family:Orbitron,sans-serif;font-size:18px;font-weight:900;color:#00f5ff;
  text-shadow:0 0 16px rgba(0,245,255,.75);letter-spacing:4px;margin-top:4px">ARCADE<br>GALAXY</div>
</div>
<div style="margin:12px 10px;padding:10px 13px;background:rgba(255,214,10,.06);
  border:1px solid rgba(255,214,10,.3);border-radius:9px;display:flex;align-items:center;gap:9px">
<span style="font-size:20px">&#128170;</span>
<div><div style="font-family:Orbitron,sans-serif;font-size:18px;font-weight:900;color:#ffd60a;
  text-shadow:0 0 9px rgba(255,214,10,.65)">{coins:,}</div>
<div style="font-size:10px;color:#6677aa">מטבעות | רמה {lv}</div></div></div>
<div style="margin:0 10px 10px;height:3px;background:rgba(255,255,255,.04);border-radius:2px">
<div style="height:100%;width:{min(S('xp',0)/(lv*120)*100,100):.0f}%;
  background:linear-gradient(90deg,#00f5ff,#bf5fff);border-radius:2px"></div></div>
<style>@keyframes gp{{0%,100%{{filter:drop-shadow(0 0 16px rgba(0,245,255,.85))}}
  50%{{filter:drop-shadow(0 0 28px rgba(0,245,255,1))}}}}</style>""",unsafe_allow_html=True)

        sel=st.radio("p",PAGES,label_visibility="collapsed",key="nav")
        total=sum(S(k,0) for k in["snake_pl","flappy_pl","mem_pl","ttt_pl","click_ses","slot_sp","pong_pl"])
        st.markdown(f"""<div style="margin:8px 10px;padding:9px;background:rgba(255,255,255,.02);
border-radius:8px;border:1px solid rgba(255,255,255,.04)">
<div style="display:flex;justify-content:space-between;font-size:11px;color:#6677aa;padding:2px 0">
<span>&#127918; משחקים</span><span style="color:#dde0ff">{total}</span></div>
<div style="display:flex;justify-content:space-between;font-size:11px;color:#6677aa;padding:2px 0">
<span>&#127942; הישגים</span><span style="color:#dde0ff">{len(S("ach",[]))}</span></div>
<div style="display:flex;justify-content:space-between;font-size:11px;color:#6677aa;padding:2px 0">
<span>&#128142; שדרוגים</span><span style="color:#dde0ff">{sum(S("owned",{}).values())}</span></div>
</div>""",unsafe_allow_html=True)
    return sel

# ═══════════════════════════════════════════════════════════════
#  LOBBY
# ═══════════════════════════════════════════════════════════════
def page_lobby():
    st.markdown("""<div style="text-align:center;padding:14px 0 20px">
<div style="font-size:60px;animation:fl 3s ease-in-out infinite;display:inline-block">&#127918;</div>
<h1 style="font-family:Orbitron,sans-serif;font-size:34px;font-weight:900;margin:8px 0 3px;
  background:linear-gradient(90deg,#00f5ff,#bf5fff,#ff006e,#00f5ff);background-size:300%;
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:sh 4s linear infinite">
  ARCADE GALAXY</h1>
<p style="color:#6677aa;letter-spacing:3px;font-size:13px">12 משחקים | משחק לשניים | חנות שדרוגים</p></div>
<style>
@keyframes fl{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
@keyframes sh{0%{background-position:0%}100%{background-position:300%}}
</style>""",unsafe_allow_html=True)

    lv=S("level",1); xpv=S("xp",0); need=lv*120
    c1,c2,c3,c4=st.columns(4)
    with c1: st.metric("💎 רמה",    lv)
    with c2: st.metric("💰 מטבעות", f"{S('coins',0):,}")
    with c3: st.metric("🏆 הישגים", len(S("ach",[])))
    with c4:
        total=sum(S(k,0) for k in["snake_pl","flappy_pl","mem_pl","ttt_pl","click_ses","slot_sp","pong_pl"])
        st.metric("🎮 משחקים", total)
    st.markdown(f"<div style='text-align:right;font-size:10px;color:#6677aa;margin:3px 0'>XP {xpv}/{need}</div>",unsafe_allow_html=True)
    st.progress(min(xpv/need,1.0))
    st.markdown("<br>",unsafe_allow_html=True)

    games_1p=[
        ("🐍","נחש","#39ff14",f"שיא: {S('snake_hi',0)}","קלאסיק מלא עם שדרוגים"),
        ("🐦","פלאפי","#ffd60a",f"שיא: {S('flappy_hi',0)}","עוף בין הצינורות"),
        ("🧠","זיכרון","#bf5fff",f"שיא: {S('mem_hi',0)}","מצא זוגות קלפים"),
        ("❌","איקס-עיגול","#00f5ff",f"נצ': {S('ttt_w',0)}","נגד AI חכם"),
        ("👆","קליקר","#ff006e",f"שיא: {S('click_hi',0)}","לחץ הכי מהר!"),
        ("🎰","מכונת מזל","#ff7c00",f"זכ': {S('slot_w',0)}","ג'קפוט!"),
        ("🏓","פונג","#00f5ff",f"שיא: {S('pong_hi',0)}","1 שחקן"),
        ("💣","מוקשים","#ff006e","","חפש את הפצצות"),
        ("🔢","מספר","#39ff14","","נחש את המספר"),
        ("🎯","מטרות","#ffd60a","","ירי מהיר"),
    ]
    games_2p=[
        ("🏓","פונג 2P","#00f5ff","","2 שחקנים, מקלדת"),
        ("❌","XO 2P","#bf5fff","","שניים על אותו מסך"),
        ("🎲","קוביות 2P","#ffd60a","","מי מגיע ל-100 ראשון"),
        ("💣","מוקשים 2P","#ff006e","","תורות"),
    ]

    st.markdown("### 🕹️ משחקי יחיד")
    cols=st.columns(5)
    for i,(ico,name,col,best,desc) in enumerate(games_1p):
        with cols[i%5]:
            st.markdown(f"""<div class="card" style="border-color:{col}28;text-align:center;padding:14px 10px;
background:linear-gradient(135deg,{col}07,var(--card))">
<div style="font-size:36px">{ico}</div>
<div style="font-family:Orbitron,sans-serif;font-size:11px;color:{col};margin:6px 0 3px">{name}</div>
<div style="color:#6677aa;font-size:10px;margin-bottom:6px">{desc}</div>
<div style="font-size:10px;color:{col}88">{best}</div>
</div><br>""",unsafe_allow_html=True)

    st.markdown("### 👥 משחקי שניים")
    cols2=st.columns(4)
    for i,(ico,name,col,best,desc) in enumerate(games_2p):
        with cols2[i%4]:
            st.markdown(f"""<div class="card" style="border-color:{col}30;text-align:center;padding:14px 10px;
background:linear-gradient(135deg,{col}08,var(--card))">
<div style="font-size:36px">{ico}</div>
<div style="font-family:Orbitron,sans-serif;font-size:11px;color:{col};margin:6px 0 3px">{name}</div>
<div style="color:#6677aa;font-size:10px">{desc}</div>
</div><br>""",unsafe_allow_html=True)

    # Daily bonus
    now=int(time.time()); last=S("daily_last",0)
    if now-last>86400:
        base=50+oc("daily_up")*25
        st.markdown("<hr>",unsafe_allow_html=True)
        st.markdown(f"<div class='warn'>🎁 בונוס יומי! קבל {base} מטבעות</div>",unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
        _,mc,_=st.columns([1,2,1])
        with mc:
            st.markdown('<div class="btng">',unsafe_allow_html=True)
            if st.button(f"🎁 קבל {base} מטבעות",use_container_width=True,key="daily"):
                earn(base); xp(15); st.session_state["daily_last"]=now
                ach("🎁 בונוס יומי!")
                st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)

    achs=S("ach",[])
    if achs:
        st.markdown("<hr>",unsafe_allow_html=True)
        st.markdown("### 🏆 הישגים")
        b="".join(f"<span style='display:inline-flex;padding:4px 10px;background:rgba(255,214,10,.07);"
                  f"border:1px solid rgba(255,214,10,.3);border-radius:14px;font-size:11px;"
                  f"font-weight:700;color:#ffd60a;margin:2px'>{a}</span>" for a in achs[-15:])
        st.markdown(f"<div style='display:flex;flex-wrap:wrap;gap:2px'>{b}</div>",unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  SNAKE  (canvas, auto-rewards on death)
# ═══════════════════════════════════════════════════════════════
def page_snake():
    st.markdown("<h1 style='text-align:center'>🐍 נחש</h1><p style='text-align:center;color:#6677aa'>חצים / WASD</p>",unsafe_allow_html=True)
    lives=1+oc("snake_life"); wp="true" if has("snake_wall") else "false"
    mag="true" if has("snake_magnet") else "false"; hi=S("snake_hi",0)
    ups=[]
    if lives>1: ups.append(f"💚 {lives} חיים")
    if has("snake_wall"): ups.append("🌀 קירות")
    if has("snake_magnet"): ups.append("🧲 מגנט")
    if ups: st.markdown(f"<div class='inf'>{'  |  '.join(ups)}</div>",unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)

    _,col,_=st.columns([1,8,1])
    with col:
        components.html(f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#060612;display:flex;flex-direction:column;align-items:center;padding:6px;user-select:none;font-family:'Orbitron',monospace}}
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');
.hud{{display:flex;gap:8px;margin-bottom:6px;font-size:12px;flex-wrap:wrap;justify-content:center}}
.hi{{background:rgba(0,245,255,.08);border:1px solid rgba(0,245,255,.25);border-radius:6px;padding:3px 9px;color:#00f5ff}}
canvas{{border:2px solid rgba(0,245,255,.3);border-radius:10px;box-shadow:0 0 24px rgba(0,245,255,.1);display:block}}
.ov{{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);background:rgba(4,4,18,.95);
  border:2px solid #00f5ff;border-radius:11px;padding:18px 26px;text-align:center;min-width:170px}}
.ov h2{{color:#00f5ff;font-size:17px;margin-bottom:7px}}.ov p{{color:#8888aa;font-size:11px;margin-bottom:11px}}
.ov button{{background:rgba(0,245,255,.16);color:#00f5ff;border:1px solid #00f5ff;
  padding:7px 18px;border-radius:6px;cursor:pointer;font-family:Orbitron;font-size:12px;font-weight:700}}
.ov button:hover{{background:rgba(0,245,255,.32)}}
.wrap{{position:relative}}</style></head><body>
<div class="hud">
  <div class="hi">ניקוד: <span id="sc">0</span></div>
  <div class="hi">שיא: <span id="hi">{hi}</span></div>
  <div class="hi">חיים: <span id="lv">{lives}</span></div>
  <div class="hi">מהירות: <span id="sp">1</span></div>
</div>
<div class="wrap"><canvas id="c"></canvas>
<div class="ov" id="ov"><h2 id="ot">🐍 נחש</h2><p id="ob">חצים / WASD לשליטה</p>
<button onclick="startGame()">▶ שחק</button></div></div>
<script>
const G=20,C=20,S={CANVAS_SIZE if (CANVAS_SIZE:=G*C) else G*C};
const WP={wp},MAG={mag},ML={lives};
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
cv.width=cv.height=G*C;
let sn,dir,nd,food,bon,score,lives2,spd,loop,run,parts;
function startGame(){{
  document.getElementById('ov').style.display='none';
  sn=[{{x:10,y:10}},{{x:9,y:10}},{{x:8,y:10}}];
  dir={{x:1,y:0}};nd={{x:1,y:0}};score=0;lives2=ML;spd=1;parts=[];bon=null;run=true;
  ['sc','lv','sp'].forEach((id,i)=>document.getElementById(id).textContent=[0,ML,1][i]);
  placeFood();if(loop)clearInterval(loop);loop=setInterval(update,155);
}}
document.addEventListener('keydown',e=>{{
  const k={{ArrowUp:{{x:0,y:-1}},ArrowDown:{{x:0,y:1}},ArrowLeft:{{x:-1,y:0}},ArrowRight:{{x:1,y:0}},
    KeyW:{{x:0,y:-1}},KeyS:{{x:0,y:1}},KeyA:{{x:-1,y:0}},KeyD:{{x:1,y:0}}}};
  const n=k[e.code];if(n&&(n.x!=-dir.x||n.y!=-dir.y)){{nd=n;e.preventDefault();}}
}});
function placeFood(){{
  let p;do p={{x:Math.floor(Math.random()*G),y:Math.floor(Math.random()*G)}};
  while(sn.some(s=>s.x===p.x&&s.y===p.y));food=p;
  if(score>0&&score%50===0&&!bon){{
    let b;do b={{x:Math.floor(Math.random()*G),y:Math.floor(Math.random()*G)}};
    while(sn.some(s=>s.x===b.x&&s.y===b.y));bon={{...b,t:100}};
  }}
}}
function spark(x,y,c){{for(let i=0;i<7;i++)parts.push({{x:x*C+C/2,y:y*C+C/2,vx:(Math.random()-.5)*4,vy:(Math.random()-.5)*4,l:25,c}});}}
function update(){{
  if(!run)return;dir={{...nd}};
  let h={{x:sn[0].x+dir.x,y:sn[0].y+dir.y}};
  if(WP){{h.x=(h.x+G)%G;h.y=(h.y+G)%G;}}
  else if(h.x<0||h.x>=G||h.y<0||h.y>=G){{die();return;}}
  if(sn.slice(1).some(s=>s.x===h.x&&s.y===h.y)){{die();return;}}
  if(MAG){{let dx=food.x-h.x,dy=food.y-h.y;if(Math.abs(dx)+Math.abs(dy)<=4){{
    if(dx)food.x+=dx>0?-1:1;else if(dy)food.y+=dy>0?-1:1;}}}}
  sn.unshift(h);let grew=false;
  if(h.x===food.x&&h.y===food.y){{score+=10;grew=true;spark(food.x,food.y,'#39ff14');placeFood();
    document.getElementById('sc').textContent=score;
    let ns=1+Math.floor(score/50);if(ns>spd){{spd=ns;clearInterval(loop);
      loop=setInterval(update,Math.max(65,155-spd*20));document.getElementById('sp').textContent=spd;}}}}
  if(bon&&h.x===bon.x&&h.y===bon.y){{score+=50;grew=true;spark(bon.x,bon.y,'#ffd60a');
    bon=null;document.getElementById('sc').textContent=score;}}
  if(!grew)sn.pop();if(bon){{bon.t--;if(!bon.t)bon=null;}}
  parts=parts.filter(p=>p.l>0);parts.forEach(p=>{{p.x+=p.vx;p.y+=p.vy;p.l--;}});draw();
}}
function die(){{
  lives2--;document.getElementById('lv').textContent=lives2;
  if(lives2<=0){{run=false;clearInterval(loop);
    let hs=+document.getElementById('hi').textContent||0;
    if(score>hs)document.getElementById('hi').textContent=score;
    document.getElementById('ot').textContent='💀 נגמר!';
    document.getElementById('ob').textContent='ניקוד: '+score;
    document.getElementById('ov').style.display='block';
    window.parent.postMessage({{type:'snake_done',score}},'*');
  }}else{{sn=[{{x:10,y:10}},{{x:9,y:10}},{{x:8,y:10}}];dir={{x:1,y:0}};nd={{x:1,y:0}};}}
}}
function rr(x,y,w,h,r){{ctx.beginPath();ctx.moveTo(x+r,y);ctx.lineTo(x+w-r,y);ctx.quadraticCurveTo(x+w,y,x+w,y+r);
  ctx.lineTo(x+w,y+h-r);ctx.quadraticCurveTo(x+w,y+h,x+w-r,y+h);ctx.lineTo(x+r,y+h);
  ctx.quadraticCurveTo(x,y+h,x,y+h-r);ctx.lineTo(x,y+r);ctx.quadraticCurveTo(x,y,x+r,y);ctx.closePath();}}
function draw(){{
  ctx.fillStyle='#06060e';ctx.fillRect(0,0,G*C,G*C);
  ctx.strokeStyle='rgba(0,245,255,.03)';ctx.lineWidth=.5;
  for(let i=0;i<=G;i++){{ctx.beginPath();ctx.moveTo(i*C,0);ctx.lineTo(i*C,G*C);ctx.stroke();
    ctx.beginPath();ctx.moveTo(0,i*C);ctx.lineTo(G*C,i*C);ctx.stroke();}}
  parts.forEach(p=>{{ctx.globalAlpha=p.l/25;ctx.fillStyle=p.c;ctx.beginPath();ctx.arc(p.x,p.y,2.5,0,Math.PI*2);ctx.fill();}});
  ctx.globalAlpha=1;
  let t=Date.now()/320;ctx.save();ctx.translate(food.x*C+C/2,food.y*C+C/2);ctx.scale(1+Math.sin(t)*.16,1+Math.sin(t)*.16);
  ctx.shadowBlur=16;ctx.shadowColor='#39ff14';ctx.fillStyle='#39ff14';ctx.beginPath();ctx.arc(0,0,C/2-2,0,Math.PI*2);ctx.fill();
  ctx.shadowBlur=0;ctx.restore();
  if(bon){{ctx.save();ctx.translate(bon.x*C+C/2,bon.y*C+C/2);ctx.scale(1+Math.sin(Date.now()/130)*.2,1+Math.sin(Date.now()/130)*.2);
    ctx.shadowBlur=20;ctx.shadowColor='#ffd60a';ctx.fillStyle='#ffd60a';
    ctx.font=(C-2)+'px serif';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('★',0,0);ctx.restore();
    ctx.fillStyle='rgba(255,214,10,'+bon.t/100+')';ctx.fillRect(bon.x*C,bon.y*C-3,C*(bon.t/100),2);}}
  sn.forEach((seg,i)=>{{ctx.save();
    if(!i){{ctx.shadowBlur=13;ctx.shadowColor='rgba(0,245,255,.75)';}}
    ctx.fillStyle=i?`rgba(0,${{Math.round(215-i/sn.length*80)}},255,.88)`:'#fff';
    let pd=i?2:1,rd=i?3:5;rr(seg.x*C+pd,seg.y*C+pd,C-pd*2,C-pd*2,rd);ctx.fill();ctx.restore();
    if(!i){{ctx.fillStyle='#06060e';
      ctx.beginPath();ctx.arc(seg.x*C+C*.3+dir.y*C*.18,seg.y*C+C*.3-dir.x*C*.18,2,0,Math.PI*2);ctx.fill();
      ctx.beginPath();ctx.arc(seg.x*C+C*.7-dir.y*C*.18,seg.y*C+C*.3-dir.x*C*.18,2,0,Math.PI*2);ctx.fill();}}
  }});
}}
ctx.fillStyle='#06060e';ctx.fillRect(0,0,G*C,G*C);
// Auto-reward on game over message
window.addEventListener('message',e=>{{
  if(e.data&&e.data.type==='snake_done'){{
    const s=e.data.score;
    // reward handled by postMessage to parent
  }}
}});
</script></body></html>""",height=G*C+80,scrolling=False)

    st.markdown("<br>",unsafe_allow_html=True)
    _,c2,_=st.columns([1,2,1])
    with c2:
        st.markdown('<div class="btnG">',unsafe_allow_html=True)
        if st.button("▶ משחק חדש",use_container_width=True,key="sn_new"):
            st.session_state["snake_pl"]=S("snake_pl",0)+1
            st.session_state["snake_sc_locked"]=False
            earn(5); xp(5); st.toast("🐍 בהצלחה!")
        st.markdown('</div>',unsafe_allow_html=True)
    st.markdown("---")
    c1,c2=st.columns(2); 
    with c1: st.metric("🏆 שיא",S("snake_hi",0))
    with c2: st.metric("🎮 משחקים",S("snake_pl",0))

# ═══════════════════════════════════════════════════════════════
#  FLAPPY  (canvas)
# ═══════════════════════════════════════════════════════════════
def page_flappy():
    st.markdown("<h1 style='text-align:center'>🐦 פלאפי</h1><p style='text-align:center;color:#6677aa'>SPACE / לחיצה לעוף</p>",unsafe_allow_html=True)
    sh=oc("flappy_shield"); slow="true" if has("flappy_slow") else "false"
    gap=110+oc("flappy_gap")*15; hi=S("flappy_hi",0)
    if sh: st.markdown(f"<div class='inf'>🛡 {sh} מגנים  {'🐌 איטי' if has('flappy_slow') else ''}  🔓 פתח {gap}</div>",unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    _,col,_=st.columns([1,7,1])
    with col:
        components.html(f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#050510;display:flex;flex-direction:column;align-items:center;padding:6px;user-select:none;font-family:'Orbitron',monospace}}
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');
.hud{{display:flex;gap:8px;margin-bottom:6px;font-size:12px}}
.hi{{background:rgba(255,214,10,.08);border:1px solid rgba(255,214,10,.25);border-radius:6px;padding:3px 9px;color:#ffd60a}}
canvas{{border:2px solid rgba(255,214,10,.3);border-radius:10px;box-shadow:0 0 24px rgba(255,214,10,.1);cursor:pointer;display:block}}
.ov{{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);background:rgba(4,4,18,.95);
  border:2px solid #ffd60a;border-radius:11px;padding:18px 24px;text-align:center;min-width:165px}}
.ov h2{{color:#ffd60a;font-size:16px;margin-bottom:7px}}.ov p{{color:#8888aa;font-size:11px;margin-bottom:11px}}
.ov button{{background:rgba(255,214,10,.16);color:#ffd60a;border:1px solid #ffd60a;
  padding:7px 18px;border-radius:6px;cursor:pointer;font-family:Orbitron;font-size:11px;font-weight:700}}
.wrap{{position:relative}}</style></head><body>
<div class="hud">
  <div class="hi">ניקוד: <span id="sc">0</span></div>
  <div class="hi">שיא: <span id="hi">{hi}</span></div>
  <div class="hi">🛡 <span id="sh">{sh}</span></div>
</div>
<div class="wrap"><canvas id="c" width="320" height="440"></canvas>
<div class="ov" id="ov"><h2 id="ot">🐦 פלאפי</h2><p id="ob">SPACE / לחץ להתחיל</p>
<button onclick="startGame()">▶ שחק</button></div></div>
<script>
const W=320,H=440,BR=12,PS={1.7 if has("flappy_slow") else 2.4},GAP={gap},ISH={sh};
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
let bird,pipes,score,frame,run,raf,shL,parts,stars;
function mkSt(){{stars=[];for(let i=0;i<50;i++)stars.push({{x:Math.random()*W,y:Math.random()*H*.76,r:Math.random()*1.3+.4,s:Math.random()*.25+.07}});}}
function startGame(){{document.getElementById('ov').style.display='none';
  bird={{x:70,y:H/2,vy:0,rot:0}};pipes=[];score=0;frame=0;run=true;shL=ISH;parts=[];
  document.getElementById('sc').textContent='0';document.getElementById('sh').textContent=shL;
  if(raf)cancelAnimationFrame(raf);mkSt();loop();
}}
function flap(){{if(run)bird.vy=-6.8;}}
cv.addEventListener('click',flap);
document.addEventListener('keydown',e=>{{if(e.code==='Space'){{flap();e.preventDefault();}}}});
function loop(){{if(!run)return;update();draw();raf=requestAnimationFrame(loop);}}
function update(){{
  frame++;bird.vy+=.33;bird.y+=bird.vy;bird.rot=Math.min(Math.max(bird.vy*3,-30),90);
  parts=parts.filter(p=>p.l>0);parts.forEach(p=>{{p.x+=p.vx;p.y+=p.vy;p.l--;p.vy+=.1;}});
  stars.forEach(s=>{{s.x-=s.s;if(s.x<0)s.x=W;}});
  if(frame%80===0){{pipes.push({{x:W,th:50+Math.random()*(H-GAP-100),ok:false}});}}
  pipes.forEach(p=>p.x-=PS);pipes=pipes.filter(p=>p.x>-65);
  pipes.forEach(p=>{{
    if(!p.ok&&p.x+40<bird.x){{p.ok=true;score++;document.getElementById('sc').textContent=score;
      for(let i=0;i<6;i++)parts.push({{x:bird.x,y:bird.y,vx:(Math.random()-.5)*4,vy:-Math.random()*3.5,l:22,c:'#ffd60a'}});}}
    if(bird.x+BR>p.x&&bird.x-BR<p.x+45&&(bird.y-BR<p.th||bird.y+BR>p.th+GAP)){{
      if(shL>0){{shL--;document.getElementById('sh').textContent=shL;
        for(let i=0;i<12;i++)parts.push({{x:bird.x,y:bird.y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,l:26,c:'#00f5ff'}});}}
      else die();
    }}
  }});
  if(bird.y+BR>H-26||bird.y-BR<0)die();
}}
function die(){{run=false;cancelAnimationFrame(raf);
  let hs=+document.getElementById('hi').textContent||0;
  if(score>hs)document.getElementById('hi').textContent=score;
  document.getElementById('ot').textContent='💥 נפלת!';
  document.getElementById('ob').textContent='ניקוד: '+score;
  document.getElementById('ov').style.display='block';
  window.parent.postMessage({{type:'flappy_done',score}},'*');
}}
function dp(x,th){{
  let g=ctx.createLinearGradient(x,0,x+45,0);g.addColorStop(0,'#14501a');g.addColorStop(.5,'#228528');g.addColorStop(1,'#14501a');
  ctx.fillStyle=g;ctx.fillRect(x,0,45,th);ctx.fillStyle='#2a9a2a';ctx.fillRect(x-4,th-16,53,16);
  let b=th+GAP;ctx.fillStyle=g;ctx.fillRect(x,b,45,H-b);ctx.fillStyle='#2a9a2a';ctx.fillRect(x-4,b,53,16);
  ctx.shadowBlur=8;ctx.shadowColor='rgba(57,255,20,.3)';ctx.strokeStyle='rgba(57,255,20,.24)';ctx.lineWidth=1;
  ctx.strokeRect(x,0,45,th);ctx.strokeRect(x,b,45,H-b);ctx.shadowBlur=0;
}}
function draw(){{
  let sky=ctx.createLinearGradient(0,0,0,H);sky.addColorStop(0,'#030310');sky.addColorStop(.7,'#07072a');sky.addColorStop(1,'#0b160b');
  ctx.fillStyle=sky;ctx.fillRect(0,0,W,H);
  stars.forEach(s=>{{ctx.globalAlpha=.45+Math.sin(frame*.05+s.x)*.4;ctx.fillStyle='#fff';ctx.beginPath();ctx.arc(s.x,s.y,s.r,0,Math.PI*2);ctx.fill();}});
  ctx.globalAlpha=1;
  parts.forEach(p=>{{ctx.globalAlpha=p.l/26;ctx.fillStyle=p.c;ctx.beginPath();ctx.arc(p.x,p.y,2.2,0,Math.PI*2);ctx.fill();}});ctx.globalAlpha=1;
  pipes.forEach(p=>dp(p.x,p.th));
  ctx.fillStyle='#14280e';ctx.fillRect(0,H-26,W,26);ctx.fillStyle='#204010';ctx.fillRect(0,H-26,W,7);
  ctx.save();ctx.translate(bird.x,bird.y);ctx.rotate(bird.rot*Math.PI/180);
  if(shL>0){{ctx.beginPath();ctx.arc(0,0,BR+7,0,Math.PI*2);ctx.strokeStyle='rgba(0,245,255,'+(0.38+Math.sin(frame*.14)*.26)+')';ctx.lineWidth=2;ctx.stroke();}}
  ctx.shadowBlur=10;ctx.shadowColor='#ffd60a';ctx.fillStyle='#ffd60a';ctx.beginPath();ctx.ellipse(0,0,BR,BR-2,0,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='#ff8f00';ctx.beginPath();ctx.ellipse(-3,2,7,4,Math.PI/4+Math.sin(frame*.28)*.4,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='#fff';ctx.beginPath();ctx.arc(5,-2,3.2,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='#1a1a3a';ctx.beginPath();ctx.arc(6,-2,2,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='#ff5500';ctx.beginPath();ctx.moveTo(BR-.5,0);ctx.lineTo(BR+5.5,1.5);ctx.lineTo(BR-.5,-1.5);ctx.fill();
  ctx.shadowBlur=0;ctx.restore();
  ctx.fillStyle='rgba(255,214,10,.9)';ctx.font='bold 24px Orbitron,monospace';ctx.textAlign='center';
  ctx.shadowBlur=13;ctx.shadowColor='#ffd60a';ctx.fillText(score,W/2,44);ctx.shadowBlur=0;
}}
mkSt();ctx.fillStyle='#030310';ctx.fillRect(0,0,W,H);
</script></body></html>""",height=490,scrolling=False)

    st.markdown("<br>",unsafe_allow_html=True)
    _,c2,_=st.columns([1,2,1])
    with c2:
        st.markdown('<div class="btng">',unsafe_allow_html=True)
        if st.button("▶ משחק חדש",use_container_width=True,key="fl_new"):
            st.session_state["flappy_pl"]=S("flappy_pl",0)+1; earn(5); xp(5)
        st.markdown('</div>',unsafe_allow_html=True)
    st.markdown("---")
    c1,c2=st.columns(2)
    with c1: st.metric("🏆 שיא",S("flappy_hi",0))
    with c2: st.metric("🎮 משחקים",S("flappy_pl",0))

# ═══════════════════════════════════════════════════════════════
#  MEMORY  (pure Streamlit grid)
# ═══════════════════════════════════════════════════════════════
EMJ=["🐉","🦄","🔥","⚡","💎","🚀","🌊","🎸","🦋","🍄","🎯","🏆","🌈","🎪","🐬","🦁"]
def _mr():
    c=random.sample(range(len(EMJ)),8); b=c*2; random.shuffle(b)
    st.session_state.update({"mb":b,"mf":[],"mm":set(),"mov":0,"mpend":False,"mptime":0,"mh":oc("mem_hint")*2})
def page_memory():
    st.markdown("<h1 style='text-align:center'>🧠 זיכרון</h1><p style='text-align:center;color:#6677aa'>לחץ על מספר קלף לגלות</p>",unsafe_allow_html=True)
    if has("mem_x2"): st.markdown("<div class='inf'>×2 ניקוד פעיל</div>",unsafe_allow_html=True)
    if "mb" not in st.session_state: _mr()
    b=st.session_state["mb"]; fl=list(st.session_state["mf"]); mm=set(st.session_state["mm"]); mv=S("mov",0); hints=S("mh",0)
    c1,c2,c3,c4=st.columns(4)
    with c1: st.metric("🎯 מהלכים",mv)
    with c2: st.metric("✅ זוגות",len(mm)//2)
    with c3: st.metric("🃏 נותרו",8-len(mm)//2)
    with c4: st.metric("💡 רמזים",hints)
    st.markdown("<br>",unsafe_allow_html=True)
    if len(mm)==16:
        sc=max(80-mv*2,10)*(2 if has("mem_x2") else 1)
        e=earn(sc); xp(sc//2); st.session_state["mem_pl"]=S("mem_pl",0)+1
        if sc>S("mem_hi",0): st.session_state["mem_hi"]=sc; ach("🧠 שיא זיכרון!")
        if mv<=10: ach("🧠 מוח של זהב!")
        st.markdown(f"<div class='ok' style='font-size:17px;padding:18px'>🎉 סיימת ב-{mv} מהלכים! +{e} 💰</div>",unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
        _,mc,_=st.columns([1,2,1])
        with mc:
            st.markdown('<div class="btnG">',unsafe_allow_html=True)
            if st.button("🔄 משחק חדש",use_container_width=True,key="mr"): _mr(); st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)
        return
    # Pending delay
    if S("mpend") and time.time()-S("mptime",0)>=0.7:
        f2=list(S("mf",[]))
        if len(f2)==2:
            i1,i2=f2
            if b[i1]==b[i2]: mm.add(i1); mm.add(i2); st.session_state["mm"]=mm
        st.session_state["mf"]=[]; st.session_state["mpend"]=False; st.rerun()
    if S("mpend"): time.sleep(0.05); st.rerun()
    can=len(fl)<2 and not S("mpend")
    # Render 4x4 grid with visual cards
    for row in range(4):
        cols=st.columns(4)
        for ci in range(4):
            idx=row*4+ci
            with cols[ci]:
                is_mm=idx in mm; is_fl=idx in fl or is_mm
                if is_fl:
                    em=EMJ[b[idx]]
                    if is_mm:
                        st.markdown(f"""<div style="height:72px;background:rgba(57,255,20,.1);
border:2px solid rgba(57,255,20,.5);border-radius:10px;display:flex;align-items:center;
justify-content:center;font-size:30px;animation:mpop .3s ease">{em}</div>
<style>@keyframes mpop{{from{{transform:scale(.8)}}to{{transform:scale(1)}}}}</style>""",unsafe_allow_html=True)
                    else:
                        st.markdown(f"""<div style="height:72px;background:rgba(0,245,255,.1);
border:2px solid rgba(0,245,255,.4);border-radius:10px;display:flex;align-items:center;
justify-content:center;font-size:30px">{em}</div>""",unsafe_allow_html=True)
                else:
                    lbl=f"{idx+1}"
                    if can:
                        if st.button(lbl,key=f"mc_{idx}_{mv}",use_container_width=True):
                            fl.append(idx); st.session_state["mf"]=fl
                            if len(fl)==2:
                                st.session_state["mov"]=mv+1
                                st.session_state["mpend"]=True; st.session_state["mptime"]=time.time()
                            st.rerun()
                    else:
                        st.markdown(f"""<div style="height:72px;background:rgba(191,95,255,.07);
border:2px solid rgba(191,95,255,.25);border-radius:10px;display:flex;align-items:center;
justify-content:center;font-size:14px;color:#6677aa;font-weight:700">{lbl}</div>""",unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    c1,c2,c3=st.columns(3)
    with c1:
        st.markdown('<div class="btnr">',unsafe_allow_html=True)
        if st.button("🔄 איפוס",use_container_width=True,key="mrst"): _mr(); st.rerun()
        st.markdown('</div>',unsafe_allow_html=True)
    with c2:
        if hints>0:
            st.markdown('<div class="btng">',unsafe_allow_html=True)
            if st.button(f"💡 רמז ({hints})",use_container_width=True,key="mhint"):
                un=[i for i in range(16) if i not in mm and i not in fl]; seen={}
                for i in un:
                    e=b[i]
                    if e in seen:
                        st.session_state["mf"]=[seen[e],i]; st.session_state["mov"]=mv+1
                        st.session_state["mpend"]=True; st.session_state["mptime"]=time.time()
                        st.session_state["mh"]=hints-1; st.rerun(); break
                    seen[e]=i
            st.markdown('</div>',unsafe_allow_html=True)
    with c3: st.metric("🏆 שיא",S("mem_hi",0))

# ═══════════════════════════════════════════════════════════════
#  TIC-TAC-TOE 1P
# ═══════════════════════════════════════════════════════════════
def _tw(b):
    for a,bx,c in[(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]:
        if b[a] and b[a]==b[bx]==b[c]: return b[a]
    return None
def _mm2(b,im,d,weak):
    w=_tw(b)
    if w=="O": return 10-d
    if w=="X": return d-10
    emp=[i for i,v in enumerate(b) if not v]
    if not emp: return 0
    if weak>0 and d==0 and random.random()<weak*0.11: return random.choice([-2,0,2])
    if im:
        best=-99
        for i in emp: b[i]="O"; best=max(best,_mm2(b,False,d+1,weak)); b[i]=""
        return best
    else:
        best=99
        for i in emp: b[i]="X"; best=min(best,_mm2(b,True,d+1,weak)); b[i]=""
        return best
def _ai(b,weak=0):
    mv=None; best=-99
    for i in[j for j,v in enumerate(b) if not v]:
        b[i]="O"; s=_mm2(b,False,0,weak); b[i]=""
        if s>best: best=s; mv=i
    return mv
def _ttr():
    st.session_state.update({"tb":[""]*9,"to":False,"ts":"","tp":None})
def page_ttt():
    st.markdown("<h1 style='text-align:center'>❌ איקס-עיגול</h1><p style='text-align:center;color:#6677aa'>אתה X נגד AI</p>",unsafe_allow_html=True)
    undo=oc("ttt_undo"); weak=oc("ttt_easy")
    if "tb" not in st.session_state: _ttr()
    b=st.session_state["tb"]; ov=S("to"); ts=S("ts",""); prev=S("tp")
    c1,c2,c3,c4=st.columns(4)
    with c1: st.metric("✅ נצ'",S("ttt_w",0))
    with c2: st.metric("❌ הפס'",S("ttt_l",0))
    with c3: st.metric("🤝 תיקו",S("ttt_d",0))
    with c4: st.metric("🎮 משחקים",S("ttt_pl",0))
    st.markdown("<br>",unsafe_allow_html=True)
    if ts:
        cls="ok" if "ניצחת" in ts else ("err" if "הפסדת" in ts else "inf")
        st.markdown(f"<div class='{cls}' style='font-size:16px;padding:14px'>{ts}</div>",unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
    _,mc,_=st.columns([1,2,1])
    with mc:
        for row in range(3):
            rc=st.columns(3)
            for ci in range(3):
                idx=row*3+ci
                with rc[ci]:
                    cell=b[idx]
                    if cell=="X":
                        st.markdown("""<div style="height:80px;background:rgba(0,245,255,.1);border:2px solid rgba(0,245,255,.5);
border-radius:11px;display:flex;align-items:center;justify-content:center;font-size:38px;font-weight:900;
color:#00f5ff;text-shadow:0 0 14px rgba(0,245,255,.8);animation:pp .2s ease">✕</div>
<style>@keyframes pp{from{transform:scale(.3)}to{transform:scale(1)}}</style>""",unsafe_allow_html=True)
                    elif cell=="O":
                        st.markdown("""<div style="height:80px;background:rgba(255,0,110,.1);border:2px solid rgba(255,0,110,.5);
border-radius:11px;display:flex;align-items:center;justify-content:center;font-size:38px;font-weight:900;
color:#ff006e;text-shadow:0 0 14px rgba(255,0,110,.8);animation:pp .2s ease">○</div>""",unsafe_allow_html=True)
                    elif not ov:
                        if st.button(" ",key=f"tt_{idx}_{sum(1 for x in b if x)}",use_container_width=True):
                            st.session_state["tp"]=b[:]
                            b[idx]="X"; w=_tw(b)
                            if w: _tte(w,b); return
                            if ""not in b: _tte("d",b); return
                            ai=_ai(b,weak)
                            if ai is not None:
                                b[ai]="O"; w=_tw(b)
                                if w: _tte(w,b); return
                                if ""not in b: _tte("d",b); return
                            st.session_state["tb"]=b; st.rerun()
                    else:
                        st.markdown("""<div style="height:80px;background:rgba(255,255,255,.02);
border:2px solid rgba(255,255,255,.05);border-radius:11px"></div>""",unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    c1,c2,c3,c4=st.columns(4)
    with c1:
        st.markdown('<div class="btnG">',unsafe_allow_html=True)
        if st.button("🔄 חדש",use_container_width=True,key="ttn"): _ttr(); st.rerun()
        st.markdown('</div>',unsafe_allow_html=True)
    with c2:
        if undo>0 and prev and not ov:
            st.markdown('<div class="btng">',unsafe_allow_html=True)
            if st.button(f"↩ ביטול ({undo})",use_container_width=True,key="ttun"):
                st.session_state["tb"]=prev; st.session_state["tp"]=None; st.session_state["ts"]=""; st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)
    with c3: st.selectbox("קושי",["רגיל","קל","ילד"],key="tts")
def _tte(r,b):
    st.session_state["ttt_pl"]=S("ttt_pl",0)+1; st.session_state["to"]=True; st.session_state["tb"]=b
    if r=="X": st.session_state["ttt_w"]+=1; e=earn(50); xp(25); st.session_state["ts"]=f"🎉 ניצחת! +{e} 💰"; ach("❌ ניצחת AI!")
    elif r=="O": st.session_state["ttt_l"]+=1; e=earn(5); st.session_state["ts"]=f"😔 הפסדת +{e} 💰"
    else: st.session_state["ttt_d"]+=1; e=earn(15); xp(8); st.session_state["ts"]=f"🤝 תיקו +{e} 💰"
    st.rerun()

# ═══════════════════════════════════════════════════════════════
#  CLICKER
# ═══════════════════════════════════════════════════════════════
def page_clicker():
    st.markdown("<h1 style='text-align:center'>👆 קליקר</h1>",unsafe_allow_html=True)
    mul=1+oc("click_mul"); dur=10+oc("click_time")*3
    if mul>1 or dur>10: st.markdown(f"<div class='inf'>×{mul} קליקים  |  {dur} שניות</div>",unsafe_allow_html=True)
    if "cks" not in st.session_state: st.session_state.update({"cks":"idle","ckc":0,"ckt":0})
    state=S("cks"); cnt=S("ckc",0); best=S("click_hi",0)
    if state=="playing":
        el=time.time()-S("ckt",0); rem=max(0,dur-el)
        st.markdown(f"""<div style="text-align:center;margin-bottom:10px">
<div style="font-family:Orbitron,sans-serif;font-size:52px;font-weight:900;color:#ff006e;
  text-shadow:0 0 26px #ff006ecc;{'animation:cf .18s infinite' if rem<3 else ''}">{rem:.1f}</div>
<div style="color:#6677aa;font-size:11px">שניות</div></div>
<style>@keyframes cf{{0%,100%{{color:#ff006e}}50%{{color:#ff5555}}}}</style>""",unsafe_allow_html=True)
        st.progress(rem/dur)
        if rem<=0: st.session_state["cks"]="done"; st.rerun()
    cl="#ff006e" if state=="playing" else("#39ff14" if state=="done" else "#6677aa")
    st.markdown(f"""<div style="text-align:center;margin:10px 0">
<div style="font-family:Orbitron,sans-serif;font-size:72px;font-weight:900;
  color:{cl};text-shadow:0 0 32px {cl}80">{cnt}</div>
<div style="color:#6677aa;font-size:12px">קליקים</div></div>""",unsafe_allow_html=True)
    _,c2,_=st.columns([1,2,1])
    with c2:
        if state=="idle":
            st.markdown('<div class="btnr">',unsafe_allow_html=True)
            if st.button("🚀 התחל!",use_container_width=True,key="ckg"):
                st.session_state.update({"cks":"playing","ckc":0,"ckt":time.time()})
                st.session_state["click_ses"]=S("click_ses",0)+1; st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)
        elif state=="playing":
            st.markdown("""<style>div.ckB .stButton>button{background:rgba(255,0,110,.32)!important;
border:2px solid rgba(255,0,110,.72)!important;color:#ff006e!important;font-size:22px!important;
height:105px!important;font-weight:900!important;}
div.ckB .stButton>button:active{transform:scale(.93)!important;}</style>""",unsafe_allow_html=True)
            st.markdown('<div class="ckB">',unsafe_allow_html=True)
            if st.button("👆 לחץ!",use_container_width=True,key="ckc_btn"):
                st.session_state["ckc"]=cnt+mul; st.session_state["click_tot"]=S("click_tot",0)+mul; st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)
        elif state=="done":
            final=S("ckc",0); e=earn(final*2); xp(final)
            if final>best: st.session_state["click_hi"]=final; ach(f"👆 שיא: {final}!")
                
            st.markdown(f"<div class='{'ok' if final>best else 'inf'}' style='margin-bottom:10px'>{final} קליקים! +{e} 💰</div>",unsafe_allow_html=True)
            st.markdown('<div class="btnG">',unsafe_allow_html=True)
            if st.button("🔄 שוב",use_container_width=True,key="ckr"):
                st.session_state["cks"]="idle"; st.session_state["ckc"]=0; st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)
    if state=="playing": time.sleep(0.05); st.rerun()
    st.markdown("---")
    c1,c2,c3=st.columns(3)
    with c1: st.metric("🏆 שיא",S("click_hi",0))
    with c2: st.metric("👆 סה\"כ",S("click_tot",0))
    with c3: st.metric("🎮 סבבים",S("click_ses",0))

# ═══════════════════════════════════════════════════════════════
#  SLOT MACHINE
# ═══════════════════════════════════════════════════════════════
SYM=["🍒","🍋","🍊","🍇","⭐","💎","🎰","🃏"]; SW=[20,18,15,12,10,7,4,14]
PAY={0:5,1:8,2:10,3:15,4:20,5:50,6:100,7:35}
def page_slot():
    st.markdown("<h1 style='text-align:center'>🎰 מכונת מזל</h1>",unsafe_allow_html=True)
    lk=oc("slot_luck"); jp=oc("slot_jackpot"); rf=has("slot_refund")
    if "slr" not in st.session_state: st.session_state.update({"slr":[6,6,6],"slres":"","slbet":10})
    reels=st.session_state["slr"]; res=S("slres",""); coins=S("coins",0); iw="ניצחת" in res or "קפוט" in res
    brd="rgba(255,214,10,.8)" if iw else "rgba(255,124,0,.4)"; glow="0 0 32px rgba(255,214,10,.4)" if iw else "0 0 14px rgba(255,124,0,.1)"
    r_html="".join(f"""<div style="flex:1;max-width:100px;aspect-ratio:1;
background:linear-gradient(160deg,#1c0d00,#100600);border:2px solid rgba(255,124,0,.4);border-radius:11px;
display:flex;align-items:center;justify-content:center;font-size:50px;
box-shadow:inset 0 0 16px rgba(0,0,0,.7)">{SYM[r]}</div>""" for r in reels)
    pulse="animation:slF .28s infinite;" if "קפוט" in res else ""
    st.markdown(f"""<div style="max-width:400px;margin:0 auto;padding:18px;
background:linear-gradient(145deg,#160900,#200c00,#160900);
border:3px solid {brd};border-radius:16px;box-shadow:{glow},inset 0 0 24px rgba(0,0,0,.5);{pulse}">
<div style="text-align:center;margin-bottom:12px">
<span style="font-family:Orbitron,sans-serif;font-size:16px;font-weight:900;color:#ff7c00;
text-shadow:0 0 11px rgba(255,124,0,.7);letter-spacing:3px">🎰 ARCADE SLOTS</span></div>
<div style="display:flex;gap:10px;justify-content:center;padding:12px;
background:rgba(0,0,0,.5);border-radius:11px;border:1px solid rgba(255,124,0,.16)">{r_html}</div>
<div style="margin-top:8px;height:2px;background:linear-gradient(90deg,transparent,{'#ffd60a' if iw else 'rgba(255,124,0,.28)'},transparent);
{'box-shadow:0 0 7px #ffd60a;' if iw else ''}"></div></div>
<style>@keyframes slF{{0%,100%{{border-color:rgba(255,214,10,.8)}}50%{{border-color:rgba(255,214,10,.1)}}}}</style>""",unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    if res:
        st.markdown(f"<div class='{'ok' if iw else 'err'}' style='font-size:14px'>{res}</div>",unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
    c1,c2=st.columns([3,1])
    with c1: bet=st.slider("הימור 💰",5,min(200,max(5,coins)),min(S("slbet",10),max(5,coins)),5,key="slsl"); st.session_state["slbet"]=bet
    with c2: st.metric("יתרה",coins)
    _,c2,_=st.columns([1,2,1])
    with c2:
        st.markdown("""<style>div.spB .stButton>button{background:rgba(255,124,0,.3)!important;
border:2px solid rgba(255,124,0,.6)!important;color:#ff7c00!important;font-size:16px!important;
height:54px!important;font-weight:900!important;}</style>""",unsafe_allow_html=True)
        st.markdown('<div class="spB">',unsafe_allow_html=True)
        if st.button("🎰 סובב!",use_container_width=True,key="slsp",disabled=coins<bet): _spin(bet,lk,jp,rf)
        st.markdown('</div>',unsafe_allow_html=True)
    if coins<bet: st.markdown("<div class='err'>אין מספיק מטבעות</div>",unsafe_allow_html=True)
    st.markdown("---")
    with st.expander("📋 טבלת תשלומים"):
        for idx,mul in PAY.items():
            am=mul*(2**jp if mul>=50 else 1)
            st.markdown(f"""<div style="display:flex;justify-content:space-between;padding:4px 10px;
background:rgba(255,124,0,.04);border-radius:6px;margin-bottom:2px">
<span style="font-size:18px">{SYM[idx]*3}</span>
<span style="color:#ff7c00;font-weight:700;font-family:Orbitron">x{am}</span></div>""",unsafe_allow_html=True)
    st.markdown("---")
    c1,c2,c3=st.columns(3)
    with c1: st.metric("🎰 סיבובים",S("slot_sp",0))
    with c2: st.metric("🏆 זכיות",S("slot_w",0))
    with c3: st.metric("💰 סה\"כ",S("slot_tot",0))
def _spin(bet,lk,jp,rf):
    st.session_state["coins"]-=bet; st.session_state["slot_sp"]=S("slot_sp",0)+1
    w=SW[:]
    for i in[4,5,6]: w[i]=int(w[i]*(1+lk*0.28))
    r=[random.choices(range(8),weights=w,k=1)[0] for _ in range(3)]
    st.session_state["slr"]=r
    if r[0]==r[1]==r[2]:
        pay=PAY[r[0]]*(2**jp if r[0]>=4 else 1)
        won=bet*pay; e=earn(won); xp(won//5)
        st.session_state["slot_w"]=S("slot_w",0)+1; st.session_state["slot_tot"]=S("slot_tot",0)+e
        st.session_state["slres"]=(f"🎉🎰 ג'קפוט!!! +{e} 💰" if pay>=100 else f"⭐ ניצחת! +{e} 💰 (x{pay})")
        if pay>=100: ach("🎰 ג'קפוט!")
    elif r[0]==r[1] or r[1]==r[2] or r[0]==r[2]:
        e=earn(bet*2); xp(3); st.session_state["slres"]=f"✅ זוג! +{e} 💰"
        st.session_state["slot_w"]=S("slot_w",0)+1
    else:
        if rf: rb=max(1,int(bet*.1)); earn(rb); st.session_state["slres"]=f"😔 הפסדת... החזר: {rb} 💰"
        else: st.session_state["slres"]=f"😔 הפסדת {bet} 💰"
    st.rerun()

# ═══════════════════════════════════════════════════════════════
#  PONG 1P  (canvas vs AI)
# ═══════════════════════════════════════════════════════════════
def page_pong():
    st.markdown("<h1 style='text-align:center'>🏓 פונג</h1><p style='text-align:center;color:#6677aa'>W/S לשחקן | AI בצד ימין</p>",unsafe_allow_html=True)
    speed_bonus=oc("pong_speed"); hi=S("pong_hi",0)
    _,col,_=st.columns([1,8,1])
    with col:
        components.html(f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#060612;display:flex;flex-direction:column;align-items:center;padding:6px;user-select:none}}
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');
canvas{{border:2px solid rgba(0,245,255,.28);border-radius:10px;box-shadow:0 0 22px rgba(0,245,255,.09);display:block}}
.ov{{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);background:rgba(4,4,18,.95);
  border:2px solid #00f5ff;border-radius:11px;padding:18px 26px;text-align:center;min-width:165px}}
.ov h2{{color:#00f5ff;font-size:17px;margin-bottom:7px}}.ov p{{color:#8888aa;font-size:11px;margin-bottom:11px}}
.ov button{{background:rgba(0,245,255,.16);color:#00f5ff;border:1px solid #00f5ff;
  padding:7px 18px;border-radius:6px;cursor:pointer;font-family:Orbitron;font-size:12px;font-weight:700}}
.wrap{{position:relative}}</style></head><body>
<div class="wrap"><canvas id="c" width="480" height="300"></canvas>
<div class="ov" id="ov"><h2 id="ot">🏓 פונג</h2><p>W/S לשחקן שמאל<br>AI בצד ימין</p>
<button onclick="start()">▶ שחק</button></div></div>
<script>
const W=480,H=300,PW=10,PH=60,BALL=7,SPB={2+speed_bonus};
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
let p1y,p2y,bx,by,vx,vy,s1,s2,run,raf,keys={{}};
function start(){{
  document.getElementById('ov').style.display='none';
  p1y=H/2-PH/2;p2y=H/2-PH/2;bx=W/2;by=H/2;
  let a=(Math.random()*0.8+0.1)*Math.PI*(Math.random()<.5?1:-1);
  vx=Math.cos(a)*(SPB+1);vy=Math.sin(a)*SPB;s1=s2=0;run=true;
  if(raf)cancelAnimationFrame(raf);loop();
}}
document.addEventListener('keydown',e=>{{keys[e.code]=true;if(['KeyW','KeyS','ArrowUp','ArrowDown'].includes(e.code))e.preventDefault();}});
document.addEventListener('keyup',e=>keys[e.code]=false);
function loop(){{if(!run)return;update();draw();raf=requestAnimationFrame(loop);}}
function update(){{
  if(keys['KeyW']||keys['ArrowUp'])p1y=Math.max(0,p1y-5);
  if(keys['KeyS']||keys['ArrowDown'])p1y=Math.min(H-PH,p1y+5);
  // AI
  let cy=p2y+PH/2;if(by<cy-3)p2y=Math.max(0,p2y-4);else if(by>cy+3)p2y=Math.min(H-PH,p2y+4);
  bx+=vx;by+=vy;
  if(by<=BALL||by>=H-BALL)vy=-vy;
  if(bx<=20+PW&&by>=p1y&&by<=p1y+PH){{vx=Math.abs(vx)*(1+s1*.04);vy+=(by-(p1y+PH/2))*0.1;}}
  if(bx>=W-20-PW&&by>=p2y&&by<=p2y+PH){{vx=-Math.abs(vx)*(1+s2*.04);vy+=(by-(p2y+PH/2))*0.1;}}
  if(bx<0){{s2++;if(s2>=7){{endGame('AI ניצח');return;}}reset();}}
  if(bx>W){{s1++;if(s1>=7){{endGame('ניצחת!');return;}}reset();}}
}}
function reset(){{bx=W/2;by=H/2;let a=(Math.random()*0.8+0.1)*Math.PI*(Math.random()<.5?1:-1);
  vx=Math.cos(a)*(SPB+1+Math.max(s1,s2)*.2);vy=Math.sin(a)*SPB;}}
function endGame(msg){{run=false;cancelAnimationFrame(raf);
  document.getElementById('ot').textContent=msg;
  document.getElementById('ov').querySelector('p').textContent='שחקן: '+s1+' | AI: '+s2;
  document.getElementById('ov').style.display='block';
  window.parent.postMessage({{type:'pong_done',score:s1,win:msg==='ניצחת!'}},'*');
}}
function draw(){{
  ctx.fillStyle='#06060e';ctx.fillRect(0,0,W,H);
  ctx.setLineDash([8,8]);ctx.strokeStyle='rgba(255,255,255,.1)';ctx.lineWidth=1;
  ctx.beginPath();ctx.moveTo(W/2,0);ctx.lineTo(W/2,H);ctx.stroke();ctx.setLineDash([]);
  ctx.fillStyle='rgba(0,245,255,.9)';ctx.font='bold 28px Orbitron,monospace';ctx.textAlign='center';
  ctx.fillText(s1,W/2-60,38);ctx.fillText(s2,W/2+60,38);
  // paddles
  [{{x:14,y:p1y,c:'#00f5ff'}},{{x:W-14-PW,y:p2y,c:'#ff006e'}}].forEach(p=>{{
    ctx.shadowBlur=14;ctx.shadowColor=p.c;ctx.fillStyle=p.c;
    ctx.beginPath();ctx.roundRect(p.x,p.y,PW,PH,4);ctx.fill();ctx.shadowBlur=0;
  }});
  // ball
  ctx.shadowBlur=16;ctx.shadowColor='#ffd60a';ctx.fillStyle='#ffd60a';
  ctx.beginPath();ctx.arc(bx,by,BALL,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
}}
ctx.fillStyle='#06060e';ctx.fillRect(0,0,W,H);
</script></body></html>""",height=350,scrolling=False)

    st.markdown("<br>",unsafe_allow_html=True)
    _,c2,_=st.columns([1,2,1])
    with c2:
        st.markdown('<div class="btnG">',unsafe_allow_html=True)
        if st.button("▶ משחק חדש",use_container_width=True,key="pnew"):
            st.session_state["pong_pl"]=S("pong_pl",0)+1; earn(5); xp(5)
        st.markdown('</div>',unsafe_allow_html=True)
    st.markdown("---")
    c1,c2=st.columns(2)
    with c1: st.metric("🏆 שיא",S("pong_hi",0))
    with c2: st.metric("🎮 משחקים",S("pong_pl",0))

# ═══════════════════════════════════════════════════════════════
#  MINESWEEPER 1P
# ═══════════════════════════════════════════════════════════════
def _ms_init(rows=8,cols=8,mines=10):
    board=[[0]*cols for _ in range(rows)]
    mine_pos=random.sample(range(rows*cols),mines)
    mines_set=set(mine_pos)
    for p in mines_set: board[p//cols][p%cols]=-1
    for r in range(rows):
        for c in range(cols):
            if board[r][c]==-1: continue
            board[r][c]=sum(1 for dr in[-1,0,1] for dc in[-1,0,1]
                           if 0<=r+dr<rows and 0<=c+dc<cols and board[r+dr][c+dc]==-1)
    st.session_state.update({"ms_b":board,"ms_rev":set(),"ms_flag":set(),
                              "ms_rows":rows,"ms_cols":cols,"ms_mines":mines,
                              "ms_over":False,"ms_win":False,"ms_start":None})

def page_minesweeper():
    st.markdown("<h1 style='text-align:center'>💣 שדה מוקשים</h1><p style='text-align:center;color:#6677aa'>מצא את כל הבטוחות!</p>",unsafe_allow_html=True)
    if "ms_b" not in st.session_state: _ms_init()
    b=st.session_state["ms_b"]; rev=st.session_state["ms_rev"]; flags=st.session_state["ms_flag"]
    rows=S("ms_rows",8); cols_n=S("ms_cols",8); mines=S("ms_mines",10)
    over=S("ms_over"); win=S("ms_win")
    safe_total=rows*cols_n-mines; revealed_safe=sum(1 for i in rev if b[i//cols_n][i%cols_n]!=-1)

    c1,c2,c3=st.columns(3)
    with c1: st.metric("💣 מוקשים",mines-len(flags))
    with c2: st.metric("✅ נחשף",f"{revealed_safe}/{safe_total}")
    with c3:
        diff=st.selectbox("קושי",["קל (6x6)","רגיל (8x8)","קשה (10x10)"],key="ms_diff",label_visibility="visible")

    if over:
        if win: st.markdown(f"<div class='ok' style='font-size:17px;padding:16px'>🎉 ניצחת! כל המוקשים מסומנים!</div>",unsafe_allow_html=True)
        else: st.markdown("<div class='err' style='font-size:16px;padding:14px'>💥 בום! דרכת על מוקש!</div>",unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)

    # Difficulty settings
    _,mc,_=st.columns([1,4,1])
    with mc:
        # Render board
        COLORS={0:"#6677aa",1:"#00f5ff",2:"#39ff14",3:"#ff006e",4:"#bf5fff",
                5:"#ff7c00",6:"#ffd60a",7:"#ffffff",8:"#8888aa"}
        for r in range(rows):
            row_cols=st.columns(cols_n)
            for c in range(cols_n):
                idx=r*cols_n+c; cell=b[r][c]
                with row_cols[c]:
                    is_rev=idx in rev; is_flag=idx in flags
                    if is_rev:
                        if cell==-1:
                            st.markdown("""<div style="height:38px;background:rgba(255,0,110,.2);
border:1px solid rgba(255,0,110,.5);border-radius:6px;display:flex;align-items:center;
justify-content:center;font-size:18px">💥</div>""",unsafe_allow_html=True)
                        else:
                            col_c=COLORS.get(cell,"#fff"); txt=str(cell) if cell>0 else ""
                            st.markdown(f"""<div style="height:38px;background:rgba(255,255,255,.04);
border:1px solid rgba(255,255,255,.08);border-radius:6px;display:flex;align-items:center;
justify-content:center;font-size:15px;font-weight:700;color:{col_c}">{txt}</div>""",unsafe_allow_html=True)
                    elif is_flag:
                        st.markdown("""<div style="height:38px;background:rgba(255,214,10,.1);
border:1px solid rgba(255,214,10,.4);border-radius:6px;display:flex;align-items:center;
justify-content:center;font-size:16px">🚩</div>""",unsafe_allow_html=True)
                        if not over:
                            if st.button("",key=f"msf_{idx}",use_container_width=True,help="הסר דגל"):
                                flags.discard(idx); st.session_state["ms_flag"]=flags; st.rerun()
                    else:
                        if not over:
                            c1b,c2b=st.columns(2)
                            with c1b:
                                if st.button("?",key=f"msr_{idx}",use_container_width=True):
                                    if st.session_state.get("ms_start") is None:
                                        st.session_state["ms_start"]=time.time()
                                    _ms_reveal(idx,b,rev,flags,rows,cols_n,mines)
                            with c2b:
                                if st.button("🚩",key=f"msfl_{idx}",use_container_width=True):
                                    if idx not in rev: flags.add(idx); st.session_state["ms_flag"]=flags; st.rerun()

    st.markdown("<br>",unsafe_allow_html=True)
    _,c2,_=st.columns([1,2,1])
    with c2:
        st.markdown('<div class="btnr">',unsafe_allow_html=True)
        if st.button("🔄 משחק חדש",use_container_width=True,key="msnew"):
            d=S("ms_diff","רגיל (8x8)")
            if "6x6" in d: _ms_init(6,6,7)
            elif "10x10" in d: _ms_init(10,10,18)
            else: _ms_init(8,8,10)
            st.rerun()
        st.markdown('</div>',unsafe_allow_html=True)

def _ms_reveal(idx,b,rev,flags,rows,cols,mines):
    if idx in rev or idx in flags: return
    r,c=idx//cols,idx%cols
    if b[r][c]==-1:
        rev.add(idx); st.session_state["ms_rev"]=rev
        st.session_state["ms_over"]=True; st.session_state["ms_win"]=False; st.rerun()
    # Flood fill for 0 cells
    stack=[idx]
    while stack:
        cur=stack.pop(); rev.add(cur)
        cr,cc=cur//cols,cur%cols
        if b[cr][cc]==0:
            for dr in[-1,0,1]:
                for dc in[-1,0,1]:
                    nr,nc=cr+dr,cc+dc
                    ni=nr*cols+nc
                    if 0<=nr<rows and 0<=nc<cols and ni not in rev: stack.append(ni)
    st.session_state["ms_rev"]=rev
    safe_total=rows*cols-mines
    if sum(1 for i in rev if b[i//cols][i%cols]!=-1)==safe_total:
        e=earn(80); xp(40); ach("💣 פוצץ את שדה המוקשים!")
        st.session_state["ms_over"]=True; st.session_state["ms_win"]=True
    st.rerun()

# ═══════════════════════════════════════════════════════════════
#  GUESS THE NUMBER
# ═══════════════════════════════════════════════════════════════
def page_guess():
    st.markdown("<h1 style='text-align:center'>🔢 מספר חשאי</h1><p style='text-align:center;color:#6677aa'>נחש מספר בין 1 ל-100</p>",unsafe_allow_html=True)
    if "gn" not in st.session_state:
        st.session_state.update({"gn":random.randint(1,100),"gattempts":0,"gover":False,"gmax":10,"gfeed":""})
    gn=S("gn"); attempts=S("gattempts",0); mx=S("gmax",10); feed=S("gfeed",""); over=S("gover")

    c1,c2=st.columns(2)
    with c1: st.metric("🔢 ניסיונות",f"{attempts}/{mx}")
    with c2: st.metric("📊 טווח","1–100")

    if over:
        won="ניצחת" in feed
        st.markdown(f"<div class='{'ok' if won else 'err'}' style='font-size:17px;padding:14px'>{feed}</div>",unsafe_allow_html=True)
        _,mc,_=st.columns([1,2,1])
        with mc:
            st.markdown('<div class="btnG">',unsafe_allow_html=True)
            if st.button("🔄 משחק חדש",use_container_width=True,key="gnnew"):
                st.session_state.update({"gn":random.randint(1,100),"gattempts":0,"gover":False,"gfeed":""})
                st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)
        return

    if feed: st.markdown(f"<div class='inf' style='font-size:16px;padding:12px'>{feed}</div>",unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)

    # Visual range indicator
    lo=S("g_lo",1); hi2=S("g_hi",100)
    st.markdown(f"<div class='warn' style='font-size:14px'>טווח אפשרי: {lo} – {hi2}</div>",unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)

    c1,c2=st.columns([3,1])
    with c1: guess=st.number_input("הניחוש שלך:",1,100,50,key="gin",label_visibility="visible")
    with c2:
        st.markdown("<br>",unsafe_allow_html=True)
        st.markdown('<div class="btng">',unsafe_allow_html=True)
        if st.button("🎯 נחש",use_container_width=True,key="gok"):
            st.session_state["gattempts"]=attempts+1
            if guess==gn:
                e=earn(max(10,(mx-attempts)*15)); xp(30)
                st.session_state["gfeed"]=f"🎉 ניצחת! המספר היה {gn}! +{e} 💰"
                st.session_state["gover"]=True
                ach("🔢 נחשת!")
            elif attempts+1>=mx:
                st.session_state["gfeed"]=f"😔 נגמרו הניסיונות! המספר היה {gn}"
                st.session_state["gover"]=True
            elif guess<gn:
                st.session_state["gfeed"]=f"📈 גבוה יותר מ-{guess}"
                st.session_state["g_lo"]=max(lo,guess+1)
            else:
                st.session_state["gfeed"]=f"📉 נמוך יותר מ-{guess}"
                st.session_state["g_hi"]=min(hi2,guess-1)
            st.rerun()
        st.markdown('</div>',unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  TARGET SHOOTING
# ═══════════════════════════════════════════════════════════════
def page_targets():
    st.markdown("<h1 style='text-align:center'>🎯 ירי מטרות</h1><p style='text-align:center;color:#6677aa'>לחץ על המטרה לפני שתיעלם! 15 שניות</p>",unsafe_allow_html=True)
    if "tgt_state" not in st.session_state:
        st.session_state.update({"tgt_state":"idle","tgt_score":0,"tgt_start":0,
                                  "tgt_pos":None,"tgt_hi":0,"tgt_appear":0})

    state=S("tgt_state"); score=S("tgt_score",0); hi=S("tgt_hi",0)

    if state=="idle":
        _,mc,_=st.columns([1,2,1])
        with mc:
            st.markdown('<div class="btnr">',unsafe_allow_html=True)
            if st.button("🎯 התחל!",use_container_width=True,key="tgtgo"):
                st.session_state.update({"tgt_state":"playing","tgt_score":0,
                                         "tgt_start":time.time(),"tgt_pos":_new_target(),"tgt_appear":time.time()})
                st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)
        st.metric("🏆 שיא",hi)
        return

    if state=="playing":
        el=time.time()-S("tgt_start",0); rem=max(0,15-el)
        if rem<=0: st.session_state["tgt_state"]="done"; st.rerun()
        c1,c2=st.columns(2)
        with c1: st.metric("🎯 ניקוד",score)
        with c2: st.markdown(f"<div style='font-family:Orbitron,sans-serif;font-size:28px;color:{'#ff006e' if rem<5 else '#00f5ff'};text-align:center;padding:10px'>{rem:.1f}</div>",unsafe_allow_html=True)
        st.progress(rem/15)
        # Target appears/disappears every 2 seconds
        pos=S("tgt_pos"); appear_t=S("tgt_appear",0)
        if time.time()-appear_t>2.5: pos=_new_target(); st.session_state.update({"tgt_pos":pos,"tgt_appear":time.time()})
        if pos:
            row,col_i=pos
            rows=st.columns(5)
            for ri in range(5):
                with rows[ri]:
                    if ri==col_i:
                        age=time.time()-appear_t; opacity=max(0.2,1-age/2.5)
                        st.markdown(f"""<div style="height:70px;background:rgba(255,0,110,{opacity:.2f});
border:2px solid rgba(255,0,110,{opacity:.1f}+.4);border-radius:50%;display:flex;align-items:center;
justify-content:center;font-size:32px;cursor:pointer;animation:tgtpulse 0.4s ease-in-out infinite">🎯</div>
<style>@keyframes tgtpulse{{0%,100%{{transform:scale(1)}}50%{{transform:scale(1.1)}}}}</style>""",unsafe_allow_html=True)
                        if st.button("🎯",key=f"tgt_{int(appear_t*100)}_{ri}",use_container_width=True):
                            bonus=max(1,int((2.5-(time.time()-appear_t))*5))
                            st.session_state["tgt_score"]=score+bonus
                            st.session_state.update({"tgt_pos":_new_target(),"tgt_appear":time.time()})
                            st.rerun()
                    else:
                        st.markdown("""<div style="height:70px;background:rgba(255,255,255,.02);
border:1px solid rgba(255,255,255,.04);border-radius:50%"></div>""",unsafe_allow_html=True)
        time.sleep(0.1); st.rerun()

    if state=="done":
        e=earn(score*3); xp(score)
        if score>hi: st.session_state["tgt_hi"]=score; ach(f"🎯 שיא מטרות: {score}!")
        st.markdown(f"<div class='ok' style='font-size:17px;padding:16px'>🎉 {score} מטרות! +{e} 💰</div>",unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
        _,mc,_=st.columns([1,2,1])
        with mc:
            st.markdown('<div class="btnG">',unsafe_allow_html=True)
            if st.button("🔄 שוב",use_container_width=True,key="tgtagn"):
                st.session_state.update({"tgt_state":"idle","tgt_score":0})
                st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)

def _new_target():
    return (random.randint(0,2), random.randint(0,4))

# ═══════════════════════════════════════════════════════════════
#  WORD SNAKE (word guessing)
# ═══════════════════════════════════════════════════════════════
WORDS=["PYTHON","STREAMLIT","GAME","CODE","PLAY","STAR","FIRE","MOON","KING","LION",
       "HERO","RACE","GOLD","DARK","NEON","PIXEL","BLAST","CYBER","QUEST","STORM"]
def page_word_snake():
    st.markdown("<h1 style='text-align:center'>🐍 נחש מילים</h1><p style='text-align:center;color:#6677aa'>נחש את המילה באנגלית — 6 ניסיונות</p>",unsafe_allow_html=True)
    if "ws_word" not in st.session_state:
        w=random.choice(WORDS); st.session_state.update({"ws_word":w,"ws_guesses":[],"ws_over":False,"ws_msg":""})
    word=S("ws_word",""); guesses=list(S("ws_guesses",[])); over=S("ws_over"); msg=S("ws_msg","")

    c1,c2=st.columns(2)
    with c1: st.metric("📝 אורך",len(word))
    with c2: st.metric("🎯 ניסיונות",f"{len(guesses)}/6")

    # Show guesses
    for g in guesses:
        row_html=""
        for i,ch in enumerate(g):
            if ch==word[i]: color="#39ff14"; bg="rgba(57,255,20,.15)"; bd="rgba(57,255,20,.5)"
            elif ch in word: color="#ffd60a"; bg="rgba(255,214,10,.12)"; bd="rgba(255,214,10,.4)"
            else: color="#6677aa"; bg="rgba(255,255,255,.04)"; bd="rgba(255,255,255,.1)"
            row_html+=f"""<div style="width:44px;height:44px;background:{bg};border:2px solid {bd};
border-radius:7px;display:flex;align-items:center;justify-content:center;
font-size:18px;font-weight:900;color:{color};font-family:Orbitron,sans-serif">{ch}</div>"""
        st.markdown(f"<div style='display:flex;gap:6px;justify-content:center;margin-bottom:6px'>{row_html}</div>",unsafe_allow_html=True)

    # Empty slots
    for _ in range(6-len(guesses)):
        empties="".join(f"""<div style="width:44px;height:44px;background:rgba(255,255,255,.02);
border:2px solid rgba(255,255,255,.07);border-radius:7px"></div>""" for _ in range(len(word)))
        st.markdown(f"<div style='display:flex;gap:6px;justify-content:center;margin-bottom:6px'>{empties}</div>",unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)
    if msg: st.markdown(f"<div class='{'ok' if 'ניצחת' in msg else ('err' if 'המילה' in msg else 'inf')}' style='padding:12px'>{msg}</div>",unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)

    if over:
        _,mc,_=st.columns([1,2,1])
        with mc:
            st.markdown('<div class="btnG">',unsafe_allow_html=True)
            if st.button("🔄 מילה חדשה",use_container_width=True,key="wsnew"):
                w=random.choice(WORDS); st.session_state.update({"ws_word":w,"ws_guesses":[],"ws_over":False,"ws_msg":""})
                st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)
        return

    c1,c2=st.columns([3,1])
    with c1: inp=st.text_input("הזן מילה:",max_chars=len(word),key="wsinp",label_visibility="collapsed").upper().strip()
    with c2:
        st.markdown('<div class="btng">',unsafe_allow_html=True)
        if st.button("🎯",use_container_width=True,key="wsok"):
            if len(inp)!=len(word):
                st.session_state["ws_msg"]=f"⚠️ המילה צריכה להיות {len(word)} אותיות"
            elif inp not in WORDS and inp not in [word]:
                st.session_state["ws_msg"]="⚠️ מילה לא מוכרת"
            elif inp in guesses:
                st.session_state["ws_msg"]="⚠️ כבר ניחשת את זה"
            else:
                guesses.append(inp); st.session_state["ws_guesses"]=guesses
                if inp==word:
                    e=earn(max(20,(6-len(guesses)+1)*25)); xp(40)
                    st.session_state["ws_msg"]=f"🎉 ניצחת! +{e} 💰"
                    st.session_state["ws_over"]=True; ach("🐍 פענחת מילה!")
                elif len(guesses)>=6:
                    st.session_state["ws_msg"]=f"😔 המילה הייתה: {word}"
                    st.session_state["ws_over"]=True
                else:
                    st.session_state["ws_msg"]="💡 ירוק=מיקום נכון | צהוב=אות נכונה"
            st.rerun()
        st.markdown('</div>',unsafe_allow_html=True)
    st.markdown("<div style='color:#6677aa;font-size:11px'>🟩 אות במיקום נכון | 🟨 אות קיימת | ⬜ לא קיים</div>",unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  PONG 2P
# ═══════════════════════════════════════════════════════════════
def page_pong2p():
    st.markdown("<h1 style='text-align:center'>🏓 פונג — 2 שחקנים</h1>",unsafe_allow_html=True)
    st.markdown("<div class='inf'>שחקן 1: W/S  |  שחקן 2: ↑/↓</div>",unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    _,col,_=st.columns([1,8,1])
    with col:
        components.html("""<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>*{margin:0;padding:0;box-sizing:border-box}
body{background:#060612;display:flex;flex-direction:column;align-items:center;padding:6px;user-select:none}
canvas{border:2px solid rgba(0,245,255,.28);border-radius:10px;box-shadow:0 0 22px rgba(0,245,255,.09);display:block}
.ov{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);background:rgba(4,4,18,.95);
border:2px solid #00f5ff;border-radius:11px;padding:18px 26px;text-align:center}
.ov h2{color:#00f5ff;font-size:17px;margin-bottom:7px}.ov p{color:#8888aa;font-size:11px;margin-bottom:11px}
.ov button{background:rgba(0,245,255,.16);color:#00f5ff;border:1px solid #00f5ff;
padding:7px 18px;border-radius:6px;cursor:pointer;font-family:Orbitron;font-size:12px;font-weight:700}
.wrap{position:relative}
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');
</style></head><body>
<div class="wrap"><canvas id="c" width="540" height="320"></canvas>
<div class="ov" id="ov"><h2>🏓 פונג 2P</h2>
<p>שחקן 1: W/S | שחקן 2: ↑/↓<br>ראשון ל-7 נקודות מנצח!</p>
<button onclick="start()">▶ שחק</button></div></div>
<script>
const W=540,H=320,PW=11,PH=65,BALL=7;
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
let p1y,p2y,bx,by,vx,vy,s1,s2,run,raf,keys={};
function start(){document.getElementById('ov').style.display='none';
  p1y=H/2-PH/2;p2y=H/2-PH/2;bx=W/2;by=H/2;
  let a=(Math.random()*0.7+0.15)*Math.PI*(Math.random()<.5?1:-1);
  vx=Math.cos(a)*3.5;vy=Math.sin(a)*3.5;s1=s2=0;run=true;
  if(raf)cancelAnimationFrame(raf);loop();
}
document.addEventListener('keydown',e=>{keys[e.code]=true;
  if(['KeyW','KeyS','ArrowUp','ArrowDown'].includes(e.code))e.preventDefault();});
document.addEventListener('keyup',e=>keys[e.code]=false);
function loop(){if(!run)return;update();draw();raf=requestAnimationFrame(loop);}
function update(){
  if(keys['KeyW'])p1y=Math.max(0,p1y-5);if(keys['KeyS'])p1y=Math.min(H-PH,p1y+5);
  if(keys['ArrowUp'])p2y=Math.max(0,p2y-5);if(keys['ArrowDown'])p2y=Math.min(H-PH,p2y+5);
  bx+=vx;by+=vy;
  if(by<=BALL||by>=H-BALL)vy=-vy;
  if(bx<=16+PW&&by>=p1y&&by<=p1y+PH){vx=Math.abs(vx)*(1.03);vy+=(by-(p1y+PH/2))*0.08;}
  if(bx>=W-16-PW&&by>=p2y&&by<=p2y+PH){vx=-Math.abs(vx)*(1.03);vy+=(by-(p2y+PH/2))*0.08;}
  if(bx<0){s2++;if(s2>=7){end('שחקן 2 ניצח! 🎉');return;}reset();}
  if(bx>W){s1++;if(s1>=7){end('שחקן 1 ניצח! 🎉');return;}reset();}
}
function reset(){bx=W/2;by=H/2;let a=(Math.random()*0.7+0.15)*Math.PI*(Math.random()<.5?1:-1);
  vx=Math.cos(a)*(3.5+Math.max(s1,s2)*.15);vy=Math.sin(a)*3.5;}
function end(msg){run=false;cancelAnimationFrame(raf);
  document.getElementById('ov').querySelector('h2').textContent=msg;
  document.getElementById('ov').querySelector('p').textContent='שחקן 1: '+s1+' | שחקן 2: '+s2;
  document.getElementById('ov').style.display='block';
}
function draw(){
  ctx.fillStyle='#06060e';ctx.fillRect(0,0,W,H);
  ctx.setLineDash([7,7]);ctx.strokeStyle='rgba(255,255,255,.08)';ctx.lineWidth=1;
  ctx.beginPath();ctx.moveTo(W/2,0);ctx.lineTo(W/2,H);ctx.stroke();ctx.setLineDash([]);
  ctx.font='bold 26px Orbitron,monospace';ctx.textAlign='center';
  ctx.fillStyle='#00f5ff';ctx.shadowBlur=12;ctx.shadowColor='#00f5ff';ctx.fillText(s1,W/2-65,36);
  ctx.fillStyle='#ff006e';ctx.shadowColor='#ff006e';ctx.fillText(s2,W/2+65,36);ctx.shadowBlur=0;
  [{x:14,y:p1y,c:'#00f5ff'},{x:W-14-PW,y:p2y,c:'#ff006e'}].forEach(p=>{
    ctx.shadowBlur=13;ctx.shadowColor=p.c;ctx.fillStyle=p.c;
    ctx.beginPath();ctx.roundRect(p.x,p.y,PW,PH,4);ctx.fill();ctx.shadowBlur=0;
  });
  ctx.shadowBlur=15;ctx.shadowColor='#ffd60a';ctx.fillStyle='#ffd60a';
  ctx.beginPath();ctx.arc(bx,by,BALL,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
}
ctx.fillStyle='#06060e';ctx.fillRect(0,0,W,H);
</script></body></html>""",height=370,scrolling=False)

# ═══════════════════════════════════════════════════════════════
#  TIC-TAC-TOE 2P
# ═══════════════════════════════════════════════════════════════
def page_ttt2p():
    st.markdown("<h1 style='text-align:center'>❌ איקס-עיגול — 2 שחקנים</h1>",unsafe_allow_html=True)
    if "tb2" not in st.session_state:
        st.session_state.update({"tb2":[""]*9,"turn2":"X","tw2":{"X":0,"O":0},"to2":False,"ts2":""})
    b=st.session_state["tb2"]; turn=S("turn2","X"); wins=S("tw2",{"X":0,"O":0}); over=S("to2"); msg=S("ts2","")

    c1,c2,c3=st.columns(3)
    with c1: st.metric("❌ שחקן 1",wins.get("X",0))
    with c2: st.metric("🔵 שחקן 2",wins.get("O",0))
    with c3: st.markdown(f"<div style='text-align:center;font-family:Orbitron;font-size:22px;color:{'#00f5ff' if turn=='X' else '#ff006e'};padding:12px'>תור: {'❌ 1' if turn=='X' else '⭕ 2'}</div>",unsafe_allow_html=True)
    if msg:
        cls="ok" if "ניצח" in msg else "inf"
        st.markdown(f"<div class='{cls}' style='font-size:16px;padding:12px;margin-bottom:10px'>{msg}</div>",unsafe_allow_html=True)
    _,mc,_=st.columns([1,2,1])
    with mc:
        for row in range(3):
            rc=st.columns(3)
            for ci in range(3):
                idx=row*3+ci
                with rc[ci]:
                    cell=b[idx]
                    if cell=="X": st.markdown("""<div style="height:78px;background:rgba(0,245,255,.1);border:2px solid rgba(0,245,255,.5);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:36px;color:#00f5ff">✕</div>""",unsafe_allow_html=True)
                    elif cell=="O": st.markdown("""<div style="height:78px;background:rgba(255,0,110,.1);border:2px solid rgba(255,0,110,.5);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:36px;color:#ff006e">○</div>""",unsafe_allow_html=True)
                    elif not over:
                        if st.button(" ",key=f"tt2_{idx}_{sum(1 for x in b if x)}",use_container_width=True):
                            b[idx]=turn; w=_tw(b)
                            if w:
                                wins[w]=wins.get(w,0)+1; st.session_state["tw2"]=wins
                                st.session_state.update({"ts2":f"{'❌ שחקן 1' if w=='X' else '⭕ שחקן 2'} ניצח! 🎉","to2":True,"tb2":b})
                                earn(30); xp(15)
                            elif ""not in b:
                                st.session_state.update({"ts2":"🤝 תיקו!","to2":True,"tb2":b})
                            else:
                                st.session_state.update({"turn2":"O" if turn=="X" else "X","tb2":b})
                            st.rerun()
                    else:
                        st.markdown("""<div style="height:78px;background:rgba(255,255,255,.02);border:2px solid rgba(255,255,255,.05);border-radius:10px"></div>""",unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    _,c2,_=st.columns([1,2,1])
    with c2:
        st.markdown('<div class="btnG">',unsafe_allow_html=True)
        if st.button("🔄 סיבוב חדש",use_container_width=True,key="tt2n"):
            st.session_state.update({"tb2":[""]*9,"turn2":"X","to2":False,"ts2":""}); st.rerun()
        st.markdown('</div>',unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  DICE 2P
# ═══════════════════════════════════════════════════════════════
def page_dice2p():
    st.markdown("<h1 style='text-align:center'>🎲 קוביות — 2 שחקנים</h1><p style='text-align:center;color:#6677aa'>ראשון ל-100 נקודות מנצח! תורות</p>",unsafe_allow_html=True)
    if "dc2" not in st.session_state:
        st.session_state.update({"dc2":{"scores":[0,0],"turn":0,"current":0,"dice":None,"over":False}})
    g=st.session_state["dc2"]; sc=g["scores"]; turn=g["turn"]; cur=g["current"]; over=g["over"]

    DICE_FACES=["","⚀","⚁","⚂","⚃","⚄","⚅"]

    c1,c2,c3=st.columns(3)
    with c1: st.metric("🟦 שחקן 1",sc[0])
    with c2: st.metric("🟥 שחקן 2",sc[1])
    with c3: st.metric("🎯 צבור",cur)

    if over:
        winner=sc.index(max(sc))+1
        e=earn(60); xp(30)
        st.markdown(f"<div class='ok' style='font-size:18px;padding:16px'>🏆 שחקן {winner} ניצח! +{e} 💰</div>",unsafe_allow_html=True)
        _,mc,_=st.columns([1,2,1])
        with mc:
            st.markdown('<div class="btnG">',unsafe_allow_html=True)
            if st.button("🔄 משחק חדש",use_container_width=True,key="dc2n"):
                st.session_state["dc2"]={"scores":[0,0],"turn":0,"current":0,"dice":None,"over":False}; st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)
        return

    col_clr=["#00f5ff","#ff006e"]
    st.markdown(f"<div class='inf' style='font-size:16px;padding:12px'>תור: <b style='color:{col_clr[turn]}'>שחקן {turn+1}</b> | צבור: {cur}</div>",unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)

    if g["dice"]: st.markdown(f"<div style='text-align:center;font-size:64px'>{DICE_FACES[g['dice']]}</div>",unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)

    c1,c2,_=st.columns([1,1,1])
    with c1:
        st.markdown(f'<div style="color:{col_clr[turn]}">',unsafe_allow_html=True)
        if st.button("🎲 הטל",use_container_width=True,key="dc2roll"):
            d=random.randint(1,6); g["dice"]=d
            if d==1:
                st.session_state["dc2"]=dict(g,current=0,turn=1-turn,dice=d)
            else:
                new_cur=cur+d
                if sc[turn]+new_cur>=100:
                    sc[turn]+=new_cur; st.session_state["dc2"]=dict(g,scores=sc,current=0,dice=d,over=True)
                else:
                    st.session_state["dc2"]=dict(g,current=new_cur,dice=d)
            st.rerun()
        st.markdown('</div>',unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="btng">',unsafe_allow_html=True)
        if st.button("✋ שמור",use_container_width=True,key="dc2hold",disabled=cur==0):
            sc[turn]+=cur; st.session_state["dc2"]=dict(g,scores=sc,current=0,turn=1-turn,dice=None)
            st.rerun()
        st.markdown('</div>',unsafe_allow_html=True)

    # Progress bars
    for i in range(2):
        st.markdown(f"<div style='font-size:11px;color:{col_clr[i]};margin:6px 0 2px'>שחקן {i+1}: {sc[i]}/100</div>",unsafe_allow_html=True)
        st.progress(min(sc[i]/100,1.0))

# ═══════════════════════════════════════════════════════════════
#  MINESWEEPER 2P
# ═══════════════════════════════════════════════════════════════
def page_ms2p():
    st.markdown("<h1 style='text-align:center'>💣 מוקשים — 2 שחקנים</h1><p style='text-align:center;color:#6677aa'>תורות — מי שמגלה יותר תאים בטוחים מנצח!</p>",unsafe_allow_html=True)
    if "ms2_b" not in st.session_state:
        _ms2_init()
    b=st.session_state["ms2_b"]; rev=st.session_state["ms2_rev"]
    turn=S("ms2_turn",0); scores=list(S("ms2_scores",[0,0])); over=S("ms2_over",False)
    rows=8; cols_n=8; mines=12
    col_clr=["#00f5ff","#ff006e"]
    c1,c2,c3=st.columns(3)
    with c1: st.metric("🟦 שחקן 1",scores[0])
    with c2: st.metric("🟥 שחקן 2",scores[1])
    with c3: st.metric("💣 נותרו",mines-sum(1 for i in rev if b[i//cols_n][i%cols_n]==-1))
    if not over:
        st.markdown(f"<div class='inf' style='font-size:15px'>תור: <b style='color:{col_clr[turn]}'>שחקן {turn+1}</b></div>",unsafe_allow_html=True)
    else:
        winner=scores.index(max(scores))+1 if scores[0]!=scores[1] else 0
        msg=f"🏆 שחקן {winner} ניצח!" if winner else "🤝 תיקו!"
        st.markdown(f"<div class='ok' style='font-size:17px;padding:14px'>{msg}</div>",unsafe_allow_html=True)
        e=earn(50); 
        _,mc,_=st.columns([1,2,1])
        with mc:
            st.markdown('<div class="btnG">',unsafe_allow_html=True)
            if st.button("🔄 חדש",use_container_width=True,key="ms2new"): _ms2_init(); st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)
        return

    COLORS={0:"#6677aa",1:"#00f5ff",2:"#39ff14",3:"#ff006e",4:"#bf5fff",5:"#ff7c00",6:"#ffd60a",7:"#fff",8:"#8888aa"}
    _,mc,_=st.columns([1,5,1])
    with mc:
        for r in range(rows):
            rc=st.columns(cols_n)
            for c in range(cols_n):
                idx=r*cols_n+c; cell=b[r][c]
                with rc[c]:
                    if idx in rev:
                        if cell==-1: st.markdown("""<div style="height:36px;background:rgba(255,0,110,.18);border:1px solid rgba(255,0,110,.45);border-radius:5px;display:flex;align-items:center;justify-content:center;font-size:16px">💥</div>""",unsafe_allow_html=True)
                        else:
                            col_c=COLORS.get(cell,"#fff"); txt=str(cell) if cell else ""
                            st.markdown(f"""<div style="height:36px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.07);border-radius:5px;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;color:{col_c}">{txt}</div>""",unsafe_allow_html=True)
                    else:
                        if st.button("?",key=f"ms2_{idx}_{len(rev)}",use_container_width=True):
                            _ms2_click(idx,b,rev,scores,turn,rows,cols_n,mines)

def _ms2_init():
    rows=8; cols_n=8; mines=12
    board=[[0]*cols_n for _ in range(rows)]
    mset=set(random.sample(range(rows*cols_n),mines))
    for p in mset: board[p//cols_n][p%cols_n]=-1
    for r in range(rows):
        for c in range(cols_n):
            if board[r][c]==-1: continue
            board[r][c]=sum(1 for dr in[-1,0,1] for dc in[-1,0,1]
                           if 0<=r+dr<rows and 0<=c+dc<cols_n and board[r+dr][c+dc]==-1)
    st.session_state.update({"ms2_b":board,"ms2_rev":set(),"ms2_turn":0,
                              "ms2_scores":[0,0],"ms2_over":False})

def _ms2_click(idx,b,rev,scores,turn,rows,cols_n,mines):
    if idx in rev: return
    r,c=idx//cols_n,idx%cols_n
    if b[r][c]==-1:
        rev.add(idx); st.session_state["ms2_rev"]=rev
        st.session_state["ms2_turn"]=1-turn  # other player gets point? no, just switch
        total=rows*cols_n-mines
        if len([i for i in rev if b[i//cols_n][i%cols_n]!=-1])>=total:
            st.session_state["ms2_over"]=True
        st.rerun()
    else:
        stack=[idx]
        gained=0
        while stack:
            cur=stack.pop()
            if cur in rev: continue
            rev.add(cur); gained+=1
            cr,cc=cur//cols_n,cur%cols_n
            if b[cr][cc]==0:
                for dr in[-1,0,1]:
                    for dc in[-1,0,1]:
                        ni=(cr+dr)*cols_n+(cc+dc)
                        if 0<=cr+dr<rows and 0<=cc+dc<cols_n and ni not in rev: stack.append(ni)
        scores[turn]+=gained; st.session_state["ms2_scores"]=scores
        st.session_state["ms2_rev"]=rev; st.session_state["ms2_turn"]=1-turn
        total=rows*cols_n-mines
        if len([i for i in rev if b[i//cols_n][i%cols_n]!=-1])>=total:
            st.session_state["ms2_over"]=True
        st.rerun()

# ═══════════════════════════════════════════════════════════════
#  SHOP
# ═══════════════════════════════════════════════════════════════
def page_shop():
    coins=S("coins",0)
    st.markdown(f"""<div style="text-align:center;margin-bottom:18px">
<h1>🛒 חנות שדרוגים</h1>
<div style="display:inline-flex;align-items:center;gap:9px;padding:9px 20px;
background:rgba(255,214,10,.06);border:1px solid rgba(255,214,10,.28);border-radius:9px;margin-top:5px">
<span style="font-size:22px">💰</span>
<span style="font-family:Orbitron,sans-serif;font-size:22px;font-weight:900;color:#ffd60a;
text-shadow:0 0 10px rgba(255,214,10,.6)">{coins:,}</span>
<span style="color:#6677aa;font-size:12px">מטבעות</span>
</div></div>""",unsafe_allow_html=True)

    by_game={}
    for uid,item in SHOP.items(): by_game.setdefault(item["game"],[]).append((uid,item))
    order=["global","snake","flappy","memory","clicker","slot","ttt","pong"]
    tabs=st.tabs([GAME_LBL.get(g,g) for g in order if g in by_game])
    for ti,(game) in enumerate([g for g in order if g in by_game]):
        with tabs[ti]:
            items=by_game[game]
            cols=st.columns(min(len(items),3))
            for i,(uid,item) in enumerate(items):
                cnt=oc(uid); mx=item["max"]; maxed=cnt>=mx; can=coins>=item["price"] and not maxed
                col_="#39ff14" if maxed else("#ffd60a" if can else "#6677aa")
                bg_="rgba(57,255,20,.06)" if maxed else "rgba(255,255,255,.02)"
                brd_="rgba(57,255,20,.38)" if maxed else("rgba(255,214,10,.3)" if can else "rgba(255,255,255,.05)")
                badge=(f"<span style='position:absolute;top:6px;right:6px;background:rgba(57,255,20,.15);border:1px solid rgba(57,255,20,.45);border-radius:4px;padding:1px 6px;font-size:9px;color:#39ff14;font-weight:700'>MAX</span>") if maxed else \
                      (f"<span style='position:absolute;top:6px;right:6px;background:rgba(255,214,10,.1);border:1px solid rgba(255,214,10,.35);border-radius:4px;padding:1px 6px;font-size:9px;color:#ffd60a;font-weight:700'>{cnt}/{mx}</span>") if cnt else ""
                with cols[i%3]:
                    st.markdown(f"""<div style="background:{bg_};border:1px solid {brd_};border-radius:10px;
padding:14px;text-align:center;margin-bottom:7px;min-height:126px;position:relative;">
{badge}
<div style="font-size:28px;margin-bottom:5px">{item['icon']}</div>
<div style="font-weight:700;font-size:11px;color:{col_};margin-bottom:3px">{item['name']}</div>
<div style="color:#6677aa;font-size:10px;margin-bottom:8px;line-height:1.4">{item['desc']}</div>
<div style="font-family:Orbitron,sans-serif;font-size:13px;font-weight:900;
color:{'#39ff14' if maxed else '#ffd60a'}">{'MAX ✓' if maxed else f'💰 {item["price"]:,}'}</div>
</div>""",unsafe_allow_html=True)
                    if not maxed:
                        st.markdown(f'<div class="{"btng" if can else ""}">',unsafe_allow_html=True)
                        if st.button("🛒 קנה" if can else "🔒",key=f"sh_{uid}_{cnt}",use_container_width=True,disabled=not can):
                            ok,msg=buy(uid)
                            if ok: st.rerun()
                            else: st.markdown(f"<div class='err'>{msg}</div>",unsafe_allow_html=True)
                        st.markdown('</div>',unsafe_allow_html=True)

    owned={k:v for k,v in S("owned",{}).items() if v>0}
    if owned:
        st.markdown("---\n### 🎒 שדרוגים שלי")
        b="".join(f"<span style='display:inline-flex;padding:4px 9px;background:rgba(57,255,20,.06);"
                  f"border:1px solid rgba(57,255,20,.28);border-radius:12px;font-size:10px;"
                  f"font-weight:700;color:#39ff14;margin:2px'>{SHOP[uid]['icon']} {SHOP[uid]['name']}"
                  f"{' x'+str(v) if v>1 else ''}</span>"
                  for uid,v in owned.items() if uid in SHOP)
        st.markdown(f"<div style='display:flex;flex-wrap:wrap;gap:2px'>{b}</div>",unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  SEPARATORS — skip rendering
# ═══════════════════════════════════════════════════════════════
def page_separator():
    st.info("בחר משחק מהתפריט בצד שמאל")

# ═══════════════════════════════════════════════════════════════
#  ROUTER
# ═══════════════════════════════════════════════════════════════
ROUTES={
    "🏠 לובי":             page_lobby,
    "🐍 נחש":              page_snake,
    "🐦 פלאפי":            page_flappy,
    "🧠 זיכרון":           page_memory,
    "❌ איקס-עיגול":       page_ttt,
    "👆 קליקר":            page_clicker,
    "🎰 מכונת מזל":        page_slot,
    "🏓 פונג (1P)":        page_pong,
    "💣 שדה מוקשים":       page_minesweeper,
    "🔢 מספר חשאי":        page_guess,
    "🎯 ירי מטרות":        page_targets,
    "🐍 נחש מילים":        page_word_snake,
    "🏓 פונג (2P)":        page_pong2p,
    "❌ איקס-עיגול (2P)":  page_ttt2p,
    "🎲 קוביות - 2P":      page_dice2p,
    "💣 שדה מוקשים (2P)":  page_ms2p,
    "🛒 חנות":             page_shop,
}

def main():
    css(); init()
    sel=sidebar()
    if sel in("── 1-PLAYER ──","── 2-PLAYER ──","── ── ── ── ──"):
        page_separator(); return
    ROUTES.get(sel, page_lobby)()

if __name__=="__main__":
    main()
