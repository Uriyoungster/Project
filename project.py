"""
🎮 ARCADE GALAXY v4
Run: pip install streamlit && streamlit run arcade_galaxy.py
"""
import streamlit as st
import streamlit.components.v1 as components
import random, time

st.set_page_config(page_title="🎮 Arcade Galaxy", page_icon="🎮",
                   layout="wide", initial_sidebar_state="collapsed")

# ═══════════════════════════════════════════════════════
#  SHOP DATA
# ═══════════════════════════════════════════════════════
SHOP = {
    "snake_life":    {"name":"+1 Extra Life",      "game":"Snake",   "price":200,"max":4,"icon":"💚","desc":"Each purchase adds 1 life"},
    "snake_wall":    {"name":"Wall Pass",           "game":"Snake",   "price":500,"max":1,"icon":"🌀","desc":"Pass through walls"},
    "snake_magnet":  {"name":"Food Magnet",         "game":"Snake",   "price":350,"max":1,"icon":"🧲","desc":"Food is attracted to you"},
    "flappy_shield": {"name":"+1 Shield",           "game":"Flappy",  "price":150,"max":5,"icon":"🛡","desc":"Each purchase adds a shield"},
    "flappy_slow":   {"name":"Slow Pipes",          "game":"Flappy",  "price":300,"max":2,"icon":"🐌","desc":"Pipes move slower"},
    "flappy_gap":    {"name":"Wider Gap",           "game":"Flappy",  "price":300,"max":3,"icon":"🔓","desc":"Each purchase widens the gap"},
    "mem_hint":      {"name":"+2 Hints",            "game":"Memory",  "price": 80,"max":6,"icon":"💡","desc":"Each purchase adds 2 hints"},
    "mem_x2":        {"name":"Double Score",        "game":"Memory",  "price":400,"max":1,"icon":"×2","desc":"2x coins on win"},
    "slot_luck":     {"name":"+Luck",               "game":"Slots",   "price":250,"max":4,"icon":"🍀","desc":"Each purchase boosts luck"},
    "slot_jackpot":  {"name":"Mega Jackpot",        "game":"Slots",   "price":500,"max":2,"icon":"💰","desc":"Double jackpot prize"},
    "slot_refund":   {"name":"Loss Refund",         "game":"Slots",   "price":600,"max":1,"icon":"↩","desc":"10% refund on losses"},
    "click_mul":     {"name":"+1 Click Multiplier", "game":"Clicker", "price":300,"max":3,"icon":"×2","desc":"Each purchase adds x1"},
    "click_time":    {"name":"+3 Seconds",          "game":"Clicker", "price":350,"max":3,"icon":"⏰","desc":"Each purchase adds 3s"},
    "ttt_undo":      {"name":"+1 Undo Move",        "game":"XO",      "price":150,"max":3,"icon":"↩","desc":"Each purchase adds 1 undo"},
    "pong_speed":    {"name":"Faster Ball",         "game":"Pong",    "price":200,"max":3,"icon":"⚡","desc":"Ball moves faster"},
    "coin_boost":    {"name":"Coin Boost",          "game":"Global",  "price":600,"max":4,"icon":"💫","desc":"Each purchase: +15% coins"},
    "xp_boost":      {"name":"XP Boost",            "game":"Global",  "price":500,"max":4,"icon":"⭐","desc":"Each purchase: +20% XP"},
    "daily_up":      {"name":"Daily Bonus+",        "game":"Global",  "price":400,"max":5,"icon":"📅","desc":"Each purchase: +25 daily"},
}

# ═══════════════════════════════════════════════════════
#  STATE
# ═══════════════════════════════════════════════════════
def init():
    D = {"coins":150,"level":1,"xp":0,"ach":[],"owned":{},
         "page":"lobby",
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
def nav(page): st.session_state["page"]=page

def earn(base):
    mul=1+oc("coin_boost")*0.15
    amt=max(1,int(base*mul))
    st.session_state["coins"]=S("coins",0)+amt
    return amt

def give_xp(base):
    mul=1+oc("xp_boost")*0.20
    amt=max(1,int(base*mul))
    st.session_state["xp"]=S("xp",0)+amt
    lv=S("level",1)
    while S("xp",0)>=lv*120:
        st.session_state["xp"]-=lv*120; lv+=1
        st.session_state["level"]=lv
        if lv in (5,10,20,50): add_ach(f"Level {lv}! ⬆️")

def add_ach(name):
    a=list(S("ach",[]))
    if name not in a: a.append(name); st.session_state["ach"]=a

def buy_item(uid):
    item=SHOP.get(uid)
    if not item: return False,"?"
    cnt=oc(uid)
    if cnt>=item["max"]: return False,"Already maxed!"
    if S("coins",0)<item["price"]: return False,f"Need {item['price']-S('coins',0)} more coins"
    st.session_state["coins"]-=item["price"]
    owned=dict(S("owned",{})); owned[uid]=cnt+1
    st.session_state["owned"]=owned
    return True,f"Bought {item['name']}!"

# ═══════════════════════════════════════════════════════
#  CSS
# ═══════════════════════════════════════════════════════
def inject_css():
    st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Exo+2:wght@400;600;700&display=swap');
:root{--bg:#07071a;--card:#0d0d22;--cyan:#00f5ff;--pink:#ff006e;--gold:#ffd60a;
      --green:#39ff14;--purple:#bf5fff;--orange:#ff7c00;--dim:#6677aa;--fg:#dde0ff;}
html,body,.stApp{background:var(--bg)!important;font-family:'Exo 2',sans-serif!important;color:var(--fg)!important;}
.stApp{background-image:radial-gradient(ellipse at 10% 50%,rgba(0,245,255,.04),transparent 55%),
  radial-gradient(ellipse at 90% 10%,rgba(255,0,110,.03),transparent 55%)!important;}
.main .block-container{padding:0 20px 24px!important;max-width:100%!important;}
section[data-testid="stSidebar"]{display:none!important;}
h1,h2,h3{font-family:Orbitron,sans-serif!important;color:var(--cyan)!important;text-shadow:0 0 16px rgba(0,245,255,.4)!important;}
/* Buttons */
.stButton>button{background:linear-gradient(135deg,rgba(0,245,255,.1),rgba(0,245,255,.03))!important;
  color:var(--cyan)!important;border:1px solid rgba(0,245,255,.3)!important;border-radius:8px!important;
  font-family:'Exo 2',sans-serif!important;font-weight:700!important;transition:all .16s!important;}
.stButton>button:hover{background:rgba(0,245,255,.2)!important;border-color:var(--cyan)!important;
  box-shadow:0 0 18px rgba(0,245,255,.25)!important;transform:translateY(-1px)!important;}
.stButton>button:active{transform:translateY(0)!important;}
.stButton>button:disabled{opacity:.3!important;transform:none!important;}
/* Colour variants */
.bg .stButton>button{background:rgba(255,214,10,.12)!important;color:var(--gold)!important;border-color:rgba(255,214,10,.4)!important;}
.bg .stButton>button:hover{box-shadow:0 0 18px rgba(255,214,10,.3)!important;}
.br .stButton>button{background:rgba(255,0,110,.12)!important;color:var(--pink)!important;border-color:rgba(255,0,110,.4)!important;}
.br .stButton>button:hover{box-shadow:0 0 18px rgba(255,0,110,.3)!important;}
.bG .stButton>button{background:rgba(57,255,20,.1)!important;color:var(--green)!important;border-color:rgba(57,255,20,.38)!important;}
.bG .stButton>button:hover{box-shadow:0 0 18px rgba(57,255,20,.25)!important;}
.bp .stButton>button{background:rgba(191,95,255,.1)!important;color:var(--purple)!important;border-color:rgba(191,95,255,.38)!important;}
/* Metrics */
[data-testid="metric-container"]{background:var(--card)!important;border:1px solid rgba(0,245,255,.16)!important;border-radius:9px!important;padding:10px!important;}
[data-testid="metric-container"] label{color:var(--dim)!important;font-size:11px!important;}
[data-testid="metric-container"] [data-testid="stMetricValue"]{color:var(--cyan)!important;font-family:Orbitron,sans-serif!important;font-size:20px!important;}
/* Alerts */
.ok{padding:10px 14px;background:rgba(57,255,20,.07);border:1px solid rgba(57,255,20,.35);border-radius:9px;color:var(--green);font-weight:600;text-align:center;}
.err{padding:10px 14px;background:rgba(255,0,110,.07);border:1px solid rgba(255,0,110,.35);border-radius:9px;color:var(--pink);font-weight:600;text-align:center;}
.inf{padding:10px 14px;background:rgba(0,245,255,.06);border:1px solid rgba(0,245,255,.25);border-radius:9px;color:var(--cyan);text-align:center;}
.warn{padding:10px 14px;background:rgba(255,214,10,.06);border:1px solid rgba(255,214,10,.3);border-radius:9px;color:var(--gold);text-align:center;}
/* Progress */
.stProgress>div>div>div{background:linear-gradient(90deg,var(--cyan),var(--purple))!important;border-radius:3px!important;}
.stProgress>div>div{background:rgba(255,255,255,.05)!important;border-radius:3px!important;}
/* Misc */
hr{border-color:rgba(0,245,255,.08)!important;}
::-webkit-scrollbar{width:4px;}::-webkit-scrollbar-track{background:var(--bg);}::-webkit-scrollbar-thumb{background:rgba(0,245,255,.2);border-radius:2px;}
#MainMenu,footer,.stDeployButton{display:none!important;}
header[data-testid="stHeader"]{display:none!important;}
.stTabs [data-baseweb="tab-list"]{background:rgba(255,255,255,.02)!important;border-radius:7px!important;}
.stTabs [data-baseweb="tab"]{font-family:'Exo 2',sans-serif!important;font-weight:700!important;color:var(--dim)!important;}
.stTabs [aria-selected="true"]{background:rgba(0,245,255,.1)!important;color:var(--cyan)!important;}
[data-testid="column"]{padding:0 5px!important;}
/* Memory / TTT fixed-size cells */
.cell-btn button{height:72px!important;min-height:72px!important;max-height:72px!important;
  font-size:28px!important;font-weight:900!important;border-radius:10px!important;
  width:100%!important;padding:0!important;}
</style>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
#  TOP NAV BAR
# ═══════════════════════════════════════════════════════
def top_nav():
    lv=S("level",1); coins=S("coins",0); xpv=S("xp",0); need=lv*120
    st.markdown(f"""
<div style="display:flex;align-items:center;justify-content:space-between;
  padding:10px 20px;background:rgba(0,0,0,.55);border-bottom:1px solid rgba(0,245,255,.12);
  backdrop-filter:blur(12px);position:sticky;top:0;z-index:999;margin-bottom:16px">
  <div id="logo-btn" style="display:flex;align-items:center;gap:10px;cursor:pointer"
    onclick="window.parent.postMessage({{type:'nav',page:'lobby'}},'*')">
    <div style="font-size:32px;filter:drop-shadow(0 0 10px rgba(0,245,255,.9));
      animation:gp 2.5s ease-in-out infinite">🎮</div>
    <div style="font-family:Orbitron,sans-serif;font-size:18px;font-weight:900;color:#00f5ff;
      text-shadow:0 0 14px rgba(0,245,255,.75);letter-spacing:3px;line-height:1">ARCADE<br>
      <span style="font-size:10px;letter-spacing:5px;opacity:.7">GALAXY</span></div>
  </div>
  <div style="display:flex;align-items:center;gap:10px">
    <div style="background:rgba(255,214,10,.08);border:1px solid rgba(255,214,10,.3);
      border-radius:8px;padding:6px 14px;display:flex;align-items:center;gap:7px">
      <span style="font-size:16px">💰</span>
      <span style="font-family:Orbitron,sans-serif;font-size:16px;font-weight:900;color:#ffd60a;
        text-shadow:0 0 8px rgba(255,214,10,.6)">{coins:,}</span>
    </div>
    <div style="background:rgba(0,245,255,.06);border:1px solid rgba(0,245,255,.2);
      border-radius:8px;padding:6px 14px;font-size:12px;color:#00f5ff;font-weight:700">
      Lv {lv} &nbsp;
      <span style="color:#6677aa;font-size:10px">XP {xpv}/{need}</span>
    </div>
  </div>
</div>
<style>
@keyframes gp{{0%,100%{{filter:drop-shadow(0 0 10px rgba(0,245,255,.9))}}50%{{filter:drop-shadow(0 0 20px rgba(0,245,255,1))}}}}
</style>""", unsafe_allow_html=True)

    # Lobby + Shop buttons (small, top right area)
    c1,c2,c3=st.columns([1,1,8])
    with c1:
        st.markdown('<div class="bG">', unsafe_allow_html=True)
        if st.button("🏠 Lobby", use_container_width=True, key="nav_lobby"):
            nav("lobby"); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="bg">', unsafe_allow_html=True)
        if st.button("🛒 Shop", use_container_width=True, key="nav_shop"):
            nav("shop"); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
#  LOBBY
# ═══════════════════════════════════════════════════════
GAME_CARDS = [
    # (key, icon, name, color, desc, hi_key, cat)
    ("snake",     "🐍","Snake",         "#39ff14","Control the snake, eat food!",       "snake_hi",   "1P"),
    ("flappy",    "🐦","Flappy Bird",   "#ffd60a","Fly between pipes!",                 "flappy_hi",  "1P"),
    ("memory",    "🧠","Memory",        "#bf5fff","Find all matching pairs!",            "mem_hi",     "1P"),
    ("ttt",       "❌","Tic-Tac-Toe",  "#00f5ff","Beat the AI!",                        "ttt_w",      "1P"),
    ("clicker",   "👆","Clicker",       "#ff006e","Click as fast as you can!",          "click_hi",   "1P"),
    ("slots",     "🎰","Slot Machine",  "#ff7c00","Spin to win the jackpot!",            "slot_w",     "1P"),
    ("pong",      "🏓","Pong (1P)",     "#00f5ff","Beat the AI paddle!",                "pong_hi",    "1P"),
    ("minesweeper","💣","Minesweeper",  "#ff006e","Find all safe cells!",               None,         "1P"),
    ("guess",     "🔢","Number Guess",  "#39ff14","Guess the secret number!",           None,         "1P"),
    ("targets",   "🎯","Target Shot",   "#ffd60a","Hit targets before they vanish!",    None,         "1P"),
    ("wordgame",  "🔤","Word Guess",    "#bf5fff","Guess the 5-letter word!",           None,         "1P"),
    ("pong2p",    "🏓","Pong (2P)",     "#00f5ff","Two players, one keyboard",          None,         "2P"),
    ("ttt2p",     "❌","Tic-Tac-Toe 2P","#bf5fff","Two players on same screen",        None,         "2P"),
    ("dice2p",    "🎲","Dice Race 2P",  "#ffd60a","First to 100 wins!",                None,         "2P"),
    ("ms2p",      "💣","Minesweeper 2P","#ff006e","Take turns uncovering cells!",      None,         "2P"),
]

def page_lobby():
    st.markdown("""<div style="text-align:center;padding:10px 0 24px">
<div style="font-size:58px;animation:fl 3s ease-in-out infinite;display:inline-block">🎮</div>
<h1 style="font-family:Orbitron,sans-serif;font-size:32px;font-weight:900;margin:8px 0 4px;
  background:linear-gradient(90deg,#00f5ff,#bf5fff,#ff006e,#00f5ff);background-size:300%;
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:sh 4s linear infinite">
ARCADE GALAXY</h1>
<p style="color:#6677aa;letter-spacing:3px;font-size:13px">15 Games • 2-Player • Upgrades Shop</p>
</div>
<style>
@keyframes fl{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
@keyframes sh{0%{background-position:0%}100%{background-position:300%}}
</style>""", unsafe_allow_html=True)

    lv=S("level",1); xpv=S("xp",0); need=lv*120
    c1,c2,c3,c4=st.columns(4)
    with c1: st.metric("💎 Level",lv)
    with c2: st.metric("💰 Coins",f"{S('coins',0):,}")
    with c3: st.metric("🏆 Achievements",len(S("ach",[])))
    with c4:
        total=sum(S(k,0) for k in["snake_pl","flappy_pl","mem_pl","ttt_pl","click_ses","slot_sp","pong_pl"])
        st.metric("🎮 Games Played",total)
    st.markdown(f"<div style='text-align:right;font-size:10px;color:#6677aa;margin:3px 0'>XP {xpv}/{need}</div>",unsafe_allow_html=True)
    st.progress(min(xpv/need,1.0))
    st.markdown("<br>",unsafe_allow_html=True)

    # 1P games
    st.markdown("<h3 style='font-size:15px;letter-spacing:2px;margin-bottom:12px'>🕹️ SINGLE PLAYER</h3>",unsafe_allow_html=True)
    cols=st.columns(4)
    sp_games=[g for g in GAME_CARDS if g[6]=="1P"]
    for i,g in enumerate(sp_games):
        key,ico,name,col,desc,hi_key,_=g
        hi_val=S(hi_key,0) if hi_key else ""
        with cols[i%4]:
            best_str=f"Best: {hi_val}" if hi_val else ""
            # Clickable card button
            st.markdown(f"""<div style="background:var(--card);border:1px solid {col}28;border-radius:12px;
  text-align:center;padding:16px 10px;margin-bottom:4px;
  background:linear-gradient(135deg,{col}07,var(--card))">
  <div style="font-size:38px;margin-bottom:6px">{ico}</div>
  <div style="font-family:Orbitron,sans-serif;font-size:11px;color:{col};margin-bottom:4px;text-shadow:0 0 10px {col}60">{name}</div>
  <div style="color:#6677aa;font-size:10px;margin-bottom:8px">{desc}</div>
  <div style="font-size:10px;color:{col}88">{best_str}</div>
</div>""", unsafe_allow_html=True)
            if st.button(f"▶ Play", key=f"lobby_{key}", use_container_width=True):
                nav(key); st.rerun()

    st.markdown("<br>",unsafe_allow_html=True)
    st.markdown("<h3 style='font-size:15px;letter-spacing:2px;margin-bottom:12px'>👥 TWO PLAYERS</h3>",unsafe_allow_html=True)
    mp_games=[g for g in GAME_CARDS if g[6]=="2P"]
    cols2=st.columns(4)
    for i,g in enumerate(mp_games):
        key,ico,name,col,desc,_,__=g
        with cols2[i%4]:
            st.markdown(f"""<div style="background:var(--card);border:1px solid {col}28;border-radius:12px;
  text-align:center;padding:16px 10px;margin-bottom:4px;
  background:linear-gradient(135deg,{col}07,var(--card))">
  <div style="font-size:38px;margin-bottom:6px">{ico}</div>
  <div style="font-family:Orbitron,sans-serif;font-size:11px;color:{col};margin-bottom:4px">{name}</div>
  <div style="color:#6677aa;font-size:10px;margin-bottom:8px">{desc}</div>
  <div style="font-size:10px;color:{col}70">👥 Local 2P</div>
</div>""", unsafe_allow_html=True)
            if st.button(f"▶ Play", key=f"lobby_{key}", use_container_width=True):
                nav(key); st.rerun()

    # Daily bonus
    now=int(time.time()); last=S("daily_last",0)
    if now-last>86400:
        base=50+oc("daily_up")*25
        st.markdown("<hr>",unsafe_allow_html=True)
        st.markdown(f"<div class='warn'>🎁 Daily bonus available! Claim {base} coins</div>",unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
        _,mc,_=st.columns([1,2,1])
        with mc:
            st.markdown('<div class="bg">',unsafe_allow_html=True)
            if st.button(f"🎁 Claim {base} Coins", use_container_width=True, key="daily"):
                earn(base); give_xp(15); st.session_state["daily_last"]=now
                add_ach("🎁 Daily Bonus!"); st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)

    achs=S("ach",[])
    if achs:
        st.markdown("<hr>",unsafe_allow_html=True)
        st.markdown("<h3 style='font-size:14px'>🏆 Achievements</h3>",unsafe_allow_html=True)
        b="".join(f"<span style='display:inline-flex;padding:4px 10px;background:rgba(255,214,10,.07);"
                  f"border:1px solid rgba(255,214,10,.28);border-radius:14px;font-size:11px;"
                  f"font-weight:700;color:#ffd60a;margin:2px'>{a}</span>" for a in achs[-15:])
        st.markdown(f"<div style='display:flex;flex-wrap:wrap;gap:2px'>{b}</div>",unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
#  SNAKE
# ═══════════════════════════════════════════════════════
def page_snake():
    st.markdown("<h1 style='text-align:center'>🐍 Snake</h1><p style='text-align:center;color:#6677aa'>Arrow keys or WASD to move</p>",unsafe_allow_html=True)
    lives=1+oc("snake_life"); wp="true" if has("snake_wall") else "false"
    mag="true" if has("snake_magnet") else "false"; hi=S("snake_hi",0)
    ups=[]
    if lives>1: ups.append(f"💚 {lives} lives")
    if has("snake_wall"): ups.append("🌀 Wall pass")
    if has("snake_magnet"): ups.append("🧲 Magnet")
    if ups: st.markdown(f"<div class='inf'>{'  |  '.join(ups)}</div>",unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    _,col,_=st.columns([1,10,1])
    with col:
        components.html(f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#06060e;display:flex;flex-direction:column;align-items:center;padding:6px;user-select:none;font-family:'Orbitron',monospace}}
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');
.hud{{display:flex;gap:8px;margin-bottom:6px;font-size:12px;flex-wrap:wrap;justify-content:center}}
.h{{background:rgba(0,245,255,.08);border:1px solid rgba(0,245,255,.24);border-radius:6px;padding:3px 9px;color:#00f5ff}}
canvas{{border:2px solid rgba(0,245,255,.28);border-radius:10px;box-shadow:0 0 22px rgba(0,245,255,.09);display:block}}
.ov{{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);background:rgba(4,4,18,.95);
  border:2px solid #00f5ff;border-radius:11px;padding:18px 26px;text-align:center;min-width:170px}}
.ov h2{{color:#00f5ff;font-size:17px;margin-bottom:7px}}.ov p{{color:#8888aa;font-size:11px;margin-bottom:11px}}
.ov button{{background:rgba(0,245,255,.16);color:#00f5ff;border:1px solid #00f5ff;padding:7px 18px;
  border-radius:6px;cursor:pointer;font-family:Orbitron;font-size:12px;font-weight:700}}
.ov button:hover{{background:rgba(0,245,255,.32)}}
.wrap{{position:relative}}</style></head><body>
<div class="hud">
  <div class="h">Score: <span id="sc">0</span></div>
  <div class="h">Best: <span id="hi">{hi}</span></div>
  <div class="h">Lives: <span id="lv">{lives}</span></div>
  <div class="h">Speed: <span id="sp">1</span></div>
</div>
<div class="wrap"><canvas id="c"></canvas>
<div class="ov" id="ov"><h2>🐍 Snake</h2><p>Arrow keys or WASD</p>
<button onclick="startGame()">▶ Play</button></div></div>
<script>
const G=20,C=20;
const WP={wp},MAG={mag},ML={lives};
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
cv.width=cv.height=G*C;
let sn,dir,nd,food,bon,score,lv2,spd,loop,run,parts;
function startGame(){{
  document.getElementById('ov').style.display='none';
  sn=[{{x:10,y:10}},{{x:9,y:10}},{{x:8,y:10}}];dir={{x:1,y:0}};nd={{x:1,y:0}};
  score=0;lv2=ML;spd=1;parts=[];bon=null;run=true;
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
  if(MAG){{let dx=food.x-h.x,dy=food.y-h.y;if(Math.abs(dx)+Math.abs(dy)<=4){{if(dx)food.x+=dx>0?-1:1;else if(dy)food.y+=dy>0?-1:1;}}}}
  sn.unshift(h);let grew=false;
  if(h.x===food.x&&h.y===food.y){{score+=10;grew=true;spark(food.x,food.y,'#39ff14');placeFood();
    document.getElementById('sc').textContent=score;
    let ns=1+Math.floor(score/50);if(ns>spd){{spd=ns;clearInterval(loop);loop=setInterval(update,Math.max(65,155-spd*20));document.getElementById('sp').textContent=spd;}}}}
  if(bon&&h.x===bon.x&&h.y===bon.y){{score+=50;grew=true;spark(bon.x,bon.y,'#ffd60a');bon=null;document.getElementById('sc').textContent=score;}}
  if(!grew)sn.pop();if(bon){{bon.t--;if(!bon.t)bon=null;}}
  parts=parts.filter(p=>p.l>0);parts.forEach(p=>{{p.x+=p.vx;p.y+=p.vy;p.l--;}});draw();
}}
function die(){{
  lv2--;document.getElementById('lv').textContent=lv2;
  if(lv2<=0){{run=false;clearInterval(loop);
    let hs=+document.getElementById('hi').textContent||0;
    if(score>hs)document.getElementById('hi').textContent=score;
    document.getElementById('ov').querySelector('h2').textContent='💀 Game Over!';
    document.getElementById('ov').querySelector('p').textContent='Score: '+score;
    document.getElementById('ov').style.display='block';
  }}else{{sn=[{{x:10,y:10}},{{x:9,y:10}},{{x:8,y:10}}];dir={{x:1,y:0}};nd={{x:1,y:0}};}}
}}
function rr(x,y,w,h,r){{ctx.beginPath();ctx.moveTo(x+r,y);ctx.lineTo(x+w-r,y);ctx.quadraticCurveTo(x+w,y,x+w,y+r);ctx.lineTo(x+w,y+h-r);ctx.quadraticCurveTo(x+w,y+h,x+w-r,y+h);ctx.lineTo(x+r,y+h);ctx.quadraticCurveTo(x,y+h,x,y+h-r);ctx.lineTo(x,y+r);ctx.quadraticCurveTo(x,y,x+r,y);ctx.closePath();}}
function draw(){{
  ctx.fillStyle='#06060e';ctx.fillRect(0,0,G*C,G*C);
  ctx.strokeStyle='rgba(0,245,255,.03)';ctx.lineWidth=.5;
  for(let i=0;i<=G;i++){{ctx.beginPath();ctx.moveTo(i*C,0);ctx.lineTo(i*C,G*C);ctx.stroke();ctx.beginPath();ctx.moveTo(0,i*C);ctx.lineTo(G*C,i*C);ctx.stroke();}}
  parts.forEach(p=>{{ctx.globalAlpha=p.l/25;ctx.fillStyle=p.c;ctx.beginPath();ctx.arc(p.x,p.y,2.5,0,Math.PI*2);ctx.fill();}});ctx.globalAlpha=1;
  let t=Date.now()/320;ctx.save();ctx.translate(food.x*C+C/2,food.y*C+C/2);ctx.scale(1+Math.sin(t)*.16,1+Math.sin(t)*.16);
  ctx.shadowBlur=16;ctx.shadowColor='#39ff14';ctx.fillStyle='#39ff14';ctx.beginPath();ctx.arc(0,0,C/2-2,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;ctx.restore();
  if(bon){{ctx.save();ctx.translate(bon.x*C+C/2,bon.y*C+C/2);ctx.scale(1+Math.sin(Date.now()/130)*.2,1+Math.sin(Date.now()/130)*.2);ctx.shadowBlur=20;ctx.shadowColor='#ffd60a';ctx.fillStyle='#ffd60a';ctx.font=(C-2)+'px serif';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('★',0,0);ctx.restore();ctx.fillStyle='rgba(255,214,10,'+bon.t/100+')';ctx.fillRect(bon.x*C,bon.y*C-3,C*(bon.t/100),2);}}
  sn.forEach((seg,i)=>{{ctx.save();if(!i){{ctx.shadowBlur=13;ctx.shadowColor='rgba(0,245,255,.75)';}}ctx.fillStyle=i?`rgba(0,${{Math.round(215-i/sn.length*80)}},255,.88)`:'#fff';let pd=i?2:1,rd=i?3:5;rr(seg.x*C+pd,seg.y*C+pd,C-pd*2,C-pd*2,rd);ctx.fill();ctx.restore();if(!i){{ctx.fillStyle='#06060e';ctx.beginPath();ctx.arc(seg.x*C+C*.3+dir.y*C*.18,seg.y*C+C*.3-dir.x*C*.18,2,0,Math.PI*2);ctx.fill();ctx.beginPath();ctx.arc(seg.x*C+C*.7-dir.y*C*.18,seg.y*C+C*.3-dir.x*C*.18,2,0,Math.PI*2);ctx.fill();}}}});
}}
ctx.fillStyle='#06060e';ctx.fillRect(0,0,G*C,G*C);
</script></body></html>""", height=G*C+86, scrolling=False)

    st.markdown("<br>",unsafe_allow_html=True)
    _,c2,_=st.columns([1,2,1])
    with c2:
        st.markdown('<div class="bG">',unsafe_allow_html=True)
        if st.button("▶ New Game", use_container_width=True, key="sn_new"):
            st.session_state["snake_pl"]=S("snake_pl",0)+1; earn(5); give_xp(5)
            st.toast("🐍 Good luck!")
        st.markdown('</div>',unsafe_allow_html=True)
    st.markdown("---",unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1: st.metric("🏆 Best",S("snake_hi",0))
    with c2: st.metric("🎮 Games",S("snake_pl",0))

# ═══════════════════════════════════════════════════════
#  FLAPPY
# ═══════════════════════════════════════════════════════
def page_flappy():
    st.markdown("<h1 style='text-align:center'>🐦 Flappy Bird</h1><p style='text-align:center;color:#6677aa'>SPACE or click to flap</p>",unsafe_allow_html=True)
    sh=oc("flappy_shield"); gap=110+oc("flappy_gap")*15
    slow_pipes = "true" if has("flappy_slow") else "false"
    hi=S("flappy_hi",0)
    if sh or has("flappy_slow"):
        gap_count = oc("flappy_gap")
        flappy_parts = filter(None, [
            f'🛡 {sh} shields' if sh else '',
            '🐌 Slow pipes' if has('flappy_slow') else '',
            f'🔓 Gap +{gap_count * 15}' if has('flappy_gap') else '',
        ])
        st.markdown(f"<div class='inf'>{'  |  '.join(flappy_parts)}</div>", unsafe_allow_html=True)
    _,col,_=st.columns([1,8,1])
    with col:
        components.html(f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>*{{margin:0;padding:0;box-sizing:border-box}}body{{background:#050510;display:flex;flex-direction:column;align-items:center;padding:6px;user-select:none;font-family:'Orbitron',monospace}}@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');.hud{{display:flex;gap:8px;margin-bottom:6px;font-size:12px}}.h{{background:rgba(255,214,10,.08);border:1px solid rgba(255,214,10,.24);border-radius:6px;padding:3px 9px;color:#ffd60a}}canvas{{border:2px solid rgba(255,214,10,.28);border-radius:10px;box-shadow:0 0 22px rgba(255,214,10,.09);cursor:pointer;display:block}}.ov{{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);background:rgba(4,4,18,.95);border:2px solid #ffd60a;border-radius:11px;padding:18px 24px;text-align:center;min-width:165px}}.ov h2{{color:#ffd60a;font-size:16px;margin-bottom:7px}}.ov p{{color:#8888aa;font-size:11px;margin-bottom:11px}}.ov button{{background:rgba(255,214,10,.16);color:#ffd60a;border:1px solid #ffd60a;padding:7px 18px;border-radius:6px;cursor:pointer;font-family:Orbitron;font-size:11px;font-weight:700}}.wrap{{position:relative}}</style></head><body>
<div class="hud"><div class="h">Score: <span id="sc">0</span></div><div class="h">Best: <span id="hi">{hi}</span></div><div class="h">🛡 <span id="sh">{sh}</span></div></div>
<div class="wrap"><canvas id="c" width="320" height="440"></canvas><div class="ov" id="ov"><h2 id="ot">🐦 Flappy Bird</h2><p>SPACE or click to flap</p><button onclick="startGame()">▶ Play</button></div></div>
<script>
const W=320,H=440,BR=12,PS={1.7 if has("flappy_slow") else 2.4},GAP={gap},ISH={sh};
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
let bird,pipes,score,frame,run,raf,shL,parts,stars;
function mkSt(){{stars=[];for(let i=0;i<50;i++)stars.push({{x:Math.random()*W,y:Math.random()*H*.76,r:Math.random()*1.3+.4,s:Math.random()*.25+.07}});}}
function startGame(){{document.getElementById('ov').style.display='none';bird={{x:70,y:H/2,vy:0,rot:0}};pipes=[];score=0;frame=0;run=true;shL=ISH;parts=[];document.getElementById('sc').textContent='0';document.getElementById('sh').textContent=shL;if(raf)cancelAnimationFrame(raf);mkSt();loop();}}
function flap(){{if(run)bird.vy=-6.8;}}
cv.addEventListener('click',flap);document.addEventListener('keydown',e=>{{if(e.code==='Space'){{flap();e.preventDefault();}}}});
function loop(){{if(!run)return;update();draw();raf=requestAnimationFrame(loop);}}
function update(){{frame++;bird.vy+=.33;bird.y+=bird.vy;bird.rot=Math.min(Math.max(bird.vy*3,-30),90);parts=parts.filter(p=>p.l>0);parts.forEach(p=>{{p.x+=p.vx;p.y+=p.vy;p.l--;p.vy+=.1;}});stars.forEach(s=>{{s.x-=s.s;if(s.x<0)s.x=W;}});if(frame%80===0){{pipes.push({{x:W,th:50+Math.random()*(H-GAP-100),ok:false}});}}pipes.forEach(p=>p.x-=PS);pipes=pipes.filter(p=>p.x>-65);pipes.forEach(p=>{{if(!p.ok&&p.x+40<bird.x){{p.ok=true;score++;document.getElementById('sc').textContent=score;for(let i=0;i<6;i++)parts.push({{x:bird.x,y:bird.y,vx:(Math.random()-.5)*4,vy:-Math.random()*3.5,l:22,c:'#ffd60a'}});}}if(bird.x+BR>p.x&&bird.x-BR<p.x+45&&(bird.y-BR<p.th||bird.y+BR>p.th+GAP)){{if(shL>0){{shL--;document.getElementById('sh').textContent=shL;for(let i=0;i<12;i++)parts.push({{x:bird.x,y:bird.y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,l:26,c:'#00f5ff'}});}}else die();}}}});if(bird.y+BR>H-26||bird.y-BR<0)die();}}
function die(){{run=false;cancelAnimationFrame(raf);let hs=+document.getElementById('hi').textContent||0;if(score>hs)document.getElementById('hi').textContent=score;document.getElementById('ot').textContent='💥 You crashed!';document.getElementById('ov').querySelector('p').textContent='Score: '+score;document.getElementById('ov').style.display='block';}}
function dp(x,th){{let g=ctx.createLinearGradient(x,0,x+45,0);g.addColorStop(0,'#14501a');g.addColorStop(.5,'#228528');g.addColorStop(1,'#14501a');ctx.fillStyle=g;ctx.fillRect(x,0,45,th);ctx.fillStyle='#2a9a2a';ctx.fillRect(x-4,th-16,53,16);let b=th+GAP;ctx.fillStyle=g;ctx.fillRect(x,b,45,H-b);ctx.fillStyle='#2a9a2a';ctx.fillRect(x-4,b,53,16);ctx.shadowBlur=8;ctx.shadowColor='rgba(57,255,20,.28)';ctx.strokeStyle='rgba(57,255,20,.22)';ctx.lineWidth=1;ctx.strokeRect(x,0,45,th);ctx.strokeRect(x,b,45,H-b);ctx.shadowBlur=0;}}
function draw(){{let sky=ctx.createLinearGradient(0,0,0,H);sky.addColorStop(0,'#030310');sky.addColorStop(.7,'#07072a');sky.addColorStop(1,'#0b160b');ctx.fillStyle=sky;ctx.fillRect(0,0,W,H);stars.forEach(s=>{{ctx.globalAlpha=.45+Math.sin(frame*.05+s.x)*.4;ctx.fillStyle='#fff';ctx.beginPath();ctx.arc(s.x,s.y,s.r,0,Math.PI*2);ctx.fill();}});ctx.globalAlpha=1;parts.forEach(p=>{{ctx.globalAlpha=p.l/26;ctx.fillStyle=p.c;ctx.beginPath();ctx.arc(p.x,p.y,2.2,0,Math.PI*2);ctx.fill();}});ctx.globalAlpha=1;pipes.forEach(p=>dp(p.x,p.th));ctx.fillStyle='#14280e';ctx.fillRect(0,H-26,W,26);ctx.fillStyle='#204010';ctx.fillRect(0,H-26,W,7);ctx.save();ctx.translate(bird.x,bird.y);ctx.rotate(bird.rot*Math.PI/180);if(shL>0){{ctx.beginPath();ctx.arc(0,0,BR+7,0,Math.PI*2);ctx.strokeStyle='rgba(0,245,255,'+(0.38+Math.sin(frame*.14)*.26)+')';ctx.lineWidth=2;ctx.stroke();}}ctx.shadowBlur=10;ctx.shadowColor='#ffd60a';ctx.fillStyle='#ffd60a';ctx.beginPath();ctx.ellipse(0,0,BR,BR-2,0,0,Math.PI*2);ctx.fill();ctx.fillStyle='#ff8f00';ctx.beginPath();ctx.ellipse(-3,2,7,4,Math.PI/4+Math.sin(frame*.28)*.4,0,Math.PI*2);ctx.fill();ctx.fillStyle='#fff';ctx.beginPath();ctx.arc(5,-2,3.2,0,Math.PI*2);ctx.fill();ctx.fillStyle='#1a1a3a';ctx.beginPath();ctx.arc(6,-2,2,0,Math.PI*2);ctx.fill();ctx.fillStyle='#ff5500';ctx.beginPath();ctx.moveTo(BR-.5,0);ctx.lineTo(BR+5.5,1.5);ctx.lineTo(BR-.5,-1.5);ctx.fill();ctx.shadowBlur=0;ctx.restore();ctx.fillStyle='rgba(255,214,10,.9)';ctx.font='bold 24px Orbitron,monospace';ctx.textAlign='center';ctx.shadowBlur=13;ctx.shadowColor='#ffd60a';ctx.fillText(score,W/2,44);ctx.shadowBlur=0;}}
mkSt();ctx.fillStyle='#030310';ctx.fillRect(0,0,W,H);
</script></body></html>""", height=490, scrolling=False)

    st.markdown("<br>",unsafe_allow_html=True)
    _,c2,_=st.columns([1,2,1])
    with c2:
        st.markdown('<div class="bg">',unsafe_allow_html=True)
        if st.button("▶ New Game", use_container_width=True, key="fl_new"):
            st.session_state["flappy_pl"]=S("flappy_pl",0)+1; earn(5); give_xp(5)
        st.markdown('</div>',unsafe_allow_html=True)
    st.markdown("---")
    c1,c2=st.columns(2)
    with c1: st.metric("🏆 Best",S("flappy_hi",0))
    with c2: st.metric("🎮 Games",S("flappy_pl",0))

# ═══════════════════════════════════════════════════════
#  MEMORY  — fixed-size grid with flip animation
# ═══════════════════════════════════════════════════════
EMJ=["🐉","🦄","🔥","⚡","💎","🚀","🌊","🎸","🦋","🍄","🎯","🏆","🌈","🎪","🐬","🦁"]

def _mr():
    c=random.sample(range(len(EMJ)),8); b=c*2; random.shuffle(b)
    st.session_state.update({"mb":b,"mf":[],"mm":set(),"mov":0,"mpend":False,"mptime":0,"mh":oc("mem_hint")*2})

def page_memory():
    st.markdown("<h1 style='text-align:center'>🧠 Memory</h1><p style='text-align:center;color:#6677aa'>Find all matching pairs!</p>",unsafe_allow_html=True)
    if has("mem_x2"): st.markdown("<div class='inf'>×2 score active!</div>",unsafe_allow_html=True)
    if "mb" not in st.session_state: _mr()
    b=st.session_state["mb"]; fl=list(st.session_state["mf"]); mm=set(st.session_state["mm"]); mv=S("mov",0); hints=S("mh",0)

    c1,c2,c3,c4=st.columns(4)
    with c1: st.metric("🎯 Moves",mv)
    with c2: st.metric("✅ Pairs",len(mm)//2)
    with c3: st.metric("🃏 Left",8-len(mm)//2)
    with c4: st.metric("💡 Hints",hints)
    st.markdown("<br>",unsafe_allow_html=True)

    if len(mm)==16:
        sc=max(80-mv*2,10)*(2 if has("mem_x2") else 1)
        e=earn(sc); give_xp(sc//2); st.session_state["mem_pl"]=S("mem_pl",0)+1
        if sc>S("mem_hi",0): st.session_state["mem_hi"]=sc; add_ach("🧠 Memory Record!")
        if mv<=10: add_ach("🧠 Golden Brain!")
        st.markdown(f"<div class='ok' style='font-size:17px;padding:18px'>🎉 Done in {mv} moves! +{e} coins</div>",unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
        _,mc,_=st.columns([1,2,1])
        with mc:
            st.markdown('<div class="bG">',unsafe_allow_html=True)
            if st.button("🔄 New Game",use_container_width=True,key="mr"): _mr(); st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)
        return

    # Pending delay: show both flipped cards, then resolve
    if S("mpend") and time.time()-S("mptime",0)>=0.8:
        f2=list(S("mf",[]))
        if len(f2)==2:
            i1,i2=f2
            if b[i1]==b[i2]: mm.add(i1); mm.add(i2); st.session_state["mm"]=mm
        st.session_state["mf"]=[]; st.session_state["mpend"]=False; st.rerun()
    if S("mpend"): time.sleep(0.05); st.rerun()

    can=len(fl)<2 and not S("mpend")

    # Build a single HTML component for the full 4×4 board with CSS flip animation
    board_cells=""
    for idx in range(16):
        is_mm=idx in mm; is_fl=idx in fl
        show=is_mm or is_fl
        em=EMJ[b[idx]]
        if is_mm:
            front_bg="rgba(57,255,20,.12)"; front_bd="rgba(57,255,20,.5)"
        elif is_fl:
            front_bg="rgba(0,245,255,.1)"; front_bd="rgba(0,245,255,.45)"
        else:
            front_bg="rgba(191,95,255,.08)"; front_bd="rgba(191,95,255,.28)"

        board_cells+=f"""
<div class="cell {'matched' if is_mm else ''}" id="c{idx}" onclick="flip({idx})"
  style="{'pointer-events:none' if (not can and not is_mm and not is_fl) else 'cursor:pointer'}">
  <div class="inner {'flipped' if show else ''}">
    <div class="back" style="background:{front_bg};border:2px solid {front_bd}">{em}</div>
    <div class="front" style="background:rgba(191,95,255,.08);border:2px solid rgba(191,95,255,.28)">?</div>
  </div>
</div>"""

    flipped_js=json_list(fl); matched_js=json_list(list(mm)); can_js="true" if can else "false"
    components.html(f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:transparent;padding:4px;font-family:sans-serif}}
.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;max-width:420px;margin:0 auto}}
.cell{{position:relative;width:100%;aspect-ratio:1;perspective:600px}}
.inner{{position:absolute;inset:0;transform-style:preserve-3d;transition:transform .45s cubic-bezier(.4,0,.2,1);border-radius:10px}}
.inner.flipped{{transform:rotateY(180deg)}}
.back,.front{{position:absolute;inset:0;border-radius:10px;display:flex;align-items:center;justify-content:center;
  backface-visibility:hidden;-webkit-backface-visibility:hidden;font-size:32px;font-weight:700}}
.back{{transform:rotateY(180deg)}}
.cell.matched .inner{{transform:rotateY(180deg)}}
.cell.matched .back{{background:rgba(57,255,20,.15)!important;border:2px solid rgba(57,255,20,.6)!important;
  box-shadow:0 0 16px rgba(57,255,20,.2);animation:matchpop .4s cubic-bezier(.34,1.56,.64,1)}}
.cell:not(.matched) .front:hover{{background:rgba(191,95,255,.18)!important;border-color:rgba(191,95,255,.6)!important}}
@keyframes matchpop{{from{{transform:rotateY(180deg) scale(.85)}}to{{transform:rotateY(180deg) scale(1)}}}}
</style></head><body>
<div class="grid">{board_cells}</div>
<script>
const CAN={can_js};
const FLIPPED=new Set({flipped_js});
const MATCHED=new Set({matched_js});
function flip(idx){{
  if(!CAN||MATCHED.has(idx)||FLIPPED.has(idx))return;
  window.parent.postMessage({{type:'mem_flip',idx}},'*');
}}
</script></body></html>""", height=450, scrolling=False)

    # Streamlit click handler: listen via a hidden form pattern
    # We use number_input trick: show which index was last flipped via a key
    st.markdown("<br>",unsafe_allow_html=True)
    st.markdown("<p style='color:#6677aa;font-size:11px;text-align:center'>Click a card number below to flip it:</p>",unsafe_allow_html=True)
    available=[i for i in range(16) if i not in mm and i not in fl and can]
    if available:
        row_size=8
        for start in range(0,len(available),row_size):
            chunk=available[start:start+row_size]
            btn_cols=st.columns(len(chunk))
            for j,idx in enumerate(chunk):
                with btn_cols[j]:
                    if st.button(f"{idx+1}", key=f"mc_{idx}_{mv}_{len(mm)}", use_container_width=True):
                        fl.append(idx); st.session_state["mf"]=fl
                        if len(fl)==2:
                            st.session_state["mov"]=mv+1
                            st.session_state["mpend"]=True; st.session_state["mptime"]=time.time()
                        st.rerun()

    # Show currently revealed (so 2nd flipped card is visible)
    if fl or mm:
        vis=[f"Card {i+1}: {EMJ[b[i]]}" for i in sorted(set(fl)|mm)]
        if vis: st.markdown(f"<div class='inf' style='font-size:11px;margin-top:6px'>Visible: {' | '.join(vis[:8])}</div>",unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)
    c1,c2,c3=st.columns(3)
    with c1:
        st.markdown('<div class="br">',unsafe_allow_html=True)
        if st.button("🔄 Reset",use_container_width=True,key="mrst"): _mr(); st.rerun()
        st.markdown('</div>',unsafe_allow_html=True)
    with c2:
        if hints>0:
            st.markdown('<div class="bg">',unsafe_allow_html=True)
            if st.button(f"💡 Hint ({hints})",use_container_width=True,key="mhint"):
                un=[i for i in range(16) if i not in mm and i not in fl]; seen={}
                for i in un:
                    e=b[i]
                    if e in seen:
                        st.session_state["mf"]=[seen[e],i]; st.session_state["mov"]=mv+1
                        st.session_state["mpend"]=True; st.session_state["mptime"]=time.time()
                        st.session_state["mh"]=hints-1; st.rerun(); break
                    seen[e]=i
            st.markdown('</div>',unsafe_allow_html=True)
    with c3: st.metric("🏆 Best",S("mem_hi",0))

def json_list(lst): return "["+",".join(str(x) for x in lst)+"]"

# ═══════════════════════════════════════════════════════
#  TIC-TAC-TOE 1P  — fixed-size cells
# ═══════════════════════════════════════════════════════
def _tw(b):
    for a,bx,c in[(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]:
        if b[a] and b[a]==b[bx]==b[c]: return b[a]
    return None

def _mm3(b,im,d,weak):
    w=_tw(b)
    if w=="O": return 10-d
    if w=="X": return d-10
    emp=[i for i,v in enumerate(b) if not v]
    if not emp: return 0
    if weak>0 and d==0 and random.random()<weak*0.11: return random.choice([-2,0,2])
    if im:
        best=-99
        for i in emp: b[i]="O"; best=max(best,_mm3(b,False,d+1,weak)); b[i]=""
        return best
    else:
        best=99
        for i in emp: b[i]="X"; best=min(best,_mm3(b,True,d+1,weak)); b[i]=""
        return best

def _ai_move(b,weak=0):
    mv=None; best=-99
    for i in[j for j,v in enumerate(b) if not v]:
        b[i]="O"; s=_mm3(b,False,0,weak); b[i]=""
        if s>best: best=s; mv=i
    return mv

def _ttr():
    st.session_state.update({"tb":[""]*9,"to":False,"ts":"","tp":None})

def page_ttt():
    st.markdown("<h1 style='text-align:center'>❌ Tic-Tac-Toe</h1><p style='text-align:center;color:#6677aa'>You are X, AI is O</p>",unsafe_allow_html=True)
    undo=oc("ttt_undo"); weak=oc("ttt_easy")
    if "tb" not in st.session_state: _ttr()
    b=st.session_state["tb"]; ov=S("to"); ts=S("ts",""); prev=S("tp")
    c1,c2,c3,c4=st.columns(4)
    with c1: st.metric("✅ Wins",S("ttt_w",0))
    with c2: st.metric("❌ Losses",S("ttt_l",0))
    with c3: st.metric("🤝 Draws",S("ttt_d",0))
    with c4: st.metric("🎮 Games",S("ttt_pl",0))
    st.markdown("<br>",unsafe_allow_html=True)
    if ts:
        cls="ok" if "Win" in ts else("err" if "Lost" in ts else "inf")
        st.markdown(f"<div class='{cls}' style='font-size:16px;padding:14px'>{ts}</div>",unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)

    _,mc,_=st.columns([1,2,1])
    with mc:
        # Fixed-height cells via CSS
        st.markdown("""<style>
div.ttt-board div[data-testid="column"] .stButton>button{
  height:80px!important;min-height:80px!important;font-size:36px!important;
  font-weight:900!important;border-radius:12px!important;padding:0!important;}
</style>""",unsafe_allow_html=True)
        st.markdown('<div class="ttt-board">',unsafe_allow_html=True)
        for row in range(3):
            rc=st.columns(3)
            for ci in range(3):
                idx=row*3+ci
                with rc[ci]:
                    cell=b[idx]
                    if cell=="X":
                        st.markdown("""<div style="height:80px;background:rgba(0,245,255,.1);border:2px solid rgba(0,245,255,.5);border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:38px;color:#00f5ff;text-shadow:0 0 14px rgba(0,245,255,.8);animation:pp .2s ease">✕</div><style>@keyframes pp{from{transform:scale(.3)}to{transform:scale(1)}}</style>""",unsafe_allow_html=True)
                    elif cell=="O":
                        st.markdown("""<div style="height:80px;background:rgba(255,0,110,.1);border:2px solid rgba(255,0,110,.5);border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:38px;color:#ff006e;text-shadow:0 0 14px rgba(255,0,110,.8)">○</div>""",unsafe_allow_html=True)
                    elif not ov:
                        if st.button(" ",key=f"tt_{idx}_{sum(1 for x in b if x)}",use_container_width=True):
                            st.session_state["tp"]=b[:]
                            b[idx]="X"; w=_tw(b)
                            if w: _tte(w,b); return
                            if ""not in b: _tte("d",b); return
                            ai=_ai_move(b,weak)
                            if ai is not None:
                                b[ai]="O"; w=_tw(b)
                                if w: _tte(w,b); return
                                if ""not in b: _tte("d",b); return
                            st.session_state["tb"]=b; st.rerun()
                    else:
                        st.markdown("""<div style="height:80px;background:rgba(255,255,255,.02);border:2px solid rgba(255,255,255,.05);border-radius:12px"></div>""",unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)
    c1,c2,c3,c4=st.columns(4)
    with c1:
        st.markdown('<div class="bG">',unsafe_allow_html=True)
        if st.button("🔄 New",use_container_width=True,key="ttn"): _ttr(); st.rerun()
        st.markdown('</div>',unsafe_allow_html=True)
    with c2:
        if undo>0 and prev and not ov:
            st.markdown('<div class="bg">',unsafe_allow_html=True)
            if st.button(f"↩ Undo ({undo})",use_container_width=True,key="ttun"):
                st.session_state["tb"]=prev; st.session_state["tp"]=None; st.session_state["ts"]=""; st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)
    with c3: st.selectbox("AI Difficulty",["Normal","Easy","Baby"],key="tts")

def _tte(r,b):
    st.session_state["ttt_pl"]=S("ttt_pl",0)+1; st.session_state["to"]=True; st.session_state["tb"]=b
    if r=="X": st.session_state["ttt_w"]+=1; e=earn(50); give_xp(25); st.session_state["ts"]=f"🎉 You Win! +{e} coins"; add_ach("❌ Beat the AI!")
    elif r=="O": st.session_state["ttt_l"]+=1; e=earn(5); st.session_state["ts"]=f"😔 You Lost... +{e} coins"
    else: st.session_state["ttt_d"]+=1; e=earn(15); give_xp(8); st.session_state["ts"]=f"🤝 Draw! +{e} coins"
    st.rerun()

# ═══════════════════════════════════════════════════════
#  CLICKER
# ═══════════════════════════════════════════════════════
def page_clicker():
    st.markdown("<h1 style='text-align:center'>👆 Clicker</h1>",unsafe_allow_html=True)
    mul=1+oc("click_mul"); dur=10+oc("click_time")*3
    if mul>1 or dur>10: st.markdown(f"<div class='inf'>×{mul} per click  |  {dur}s duration</div>",unsafe_allow_html=True)
    if "cks" not in st.session_state: st.session_state.update({"cks":"idle","ckc":0,"ckt":0})
    state=S("cks"); cnt=S("ckc",0); best=S("click_hi",0)
    if state=="playing":
        el=time.time()-S("ckt",0); rem=max(0,dur-el)
        anim="animation:cf .18s infinite" if rem<3 else ""
        st.markdown(f"""<div style="text-align:center;margin-bottom:10px">
<div style="font-family:Orbitron,sans-serif;font-size:52px;font-weight:900;color:#ff006e;
  text-shadow:0 0 26px #ff006ecc;{anim}">{rem:.1f}</div>
<div style="color:#6677aa;font-size:11px">seconds left</div></div>
<style>@keyframes cf{{0%,100%{{color:#ff006e}}50%{{color:#ff5555}}}}</style>""",unsafe_allow_html=True)
        st.progress(rem/dur)
        if rem<=0: st.session_state["cks"]="done"; st.rerun()
    cl="#ff006e" if state=="playing" else("#39ff14" if state=="done" else "#6677aa")
    st.markdown(f"""<div style="text-align:center;margin:10px 0">
<div style="font-family:Orbitron,sans-serif;font-size:72px;font-weight:900;
  color:{cl};text-shadow:0 0 32px {cl}80">{cnt}</div>
<div style="color:#6677aa;font-size:12px">clicks</div></div>""",unsafe_allow_html=True)
    _,c2,_=st.columns([1,2,1])
    with c2:
        if state=="idle":
            st.markdown('<div class="br">',unsafe_allow_html=True)
            if st.button("🚀 Start!",use_container_width=True,key="ckg"):
                st.session_state.update({"cks":"playing","ckc":0,"ckt":time.time()})
                st.session_state["click_ses"]=S("click_ses",0)+1; st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)
        elif state=="playing":
            st.markdown("""<style>div.ckB .stButton>button{background:rgba(255,0,110,.32)!important;
border:2px solid rgba(255,0,110,.72)!important;color:#ff006e!important;font-size:22px!important;
height:110px!important;font-weight:900!important;}
div.ckB .stButton>button:active{transform:scale(.93)!important;}</style>""",unsafe_allow_html=True)
            st.markdown('<div class="ckB">',unsafe_allow_html=True)
            if st.button("👆 CLICK!",use_container_width=True,key="ckc_btn"):
                st.session_state["ckc"]=cnt+mul; st.session_state["click_tot"]=S("click_tot",0)+mul; st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)
        elif state=="done":
            final=S("ckc",0); e=earn(final*2); give_xp(final)
            if final>best: st.session_state["click_hi"]=final; add_ach(f"👆 Clicker Record: {final}!")
            st.markdown(f"<div class='{'ok' if final>=best else 'inf'}' style='margin-bottom:10px'>{final} clicks! +{e} coins</div>",unsafe_allow_html=True)
            st.markdown('<div class="bG">',unsafe_allow_html=True)
            if st.button("🔄 Again",use_container_width=True,key="ckr"):
                st.session_state["cks"]="idle"; st.session_state["ckc"]=0; st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)
    if state=="playing": time.sleep(0.05); st.rerun()
    st.markdown("---")
    c1,c2,c3=st.columns(3)
    with c1: st.metric("🏆 Best",S("click_hi",0))
    with c2: st.metric("👆 Total",S("click_tot",0))
    with c3: st.metric("🎮 Rounds",S("click_ses",0))

# ═══════════════════════════════════════════════════════
#  SLOT MACHINE  — animated spinning reels
# ═══════════════════════════════════════════════════════
SYM=["🍒","🍋","🍊","🍇","⭐","💎","🎰","🃏"]
SW=[20,18,15,12,10,7,4,14]
PAY={0:5,1:8,2:10,3:15,4:20,5:50,6:100,7:35}
SYM_NAMES=["Cherry","Lemon","Orange","Grapes","Star","Diamond","Jackpot","Joker"]

def page_slot():
    st.markdown("<h1 style='text-align:center'>🎰 Slot Machine</h1>",unsafe_allow_html=True)
    lk=oc("slot_luck"); jp=oc("slot_jackpot"); rf=has("slot_refund")
    if lk or jp or rf:
        ups=filter(None,[f"🍀 Luck +{lk}" if lk else "",f"💰 Jackpot x{2**jp}" if jp else "",f"↩ Refund" if rf else ""])
        st.markdown(f"<div class='inf'>{'  |  '.join(ups)}</div>",unsafe_allow_html=True)
    if "slr" not in st.session_state:
        st.session_state.update({"slr":[6,6,6],"slres":"","slbet":10,"sl_anim":False,"sl_anim_reels":[[6,6,6],[6,6,6],[6,6,6]]})

    reels=st.session_state["slr"]; res=S("slres",""); coins=S("coins",0)
    iw="Won" in res or "Jackpot" in res; ijp="Jackpot" in res

    # Animated slot machine rendered in a canvas component
    r0,r1,r2=reels
    anim_data = json_list(reels)
    components.html(f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:transparent;display:flex;justify-content:center;padding:8px;font-family:'Orbitron',monospace}}
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');
.machine{{
  background:linear-gradient(145deg,#1a0a00,#240e00,#1a0a00);
  border:3px solid {("rgba(255,214,10,.9)" if ijp else "rgba(255,214,10,.55)" if iw else "rgba(255,124,0,.4)")};
  border-radius:18px;padding:20px 24px;max-width:460px;width:100%;
  box-shadow:{("0 0 40px rgba(255,214,10,.5),0 0 80px rgba(255,214,10,.2)" if iw else "0 0 16px rgba(255,124,0,.12)")},inset 0 0 24px rgba(0,0,0,.5);
  {("animation:jpFlash .3s infinite;" if ijp else "")}
}}
.title{{text-align:center;font-family:Orbitron,monospace;font-size:16px;font-weight:900;color:#ff7c00;
  text-shadow:0 0 12px rgba(255,124,0,.7);letter-spacing:4px;margin-bottom:14px}}
.reels{{display:flex;gap:12px;justify-content:center;padding:14px;
  background:rgba(0,0,0,.55);border-radius:12px;border:1px solid rgba(255,124,0,.18);position:relative}}
.reel-wrap{{flex:1;max-width:110px;aspect-ratio:1;overflow:hidden;border-radius:10px;position:relative}}
.reel-strip{{display:flex;flex-direction:column;transition:transform .0s;}}
.reel-item{{height:100%;display:flex;align-items:center;justify-content:center;font-size:52px;
  background:linear-gradient(160deg,#1e0e00,#120800);border:2px solid rgba(255,124,0,.4);border-radius:10px;min-height:90px}}
.reel-item.lit{{background:linear-gradient(160deg,#2a1600,#1e0c00);box-shadow:inset 0 0 20px rgba(255,214,10,.15)}}
.win-line{{height:3px;background:linear-gradient(90deg,transparent,{("#ffd60a" if iw else "rgba(255,124,0,.3)")},transparent);margin:8px 0;
  {("box-shadow:0 0 8px #ffd60a,0 0 20px rgba(255,214,10,.5);" if iw else "")}}}
@keyframes jpFlash{{0%,100%{{border-color:rgba(255,214,10,.9)}}50%{{border-color:rgba(255,214,10,.15)}}}}
@keyframes reelSpin{{from{{filter:blur(4px) brightness(1.5)}}to{{filter:blur(0) brightness(1)}}}}
.spinning{{animation:reelSpin .6s ease-out}}
</style></head><body>
<div class="machine">
  <div class="title">🎰 ARCADE SLOTS</div>
  <div class="reels">
    <div class="reel-wrap"><div class="reel-item {'spinning' if S('sl_anim') else ''}" id="r0">{SYM[r0]}</div></div>
    <div class="reel-wrap"><div class="reel-item {'spinning' if S('sl_anim') else ''}" id="r1" style="animation-delay:.1s">{SYM[r1]}</div></div>
    <div class="reel-wrap"><div class="reel-item {'spinning' if S('sl_anim') else ''}" id="r2" style="animation-delay:.2s">{SYM[r2]}</div></div>
  </div>
  <div class="win-line"></div>
</div>
</body></html>""", height=190, scrolling=False)

    st.markdown("<br>",unsafe_allow_html=True)
    if res:
        cls="ok" if iw else "err"
        icon = "🎉" if ijp else ("✅" if iw else "😔")
        st.markdown(f"<div class='{cls}' style='font-size:15px;padding:12px'>{icon} {res}</div>",unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)

    c1,c2=st.columns([3,1])
    with c1:
        maxbet=max(5,min(200,coins)) if coins>=5 else 5
        bet=st.slider("Bet 💰",5,maxbet,min(S("slbet",10),maxbet),5,key="slsl")
        st.session_state["slbet"]=bet
    with c2: st.metric("Balance",coins)

    _,c2,_=st.columns([1,2,1])
    with c2:
        st.markdown("""<style>div.spB .stButton>button{background:rgba(255,124,0,.3)!important;
border:2px solid rgba(255,124,0,.6)!important;color:#ff7c00!important;font-size:17px!important;
height:56px!important;font-weight:900!important;letter-spacing:2px!important;}
div.spB .stButton>button:hover{box-shadow:0 0 24px rgba(255,124,0,.45)!important;}</style>""",unsafe_allow_html=True)
        st.markdown('<div class="spB">',unsafe_allow_html=True)
        if st.button("🎰  SPIN!",use_container_width=True,key="slsp",disabled=coins<bet):
            _spin(bet,lk,jp,rf)
        st.markdown('</div>',unsafe_allow_html=True)
    if coins<bet: st.markdown("<div class='err'>Not enough coins!</div>",unsafe_allow_html=True)

    st.markdown("---")
    with st.expander("📋 Paytable"):
        for idx,mult in PAY.items():
            am=mult*(2**jp if mult>=50 else 1)
            st.markdown(f"""<div style="display:flex;justify-content:space-between;align-items:center;padding:5px 10px;
background:rgba(255,124,0,.04);border-radius:6px;margin-bottom:2px">
<span style="font-size:22px">{SYM[idx]*3}</span>
<span style="color:#6677aa;font-size:12px">{SYM_NAMES[idx]}</span>
<span style="color:#ff7c00;font-weight:900;font-family:Orbitron;font-size:14px">×{am}</span></div>""",unsafe_allow_html=True)
    st.markdown("---")
    c1,c2,c3=st.columns(3)
    with c1: st.metric("🎰 Spins",S("slot_sp",0))
    with c2: st.metric("🏆 Wins",S("slot_w",0))
    with c3: st.metric("💰 Total Won",S("slot_tot",0))

def _spin(bet,lk,jp,rf):
    st.session_state["coins"]-=bet; st.session_state["slot_sp"]=S("slot_sp",0)+1
    w=SW[:]
    for i in[4,5,6]: w[i]=int(w[i]*(1+lk*0.28))
    r=[random.choices(range(8),weights=w,k=1)[0] for _ in range(3)]
    st.session_state["slr"]=r; st.session_state["sl_anim"]=True
    if r[0]==r[1]==r[2]:
        pay=PAY[r[0]]*(2**jp if r[0]>=4 else 1)
        won=bet*pay; e=earn(won); give_xp(won//5)
        st.session_state["slot_w"]=S("slot_w",0)+1; st.session_state["slot_tot"]=S("slot_tot",0)+e
        if pay>=100: st.session_state["slres"]=f"🎰 JACKPOT!!! +{e} coins"; add_ach("🎰 Jackpot!")
        else: st.session_state["slres"]=f"Won {SYM_NAMES[r[0]]}×3! +{e} coins (×{pay})"
    elif r[0]==r[1] or r[1]==r[2] or r[0]==r[2]:
        e=earn(bet*2); give_xp(3); st.session_state["slres"]=f"Pair! +{e} coins"
        st.session_state["slot_w"]=S("slot_w",0)+1
    else:
        if rf: rb=max(1,int(bet*.1)); earn(rb); st.session_state["slres"]=f"Lost {bet} coins. Refund: {rb}"
        else: st.session_state["slres"]=f"Lost {bet} coins. Try again!"
    st.rerun()

# ═══════════════════════════════════════════════════════
#  PONG 1P
# ═══════════════════════════════════════════════════════
def page_pong():
    st.markdown("<h1 style='text-align:center'>🏓 Pong</h1><p style='text-align:center;color:#6677aa'>W/S or ↑/↓ to move your paddle</p>",unsafe_allow_html=True)
    spb=2+oc("pong_speed"); hi=S("pong_hi",0)
    _,col,_=st.columns([1,10,1])
    with col:
        components.html(f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>*{{margin:0;padding:0;box-sizing:border-box}}body{{background:#06060e;display:flex;flex-direction:column;align-items:center;padding:6px;user-select:none}}@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');canvas{{border:2px solid rgba(0,245,255,.26);border-radius:10px;box-shadow:0 0 20px rgba(0,245,255,.08);display:block}}.ov{{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);background:rgba(4,4,18,.95);border:2px solid #00f5ff;border-radius:11px;padding:18px 26px;text-align:center}}.ov h2{{color:#00f5ff;font-size:17px;margin-bottom:7px}}.ov p{{color:#8888aa;font-size:11px;margin-bottom:11px}}.ov button{{background:rgba(0,245,255,.16);color:#00f5ff;border:1px solid #00f5ff;padding:7px 18px;border-radius:6px;cursor:pointer;font-family:Orbitron;font-size:12px;font-weight:700}}.wrap{{position:relative}}</style></head><body>
<div class="wrap"><canvas id="c" width="480" height="300"></canvas><div class="ov" id="ov"><h2>🏓 Pong</h2><p>W/S or ↑/↓ | First to 7 wins</p><button onclick="start()">▶ Play</button></div></div>
<script>
const W=480,H=300,PW=10,PH=60,BALL=7,SPB={spb};
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
let p1y,p2y,bx,by,vx,vy,s1,s2,run,raf,keys={{}};
function start(){{document.getElementById('ov').style.display='none';p1y=H/2-PH/2;p2y=H/2-PH/2;bx=W/2;by=H/2;let a=(Math.random()*.8+.1)*Math.PI*(Math.random()<.5?1:-1);vx=Math.cos(a)*(SPB+1);vy=Math.sin(a)*SPB;s1=s2=0;run=true;if(raf)cancelAnimationFrame(raf);loop();}}
document.addEventListener('keydown',e=>{{keys[e.code]=true;if(['KeyW','KeyS','ArrowUp','ArrowDown'].includes(e.code))e.preventDefault();}});
document.addEventListener('keyup',e=>keys[e.code]=false);
function loop(){{if(!run)return;update();draw();raf=requestAnimationFrame(loop);}}
function update(){{if(keys['KeyW']||keys['ArrowUp'])p1y=Math.max(0,p1y-5);if(keys['KeyS']||keys['ArrowDown'])p1y=Math.min(H-PH,p1y+5);let cy=p2y+PH/2;if(by<cy-3)p2y=Math.max(0,p2y-4);else if(by>cy+3)p2y=Math.min(H-PH,p2y+4);bx+=vx;by+=vy;if(by<=BALL||by>=H-BALL)vy=-vy;if(bx<=20+PW&&by>=p1y&&by<=p1y+PH){{vx=Math.abs(vx)*(1+s1*.04);vy+=(by-(p1y+PH/2))*.1;}}if(bx>=W-20-PW&&by>=p2y&&by<=p2y+PH){{vx=-Math.abs(vx)*(1+s2*.04);vy+=(by-(p2y+PH/2))*.1;}}if(bx<0){{s2++;if(s2>=7){{endGame('AI Wins!');return;}}reset();}}if(bx>W){{s1++;if(s1>=7){{endGame('You Win! 🎉');return;}}reset();}}}}
function reset(){{bx=W/2;by=H/2;let a=(Math.random()*.8+.1)*Math.PI*(Math.random()<.5?1:-1);vx=Math.cos(a)*(SPB+1+Math.max(s1,s2)*.2);vy=Math.sin(a)*SPB;}}
function endGame(msg){{run=false;cancelAnimationFrame(raf);document.getElementById('ov').querySelector('h2').textContent=msg;document.getElementById('ov').querySelector('p').textContent='You: '+s1+' | AI: '+s2;document.getElementById('ov').style.display='block';}}
function draw(){{ctx.fillStyle='#06060e';ctx.fillRect(0,0,W,H);ctx.setLineDash([8,8]);ctx.strokeStyle='rgba(255,255,255,.08)';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(W/2,0);ctx.lineTo(W/2,H);ctx.stroke();ctx.setLineDash([]);ctx.fillStyle='rgba(0,245,255,.9)';ctx.font='bold 28px Orbitron,monospace';ctx.textAlign='center';ctx.fillText(s1,W/2-60,36);ctx.fillText(s2,W/2+60,36);[{{x:14,y:p1y,c:'#00f5ff'}},{{x:W-14-PW,y:p2y,c:'#ff006e'}}].forEach(p=>{{ctx.shadowBlur=13;ctx.shadowColor=p.c;ctx.fillStyle=p.c;ctx.beginPath();ctx.roundRect(p.x,p.y,PW,PH,4);ctx.fill();ctx.shadowBlur=0;}});ctx.shadowBlur=15;ctx.shadowColor='#ffd60a';ctx.fillStyle='#ffd60a';ctx.beginPath();ctx.arc(bx,by,BALL,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;}}
ctx.fillStyle='#06060e';ctx.fillRect(0,0,W,H);
</script></body></html>""", height=350, scrolling=False)
    st.markdown("<br>",unsafe_allow_html=True)
    _,c2,_=st.columns([1,2,1])
    with c2:
        st.markdown('<div class="bG">',unsafe_allow_html=True)
        if st.button("▶ New Game",use_container_width=True,key="pnew"):
            st.session_state["pong_pl"]=S("pong_pl",0)+1; earn(5); give_xp(5)
        st.markdown('</div>',unsafe_allow_html=True)
    st.markdown("---")
    c1,c2=st.columns(2)
    with c1: st.metric("🏆 Best",S("pong_hi",0))
    with c2: st.metric("🎮 Games",S("pong_pl",0))

# ═══════════════════════════════════════════════════════
#  MINESWEEPER
# ═══════════════════════════════════════════════════════
def _ms_init(rows=8,cols=8,mines=10):
    board=[[0]*cols for _ in range(rows)]
    mset=set(random.sample(range(rows*cols),mines))
    for p in mset: board[p//cols][p%cols]=-1
    for r in range(rows):
        for c in range(cols):
            if board[r][c]==-1: continue
            board[r][c]=sum(1 for dr in[-1,0,1] for dc in[-1,0,1] if 0<=r+dr<rows and 0<=c+dc<cols and board[r+dr][c+dc]==-1)
    st.session_state.update({"ms_b":board,"ms_rev":set(),"ms_flag":set(),"ms_rows":rows,"ms_cols":cols,"ms_mines":mines,"ms_over":False,"ms_win":False})

def page_minesweeper():
    st.markdown("<h1 style='text-align:center'>💣 Minesweeper</h1><p style='text-align:center;color:#6677aa'>? = reveal · 🚩 = flag</p>",unsafe_allow_html=True)
    if "ms_b" not in st.session_state: _ms_init()
    b=st.session_state["ms_b"]; rev=st.session_state["ms_rev"]; flags=st.session_state["ms_flag"]
    rows=S("ms_rows",8); cols_n=S("ms_cols",8); mines=S("ms_mines",10); over=S("ms_over"); win=S("ms_win")
    safe_total=rows*cols_n-mines; rev_safe=sum(1 for i in rev if b[i//cols_n][i%cols_n]!=-1)
    c1,c2,c3,c4=st.columns(4)
    with c1: st.metric("💣 Mines",mines-len(flags))
    with c2: st.metric("✅ Revealed",f"{rev_safe}/{safe_total}")
    with c3: st.metric("🚩 Flags",len(flags))
    with c4: diff=st.selectbox("Difficulty",["Easy (6×6)","Normal (8×8)","Hard (10×10)"],key="ms_diff",label_visibility="visible")
    st.markdown("<br>",unsafe_allow_html=True)
    if over:
        if win: st.markdown(f"<div class='ok' style='font-size:16px;padding:14px'>🎉 You cleared the field!</div>",unsafe_allow_html=True)
        else: st.markdown("<div class='err' style='font-size:16px;padding:14px'>💥 BOOM! Hit a mine!</div>",unsafe_allow_html=True)
    COLORS={0:"#555",1:"#00f5ff",2:"#39ff14",3:"#ff006e",4:"#bf5fff",5:"#ff7c00",6:"#ffd60a",7:"#fff",8:"#888"}
    _,mc,_=st.columns([1,5,1])
    with mc:
        for r in range(rows):
            rc=st.columns(cols_n)
            for c in range(cols_n):
                idx=r*cols_n+c; cell=b[r][c]
                with rc[c]:
                    if idx in rev:
                        if cell==-1: st.markdown("""<div style="height:36px;background:rgba(255,0,110,.18);border:1px solid rgba(255,0,110,.5);border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:16px">💥</div>""",unsafe_allow_html=True)
                        else:
                            col_c=COLORS.get(cell,"#fff"); txt=str(cell) if cell else "·"
                            st.markdown(f"""<div style="height:36px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.07);border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;color:{col_c}">{txt}</div>""",unsafe_allow_html=True)
                    elif idx in flags:
                        st.markdown("""<div style="height:36px;background:rgba(255,214,10,.1);border:1px solid rgba(255,214,10,.4);border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:14px">🚩</div>""",unsafe_allow_html=True)
                        if not over and st.button("✕",key=f"msu_{idx}",use_container_width=True):
                            flags.discard(idx); st.session_state["ms_flag"]=flags; st.rerun()
                    elif not over:
                        c1b,c2b=st.columns(2)
                        with c1b:
                            if st.button("?",key=f"msr_{idx}",use_container_width=True): _ms_rev(idx,b,rev,flags,rows,cols_n,mines)
                        with c2b:
                            if st.button("🚩",key=f"msf_{idx}",use_container_width=True):
                                flags.add(idx); st.session_state["ms_flag"]=flags; st.rerun()
    st.markdown("<br>",unsafe_allow_html=True)
    _,c2,_=st.columns([1,2,1])
    with c2:
        st.markdown('<div class="br">',unsafe_allow_html=True)
        if st.button("🔄 New Game",use_container_width=True,key="msnew"):
            d=S("ms_diff","Normal (8×8)")
            if "6" in d: _ms_init(6,6,7)
            elif "10" in d: _ms_init(10,10,18)
            else: _ms_init(8,8,10)
            st.rerun()
        st.markdown('</div>',unsafe_allow_html=True)

def _ms_rev(idx,b,rev,flags,rows,cols,mines):
    if idx in rev or idx in flags: return
    r,c=idx//cols,idx%cols
    if b[r][c]==-1:
        rev.add(idx); st.session_state["ms_rev"]=rev
        st.session_state["ms_over"]=True; st.session_state["ms_win"]=False; st.rerun()
    stack=[idx]
    while stack:
        cur=stack.pop(); rev.add(cur)
        cr,cc=cur//cols,cur%cols
        if b[cr][cc]==0:
            for dr in[-1,0,1]:
                for dc in[-1,0,1]:
                    ni=(cr+dr)*cols+(cc+dc)
                    if 0<=cr+dr<rows and 0<=cc+dc<cols and ni not in rev: stack.append(ni)
    st.session_state["ms_rev"]=rev
    if sum(1 for i in rev if b[i//cols][i%cols]!=-1)==rows*cols-mines:
        e=earn(80); give_xp(40); add_ach("💣 Minesweeper Clear!")
        st.session_state["ms_over"]=True; st.session_state["ms_win"]=True
    st.rerun()

# ═══════════════════════════════════════════════════════
#  NUMBER GUESS
# ═══════════════════════════════════════════════════════
def page_guess():
    st.markdown("<h1 style='text-align:center'>🔢 Number Guess</h1><p style='text-align:center;color:#6677aa'>Guess the secret number between 1–100</p>",unsafe_allow_html=True)
    if "gn" not in st.session_state:
        st.session_state.update({"gn":random.randint(1,100),"gatt":0,"gover":False,"gfeed":"","g_lo":1,"g_hi":100})
    gn=S("gn"); att=S("gatt",0); mx=10; feed=S("gfeed",""); over=S("gover")
    c1,c2=st.columns(2)
    with c1: st.metric("🎯 Attempts",f"{att}/{mx}")
    with c2: st.metric("📊 Range",f"{S('g_lo',1)}–{S('g_hi',100)}")
    if over:
        won="Win" in feed
        st.markdown(f"<div class='{'ok' if won else 'err'}' style='font-size:17px;padding:14px'>{feed}</div>",unsafe_allow_html=True)
        _,mc,_=st.columns([1,2,1])
        with mc:
            st.markdown('<div class="bG">',unsafe_allow_html=True)
            if st.button("🔄 New Game",use_container_width=True,key="gnnew"):
                st.session_state.update({"gn":random.randint(1,100),"gatt":0,"gover":False,"gfeed":"","g_lo":1,"g_hi":100}); st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)
        return
    if feed: st.markdown(f"<div class='inf' style='font-size:15px;padding:12px'>{feed}</div>",unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    c1,c2=st.columns([3,1])
    with c1: guess=st.number_input("Your guess:",1,100,50,key="gin",label_visibility="visible")
    with c2:
        st.markdown("<br>",unsafe_allow_html=True)
        st.markdown('<div class="bg">',unsafe_allow_html=True)
        if st.button("🎯 Guess",use_container_width=True,key="gok"):
            st.session_state["gatt"]=att+1
            if guess==gn:
                e=earn(max(10,(mx-att)*15)); give_xp(30)
                st.session_state["gfeed"]=f"🎉 Win! The number was {gn}! +{e} coins"
                st.session_state["gover"]=True; add_ach("🔢 Guessed it!")
            elif att+1>=mx:
                st.session_state["gfeed"]=f"😔 Out of guesses! It was {gn}"
                st.session_state["gover"]=True
            elif guess<gn:
                st.session_state["gfeed"]=f"📈 Higher than {guess}!"
                st.session_state["g_lo"]=max(S("g_lo",1),guess+1)
            else:
                st.session_state["gfeed"]=f"📉 Lower than {guess}!"
                st.session_state["g_hi"]=min(S("g_hi",100),guess-1)
            st.rerun()
        st.markdown('</div>',unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
#  TARGET SHOOTING
# ═══════════════════════════════════════════════════════
def page_targets():
    st.markdown("<h1 style='text-align:center'>🎯 Target Shooting</h1><p style='text-align:center;color:#6677aa'>Click targets before they vanish! 15 seconds</p>",unsafe_allow_html=True)
    if "tgt" not in st.session_state:
        st.session_state.update({"tgt":"idle","tgt_sc":0,"tgt_t":0,"tgt_pos":None,"tgt_app":0,"tgt_hi":0})
    state=S("tgt"); score=S("tgt_sc",0); hi=S("tgt_hi",0)
    if state=="idle":
        st.metric("🏆 Best",hi); st.markdown("<br>",unsafe_allow_html=True)
        _,mc,_=st.columns([1,2,1])
        with mc:
            st.markdown('<div class="br">',unsafe_allow_html=True)
            if st.button("🎯 Start!",use_container_width=True,key="tgo"):
                st.session_state.update({"tgt":"playing","tgt_sc":0,"tgt_t":time.time(),"tgt_pos":(random.randint(0,2),random.randint(0,4)),"tgt_app":time.time()})
                st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)
        return
    if state=="playing":
        el=time.time()-S("tgt_t",0); rem=max(0,15-el)
        if rem<=0: st.session_state["tgt"]="done"; st.rerun()
        c1,c2=st.columns(2)
        with c1: st.metric("🎯 Score",score)
        with c2: st.markdown(f"<div style='font-family:Orbitron,sans-serif;font-size:26px;color:{'#ff006e' if rem<5 else '#00f5ff'};text-align:center;padding:8px'>{rem:.1f}s</div>",unsafe_allow_html=True)
        st.progress(rem/15)
        pos=S("tgt_pos"); app_t=S("tgt_app",0)
        if time.time()-app_t>2.5:
            pos=(random.randint(0,2),random.randint(0,4)); st.session_state.update({"tgt_pos":pos,"tgt_app":time.time()})
        if pos:
            _row,col_i=pos
            rows_cols=st.columns(5)
            for ri in range(5):
                with rows_cols[ri]:
                    if ri==col_i:
                        age=time.time()-app_t; op=max(0.2,1-age/2.5)
                        st.markdown(f"""<div style="height:70px;background:rgba(255,0,110,{op*0.25:.2f});
border:2px solid rgba(255,0,110,{min(op+0.2,1):.2f});border-radius:50%;display:flex;align-items:center;
justify-content:center;font-size:30px;animation:tpulse .4s ease-in-out infinite">🎯</div>
<style>@keyframes tpulse{{0%,100%{{transform:scale(1)}}50%{{transform:scale(1.12)}}}}</style>""",unsafe_allow_html=True)
                        if st.button("🎯",key=f"tgt_{int(app_t*10)}_{ri}",use_container_width=True):
                            bonus=max(1,int((2.5-(time.time()-app_t))*5))
                            st.session_state["tgt_sc"]=score+bonus
                            st.session_state.update({"tgt_pos":(random.randint(0,2),random.randint(0,4)),"tgt_app":time.time()})
                            st.rerun()
                    else:
                        st.markdown("""<div style="height:70px;background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.04);border-radius:50%"></div>""",unsafe_allow_html=True)
        time.sleep(0.1); st.rerun()
    if state=="done":
        e=earn(score*3); give_xp(score)
        if score>hi: st.session_state["tgt_hi"]=score; add_ach(f"🎯 Target Record: {score}!")
        st.markdown(f"<div class='ok' style='font-size:17px;padding:16px'>🎉 {score} targets hit! +{e} coins</div>",unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
        _,mc,_=st.columns([1,2,1])
        with mc:
            st.markdown('<div class="bG">',unsafe_allow_html=True)
            if st.button("🔄 Play Again",use_container_width=True,key="tga"):
                st.session_state.update({"tgt":"idle","tgt_sc":0}); st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
#  WORD GUESS (Wordle-like)
# ═══════════════════════════════════════════════════════
WORDS=["PYTHON","STREAM","LASER","NEON","PIXEL","BLAST","CYBER","QUEST","STORM","SWORD",
       "FLAME","GHOST","QUEEN","BRAVE","CRISP","SHINY","PRIME","VIBES","ULTRA","LUNAR"]

def page_wordgame():
    st.markdown("<h1 style='text-align:center'>🔤 Word Guess</h1><p style='text-align:center;color:#6677aa'>Guess the English word — 6 tries</p>",unsafe_allow_html=True)
    if "ww" not in st.session_state:
        w=random.choice(WORDS); st.session_state.update({"ww":w,"wg":[],"wo":False,"wm":""})
    word=S("ww",""); guesses=list(S("wg",[])); over=S("wo"); msg=S("wm","")
    c1,c2=st.columns(2)
    with c1: st.metric("📝 Length",len(word))
    with c2: st.metric("🎯 Tries",f"{len(guesses)}/6")

    for g in guesses:
        row_html=""
        for i,ch in enumerate(g):
            if i<len(word):
                if ch==word[i]: bg="rgba(57,255,20,.15)"; bd="rgba(57,255,20,.55)"; col="#39ff14"
                elif ch in word: bg="rgba(255,214,10,.12)"; bd="rgba(255,214,10,.45)"; col="#ffd60a"
                else: bg="rgba(255,255,255,.04)"; bd="rgba(255,255,255,.1)"; col="#6677aa"
            else: bg="rgba(255,255,255,.02)"; bd="rgba(255,255,255,.06)"; col="#444"
            row_html+=f"""<div style="width:46px;height:46px;background:{bg};border:2px solid {bd};border-radius:7px;
display:flex;align-items:center;justify-content:center;font-size:18px;font-weight:900;color:{col};font-family:Orbitron,sans-serif">{ch}</div>"""
        st.markdown(f"<div style='display:flex;gap:6px;justify-content:center;margin-bottom:5px'>{row_html}</div>",unsafe_allow_html=True)

    for _ in range(6-len(guesses)):
        empty="".join(f"""<div style="width:46px;height:46px;background:rgba(255,255,255,.02);border:2px solid rgba(255,255,255,.06);border-radius:7px"></div>""" for _ in range(len(word)))
        st.markdown(f"<div style='display:flex;gap:6px;justify-content:center;margin-bottom:5px'>{empty}</div>",unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)
    if msg: st.markdown(f"<div class='{'ok' if 'Win' in msg else ('err' if 'word was' in msg else 'inf')}' style='padding:11px'>{msg}</div>",unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    if over:
        _,mc,_=st.columns([1,2,1])
        with mc:
            st.markdown('<div class="bG">',unsafe_allow_html=True)
            if st.button("🔄 New Word",use_container_width=True,key="wwnew"):
                w=random.choice(WORDS); st.session_state.update({"ww":w,"wg":[],"wo":False,"wm":""}); st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)
        return
    c1,c2=st.columns([3,1])
    with c1: inp=st.text_input("Enter your guess:",max_chars=len(word),key="wwin",label_visibility="collapsed").upper().strip()
    with c2:
        st.markdown('<div class="bg">',unsafe_allow_html=True)
        if st.button("🎯 Guess",use_container_width=True,key="wwok"):
            if len(inp)!=len(word): st.session_state["wm"]=f"⚠️ Word must be {len(word)} letters!"
            elif inp in guesses: st.session_state["wm"]="⚠️ Already guessed!"
            else:
                guesses.append(inp); st.session_state["wg"]=guesses
                if inp==word:
                    e=earn(max(20,(6-len(guesses)+1)*25)); give_xp(40)
                    st.session_state["wm"]=f"🎉 Win! +{e} coins"; st.session_state["wo"]=True; add_ach("🔤 Word Master!")
                elif len(guesses)>=6:
                    st.session_state["wm"]=f"😔 The word was: {word}"; st.session_state["wo"]=True
                else: st.session_state["wm"]="🟩 right spot  🟨 wrong spot  ⬜ not in word"
            st.rerun()
        st.markdown('</div>',unsafe_allow_html=True)
    st.markdown("<div style='color:#6677aa;font-size:11px;text-align:center;margin-top:6px'>🟩 Correct position | 🟨 Wrong position | ⬜ Not in word</div>",unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
#  PONG 2P
# ═══════════════════════════════════════════════════════
def page_pong2p():
    st.markdown("<h1 style='text-align:center'>🏓 Pong — 2 Players</h1>",unsafe_allow_html=True)
    st.markdown("<div class='inf'>Player 1: W/S  |  Player 2: ↑/↓  |  First to 7 wins!</div>",unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    _,col,_=st.columns([1,10,1])
    with col:
        components.html("""<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>*{margin:0;padding:0;box-sizing:border-box}body{background:#06060e;display:flex;flex-direction:column;align-items:center;padding:6px;user-select:none}@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');canvas{border:2px solid rgba(0,245,255,.26);border-radius:10px;box-shadow:0 0 20px rgba(0,245,255,.08);display:block}.ov{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);background:rgba(4,4,18,.95);border:2px solid #00f5ff;border-radius:11px;padding:18px 26px;text-align:center}.ov h2{color:#00f5ff;font-size:17px;margin-bottom:7px}.ov p{color:#8888aa;font-size:11px;margin-bottom:11px}.ov button{background:rgba(0,245,255,.16);color:#00f5ff;border:1px solid #00f5ff;padding:7px 18px;border-radius:6px;cursor:pointer;font-family:Orbitron;font-size:12px;font-weight:700}.wrap{position:relative}</style></head><body>
<div class="wrap"><canvas id="c" width="540" height="320"></canvas><div class="ov" id="ov"><h2>🏓 2-Player Pong</h2><p>P1: W/S | P2: ↑/↓<br>First to 7 wins!</p><button onclick="start()">▶ Play</button></div></div>
<script>
const W=540,H=320,PW=11,PH=65,BALL=7;const cv=document.getElementById('c'),ctx=cv.getContext('2d');let p1y,p2y,bx,by,vx,vy,s1,s2,run,raf,keys={};
function start(){document.getElementById('ov').style.display='none';p1y=H/2-PH/2;p2y=H/2-PH/2;bx=W/2;by=H/2;let a=(Math.random()*.7+.15)*Math.PI*(Math.random()<.5?1:-1);vx=Math.cos(a)*3.5;vy=Math.sin(a)*3.5;s1=s2=0;run=true;if(raf)cancelAnimationFrame(raf);loop();}
document.addEventListener('keydown',e=>{keys[e.code]=true;if(['KeyW','KeyS','ArrowUp','ArrowDown'].includes(e.code))e.preventDefault();});document.addEventListener('keyup',e=>keys[e.code]=false);
function loop(){if(!run)return;update();draw();raf=requestAnimationFrame(loop);}
function update(){if(keys['KeyW'])p1y=Math.max(0,p1y-5);if(keys['KeyS'])p1y=Math.min(H-PH,p1y+5);if(keys['ArrowUp'])p2y=Math.max(0,p2y-5);if(keys['ArrowDown'])p2y=Math.min(H-PH,p2y+5);bx+=vx;by+=vy;if(by<=BALL||by>=H-BALL)vy=-vy;if(bx<=16+PW&&by>=p1y&&by<=p1y+PH){vx=Math.abs(vx)*1.03;vy+=(by-(p1y+PH/2))*.08;}if(bx>=W-16-PW&&by>=p2y&&by<=p2y+PH){vx=-Math.abs(vx)*1.03;vy+=(by-(p2y+PH/2))*.08;}if(bx<0){s2++;if(s2>=7){end('Player 2 Wins! 🎉');return;}reset();}if(bx>W){s1++;if(s1>=7){end('Player 1 Wins! 🎉');return;}reset();}}
function reset(){bx=W/2;by=H/2;let a=(Math.random()*.7+.15)*Math.PI*(Math.random()<.5?1:-1);vx=Math.cos(a)*(3.5+Math.max(s1,s2)*.15);vy=Math.sin(a)*3.5;}
function end(msg){run=false;cancelAnimationFrame(raf);document.getElementById('ov').querySelector('h2').textContent=msg;document.getElementById('ov').querySelector('p').textContent='P1: '+s1+' | P2: '+s2;document.getElementById('ov').style.display='block';}
function draw(){ctx.fillStyle='#06060e';ctx.fillRect(0,0,W,H);ctx.setLineDash([7,7]);ctx.strokeStyle='rgba(255,255,255,.07)';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(W/2,0);ctx.lineTo(W/2,H);ctx.stroke();ctx.setLineDash([]);ctx.font='bold 26px Orbitron,monospace';ctx.textAlign='center';ctx.fillStyle='#00f5ff';ctx.shadowBlur=11;ctx.shadowColor='#00f5ff';ctx.fillText(s1,W/2-65,35);ctx.fillStyle='#ff006e';ctx.shadowColor='#ff006e';ctx.fillText(s2,W/2+65,35);ctx.shadowBlur=0;[{x:14,y:p1y,c:'#00f5ff'},{x:W-14-PW,y:p2y,c:'#ff006e'}].forEach(p=>{ctx.shadowBlur=12;ctx.shadowColor=p.c;ctx.fillStyle=p.c;ctx.beginPath();ctx.roundRect(p.x,p.y,PW,PH,4);ctx.fill();ctx.shadowBlur=0;});ctx.shadowBlur=14;ctx.shadowColor='#ffd60a';ctx.fillStyle='#ffd60a';ctx.beginPath();ctx.arc(bx,by,BALL,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;}
ctx.fillStyle='#06060e';ctx.fillRect(0,0,W,H);
</script></body></html>""", height=370, scrolling=False)

# ═══════════════════════════════════════════════════════
#  TIC-TAC-TOE 2P
# ═══════════════════════════════════════════════════════
def page_ttt2p():
    st.markdown("<h1 style='text-align:center'>❌ Tic-Tac-Toe — 2 Players</h1>",unsafe_allow_html=True)
    if "tb2" not in st.session_state:
        st.session_state.update({"tb2":[""]*9,"turn2":"X","tw2":{"X":0,"O":0},"to2":False,"ts2":""})
    b=st.session_state["tb2"]; turn=S("turn2","X"); wins=S("tw2",{"X":0,"O":0}); over=S("to2"); msg=S("ts2","")
    c1,c2,c3=st.columns(3)
    with c1: st.metric("❌ Player 1",wins.get("X",0))
    with c2: st.metric("⭕ Player 2",wins.get("O",0))
    with c3: st.markdown(f"<div style='text-align:center;font-family:Orbitron;font-size:20px;color:{'#00f5ff' if turn=='X' else '#ff006e'};padding:10px'>Turn: {'❌ P1' if turn=='X' else '⭕ P2'}</div>",unsafe_allow_html=True)
    if msg:
        cls="ok" if "Wins" in msg else "inf"
        st.markdown(f"<div class='{cls}' style='font-size:15px;padding:12px;margin-bottom:10px'>{msg}</div>",unsafe_allow_html=True)
    _,mc,_=st.columns([1,2,1])
    with mc:
        for row in range(3):
            rc=st.columns(3)
            for ci in range(3):
                idx=row*3+ci
                with rc[ci]:
                    cell=b[idx]
                    if cell=="X": st.markdown("""<div style="height:78px;background:rgba(0,245,255,.1);border:2px solid rgba(0,245,255,.5);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:36px;color:#00f5ff;animation:pp .2s ease">✕</div>""",unsafe_allow_html=True)
                    elif cell=="O": st.markdown("""<div style="height:78px;background:rgba(255,0,110,.1);border:2px solid rgba(255,0,110,.5);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:36px;color:#ff006e">○</div>""",unsafe_allow_html=True)
                    elif not over:
                        if st.button(" ",key=f"tt2_{idx}_{sum(1 for x in b if x)}",use_container_width=True):
                            b[idx]=turn; w=_tw(b)
                            if w:
                                wins[w]=wins.get(w,0)+1; st.session_state["tw2"]=wins
                                st.session_state.update({"ts2":f"{'❌ Player 1' if w=='X' else '⭕ Player 2'} Wins! 🎉","to2":True,"tb2":b})
                                earn(30); give_xp(15)
                            elif ""not in b: st.session_state.update({"ts2":"🤝 Draw!","to2":True,"tb2":b})
                            else: st.session_state.update({"turn2":"O" if turn=="X" else "X","tb2":b})
                            st.rerun()
                    else:
                        st.markdown("""<div style="height:78px;background:rgba(255,255,255,.02);border:2px solid rgba(255,255,255,.05);border-radius:10px"></div>""",unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    _,c2,_=st.columns([1,2,1])
    with c2:
        st.markdown('<div class="bG">',unsafe_allow_html=True)
        if st.button("🔄 New Round",use_container_width=True,key="tt2n"):
            st.session_state.update({"tb2":[""]*9,"turn2":"X","to2":False,"ts2":""}); st.rerun()
        st.markdown('</div>',unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
#  DICE RACE 2P
# ═══════════════════════════════════════════════════════
def page_dice2p():
    st.markdown("<h1 style='text-align:center'>🎲 Dice Race — 2 Players</h1><p style='text-align:center;color:#6677aa'>First to 100 wins! Roll or Hold each turn.</p>",unsafe_allow_html=True)
    if "dc2" not in st.session_state:
        st.session_state.update({"dc2":{"sc":[0,0],"turn":0,"cur":0,"dice":None,"over":False}})
    g=dict(st.session_state["dc2"]); sc=list(g["sc"]); turn=g["turn"]; cur=g["cur"]; over=g["over"]
    FACES=["","⚀","⚁","⚂","⚃","⚄","⚅"]
    cols_c=["#00f5ff","#ff006e"]
    c1,c2,c3=st.columns(3)
    with c1: st.metric("🟦 Player 1",sc[0])
    with c2: st.metric("🟥 Player 2",sc[1])
    with c3: st.metric("🎯 Banked",cur)
    if over:
        w=sc.index(max(sc))+1 if sc[0]!=sc[1] else 0
        e=earn(60); give_xp(30)
        st.markdown(f"<div class='ok' style='font-size:18px;padding:16px'>{'🏆 Player '+str(w)+' Wins!' if w else '🤝 Draw!'} +{e} coins</div>",unsafe_allow_html=True)
        _,mc,_=st.columns([1,2,1])
        with mc:
            st.markdown('<div class="bG">',unsafe_allow_html=True)
            if st.button("🔄 New Game",use_container_width=True,key="dc2n"):
                st.session_state["dc2"]={"sc":[0,0],"turn":0,"cur":0,"dice":None,"over":False}; st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)
        return
    st.markdown(f"<div class='inf' style='font-size:15px;padding:12px'>Turn: <b style='color:{cols_c[turn]}'>Player {turn+1}</b> | Current bank: {cur}</div>",unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    if g["dice"]: st.markdown(f"<div style='text-align:center;font-size:70px;filter:drop-shadow(0 0 12px {cols_c[turn]}80)'>{FACES[g['dice']]}</div>",unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    c1,c2,_=st.columns([1,1,1])
    with c1:
        st.markdown(f'<div style="color:{cols_c[turn]}">',unsafe_allow_html=True)
        if st.button("🎲 Roll",use_container_width=True,key="dc2r"):
            d=random.randint(1,6); g["dice"]=d
            if d==1: g["cur"]=0; g["turn"]=1-turn; g["dice"]=d
            else:
                g["cur"]=cur+d
                if sc[turn]+g["cur"]>=100:
                    sc[turn]+=g["cur"]; g["sc"]=sc; g["over"]=True
            st.session_state["dc2"]=g; st.rerun()
        st.markdown('</div>',unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="bg">',unsafe_allow_html=True)
        if st.button("✋ Hold",use_container_width=True,key="dc2h",disabled=cur==0):
            sc[turn]+=cur; g["sc"]=sc; g["cur"]=0; g["turn"]=1-turn; g["dice"]=None
            st.session_state["dc2"]=g; st.rerun()
        st.markdown('</div>',unsafe_allow_html=True)
    for i in range(2):
        st.markdown(f"<div style='font-size:11px;color:{cols_c[i]};margin:6px 0 2px'>Player {i+1}: {sc[i]}/100</div>",unsafe_allow_html=True)
        st.progress(min(sc[i]/100,1.0))

# ═══════════════════════════════════════════════════════
#  MINESWEEPER 2P
# ═══════════════════════════════════════════════════════
def _ms2_init():
    rows=8; cols_n=8; mines=12
    board=[[0]*cols_n for _ in range(rows)]
    mset=set(random.sample(range(rows*cols_n),mines))
    for p in mset: board[p//cols_n][p%cols_n]=-1
    for r in range(rows):
        for c in range(cols_n):
            if board[r][c]==-1: continue
            board[r][c]=sum(1 for dr in[-1,0,1] for dc in[-1,0,1] if 0<=r+dr<rows and 0<=c+dc<cols_n and board[r+dr][c+dc]==-1)
    st.session_state.update({"ms2_b":board,"ms2_rev":set(),"ms2_turn":0,"ms2_sc":[0,0],"ms2_over":False})

def page_ms2p():
    st.markdown("<h1 style='text-align:center'>💣 Minesweeper — 2 Players</h1><p style='text-align:center;color:#6677aa'>Take turns revealing cells. Most safe cells wins!</p>",unsafe_allow_html=True)
    if "ms2_b" not in st.session_state: _ms2_init()
    b=st.session_state["ms2_b"]; rev=st.session_state["ms2_rev"]
    turn=S("ms2_turn",0); sc=list(S("ms2_sc",[0,0])); over=S("ms2_over",False)
    rows=8; cols_n=8; mines=12
    cc=["#00f5ff","#ff006e"]
    c1,c2,c3=st.columns(3)
    with c1: st.metric("🟦 Player 1",sc[0])
    with c2: st.metric("🟥 Player 2",sc[1])
    with c3: st.metric("💣 Mines",mines)
    if not over: st.markdown(f"<div class='inf'>Turn: <b style='color:{cc[turn]}'>Player {turn+1}</b></div>",unsafe_allow_html=True)
    else:
        w=sc.index(max(sc))+1 if sc[0]!=sc[1] else 0
        e=earn(50)
        st.markdown(f"<div class='ok' style='font-size:16px;padding:12px'>{'🏆 Player '+str(w)+' Wins!' if w else '🤝 Draw!'} +{e} coins</div>",unsafe_allow_html=True)
        _,mc,_=st.columns([1,2,1])
        with mc:
            st.markdown('<div class="bG">',unsafe_allow_html=True)
            if st.button("🔄 New Game",use_container_width=True,key="ms2n"): _ms2_init(); st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)
        return
    COLORS={0:"#555",1:"#00f5ff",2:"#39ff14",3:"#ff006e",4:"#bf5fff",5:"#ff7c00",6:"#ffd60a",7:"#fff",8:"#888"}
    _,mc,_=st.columns([1,6,1])
    with mc:
        for r in range(rows):
            rc=st.columns(cols_n)
            for c in range(cols_n):
                idx=r*cols_n+c; cell=b[r][c]
                with rc[c]:
                    if idx in rev:
                        if cell==-1: st.markdown("""<div style="height:34px;background:rgba(255,0,110,.18);border:1px solid rgba(255,0,110,.45);border-radius:5px;display:flex;align-items:center;justify-content:center;font-size:14px">💥</div>""",unsafe_allow_html=True)
                        else:
                            col_c=COLORS.get(cell,"#fff"); txt=str(cell) if cell else "·"
                            st.markdown(f"""<div style="height:34px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.06);border-radius:5px;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;color:{col_c}">{txt}</div>""",unsafe_allow_html=True)
                    else:
                        if st.button("?",key=f"ms2_{idx}_{len(rev)}",use_container_width=True):
                            if idx in rev: st.rerun()
                            cr,cc2=idx//cols_n,idx%cols_n
                            if b[cr][cc2]==-1:
                                rev.add(idx); st.session_state["ms2_rev"]=rev
                                st.session_state["ms2_turn"]=1-turn
                                if sum(1 for i in rev if b[i//cols_n][i%cols_n]!=-1)>=rows*cols_n-mines:
                                    st.session_state["ms2_over"]=True
                                st.rerun()
                            else:
                                stack=[idx]; gained=0
                                while stack:
                                    cur=stack.pop()
                                    if cur in rev: continue
                                    rev.add(cur); gained+=1
                                    cr2,cc3=cur//cols_n,cur%cols_n
                                    if b[cr2][cc3]==0:
                                        for dr in[-1,0,1]:
                                            for dc in[-1,0,1]:
                                                ni=(cr2+dr)*cols_n+(cc3+dc)
                                                if 0<=cr2+dr<rows and 0<=cc3+dc<cols_n and ni not in rev: stack.append(ni)
                                sc[turn]+=gained; st.session_state["ms2_sc"]=sc
                                st.session_state["ms2_rev"]=rev; st.session_state["ms2_turn"]=1-turn
                                if sum(1 for i in rev if b[i//cols_n][i%cols_n]!=-1)>=rows*cols_n-mines:
                                    st.session_state["ms2_over"]=True
                                st.rerun()

# ═══════════════════════════════════════════════════════
#  SHOP
# ═══════════════════════════════════════════════════════
def page_shop():
    coins=S("coins",0)
    st.markdown(f"""<div style="text-align:center;margin-bottom:18px">
<h1>🛒 Upgrade Shop</h1>
<div style="display:inline-flex;align-items:center;gap:10px;padding:10px 22px;
background:rgba(255,214,10,.06);border:1px solid rgba(255,214,10,.28);border-radius:9px;margin-top:6px">
<span style="font-size:22px">💰</span>
<span style="font-family:Orbitron,sans-serif;font-size:22px;font-weight:900;color:#ffd60a;
text-shadow:0 0 10px rgba(255,214,10,.6)">{coins:,}</span>
<span style="color:#6677aa;font-size:12px">coins available</span>
</div></div>""", unsafe_allow_html=True)

    by_game={}
    for uid,item in SHOP.items(): by_game.setdefault(item["game"],[]).append((uid,item))
    tab_order=["Global","Snake","Flappy","Memory","Clicker","Slots","XO","Pong"]
    tabs=st.tabs([f"{'🌐' if g=='Global' else ''} {g}" for g in tab_order if g in by_game])
    for ti,game in enumerate([g for g in tab_order if g in by_game]):
        with tabs[ti]:
            items=by_game[game]
            cols=st.columns(min(len(items),3))
            for i,(uid,item) in enumerate(items):
                cnt=oc(uid); mx=item["max"]; maxed=cnt>=mx; can=coins>=item["price"] and not maxed
                col_="#39ff14" if maxed else("#ffd60a" if can else "#6677aa")
                bg_="rgba(57,255,20,.06)" if maxed else "rgba(255,255,255,.02)"
                brd_="rgba(57,255,20,.36)" if maxed else("rgba(255,214,10,.3)" if can else "rgba(255,255,255,.05)")
                badge=(f"<span style='position:absolute;top:6px;right:6px;background:rgba(57,255,20,.14);border:1px solid rgba(57,255,20,.42);border-radius:4px;padding:1px 6px;font-size:9px;color:#39ff14;font-weight:700'>MAX</span>") if maxed else \
                      (f"<span style='position:absolute;top:6px;right:6px;background:rgba(255,214,10,.1);border:1px solid rgba(255,214,10,.35);border-radius:4px;padding:1px 6px;font-size:9px;color:#ffd60a;font-weight:700'>{cnt}/{mx}</span>") if cnt else ""
                with cols[i%3]:
                    # Animated hover card
                    st.markdown(f"""<div style="background:{bg_};border:1px solid {brd_};border-radius:11px;
padding:16px;text-align:center;margin-bottom:8px;min-height:135px;position:relative;
transition:all .2s ease;">
{badge}
<div style="font-size:30px;margin-bottom:6px;filter:drop-shadow(0 0 8px {col_}60)">{item['icon']}</div>
<div style="font-weight:700;font-size:12px;color:{col_};margin-bottom:3px">{item['name']}</div>
<div style="color:#6677aa;font-size:10px;margin-bottom:9px;line-height:1.4">{item['desc']}</div>
<div style="font-family:Orbitron,sans-serif;font-size:13px;font-weight:900;
color:{'#39ff14' if maxed else '#ffd60a'}">{'MAX ✓' if maxed else f'💰 {item["price"]:,}'}</div>
</div>""",unsafe_allow_html=True)
                    if not maxed:
                        st.markdown(f'<div class="{"bg" if can else ""}">',unsafe_allow_html=True)
                        label="🛒 Buy" if can else "🔒 Need more"
                        if st.button(label,key=f"sh_{uid}_{cnt}",use_container_width=True,disabled=not can):
                            ok,msg=buy_item(uid)
                            if ok: st.balloons(); st.rerun()
                            else: st.markdown(f"<div class='err'>{msg}</div>",unsafe_allow_html=True)
                        st.markdown('</div>',unsafe_allow_html=True)

    owned={k:v for k,v in S("owned",{}).items() if v>0}
    if owned:
        st.markdown("---")
        st.markdown("<h3 style='font-size:14px'>🎒 My Upgrades</h3>",unsafe_allow_html=True)
        b="".join(f"<span style='display:inline-flex;padding:4px 10px;background:rgba(57,255,20,.06);"
                  f"border:1px solid rgba(57,255,20,.28);border-radius:12px;font-size:11px;"
                  f"font-weight:700;color:#39ff14;margin:2px'>{SHOP[uid]['icon']} {SHOP[uid]['name']}"
                  f"{' ×'+str(v) if v>1 else ''}</span>"
                  for uid,v in owned.items() if uid in SHOP)
        st.markdown(f"<div style='display:flex;flex-wrap:wrap;gap:2px'>{b}</div>",unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<h3 style='font-size:14px'>💰 How to Earn Coins</h3>",unsafe_allow_html=True)
    tips=[("🐍 Snake","Play & set high scores"),("🐦 Flappy","Pass pipes"),("🧠 Memory","Fewer moves = more coins"),
          ("❌ XO","Win vs AI = 50 coins"),("👆 Clicker","Clicks × 2"),("🎰 Slots","Match symbols"),
          ("🏓 Pong","Beat the AI"),("💣 Mines","Clear the field = 80 coins"),("🎯 Targets","Hit targets"),("🎲 Dice","Win race"),]
    cols=st.columns(5)
    for i,(ico,tip) in enumerate(tips):
        with cols[i%5]:
            st.markdown(f"""<div style="background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.06);
border-radius:8px;padding:10px;text-align:center;margin-bottom:6px">
<div style="font-size:20px;margin-bottom:4px">{ico}</div>
<div style="color:#6677aa;font-size:10px">{tip}</div></div>""",unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
#  ROUTER
# ═══════════════════════════════════════════════════════
ROUTES = {
    "lobby":      page_lobby,
    "snake":      page_snake,
    "flappy":     page_flappy,
    "memory":     page_memory,
    "ttt":        page_ttt,
    "clicker":    page_clicker,
    "slots":      page_slot,
    "pong":       page_pong,
    "minesweeper":page_minesweeper,
    "guess":      page_guess,
    "targets":    page_targets,
    "wordgame":   page_wordgame,
    "pong2p":     page_pong2p,
    "ttt2p":      page_ttt2p,
    "dice2p":     page_dice2p,
    "ms2p":       page_ms2p,
    "shop":       page_shop,
}

def main():
    inject_css()
    init()
    top_nav()
    page=S("page","lobby")
    ROUTES.get(page, page_lobby)()

if __name__=="__main__":
    main()
