"""
🎮 ARCADE GALAXY v5 — Insane Graphics Edition
Run: pip install streamlit && streamlit run project.py
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
#  CSS — Insane Galaxy Theme
# ═══════════════════════════════════════════════════════
def inject_css():
    st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;600;700&family=Share+Tech+Mono&display=swap');
:root{
  --bg:#04040f;--card:#080818;--card2:#0c0c20;
  --cyan:#00f5ff;--pink:#ff006e;--gold:#ffd60a;
  --green:#39ff14;--purple:#bf5fff;--orange:#ff7c00;
  --blue:#4488ff;--dim:#5566aa;--fg:#ccd0ff;
  --glow-c:rgba(0,245,255,.5);--glow-p:rgba(255,0,110,.5);--glow-g:rgba(255,214,10,.5);
}
html,body,.stApp{background:var(--bg)!important;font-family:'Rajdhani',sans-serif!important;color:var(--fg)!important;}
.stApp{
  background-image:
    radial-gradient(ellipse 80% 50% at 20% 20%,rgba(0,245,255,.06),transparent),
    radial-gradient(ellipse 60% 40% at 80% 80%,rgba(191,95,255,.05),transparent),
    radial-gradient(ellipse 40% 60% at 50% 50%,rgba(255,0,110,.03),transparent)
  !important;
}
.main .block-container{padding:0 16px 32px!important;max-width:100%!important;}
section[data-testid="stSidebar"]{display:none!important;}
h1,h2,h3{font-family:'Orbitron',sans-serif!important;color:var(--cyan)!important;}
/* Buttons */
.stButton>button{
  background:linear-gradient(135deg,rgba(0,245,255,.08),rgba(0,245,255,.02))!important;
  color:var(--cyan)!important;border:1px solid rgba(0,245,255,.25)!important;
  border-radius:8px!important;font-family:'Rajdhani',sans-serif!important;
  font-weight:700!important;font-size:14px!important;letter-spacing:.5px!important;
  transition:all .18s cubic-bezier(.4,0,.2,1)!important;
  text-shadow:0 0 8px rgba(0,245,255,.4)!important;
}
.stButton>button:hover{
  background:rgba(0,245,255,.16)!important;border-color:var(--cyan)!important;
  box-shadow:0 0 20px rgba(0,245,255,.3),inset 0 0 20px rgba(0,245,255,.05)!important;
  transform:translateY(-2px) scale(1.01)!important;
}
.stButton>button:active{transform:translateY(0) scale(.99)!important;}
.stButton>button:disabled{opacity:.25!important;transform:none!important;}
/* Colour variants */
.bg .stButton>button{background:linear-gradient(135deg,rgba(255,214,10,.1),rgba(255,214,10,.03))!important;color:var(--gold)!important;border-color:rgba(255,214,10,.35)!important;text-shadow:0 0 8px rgba(255,214,10,.4)!important;}
.bg .stButton>button:hover{background:rgba(255,214,10,.18)!important;box-shadow:0 0 20px rgba(255,214,10,.35)!important;}
.br .stButton>button{background:linear-gradient(135deg,rgba(255,0,110,.1),rgba(255,0,110,.03))!important;color:var(--pink)!important;border-color:rgba(255,0,110,.35)!important;text-shadow:0 0 8px rgba(255,0,110,.4)!important;}
.br .stButton>button:hover{background:rgba(255,0,110,.18)!important;box-shadow:0 0 20px rgba(255,0,110,.35)!important;}
.bG .stButton>button{background:linear-gradient(135deg,rgba(57,255,20,.08),rgba(57,255,20,.02))!important;color:var(--green)!important;border-color:rgba(57,255,20,.3)!important;text-shadow:0 0 8px rgba(57,255,20,.4)!important;}
.bG .stButton>button:hover{background:rgba(57,255,20,.15)!important;box-shadow:0 0 20px rgba(57,255,20,.3)!important;}
.bp .stButton>button{background:linear-gradient(135deg,rgba(191,95,255,.1),rgba(191,95,255,.03))!important;color:var(--purple)!important;border-color:rgba(191,95,255,.35)!important;}
/* Metrics */
[data-testid="metric-container"]{
  background:linear-gradient(135deg,rgba(0,245,255,.04),rgba(0,0,0,.3))!important;
  border:1px solid rgba(0,245,255,.14)!important;border-radius:10px!important;
  padding:12px!important;backdrop-filter:blur(8px)!important;
  box-shadow:inset 0 1px 0 rgba(0,245,255,.08)!important;
}
[data-testid="metric-container"] label{color:var(--dim)!important;font-size:11px!important;font-family:'Share Tech Mono',monospace!important;letter-spacing:1px!important;}
[data-testid="metric-container"] [data-testid="stMetricValue"]{color:var(--cyan)!important;font-family:'Orbitron',sans-serif!important;font-size:22px!important;text-shadow:0 0 12px rgba(0,245,255,.5)!important;}
/* Alerts */
.ok{padding:12px 16px;background:linear-gradient(135deg,rgba(57,255,20,.08),rgba(57,255,20,.02));border:1px solid rgba(57,255,20,.4);border-radius:10px;color:var(--green);font-weight:700;text-align:center;box-shadow:0 0 20px rgba(57,255,20,.1);font-family:'Rajdhani',sans-serif;font-size:15px;}
.err{padding:12px 16px;background:linear-gradient(135deg,rgba(255,0,110,.08),rgba(255,0,110,.02));border:1px solid rgba(255,0,110,.4);border-radius:10px;color:var(--pink);font-weight:700;text-align:center;box-shadow:0 0 20px rgba(255,0,110,.1);font-family:'Rajdhani',sans-serif;font-size:15px;}
.inf{padding:12px 16px;background:linear-gradient(135deg,rgba(0,245,255,.06),rgba(0,245,255,.01));border:1px solid rgba(0,245,255,.25);border-radius:10px;color:var(--cyan);text-align:center;box-shadow:0 0 20px rgba(0,245,255,.08);font-family:'Rajdhani',sans-serif;}
.warn{padding:12px 16px;background:linear-gradient(135deg,rgba(255,214,10,.07),rgba(255,214,10,.01));border:1px solid rgba(255,214,10,.3);border-radius:10px;color:var(--gold);text-align:center;font-family:'Rajdhani',sans-serif;}
/* Progress */
.stProgress>div>div>div{background:linear-gradient(90deg,var(--cyan),var(--purple),var(--pink))!important;border-radius:4px!important;box-shadow:0 0 8px rgba(0,245,255,.4)!important;}
.stProgress>div>div{background:rgba(255,255,255,.04)!important;border-radius:4px!important;}
/* Misc */
hr{border:none!important;border-top:1px solid rgba(0,245,255,.08)!important;margin:20px 0!important;}
::-webkit-scrollbar{width:4px;}::-webkit-scrollbar-track{background:var(--bg);}::-webkit-scrollbar-thumb{background:rgba(0,245,255,.2);border-radius:2px;}
#MainMenu,footer,.stDeployButton{display:none!important;}
header[data-testid="stHeader"]{display:none!important;}
.stTabs [data-baseweb="tab-list"]{background:rgba(255,255,255,.02)!important;border-radius:8px!important;padding:3px!important;border:1px solid rgba(0,245,255,.1)!important;}
.stTabs [data-baseweb="tab"]{font-family:'Rajdhani',sans-serif!important;font-weight:700!important;color:var(--dim)!important;border-radius:6px!important;}
.stTabs [aria-selected="true"]{background:linear-gradient(135deg,rgba(0,245,255,.15),rgba(0,245,255,.05))!important;color:var(--cyan)!important;box-shadow:0 0 12px rgba(0,245,255,.2)!important;}
[data-testid="column"]{padding:0 4px!important;}
/* Number input */
.stNumberInput input{background:rgba(0,245,255,.04)!important;border:1px solid rgba(0,245,255,.2)!important;border-radius:8px!important;color:var(--fg)!important;font-family:'Share Tech Mono',monospace!important;}
/* Text input */
.stTextInput input{background:rgba(0,245,255,.04)!important;border:1px solid rgba(0,245,255,.2)!important;border-radius:8px!important;color:var(--fg)!important;font-family:'Orbitron',sans-serif!important;letter-spacing:3px!important;text-transform:uppercase!important;}
/* Slider */
.stSlider [data-baseweb="slider"] div[role="slider"]{background:var(--gold)!important;box-shadow:0 0 10px var(--gold)!important;}
/* Selectbox */
.stSelectbox select,.stSelectbox [data-baseweb="select"] div{background:rgba(0,245,255,.04)!important;border-color:rgba(0,245,255,.2)!important;color:var(--fg)!important;}
</style>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
#  TOP NAV BAR
# ═══════════════════════════════════════════════════════
def top_nav():
    lv=S("level",1); coins=S("coins",0); xpv=S("xp",0); need=lv*120
    pct=int(xpv/need*100)
    st.markdown(f"""
<div style="display:flex;align-items:center;justify-content:space-between;
  padding:10px 24px;
  background:linear-gradient(180deg,rgba(4,4,20,.95),rgba(4,4,15,.9));
  border-bottom:1px solid rgba(0,245,255,.1);
  backdrop-filter:blur(20px);position:sticky;top:0;z-index:999;margin-bottom:20px;
  box-shadow:0 4px 30px rgba(0,0,0,.5)">
  <div style="display:flex;align-items:center;gap:12px">
    <div style="font-size:34px;animation:logoPulse 3s ease-in-out infinite;filter:drop-shadow(0 0 14px rgba(0,245,255,.9))">🎮</div>
    <div>
      <div style="font-family:'Orbitron',sans-serif;font-size:20px;font-weight:900;
        background:linear-gradient(90deg,#00f5ff,#bf5fff,#ff006e);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;
        background-size:200%;animation:gradShift 4s linear infinite;letter-spacing:4px">ARCADE GALAXY</div>
      <div style="font-size:10px;color:#5566aa;letter-spacing:3px;margin-top:-2px">ULTIMATE EDITION</div>
    </div>
  </div>
  <div style="display:flex;align-items:center;gap:10px">
    <div style="background:linear-gradient(135deg,rgba(255,214,10,.12),rgba(255,214,10,.04));
      border:1px solid rgba(255,214,10,.4);border-radius:10px;padding:8px 16px;
      display:flex;align-items:center;gap:8px;box-shadow:0 0 16px rgba(255,214,10,.1)">
      <span style="font-size:18px">💰</span>
      <span style="font-family:'Orbitron',sans-serif;font-size:18px;font-weight:900;color:#ffd60a;
        text-shadow:0 0 12px rgba(255,214,10,.7)">{coins:,}</span>
    </div>
    <div style="background:linear-gradient(135deg,rgba(0,245,255,.08),rgba(0,245,255,.02));
      border:1px solid rgba(0,245,255,.2);border-radius:10px;padding:8px 14px;min-width:100px">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">
        <span style="font-family:'Orbitron',sans-serif;font-size:11px;color:#00f5ff;font-weight:700">LV {lv}</span>
        <span style="font-size:9px;color:#5566aa;font-family:'Share Tech Mono',monospace">{xpv}/{need}</span>
      </div>
      <div style="background:rgba(255,255,255,.05);border-radius:3px;height:4px;overflow:hidden">
        <div style="background:linear-gradient(90deg,#00f5ff,#bf5fff);width:{pct}%;height:100%;
          border-radius:3px;box-shadow:0 0 6px rgba(0,245,255,.6);transition:width .3s ease"></div>
      </div>
    </div>
  </div>
</div>
<style>
@keyframes logoPulse{{0%,100%{{filter:drop-shadow(0 0 14px rgba(0,245,255,.9)) drop-shadow(0 0 28px rgba(0,245,255,.4))}}50%{{filter:drop-shadow(0 0 22px rgba(0,245,255,1)) drop-shadow(0 0 44px rgba(0,245,255,.6))}}}}
@keyframes gradShift{{0%{{background-position:0%}}100%{{background-position:200%}}}}
</style>""", unsafe_allow_html=True)

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
    ("snake","🐍","Snake","#39ff14","Control the snake, eat food!","snake_hi","1P"),
    ("flappy","🐦","Flappy Bird","#ffd60a","Fly between pipes!","flappy_hi","1P"),
    ("memory","🧠","Memory","#bf5fff","Find all matching pairs!","mem_hi","1P"),
    ("ttt","❌","Tic-Tac-Toe","#00f5ff","Beat the AI!","ttt_w","1P"),
    ("clicker","👆","Clicker","#ff006e","Click as fast as you can!","click_hi","1P"),
    ("slots","🎰","Slot Machine","#ff7c00","Spin to win the jackpot!","slot_w","1P"),
    ("pong","🏓","Pong (1P)","#00f5ff","Beat the AI paddle!","pong_hi","1P"),
    ("minesweeper","💣","Minesweeper","#ff006e","Find all safe cells!",None,"1P"),
    ("guess","🔢","Number Guess","#39ff14","Guess the secret number!",None,"1P"),
    ("targets","🎯","Target Shot","#ffd60a","Hit targets before they vanish!",None,"1P"),
    ("wordgame","🔤","Word Guess","#bf5fff","Guess the 5-letter word!",None,"1P"),
    ("pong2p","🏓","Pong (2P)","#00f5ff","Two players, one keyboard",None,"2P"),
    ("ttt2p","❌","Tic-Tac-Toe 2P","#bf5fff","Two players on same screen",None,"2P"),
    ("dice2p","🎲","Dice Race 2P","#ffd60a","First to 100 wins!",None,"2P"),
    ("ms2p","💣","Minesweeper 2P","#ff006e","Take turns uncovering cells!",None,"2P"),
]

def page_lobby():
    # Hero
    st.markdown("""<div style="text-align:center;padding:16px 0 30px">
<div style="font-size:64px;display:inline-block;animation:heroFloat 3s ease-in-out infinite;
  filter:drop-shadow(0 0 20px rgba(0,245,255,.9)) drop-shadow(0 0 40px rgba(0,245,255,.4))">🎮</div>
<h1 style="font-family:'Orbitron',sans-serif;font-size:36px;font-weight:900;margin:10px 0 6px;
  background:linear-gradient(90deg,#00f5ff,#bf5fff,#ff006e,#ffd60a,#00f5ff);background-size:400%;
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:sh 5s linear infinite;
  text-shadow:none;letter-spacing:4px">ARCADE GALAXY</h1>
<p style="color:#5566aa;letter-spacing:4px;font-size:12px;margin:0">15 GAMES · 2-PLAYER · UPGRADES</p>
</div>
<style>
@keyframes heroFloat{0%,100%{transform:translateY(0) rotate(0deg)}33%{transform:translateY(-10px) rotate(-3deg)}66%{transform:translateY(-5px) rotate(3deg)}}
@keyframes sh{0%{background-position:0%}100%{background-position:400%}}
</style>""", unsafe_allow_html=True)

    lv=S("level",1); xpv=S("xp",0); need=lv*120
    c1,c2,c3,c4=st.columns(4)
    with c1: st.metric("💎 Level",lv)
    with c2: st.metric("💰 Coins",f"{S('coins',0):,}")
    with c3: st.metric("🏆 Achievements",len(S("ach",[])))
    with c4:
        total=sum(S(k,0) for k in["snake_pl","flappy_pl","mem_pl","ttt_pl","click_ses","slot_sp","pong_pl"])
        st.metric("🎮 Games Played",total)
    st.markdown("<br>",unsafe_allow_html=True)

    # 1P games
    st.markdown("""<div style="display:flex;align-items:center;gap:12px;margin-bottom:16px">
<div style="height:1px;flex:1;background:linear-gradient(90deg,transparent,rgba(0,245,255,.3))"></div>
<span style="font-family:'Orbitron',sans-serif;font-size:12px;color:#00f5ff;letter-spacing:3px">🕹️ SINGLE PLAYER</span>
<div style="height:1px;flex:1;background:linear-gradient(90deg,rgba(0,245,255,.3),transparent)"></div>
</div>""", unsafe_allow_html=True)

    sp_games=[g for g in GAME_CARDS if g[6]=="1P"]
    cols=st.columns(4)
    for i,g in enumerate(sp_games):
        key,ico,name,col,desc,hi_key,_=g
        hi_val=S(hi_key,0) if hi_key else ""
        with cols[i%4]:
            best_str=f"Best: {hi_val}" if hi_val else "Play to set record"
            st.markdown(f"""<div style="
  background:linear-gradient(145deg,{col}09,rgba(4,4,20,.95));
  border:1px solid {col}30;border-radius:14px;text-align:center;
  padding:18px 10px 14px;margin-bottom:6px;
  box-shadow:0 4px 20px {col}10,inset 0 1px 0 {col}18;
  transition:all .2s ease;position:relative;overflow:hidden">
  <div style="position:absolute;top:0;left:0;right:0;height:2px;
    background:linear-gradient(90deg,transparent,{col}80,transparent)"></div>
  <div style="font-size:40px;margin-bottom:8px;filter:drop-shadow(0 0 12px {col}80)">{ico}</div>
  <div style="font-family:'Orbitron',sans-serif;font-size:11px;font-weight:900;
    color:{col};margin-bottom:4px;letter-spacing:1px;
    text-shadow:0 0 10px {col}70">{name}</div>
  <div style="color:#5566aa;font-size:11px;margin-bottom:10px;font-family:'Rajdhani',sans-serif">{desc}</div>
  <div style="font-size:10px;color:{col}80;font-family:'Share Tech Mono',monospace">{best_str}</div>
</div>""", unsafe_allow_html=True)
            if st.button(f"▶ Play", key=f"lobby_{key}", use_container_width=True):
                nav(key); st.rerun()

    st.markdown("<br>",unsafe_allow_html=True)
    st.markdown("""<div style="display:flex;align-items:center;gap:12px;margin-bottom:16px">
<div style="height:1px;flex:1;background:linear-gradient(90deg,transparent,rgba(255,0,110,.3))"></div>
<span style="font-family:'Orbitron',sans-serif;font-size:12px;color:#ff006e;letter-spacing:3px">👥 TWO PLAYERS</span>
<div style="height:1px;flex:1;background:linear-gradient(90deg,rgba(255,0,110,.3),transparent)"></div>
</div>""", unsafe_allow_html=True)

    mp_games=[g for g in GAME_CARDS if g[6]=="2P"]
    cols2=st.columns(4)
    for i,g in enumerate(mp_games):
        key,ico,name,col,desc,_,__=g
        with cols2[i%4]:
            st.markdown(f"""<div style="
  background:linear-gradient(145deg,{col}09,rgba(4,4,20,.95));
  border:1px solid {col}30;border-radius:14px;text-align:center;
  padding:18px 10px 14px;margin-bottom:6px;
  box-shadow:0 4px 20px {col}10,inset 0 1px 0 {col}18;
  position:relative;overflow:hidden">
  <div style="position:absolute;top:0;left:0;right:0;height:2px;
    background:linear-gradient(90deg,transparent,{col}80,transparent)"></div>
  <div style="font-size:40px;margin-bottom:8px;filter:drop-shadow(0 0 12px {col}80)">{ico}</div>
  <div style="font-family:'Orbitron',sans-serif;font-size:11px;font-weight:900;color:{col};
    margin-bottom:4px;letter-spacing:1px">{name}</div>
  <div style="color:#5566aa;font-size:11px;margin-bottom:10px">{desc}</div>
  <div style="font-size:10px;color:{col}80;font-family:'Share Tech Mono',monospace">👥 Local Multiplayer</div>
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
        st.markdown("<h3 style='font-size:14px;letter-spacing:2px'>🏆 ACHIEVEMENTS</h3>",unsafe_allow_html=True)
        b="".join(f"<span style='display:inline-flex;padding:5px 12px;"
                  f"background:linear-gradient(135deg,rgba(255,214,10,.08),rgba(255,214,10,.02));"
                  f"border:1px solid rgba(255,214,10,.3);border-radius:16px;font-size:11px;"
                  f"font-weight:700;color:#ffd60a;margin:2px;font-family:Rajdhani,sans-serif;"
                  f"box-shadow:0 0 10px rgba(255,214,10,.08)'>{a}</span>" for a in achs[-15:])
        st.markdown(f"<div style='display:flex;flex-wrap:wrap;gap:3px'>{b}</div>",unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
#  SNAKE
# ═══════════════════════════════════════════════════════
def page_snake():
    st.markdown("<h1 style='text-align:center;letter-spacing:3px'>🐍 SNAKE</h1>",unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#5566aa;font-family:Share Tech Mono,monospace'>ARROW KEYS or WASD to move</p>",unsafe_allow_html=True)
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
body{{background:#04040f;display:flex;flex-direction:column;align-items:center;padding:10px;user-select:none}}
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Share+Tech+Mono&display=swap');
.hud{{display:flex;gap:10px;margin-bottom:10px;font-family:'Share Tech Mono',monospace;flex-wrap:wrap;justify-content:center}}
.h{{background:linear-gradient(135deg,rgba(57,255,20,.08),rgba(57,255,20,.02));
  border:1px solid rgba(57,255,20,.3);border-radius:8px;padding:5px 14px;color:#39ff14;font-size:12px;
  box-shadow:0 0 10px rgba(57,255,20,.08)}}
canvas{{border:2px solid rgba(57,255,20,.25);border-radius:12px;
  box-shadow:0 0 40px rgba(57,255,20,.12),0 0 80px rgba(57,255,20,.05);display:block}}
.ov{{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
  background:linear-gradient(145deg,rgba(4,4,20,.97),rgba(8,8,28,.97));
  border:1px solid rgba(57,255,20,.4);border-radius:16px;padding:24px 32px;
  text-align:center;min-width:190px;backdrop-filter:blur(20px);
  box-shadow:0 0 40px rgba(57,255,20,.15),inset 0 1px 0 rgba(57,255,20,.1)}}
.ov h2{{color:#39ff14;font-family:'Orbitron',sans-serif;font-size:18px;
  margin-bottom:8px;text-shadow:0 0 16px rgba(57,255,20,.7)}}
.ov p{{color:#8899bb;font-size:12px;margin-bottom:14px;font-family:'Share Tech Mono',monospace}}
.ov button{{background:linear-gradient(135deg,rgba(57,255,20,.2),rgba(57,255,20,.06));
  color:#39ff14;border:1px solid rgba(57,255,20,.5);padding:9px 22px;
  border-radius:8px;cursor:pointer;font-family:'Orbitron',sans-serif;font-size:12px;font-weight:700;
  transition:all .18s;box-shadow:0 0 14px rgba(57,255,20,.15)}}
.ov button:hover{{background:rgba(57,255,20,.3);box-shadow:0 0 24px rgba(57,255,20,.35)}}
.wrap{{position:relative}}</style></head><body>
<div class="hud">
  <div class="h">SCORE: <span id="sc">0</span></div>
  <div class="h">BEST: <span id="hi">{hi}</span></div>
  <div class="h">LIVES: <span id="lv">{lives}</span></div>
  <div class="h">SPEED: <span id="sp">1</span></div>
</div>
<div class="wrap"><canvas id="c"></canvas>
<div class="ov" id="ov"><h2>🐍 SNAKE</h2><p>Arrow keys or WASD</p>
<button onclick="startGame()">▶ PLAY</button></div></div>
<script>
const G=22,C=20;
const WP={wp},MAG={mag},ML={lives};
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
cv.width=cv.height=G*C;
let sn,dir,nd,food,bon,score,lv2,spd,loop,run,parts,trail;
function startGame(){{
  document.getElementById('ov').style.display='none';
  sn=[{{x:11,y:11}},{{x:10,y:11}},{{x:9,y:11}}];
  dir={{x:1,y:0}};nd={{x:1,y:0}};
  score=0;lv2=ML;spd=1;parts=[];bon=null;trail=[];run=true;
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
  if(score>0&&score%60===0&&!bon){{
    let b;do b={{x:Math.floor(Math.random()*G),y:Math.floor(Math.random()*G)}};
    while(sn.some(s=>s.x===b.x&&s.y===b.y));bon={{...b,t:120}};
  }}
}}
function spark(x,y,c,n=10){{
  for(let i=0;i<n;i++)parts.push({{
    x:x*C+C/2,y:y*C+C/2,
    vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,
    l:30,c,r:Math.random()*3+1
  }});
}}
function update(){{
  if(!run)return;
  dir={{...nd}};
  let h={{x:sn[0].x+dir.x,y:sn[0].y+dir.y}};
  if(WP){{h.x=(h.x+G)%G;h.y=(h.y+G)%G;}}
  else if(h.x<0||h.x>=G||h.y<0||h.y>=G){{die();return;}}
  if(sn.slice(1).some(s=>s.x===h.x&&s.y===h.y)){{die();return;}}
  if(MAG){{
    let dx=food.x-h.x,dy=food.y-h.y;
    if(Math.abs(dx)+Math.abs(dy)<=4){{
      if(dx)food.x+=dx>0?-1:1;else if(dy)food.y+=dy>0?-1:1;
    }}
  }}
  trail.push({{x:sn[0].x*C+C/2,y:sn[0].y*C+C/2,l:8}});
  if(trail.length>12)trail.shift();
  sn.unshift(h);let grew=false;
  if(h.x===food.x&&h.y===food.y){{
    score+=10;grew=true;
    spark(food.x,food.y,'#39ff14',12);
    placeFood();
    document.getElementById('sc').textContent=score;
    let ns=1+Math.floor(score/60);
    if(ns>spd){{spd=ns;clearInterval(loop);loop=setInterval(update,Math.max(60,155-spd*22));document.getElementById('sp').textContent=spd;}}
  }}
  if(bon&&h.x===bon.x&&h.y===bon.y){{score+=50;grew=true;spark(bon.x,bon.y,'#ffd60a',16);bon=null;document.getElementById('sc').textContent=score;}}
  if(!grew)sn.pop();
  if(bon){{bon.t--;if(!bon.t)bon=null;}}
  parts=parts.filter(p=>p.l>0);
  parts.forEach(p=>{{p.x+=p.vx;p.y+=p.vy;p.l--;p.vy+=.08;p.vx*=.97;}});
  trail=trail.filter(t=>t.l>0);trail.forEach(t=>t.l--);
  draw();
}}
function die(){{
  lv2--;document.getElementById('lv').textContent=lv2;
  spark(sn[0].x,sn[0].y,'#ff006e',20);
  if(lv2<=0){{
    run=false;clearInterval(loop);
    let hs=+document.getElementById('hi').textContent||0;
    if(score>hs)document.getElementById('hi').textContent=score;
    const ov=document.getElementById('ov');
    ov.querySelector('h2').textContent='💀 GAME OVER';
    ov.querySelector('p').textContent='Score: '+score;
    ov.style.display='block';
  }}else{{
    sn=[{{x:11,y:11}},{{x:10,y:11}},{{x:9,y:11}}];
    dir={{x:1,y:0}};nd={{x:1,y:0}};trail=[];
  }}
}}
function rr(x,y,w,h,r){{
  ctx.beginPath();ctx.moveTo(x+r,y);ctx.lineTo(x+w-r,y);
  ctx.quadraticCurveTo(x+w,y,x+w,y+r);ctx.lineTo(x+w,y+h-r);
  ctx.quadraticCurveTo(x+w,y+h,x+w-r,y+h);ctx.lineTo(x+r,y+h);
  ctx.quadraticCurveTo(x,y+h,x,y+h-r);ctx.lineTo(x,y+r);
  ctx.quadraticCurveTo(x,y,x+r,y);ctx.closePath();
}}
function draw(){{
  // Background
  ctx.fillStyle='#04040f';ctx.fillRect(0,0,G*C,G*C);
  // Grid
  ctx.strokeStyle='rgba(57,255,20,.04)';ctx.lineWidth=.5;
  for(let i=0;i<=G;i++){{
    ctx.beginPath();ctx.moveTo(i*C,0);ctx.lineTo(i*C,G*C);ctx.stroke();
    ctx.beginPath();ctx.moveTo(0,i*C);ctx.lineTo(G*C,i*C);ctx.stroke();
  }}
  // Trail
  trail.forEach((t,i)=>{{
    ctx.globalAlpha=t.l/8*.3;ctx.fillStyle='#39ff14';
    ctx.beginPath();ctx.arc(t.x,t.y,2,0,Math.PI*2);ctx.fill();
  }});ctx.globalAlpha=1;
  // Particles
  parts.forEach(p=>{{
    ctx.globalAlpha=p.l/30;ctx.fillStyle=p.c;
    ctx.shadowBlur=6;ctx.shadowColor=p.c;
    ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill();
    ctx.shadowBlur=0;
  }});ctx.globalAlpha=1;
  // Food
  let t=Date.now()/300;
  ctx.save();ctx.translate(food.x*C+C/2,food.y*C+C/2);
  ctx.scale(1+Math.sin(t)*.18,1+Math.sin(t)*.18);
  ctx.shadowBlur=20;ctx.shadowColor='#39ff14';
  ctx.fillStyle='#39ff14';ctx.beginPath();ctx.arc(0,0,C/2-2,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='rgba(255,255,255,.35)';ctx.beginPath();ctx.arc(-2,-2,C/5,0,Math.PI*2);ctx.fill();
  ctx.shadowBlur=0;ctx.restore();
  // Bonus star
  if(bon){{
    ctx.save();ctx.translate(bon.x*C+C/2,bon.y*C+C/2);
    ctx.rotate(Date.now()/400);ctx.scale(1+Math.sin(Date.now()/130)*.18,1+Math.sin(Date.now()/130)*.18);
    ctx.shadowBlur=24;ctx.shadowColor='#ffd60a';ctx.fillStyle='#ffd60a';
    ctx.font=(C-1)+'px serif';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('★',0,0);
    ctx.shadowBlur=0;ctx.restore();
    ctx.fillStyle='rgba(255,214,10,'+bon.t/120+')';ctx.fillRect(bon.x*C,bon.y*C-3,C*(bon.t/120),2);
  }}
  // Snake
  sn.forEach((seg,i)=>{{
    ctx.save();
    const ratio=i/sn.length;
    const baseG=215-ratio*90;
    if(i===0){{
      ctx.shadowBlur=16;ctx.shadowColor='rgba(57,255,20,.9)';
      ctx.fillStyle='#fff';
    }}else{{
      ctx.fillStyle=`rgba(0,${{Math.round(baseG)}},255,.9)`;
    }}
    let pd=i===0?1:2,rd=i===0?5:3;
    rr(seg.x*C+pd,seg.y*C+pd,C-pd*2,C-pd*2,rd);ctx.fill();
    if(i===0){{
      // Eyes
      ctx.shadowBlur=0;ctx.fillStyle='#04040f';
      ctx.beginPath();ctx.arc(seg.x*C+C*.3+dir.y*C*.2,seg.y*C+C*.3-dir.x*C*.2,2.2,0,Math.PI*2);ctx.fill();
      ctx.beginPath();ctx.arc(seg.x*C+C*.7-dir.y*C*.2,seg.y*C+C*.3-dir.x*C*.2,2.2,0,Math.PI*2);ctx.fill();
      // Pupils glow
      ctx.fillStyle='rgba(57,255,20,.6)';
      ctx.beginPath();ctx.arc(seg.x*C+C*.3+dir.y*C*.2,seg.y*C+C*.3-dir.x*C*.2,1,0,Math.PI*2);ctx.fill();
      ctx.beginPath();ctx.arc(seg.x*C+C*.7-dir.y*C*.2,seg.y*C+C*.3-dir.x*C*.2,1,0,Math.PI*2);ctx.fill();
    }}
    ctx.restore();
  }});
}}
ctx.fillStyle='#04040f';ctx.fillRect(0,0,G*C,G*C);
</script></body></html>""", height=G*C+100, scrolling=False)

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
    st.markdown("<h1 style='text-align:center;letter-spacing:3px'>🐦 FLAPPY BIRD</h1>",unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#5566aa;font-family:Share Tech Mono,monospace'>SPACE or CLICK to flap</p>",unsafe_allow_html=True)
    sh=oc("flappy_shield"); gap=110+oc("flappy_gap")*15
    slow_ps=1.7 if has("flappy_slow") else 2.5
    hi=S("flappy_hi",0)
    if sh or has("flappy_slow") or has("flappy_gap"):
        gap_count=oc("flappy_gap")
        parts=filter(None,[
            f'🛡 {sh} shields' if sh else '',
            '🐌 Slow pipes' if has("flappy_slow") else '',
            f'🔓 Gap +{gap_count*15}' if has("flappy_gap") else '',
        ])
        st.markdown(f"<div class='inf'>{'  |  '.join(parts)}</div>",unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    _,col,_=st.columns([1,8,1])
    with col:
        components.html(f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#04040f;display:flex;flex-direction:column;align-items:center;padding:10px;user-select:none}}
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Share+Tech+Mono&display=swap');
.hud{{display:flex;gap:10px;margin-bottom:10px;font-family:'Share Tech Mono',monospace}}
.h{{background:linear-gradient(135deg,rgba(255,214,10,.08),rgba(255,214,10,.02));
  border:1px solid rgba(255,214,10,.3);border-radius:8px;padding:5px 14px;color:#ffd60a;font-size:12px}}
canvas{{border:2px solid rgba(255,214,10,.3);border-radius:12px;
  box-shadow:0 0 40px rgba(255,214,10,.1),0 0 80px rgba(255,214,10,.04);cursor:pointer;display:block}}
.ov{{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
  background:linear-gradient(145deg,rgba(4,4,20,.97),rgba(8,8,28,.97));
  border:1px solid rgba(255,214,10,.4);border-radius:16px;padding:24px 32px;
  text-align:center;min-width:190px;backdrop-filter:blur(20px);
  box-shadow:0 0 40px rgba(255,214,10,.15),inset 0 1px 0 rgba(255,214,10,.1)}}
.ov h2{{color:#ffd60a;font-family:'Orbitron',sans-serif;font-size:18px;margin-bottom:8px;text-shadow:0 0 16px rgba(255,214,10,.7)}}
.ov p{{color:#8899bb;font-size:12px;margin-bottom:14px;font-family:'Share Tech Mono',monospace}}
.ov button{{background:linear-gradient(135deg,rgba(255,214,10,.2),rgba(255,214,10,.06));
  color:#ffd60a;border:1px solid rgba(255,214,10,.5);padding:9px 22px;
  border-radius:8px;cursor:pointer;font-family:'Orbitron',sans-serif;font-size:12px;font-weight:700;transition:all .18s}}
.ov button:hover{{background:rgba(255,214,10,.3)}}
.wrap{{position:relative}}</style></head><body>
<div class="hud">
  <div class="h">SCORE: <span id="sc">0</span></div>
  <div class="h">BEST: <span id="hi">{hi}</span></div>
  <div class="h">🛡 <span id="sh">{sh}</span></div>
</div>
<div class="wrap"><canvas id="c" width="340" height="460"></canvas>
<div class="ov" id="ov">
  <h2 id="ot">🐦 FLAPPY BIRD</h2>
  <p>SPACE or click to flap</p>
  <button onclick="startGame()">▶ PLAY</button>
</div></div>
<script>
const W=340,H=460,BR=13,PS={slow_ps},GAP={gap},ISH={sh};
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
let bird,pipes,score,frame,run,raf,shL,parts,stars,clouds;
function mkBg(){{
  stars=[];for(let i=0;i<70;i++)stars.push({{x:Math.random()*W,y:Math.random()*H*.72,r:Math.random()*1.5+.3,s:Math.random()*.2+.06,b:Math.random()}});
  clouds=[];for(let i=0;i<5;i++)clouds.push({{x:Math.random()*W,y:20+Math.random()*80,w:40+Math.random()*60,s:Math.random()*.3+.1}});
}}
function startGame(){{
  document.getElementById('ov').style.display='none';
  bird={{x:75,y:H/2,vy:0,rot:0}};pipes=[];score=0;frame=0;run=true;shL=ISH;parts=[];
  document.getElementById('sc').textContent='0';
  document.getElementById('sh').textContent=shL;
  if(raf)cancelAnimationFrame(raf);mkBg();loop();
}}
function flap(){{if(run){{bird.vy=-7.2;parts.push(...Array.from({{length:4}},()=>({{'type':'flap',x:bird.x-BR,y:bird.y,vx:-Math.random()*2-1,vy:(Math.random()-.5)*2,l:15}})))}}}}
cv.addEventListener('click',flap);
document.addEventListener('keydown',e=>{{if(e.code==='Space'){{flap();e.preventDefault();}}}});
function loop(){{if(!run)return;update();draw();raf=requestAnimationFrame(loop);}}
function update(){{
  frame++;bird.vy+=.35;bird.y+=bird.vy;bird.rot=Math.min(Math.max(bird.vy*3.5,-35),90);
  parts=parts.filter(p=>p.l>0);
  parts.forEach(p=>{{p.x+=p.vx;p.y+=p.vy;p.l--;if(p.type!=='flap')p.vy+=.1;}});
  stars.forEach(s=>{{s.x-=s.s;if(s.x<0){{s.x=W;s.y=Math.random()*H*.72;}}}});
  clouds.forEach(c=>{{c.x-=c.s;if(c.x+c.w<0)c.x=W+c.w;}});
  if(frame%85===0)pipes.push({{x:W,th:55+Math.random()*(H-GAP-105),ok:false}});
  pipes.forEach(p=>p.x-=PS);
  pipes=pipes.filter(p=>p.x>-55);
  pipes.forEach(p=>{{
    if(!p.ok&&p.x+45<bird.x){{
      p.ok=true;score++;document.getElementById('sc').textContent=score;
      for(let i=0;i<8;i++)parts.push({{type:'score',x:bird.x,y:bird.y,vx:(Math.random()-.5)*5,vy:-Math.random()*4,l:28,c:'#ffd60a'}});
    }}
    if(bird.x+BR>p.x&&bird.x-BR<p.x+46&&(bird.y-BR<p.th||bird.y+BR>p.th+GAP)){{
      if(shL>0){{
        shL--;document.getElementById('sh').textContent=shL;
        for(let i=0;i<16;i++)parts.push({{type:'shield',x:bird.x,y:bird.y,vx:(Math.random()-.5)*7,vy:(Math.random()-.5)*7,l:30,c:'#00f5ff'}});
      }}else die();
    }}
  }});
  if(bird.y+BR>H-28||bird.y-BR<0)die();
}}
function die(){{
  run=false;cancelAnimationFrame(raf);
  let hs=+document.getElementById('hi').textContent||0;
  if(score>hs)document.getElementById('hi').textContent=score;
  document.getElementById('ot').textContent='💥 CRASHED!';
  document.getElementById('ov').querySelector('p').textContent='Score: '+score;
  document.getElementById('ov').style.display='block';
}}
function drawPipe(x,th){{
  // Pipe body gradient
  let g=ctx.createLinearGradient(x,0,x+46,0);
  g.addColorStop(0,'#0d3d12');g.addColorStop(.4,'#1a6b20');g.addColorStop(.6,'#1a6b20');g.addColorStop(1,'#0d3d12');
  ctx.fillStyle=g;
  ctx.fillRect(x,0,46,th);
  ctx.fillRect(x,th+GAP,46,H-(th+GAP));
  // Cap
  let cg=ctx.createLinearGradient(x-5,0,x+51,0);
  cg.addColorStop(0,'#0d3d12');cg.addColorStop(.4,'#28a030');cg.addColorStop(.6,'#28a030');cg.addColorStop(1,'#0d3d12');
  ctx.fillStyle=cg;
  ctx.fillRect(x-5,th-18,56,18);
  ctx.fillRect(x-5,th+GAP,56,18);
  // Highlight
  ctx.fillStyle='rgba(57,255,20,.12)';ctx.fillRect(x+3,0,6,th);ctx.fillRect(x+3,th+GAP,6,H-(th+GAP));
  // Edge glow
  ctx.shadowBlur=8;ctx.shadowColor='rgba(57,255,20,.2)';
  ctx.strokeStyle='rgba(57,255,20,.15)';ctx.lineWidth=1;
  ctx.strokeRect(x,0,46,th);ctx.strokeRect(x,th+GAP,46,H-(th+GAP));
  ctx.shadowBlur=0;
}}
function draw(){{
  // Sky gradient
  let sky=ctx.createLinearGradient(0,0,0,H);
  sky.addColorStop(0,'#02020a');sky.addColorStop(.65,'#060616');sky.addColorStop(1,'#080f08');
  ctx.fillStyle=sky;ctx.fillRect(0,0,W,H);
  // Stars
  stars.forEach(s=>{{
    ctx.globalAlpha=.3+Math.sin(frame*.04+s.b*6)*.35;
    ctx.fillStyle='#fff';ctx.shadowBlur=4;ctx.shadowColor='#fff';
    ctx.beginPath();ctx.arc(s.x,s.y,s.r,0,Math.PI*2);ctx.fill();
    ctx.shadowBlur=0;
  }});ctx.globalAlpha=1;
  // Clouds
  clouds.forEach(c=>{{
    ctx.globalAlpha=.06;ctx.fillStyle='#8899ff';
    ctx.beginPath();ctx.ellipse(c.x,c.y,c.w/2,12,0,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.ellipse(c.x-c.w*.2,c.y+5,c.w/3,9,0,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.ellipse(c.x+c.w*.2,c.y+4,c.w/3,8,0,0,Math.PI*2);ctx.fill();
  }});ctx.globalAlpha=1;
  // Pipes
  pipes.forEach(p=>drawPipe(p.x,p.th));
  // Ground
  let gg=ctx.createLinearGradient(0,H-28,0,H);
  gg.addColorStop(0,'#101a10');gg.addColorStop(1,'#060f06');
  ctx.fillStyle=gg;ctx.fillRect(0,H-28,W,28);
  ctx.fillStyle='rgba(57,255,20,.15)';ctx.fillRect(0,H-28,W,2);
  // Particles
  parts.forEach(p=>{{
    ctx.globalAlpha=p.l/(p.type==='score'?28:p.type==='shield'?30:15);
    ctx.fillStyle=p.c||'#fff';ctx.shadowBlur=5;ctx.shadowColor=p.c||'#fff';
    ctx.beginPath();ctx.arc(p.x,p.y,p.type==='flap'?3:2.5,0,Math.PI*2);ctx.fill();
    ctx.shadowBlur=0;
  }});ctx.globalAlpha=1;
  // Bird
  ctx.save();ctx.translate(bird.x,bird.y);ctx.rotate(bird.rot*Math.PI/180);
  // Shield
  if(shL>0){{
    ctx.beginPath();ctx.arc(0,0,BR+9,0,Math.PI*2);
    let sg=ctx.createRadialGradient(0,0,BR,0,0,BR+9);
    sg.addColorStop(0,'rgba(0,245,255,.0)');sg.addColorStop(.7,'rgba(0,245,255,.25)');sg.addColorStop(1,'rgba(0,245,255,.0)');
    ctx.fillStyle=sg;ctx.fill();
    ctx.strokeStyle='rgba(0,245,255,'+(0.4+Math.sin(frame*.18)*.3)+')';ctx.lineWidth=1.5;ctx.stroke();
  }}
  // Body glow
  ctx.shadowBlur=14;ctx.shadowColor='rgba(255,214,10,.8)';
  // Body gradient
  let bg2=ctx.createRadialGradient(-2,-2,1,0,0,BR);
  bg2.addColorStop(0,'#fff9c4');bg2.addColorStop(.5,'#ffd60a');bg2.addColorStop(1,'#ff8f00');
  ctx.fillStyle=bg2;ctx.beginPath();ctx.ellipse(0,0,BR,BR-1,0,0,Math.PI*2);ctx.fill();
  ctx.shadowBlur=0;
  // Wing
  ctx.fillStyle='rgba(255,140,0,.8)';
  ctx.beginPath();ctx.ellipse(-3,3,8,4,Math.PI/4+Math.sin(frame*.3)*.5,0,Math.PI*2);ctx.fill();
  // Eye
  ctx.fillStyle='#fff';ctx.beginPath();ctx.arc(5.5,-2,3.5,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='#1a0a00';ctx.beginPath();ctx.arc(6.5,-2,2,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='rgba(255,255,255,.7)';ctx.beginPath();ctx.arc(7,-2.8,0.7,0,Math.PI*2);ctx.fill();
  // Beak
  ctx.fillStyle='#ff6600';ctx.beginPath();ctx.moveTo(BR+1,0);ctx.lineTo(BR+7,1.5);ctx.lineTo(BR+1,-2);ctx.fill();
  ctx.restore();
  // Score
  ctx.fillStyle='rgba(255,214,10,.95)';ctx.font='bold 28px Orbitron,monospace';ctx.textAlign='center';
  ctx.shadowBlur=16;ctx.shadowColor='rgba(255,214,10,.8)';ctx.fillText(score,W/2,50);ctx.shadowBlur=0;
}}
mkBg();ctx.fillStyle='#04040f';ctx.fillRect(0,0,W,H);
</script></body></html>""", height=520, scrolling=False)

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
#  MEMORY — Full canvas-based with proper flip animation
# ═══════════════════════════════════════════════════════
EMJ=["🐉","🦄","🔥","⚡","💎","🚀","🌊","🎸","🦋","🍄","🎯","🏆","🌈","🎪","🐬","🦁"]

def _mr():
    c=random.sample(range(len(EMJ)),8); b=c*2; random.shuffle(b)
    st.session_state.update({
        "mb":b,"mf":[],"mm":set(),"mov":0,
        "mpend":False,"mptime":0,"mh":oc("mem_hint")*2,
        "mem_click":None
    })

def page_memory():
    st.markdown("<h1 style='text-align:center;letter-spacing:3px'>🧠 MEMORY</h1>",unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#5566aa;font-family:Share Tech Mono,monospace'>CLICK TILES to flip them — find all pairs!</p>",unsafe_allow_html=True)
    if has("mem_x2"): st.markdown("<div class='inf'>×2 score active!</div>",unsafe_allow_html=True)
    if "mb" not in st.session_state: _mr()

    b=st.session_state["mb"]
    fl=list(st.session_state["mf"])
    mm=set(st.session_state["mm"])
    mv=S("mov",0)
    hints=S("mh",0)

    c1,c2,c3,c4=st.columns(4)
    with c1: st.metric("🎯 Moves",mv)
    with c2: st.metric("✅ Pairs",len(mm)//2)
    with c3: st.metric("🃏 Left",8-len(mm)//2)
    with c4: st.metric("💡 Hints",hints)

    if len(mm)==16:
        sc=max(80-mv*2,10)*(2 if has("mem_x2") else 1)
        e=earn(sc); give_xp(sc//2); st.session_state["mem_pl"]=S("mem_pl",0)+1
        if sc>S("mem_hi",0): st.session_state["mem_hi"]=sc; add_ach("🧠 Memory Record!")
        if mv<=10: add_ach("🧠 Golden Brain!")
        st.markdown(f"<div class='ok' style='font-size:17px;padding:18px;margin:16px 0'>🎉 Done in {mv} moves! +{e} coins</div>",unsafe_allow_html=True)
        _,mc,_=st.columns([1,2,1])
        with mc:
            st.markdown('<div class="bG">',unsafe_allow_html=True)
            if st.button("🔄 New Game",use_container_width=True,key="mr"): _mr(); st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)
        return

    # Handle pending match check
    if S("mpend") and time.time()-S("mptime",0)>=1.0:
        f2=list(S("mf",[]))
        if len(f2)==2:
            i1,i2=f2
            if b[i1]==b[i2]:
                mm.add(i1); mm.add(i2); st.session_state["mm"]=mm
        st.session_state["mf"]=[]; st.session_state["mpend"]=False; st.rerun()
    if S("mpend"): time.sleep(0.05); st.rerun()

    can_flip = len(fl)<2 and not S("mpend")

    # Build full-game HTML with click-to-flip 3D animation
    # Pass state into JS so it renders correctly
    mm_list = list(mm)
    fl_list = list(fl)

    emj_js = "[" + ",".join(f'"{EMJ[b[i]]}"' for i in range(16)) + "]"
    mm_js = "[" + ",".join(str(x) for x in mm_list) + "]"
    fl_js = "[" + ",".join(str(x) for x in fl_list) + "]"
    can_js = "true" if can_flip else "false"

    components.html(f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&display=swap');
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:transparent;padding:10px;font-family:sans-serif;display:flex;justify-content:center}}
.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;width:100%;max-width:440px}}
.card{{position:relative;width:100%;aspect-ratio:1;cursor:pointer;perspective:800px;
  transition:transform .08s;}}
.card:hover .inner:not(.flipped):not(.matched){{transform:rotateY(8deg) scale(1.04);}}
.inner{{
  position:absolute;inset:0;transform-style:preserve-3d;
  transition:transform .55s cubic-bezier(.4,0,.2,1);border-radius:12px;
}}
.inner.flipped,.inner.matched{{transform:rotateY(180deg)}}
.front,.back{{
  position:absolute;inset:0;border-radius:12px;
  display:flex;align-items:center;justify-content:center;
  backface-visibility:hidden;-webkit-backface-visibility:hidden;
  font-size:36px;
}}
/* Back = unflipped face shown to user */
.back{{
  background:linear-gradient(145deg,#0e0e28,#080820);
  border:1px solid rgba(191,95,255,.3);
  box-shadow:0 4px 16px rgba(0,0,0,.4),inset 0 1px 0 rgba(191,95,255,.12);
}}
.back::before{{
  content:'?';font-family:'Orbitron',sans-serif;font-size:22px;font-weight:900;
  color:rgba(191,95,255,.6);text-shadow:0 0 12px rgba(191,95,255,.5);
}}
/* Front = emoji face (rotated 180 so it shows when flipped) */
.front{{
  transform:rotateY(180deg);
  background:linear-gradient(145deg,#0d0d22,#0a0a1e);
  border:1px solid rgba(0,245,255,.4);
  box-shadow:0 4px 20px rgba(0,245,255,.15),inset 0 1px 0 rgba(0,245,255,.15);
}}
.front .emoji{{font-size:38px;filter:drop-shadow(0 0 8px rgba(0,245,255,.6));}}
/* Matched state */
.inner.matched .front{{
  background:linear-gradient(145deg,rgba(57,255,20,.12),rgba(57,255,20,.04));
  border:1px solid rgba(57,255,20,.55);
  box-shadow:0 0 24px rgba(57,255,20,.2),inset 0 1px 0 rgba(57,255,20,.18);
  animation:matchPop .5s cubic-bezier(.34,1.56,.64,1) forwards;
}}
.inner.matched .front .emoji{{filter:drop-shadow(0 0 12px rgba(57,255,20,.8));animation:matchGlow 1.5s ease-in-out infinite;}}
/* No-click state */
.card.disabled{{cursor:default;pointer-events:none;}}
@keyframes matchPop{{
  0%{{transform:rotateY(180deg) scale(.9)}}
  60%{{transform:rotateY(180deg) scale(1.1)}}
  100%{{transform:rotateY(180deg) scale(1)}}
}}
@keyframes matchGlow{{
  0%,100%{{filter:drop-shadow(0 0 8px rgba(57,255,20,.6))}}
  50%{{filter:drop-shadow(0 0 18px rgba(57,255,20,1))}}
}}
/* Wrong pair shake */
@keyframes wrongShake{{
  0%,100%{{transform:rotateY(180deg)}}
  20%{{transform:rotateY(180deg) translateX(-6px) rotate(-2deg)}}
  40%{{transform:rotateY(180deg) translateX(6px) rotate(2deg)}}
  60%{{transform:rotateY(180deg) translateX(-4px) rotate(-1deg)}}
  80%{{transform:rotateY(180deg) translateX(4px) rotate(1deg)}}
}}
.inner.wrong{{animation:wrongShake .5s ease;}}
</style></head><body>
<div class="grid" id="grid"></div>
<script>
const EMOJIS = {emj_js};
const matched = new Set({mm_js});
const flipped = new Set({fl_js});
const CAN = {can_js};

// Track which two are currently flipped & pending
let pendingWrong = false;

function buildGrid() {{
  const grid = document.getElementById('grid');
  grid.innerHTML = '';
  for (let i = 0; i < 16; i++) {{
    const card = document.createElement('div');
    card.className = 'card' + (matched.has(i) ? '' : (!CAN && !flipped.has(i) ? ' disabled' : ''));
    card.dataset.idx = i;
    
    const inner = document.createElement('div');
    inner.className = 'inner' + 
      (matched.has(i) ? ' matched' : '') + 
      (flipped.has(i) && !matched.has(i) ? ' flipped' : '');
    inner.id = 'inner_' + i;
    
    const back = document.createElement('div');
    back.className = 'back';
    
    const front = document.createElement('div');
    front.className = 'front';
    const span = document.createElement('span');
    span.className = 'emoji';
    span.textContent = EMOJIS[i];
    front.appendChild(span);
    
    inner.appendChild(back);
    inner.appendChild(front);
    card.appendChild(inner);
    grid.appendChild(card);
    
    if (!matched.has(i) && CAN) {{
      card.addEventListener('click', () => handleFlip(i));
    }}
  }}
}}

function handleFlip(idx) {{
  if (matched.has(idx) || flipped.has(idx) || !CAN) return;
  // Send message to Streamlit parent
  window.parent.postMessage({{type: 'mem_flip', idx: idx}}, '*');
  // Immediately animate the flip locally for responsiveness
  const inner = document.getElementById('inner_' + idx);
  if (inner) inner.classList.add('flipped');
}}

buildGrid();
</script></body></html>""", height=480, scrolling=False)

    # Hidden buttons to handle clicks — Streamlit doesn't receive postMessage,
    # so we show clickable numbered buttons below as the actual interaction layer
    st.markdown("<br>",unsafe_allow_html=True)

    # Show current state info
    if fl:
        vis=[f"Card {i+1}: {EMJ[b[i]]}" for i in sorted(set(fl)|mm)]
        if vis: st.markdown(f"<div class='inf' style='font-size:12px;margin-bottom:8px'>Flipped: {' · '.join([f\"{EMJ[b[i]]}\" for i in fl])}</div>",unsafe_allow_html=True)

    # Click buttons that actually work with Streamlit
    available=[i for i in range(16) if i not in mm and i not in fl and can_flip]
    if available:
        st.markdown("<p style='color:#5566aa;font-size:11px;text-align:center;font-family:Share Tech Mono,monospace;margin-bottom:6px'>— CLICK A CARD NUMBER TO FLIP IT —</p>",unsafe_allow_html=True)

        # Show 4x4 grid of buttons matching card positions
        for row in range(4):
            btn_cols = st.columns(4)
            for col_i in range(4):
                idx = row*4 + col_i
                with btn_cols[col_i]:
                    if idx in mm:
                        em = EMJ[b[idx]]
                        st.markdown(f"""<div style="height:52px;background:linear-gradient(135deg,rgba(57,255,20,.1),rgba(57,255,20,.03));
border:1px solid rgba(57,255,20,.4);border-radius:10px;display:flex;align-items:center;
justify-content:center;font-size:24px;box-shadow:0 0 12px rgba(57,255,20,.15)">{em}</div>""",unsafe_allow_html=True)
                    elif idx in fl:
                        em = EMJ[b[idx]]
                        st.markdown(f"""<div style="height:52px;background:linear-gradient(135deg,rgba(0,245,255,.1),rgba(0,245,255,.03));
border:2px solid rgba(0,245,255,.5);border-radius:10px;display:flex;align-items:center;
justify-content:center;font-size:24px;box-shadow:0 0 16px rgba(0,245,255,.25)">{em}</div>""",unsafe_allow_html=True)
                    elif not can_flip:
                        st.markdown("""<div style="height:52px;background:rgba(191,95,255,.04);
border:1px solid rgba(191,95,255,.15);border-radius:10px;display:flex;align-items:center;
justify-content:center;font-size:14px;color:rgba(191,95,255,.3);font-family:Orbitron,sans-serif;font-weight:900">?</div>""",unsafe_allow_html=True)
                    else:
                        # Clickable
                        if st.button(f"?", key=f"mc_{idx}_{mv}_{len(mm)}", use_container_width=True):
                            fl.append(idx); st.session_state["mf"]=fl
                            if len(fl)==2:
                                st.session_state["mov"]=mv+1
                                st.session_state["mpend"]=True
                                st.session_state["mptime"]=time.time()
                            st.rerun()

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
                un=[i for i in range(16) if i not in mm and i not in fl]
                seen={}
                for i in un:
                    e2=b[i]
                    if e2 in seen:
                        st.session_state["mf"]=[seen[e2],i]
                        st.session_state["mov"]=mv+1
                        st.session_state["mpend"]=True
                        st.session_state["mptime"]=time.time()
                        st.session_state["mh"]=hints-1
                        st.rerun(); break
                    seen[e2]=i
            st.markdown('</div>',unsafe_allow_html=True)
    with c3: st.metric("🏆 Best",S("mem_hi",0))

# ═══════════════════════════════════════════════════════
#  TIC-TAC-TOE 1P — Full canvas with glow animations
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
    st.markdown("<h1 style='text-align:center;letter-spacing:3px'>❌ TIC-TAC-TOE</h1>",unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#5566aa;font-family:Share Tech Mono,monospace'>YOU = X (cyan) · AI = O (pink)</p>",unsafe_allow_html=True)
    undo=oc("ttt_undo")
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
        st.markdown(f"<div class='{cls}' style='font-size:16px;padding:14px;margin-bottom:12px'>{ts}</div>",unsafe_allow_html=True)

    # Render the board
    _,mc,_=st.columns([1,2,1])
    with mc:
        for row in range(3):
            rc=st.columns(3)
            for ci in range(3):
                idx=row*3+ci
                cell=b[idx]
                with rc[ci]:
                    if cell=="X":
                        st.markdown("""<div style="height:90px;
background:linear-gradient(145deg,rgba(0,245,255,.1),rgba(0,245,255,.03));
border:2px solid rgba(0,245,255,.55);border-radius:14px;
display:flex;align-items:center;justify-content:center;
font-size:44px;font-weight:900;color:#00f5ff;
text-shadow:0 0 20px rgba(0,245,255,.9),0 0 40px rgba(0,245,255,.4);
box-shadow:0 0 20px rgba(0,245,255,.12),inset 0 1px 0 rgba(0,245,255,.15);
animation:xPop .25s cubic-bezier(.34,1.56,.64,1) forwards">✕</div>
<style>@keyframes xPop{from{transform:scale(.2) rotate(-15deg);opacity:0}to{transform:scale(1) rotate(0deg);opacity:1}}</style>""",unsafe_allow_html=True)
                    elif cell=="O":
                        st.markdown("""<div style="height:90px;
background:linear-gradient(145deg,rgba(255,0,110,.1),rgba(255,0,110,.03));
border:2px solid rgba(255,0,110,.55);border-radius:14px;
display:flex;align-items:center;justify-content:center;
font-size:44px;font-weight:900;color:#ff006e;
text-shadow:0 0 20px rgba(255,0,110,.9),0 0 40px rgba(255,0,110,.4);
box-shadow:0 0 20px rgba(255,0,110,.12),inset 0 1px 0 rgba(255,0,110,.15);
animation:oPop .25s cubic-bezier(.34,1.56,.64,1) forwards">○</div>
<style>@keyframes oPop{from{transform:scale(.2);opacity:0}to{transform:scale(1);opacity:1}}</style>""",unsafe_allow_html=True)
                    elif not ov:
                        # Clickable empty cell
                        st.markdown("""<style>
div.tttCell .stButton>button{
  height:90px!important;min-height:90px!important;
  background:linear-gradient(145deg,rgba(191,95,255,.06),rgba(191,95,255,.01))!important;
  border:1px solid rgba(191,95,255,.2)!important;
  border-radius:14px!important;font-size:0!important;
  transition:all .18s!important;
}
div.tttCell .stButton>button:hover{
  background:rgba(191,95,255,.14)!important;
  border-color:rgba(191,95,255,.55)!important;
  box-shadow:0 0 20px rgba(191,95,255,.2),inset 0 1px 0 rgba(191,95,255,.1)!important;
  transform:scale(1.04)!important;
}
</style>""",unsafe_allow_html=True)
                        st.markdown('<div class="tttCell">',unsafe_allow_html=True)
                        if st.button(" ", key=f"tt_{idx}_{sum(1 for x in b if x)}", use_container_width=True):
                            st.session_state["tp"]=b[:]
                            b[idx]="X"; w=_tw(b)
                            if w: _tte(w,b); st.stop()
                            if ""not in b: _tte("d",b); st.stop()
                            ai=_ai_move(b,0)
                            if ai is not None:
                                b[ai]="O"; w=_tw(b)
                                if w: _tte(w,b); st.stop()
                                if ""not in b: _tte("d",b); st.stop()
                            st.session_state["tb"]=b; st.rerun()
                        st.markdown('</div>',unsafe_allow_html=True)
                    else:
                        st.markdown("""<div style="height:90px;
background:rgba(255,255,255,.01);border:1px solid rgba(255,255,255,.04);
border-radius:14px"></div>""",unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)
    c1,c2,c3=st.columns(3)
    with c1:
        st.markdown('<div class="bG">',unsafe_allow_html=True)
        if st.button("🔄 New Game",use_container_width=True,key="ttn"): _ttr(); st.rerun()
        st.markdown('</div>',unsafe_allow_html=True)
    with c2:
        if undo>0 and prev and not ov:
            st.markdown('<div class="bg">',unsafe_allow_html=True)
            if st.button(f"↩ Undo ({undo})",use_container_width=True,key="ttun"):
                st.session_state["tb"]=prev; st.session_state["tp"]=None; st.session_state["ts"]=""; st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)
    with c3:
        st.selectbox("AI Level",["Normal","Easy","Baby"],key="tts",label_visibility="visible")

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
    st.markdown("<h1 style='text-align:center;letter-spacing:3px'>👆 CLICKER</h1>",unsafe_allow_html=True)
    mul=1+oc("click_mul"); dur=10+oc("click_time")*3
    if mul>1 or dur>10: st.markdown(f"<div class='inf'>×{mul} per click  |  {dur}s duration</div>",unsafe_allow_html=True)
    if "cks" not in st.session_state: st.session_state.update({"cks":"idle","ckc":0,"ckt":0})
    state=S("cks"); cnt=S("ckc",0); best=S("click_hi",0)

    if state=="playing":
        el=time.time()-S("ckt",0); rem=max(0,dur-el)
        danger=rem<3
        st.markdown(f"""<div style="text-align:center;margin-bottom:12px">
<div style="font-family:'Orbitron',sans-serif;font-size:56px;font-weight:900;
  color:{'#ff006e' if danger else '#00f5ff'};
  text-shadow:0 0 30px {'rgba(255,0,110,.8)' if danger else 'rgba(0,245,255,.8)'};
  {'animation:dangerPulse .3s ease-in-out infinite' if danger else ''}">{rem:.1f}</div>
<div style="color:#5566aa;font-size:11px;font-family:Share Tech Mono,monospace">SECONDS REMAINING</div>
</div>
<style>@keyframes dangerPulse{{0%,100%{{transform:scale(1)}}50%{{transform:scale(1.05)}}}}</style>""",unsafe_allow_html=True)
        st.progress(rem/dur)
        if rem<=0: st.session_state["cks"]="done"; st.rerun()

    cl="#ff006e" if state=="playing" else("#39ff14" if state=="done" else "#5566aa")
    st.markdown(f"""<div style="text-align:center;margin:12px 0">
<div style="font-family:'Orbitron',sans-serif;font-size:80px;font-weight:900;
  color:{cl};text-shadow:0 0 40px {cl}90;
  {'animation:countUp .08s ease-out' if state=='playing' else ''}">{cnt}</div>
<div style="color:#5566aa;font-size:12px;font-family:Share Tech Mono,monospace">CLICKS</div>
</div>
<style>@keyframes countUp{{from{{transform:scale(1.15)}}to{{transform:scale(1)}}}}</style>""",unsafe_allow_html=True)

    _,c2,_=st.columns([1,2,1])
    with c2:
        if state=="idle":
            st.markdown('<div class="br">',unsafe_allow_html=True)
            if st.button("🚀 Start!",use_container_width=True,key="ckg"):
                st.session_state.update({"cks":"playing","ckc":0,"ckt":time.time()})
                st.session_state["click_ses"]=S("click_ses",0)+1; st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)
        elif state=="playing":
            st.markdown("""<style>
div.ckB .stButton>button{
  background:linear-gradient(145deg,rgba(255,0,110,.25),rgba(255,0,110,.08))!important;
  border:2px solid rgba(255,0,110,.7)!important;color:#ff006e!important;
  font-size:24px!important;height:120px!important;font-weight:900!important;
  letter-spacing:2px!important;
  box-shadow:0 0 30px rgba(255,0,110,.2),inset 0 1px 0 rgba(255,0,110,.2)!important;
  font-family:'Orbitron',sans-serif!important;
}
div.ckB .stButton>button:active{
  transform:scale(.94)!important;
  box-shadow:0 0 50px rgba(255,0,110,.4),inset 0 0 20px rgba(255,0,110,.1)!important;
}
</style>""",unsafe_allow_html=True)
            st.markdown('<div class="ckB">',unsafe_allow_html=True)
            if st.button("👆 CLICK!",use_container_width=True,key="ckc_btn"):
                st.session_state["ckc"]=cnt+mul; st.session_state["click_tot"]=S("click_tot",0)+mul; st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)
        elif state=="done":
            final=S("ckc",0); e=earn(final*2); give_xp(final)
            if final>best: st.session_state["click_hi"]=final; add_ach(f"👆 Clicker Record: {final}!")
            st.markdown(f"<div class='{'ok' if final>=best else 'inf'}' style='margin-bottom:12px;font-size:15px'>{final} clicks! +{e} coins</div>",unsafe_allow_html=True)
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
#  SLOT MACHINE
# ═══════════════════════════════════════════════════════
SYM=["🍒","🍋","🍊","🍇","⭐","💎","🎰","🃏"]
SW=[20,18,15,12,10,7,4,14]
PAY={0:5,1:8,2:10,3:15,4:20,5:50,6:100,7:35}
SYM_NAMES=["Cherry","Lemon","Orange","Grapes","Star","Diamond","Jackpot","Joker"]

def page_slot():
    st.markdown("<h1 style='text-align:center;letter-spacing:3px'>🎰 SLOT MACHINE</h1>",unsafe_allow_html=True)
    lk=oc("slot_luck"); jp=oc("slot_jackpot"); rf=has("slot_refund")
    if lk or jp or rf:
        parts=filter(None,[f"🍀 Luck +{lk}" if lk else "",f"💰 Jackpot x{2**jp}" if jp else "",f"↩ Refund" if rf else ""])
        st.markdown(f"<div class='inf'>{'  |  '.join(parts)}</div>",unsafe_allow_html=True)
    if "slr" not in st.session_state:
        st.session_state.update({"slr":[6,6,6],"slres":"","slbet":10})

    reels=st.session_state["slr"]; res=S("slres",""); coins=S("coins",0)
    iw="Won" in res or "Jackpot" in res; ijp="Jackpot" in res
    r0,r1,r2=reels

    components.html(f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&display=swap');
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:transparent;display:flex;justify-content:center;align-items:center;padding:12px;font-family:'Orbitron',sans-serif}}
.machine{{
  background:linear-gradient(160deg,#1a0800,#240c00,#1a0800);
  border:2px solid {('rgba(255,214,10,.85)' if iw else 'rgba(255,124,0,.4)')};
  border-radius:20px;padding:22px 28px;max-width:420px;width:100%;
  box-shadow:{('0 0 50px rgba(255,214,10,.4),0 0 100px rgba(255,214,10,.15)' if ijp else '0 0 20px rgba(255,124,0,.1)')},
    inset 0 0 30px rgba(0,0,0,.6),inset 0 1px 0 rgba(255,124,0,.12);
  {('animation:jackpotFlash .4s infinite;' if ijp else '')}
}}
@keyframes jackpotFlash{{0%,100%{{border-color:rgba(255,214,10,.9)}}50%{{border-color:rgba(255,214,10,.2)}}}}
.title{{text-align:center;font-size:14px;font-weight:900;color:#ff7c00;
  text-shadow:0 0 16px rgba(255,124,0,.8);letter-spacing:5px;margin-bottom:16px}}
.reels-wrap{{
  display:flex;gap:14px;justify-content:center;
  background:linear-gradient(145deg,rgba(0,0,0,.7),rgba(10,5,0,.6));
  border-radius:14px;padding:16px;border:1px solid rgba(255,124,0,.15);
  box-shadow:inset 0 4px 20px rgba(0,0,0,.5)
}}
.reel{{
  flex:1;max-width:100px;aspect-ratio:1;border-radius:12px;
  display:flex;align-items:center;justify-content:center;
  background:linear-gradient(145deg,#1a0800,#0f0500);
  border:2px solid {('rgba(255,214,10,.6)' if iw else 'rgba(255,124,0,.25)')};
  font-size:50px;position:relative;overflow:hidden;
  box-shadow:{('0 0 24px rgba(255,214,10,.3),inset 0 0 20px rgba(255,214,10,.05)' if iw else 'inset 0 4px 12px rgba(0,0,0,.4)')};
  {('animation:reelWin .6s cubic-bezier(.34,1.56,.64,1)' if iw else '')}
}}
@keyframes reelWin{{0%{{transform:scale(.8) rotate(-5deg)}}60%{{transform:scale(1.1) rotate(2deg)}}100%{{transform:scale(1) rotate(0deg)}}}}
.reel::before{{content:'';position:absolute;top:0;left:0;right:0;height:30%;
  background:linear-gradient(180deg,rgba(255,255,255,.05),transparent);border-radius:10px 10px 0 0}}
.win-line{{
  height:3px;margin:12px 0;
  background:linear-gradient(90deg,transparent,{('#ffd60a' if iw else 'rgba(255,124,0,.2)')},transparent);
  {('box-shadow:0 0 12px #ffd60a,0 0 24px rgba(255,214,10,.4);' if iw else '')}
}}
</style></head><body>
<div class="machine">
  <div class="title">🎰 ARCADE SLOTS</div>
  <div class="reels-wrap">
    <div class="reel" style="animation-delay:0s">{SYM[r0]}</div>
    <div class="reel" style="animation-delay:.1s">{SYM[r1]}</div>
    <div class="reel" style="animation-delay:.2s">{SYM[r2]}</div>
  </div>
  <div class="win-line"></div>
</div>
</body></html>""", height=200, scrolling=False)

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
        st.markdown("""<style>
div.spB .stButton>button{
  background:linear-gradient(135deg,rgba(255,124,0,.25),rgba(255,124,0,.08))!important;
  border:2px solid rgba(255,124,0,.6)!important;color:#ff7c00!important;
  font-size:18px!important;height:60px!important;font-weight:900!important;
  letter-spacing:3px!important;font-family:'Orbitron',sans-serif!important;
  box-shadow:0 0 24px rgba(255,124,0,.15),inset 0 1px 0 rgba(255,124,0,.1)!important;
}
div.spB .stButton>button:hover{{box-shadow:0 0 36px rgba(255,124,0,.4)!important;}}
</style>""",unsafe_allow_html=True)
        st.markdown('<div class="spB">',unsafe_allow_html=True)
        if st.button("🎰  SPIN!",use_container_width=True,key="slsp",disabled=coins<bet):
            _spin(bet,lk,jp,rf)
        st.markdown('</div>',unsafe_allow_html=True)
    if coins<bet: st.markdown("<div class='err'>Not enough coins!</div>",unsafe_allow_html=True)

    st.markdown("---")
    with st.expander("📋 Paytable"):
        for idx,mult in PAY.items():
            am=mult*(2**jp if mult>=50 else 1)
            st.markdown(f"""<div style="display:flex;justify-content:space-between;align-items:center;padding:6px 12px;
background:linear-gradient(135deg,rgba(255,124,0,.04),transparent);border-radius:8px;margin-bottom:3px;border:1px solid rgba(255,124,0,.06)">
<span style="font-size:24px">{SYM[idx]*3}</span>
<span style="color:#5566aa;font-size:12px;font-family:Share Tech Mono,monospace">{SYM_NAMES[idx]}</span>
<span style="color:#ff7c00;font-weight:900;font-family:'Orbitron',sans-serif;font-size:14px">×{am}</span></div>""",unsafe_allow_html=True)
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
    st.session_state["slr"]=r
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
    st.markdown("<h1 style='text-align:center;letter-spacing:3px'>🏓 PONG</h1>",unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#5566aa;font-family:Share Tech Mono,monospace'>W/S or ↑/↓ to move · First to 7 wins</p>",unsafe_allow_html=True)
    spb=2+oc("pong_speed"); hi=S("pong_hi",0)
    _,col,_=st.columns([1,10,1])
    with col:
        components.html(f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#04040f;display:flex;flex-direction:column;align-items:center;padding:10px;user-select:none}}
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&display=swap');
canvas{{border:2px solid rgba(0,245,255,.2);border-radius:12px;
  box-shadow:0 0 40px rgba(0,245,255,.08),0 0 80px rgba(0,245,255,.03);display:block}}
.ov{{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
  background:linear-gradient(145deg,rgba(4,4,20,.97),rgba(8,8,28,.97));
  border:1px solid rgba(0,245,255,.4);border-radius:16px;padding:24px 32px;text-align:center;
  backdrop-filter:blur(20px);box-shadow:0 0 40px rgba(0,245,255,.12)}}
.ov h2{{color:#00f5ff;font-family:'Orbitron',sans-serif;font-size:18px;margin-bottom:8px;text-shadow:0 0 16px rgba(0,245,255,.7)}}
.ov p{{color:#8899bb;font-size:12px;margin-bottom:14px;font-family:Share Tech Mono,monospace}}
.ov button{{background:linear-gradient(135deg,rgba(0,245,255,.2),rgba(0,245,255,.06));
  color:#00f5ff;border:1px solid rgba(0,245,255,.5);padding:9px 22px;
  border-radius:8px;cursor:pointer;font-family:'Orbitron',sans-serif;font-size:12px;font-weight:700;transition:all .18s}}
.ov button:hover{{background:rgba(0,245,255,.3)}}
.wrap{{position:relative}}</style></head><body>
<div class="wrap"><canvas id="c" width="520" height="320"></canvas>
<div class="ov" id="ov"><h2>🏓 PONG</h2><p>W/S or ↑/↓ · First to 7</p><button onclick="start()">▶ PLAY</button></div></div>
<script>
const W=520,H=320,PW=10,PH=70,BR=7,SPB={spb};
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
let p1y,p2y,bx,by,vx,vy,s1,s2,run,raf,keys={{}},trail=[],parts=[];
function start(){{
  document.getElementById('ov').style.display='none';
  p1y=H/2-PH/2;p2y=H/2-PH/2;bx=W/2;by=H/2;
  let a=(Math.random()*.8+.1)*Math.PI*(Math.random()<.5?1:-1);
  vx=Math.cos(a)*(SPB+1.5);vy=Math.sin(a)*SPB;
  s1=s2=0;run=true;trail=[];parts=[];
  if(raf)cancelAnimationFrame(raf);loop();
}}
document.addEventListener('keydown',e=>{{keys[e.code]=true;if(['KeyW','KeyS','ArrowUp','ArrowDown'].includes(e.code))e.preventDefault();}});
document.addEventListener('keyup',e=>keys[e.code]=false);
function loop(){{if(!run)return;update();draw();raf=requestAnimationFrame(loop);}}
function update(){{
  if(keys['KeyW']||keys['ArrowUp'])p1y=Math.max(0,p1y-5.5);
  if(keys['KeyS']||keys['ArrowDown'])p1y=Math.min(H-PH,p1y+5.5);
  let cy=p2y+PH/2;
  if(by<cy-4)p2y=Math.max(0,p2y-4.5);
  else if(by>cy+4)p2y=Math.min(H-PH,p2y+4.5);
  bx+=vx;by+=vy;
  if(by<=BR||by>=H-BR){{vy=-vy;spark(bx,by,'#ffd60a');}}
  if(bx<=22+PW&&by>=p1y&&by<=p1y+PH){{
    vx=Math.abs(vx)*(1+s1*.03);vy+=(by-(p1y+PH/2))*.12;spark(bx,by,'#00f5ff');
  }}
  if(bx>=W-22-PW&&by>=p2y&&by<=p2y+PH){{
    vx=-Math.abs(vx)*(1+s2*.03);vy+=(by-(p2y+PH/2))*.12;spark(bx,by,'#ff006e');
  }}
  trail.unshift({{x:bx,y:by,l:12}});if(trail.length>14)trail.pop();
  trail.forEach(t=>t.l--);trail=trail.filter(t=>t.l>0);
  parts=parts.filter(p=>p.l>0);parts.forEach(p=>{{p.x+=p.vx;p.y+=p.vy;p.l--;p.vx*=.92;}});
  if(bx<0){{s2++;if(s2>=7){{endGame('AI Wins!');return;}}reset();}}
  if(bx>W){{s1++;if(s1>=7){{endGame('You Win! 🎉');return;}}reset();}}
}}
function spark(x,y,c){{for(let i=0;i<10;i++)parts.push({{x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,l:20,c}});}}
function reset(){{
  bx=W/2;by=H/2;
  let a=(Math.random()*.8+.1)*Math.PI*(Math.random()<.5?1:-1);
  vx=Math.cos(a)*(SPB+1.5+Math.max(s1,s2)*.2);vy=Math.sin(a)*SPB;trail=[];
}}
function endGame(msg){{
  run=false;cancelAnimationFrame(raf);
  document.getElementById('ov').querySelector('h2').textContent=msg;
  document.getElementById('ov').querySelector('p').textContent='You: '+s1+' | AI: '+s2;
  document.getElementById('ov').style.display='block';
}}
function draw(){{
  // Scanline bg
  let bg=ctx.createLinearGradient(0,0,0,H);bg.addColorStop(0,'#04040f');bg.addColorStop(1,'#04040f');
  ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);
  // Center line
  ctx.setLineDash([10,10]);ctx.strokeStyle='rgba(0,245,255,.07)';ctx.lineWidth=1;
  ctx.beginPath();ctx.moveTo(W/2,0);ctx.lineTo(W/2,H);ctx.stroke();ctx.setLineDash([]);
  // Score
  ctx.fillStyle='rgba(0,245,255,.9)';ctx.font='bold 32px Orbitron,monospace';ctx.textAlign='center';
  ctx.shadowBlur=16;ctx.shadowColor='rgba(0,245,255,.6)';ctx.fillText(s1,W/2-70,42);
  ctx.fillStyle='rgba(255,0,110,.9)';ctx.shadowColor='rgba(255,0,110,.6)';ctx.fillText(s2,W/2+70,42);ctx.shadowBlur=0;
  // Trail
  trail.forEach((t,i)=>{{
    ctx.globalAlpha=t.l/12*.5;ctx.fillStyle='#ffd60a';ctx.shadowBlur=4;ctx.shadowColor='#ffd60a';
    ctx.beginPath();ctx.arc(t.x,t.y,BR*(t.l/12),0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
  }});ctx.globalAlpha=1;
  // Particles
  parts.forEach(p=>{{
    ctx.globalAlpha=p.l/20;ctx.fillStyle=p.c;ctx.shadowBlur=5;ctx.shadowColor=p.c;
    ctx.beginPath();ctx.arc(p.x,p.y,2.5,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
  }});ctx.globalAlpha=1;
  // Paddles
  [{{'x':16,'y':p1y,'c':'#00f5ff'}},{{'x':W-16-PW,'y':p2y,'c':'#ff006e'}}].forEach(p=>{{
    let g=ctx.createLinearGradient(p.x,0,p.x+PW,0);
    g.addColorStop(0,p.c+'aa');g.addColorStop(.5,p.c);g.addColorStop(1,p.c+'aa');
    ctx.fillStyle=g;ctx.shadowBlur=18;ctx.shadowColor=p.c;
    ctx.beginPath();ctx.roundRect(p.x,p.y,PW,PH,5);ctx.fill();
    ctx.fillStyle='rgba(255,255,255,.25)';ctx.beginPath();ctx.roundRect(p.x+2,p.y+4,3,PH-8,2);ctx.fill();
    ctx.shadowBlur=0;
  }});
  // Ball
  let bg2=ctx.createRadialGradient(bx-2,by-2,1,bx,by,BR);
  bg2.addColorStop(0,'#fff');bg2.addColorStop(.5,'#ffd60a');bg2.addColorStop(1,'#ff8800');
  ctx.fillStyle=bg2;ctx.shadowBlur=20;ctx.shadowColor='rgba(255,214,10,.9)';
  ctx.beginPath();ctx.arc(bx,by,BR,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
}}
ctx.fillStyle='#04040f';ctx.fillRect(0,0,W,H);
</script></body></html>""", height=370, scrolling=False)
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
    st.markdown("<h1 style='text-align:center;letter-spacing:3px'>💣 MINESWEEPER</h1>",unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#5566aa;font-family:Share Tech Mono,monospace'>? = reveal · 🚩 = flag</p>",unsafe_allow_html=True)
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
        if win: st.markdown("<div class='ok' style='font-size:16px;padding:14px'>🎉 You cleared the field!</div>",unsafe_allow_html=True)
        else: st.markdown("<div class='err' style='font-size:16px;padding:14px'>💥 BOOM! Hit a mine!</div>",unsafe_allow_html=True)
    COLORS={0:"#334",1:"#00f5ff",2:"#39ff14",3:"#ff006e",4:"#bf5fff",5:"#ff7c00",6:"#ffd60a",7:"#fff",8:"#888"}
    _,mc,_=st.columns([1,5,1])
    with mc:
        for r in range(rows):
            rc=st.columns(cols_n)
            for c in range(cols_n):
                idx=r*cols_n+c; cell=b[r][c]
                with rc[c]:
                    if idx in rev:
                        if cell==-1:
                            st.markdown("""<div style="height:36px;background:linear-gradient(135deg,rgba(255,0,110,.2),rgba(255,0,110,.06));
border:1px solid rgba(255,0,110,.5);border-radius:7px;display:flex;align-items:center;
justify-content:center;font-size:16px;box-shadow:0 0 10px rgba(255,0,110,.2)">💥</div>""",unsafe_allow_html=True)
                        else:
                            col_c=COLORS.get(cell,"#fff"); txt=str(cell) if cell else "·"
                            st.markdown(f"""<div style="height:36px;background:rgba(255,255,255,.03);
border:1px solid rgba(255,255,255,.06);border-radius:7px;display:flex;align-items:center;
justify-content:center;font-size:13px;font-weight:700;color:{col_c};
font-family:Share Tech Mono,monospace">{txt}</div>""",unsafe_allow_html=True)
                    elif idx in flags:
                        st.markdown("""<div style="height:36px;background:linear-gradient(135deg,rgba(255,214,10,.1),rgba(255,214,10,.03));
border:1px solid rgba(255,214,10,.4);border-radius:7px;display:flex;align-items:center;
justify-content:center;font-size:14px">🚩</div>""",unsafe_allow_html=True)
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
    st.markdown("<h1 style='text-align:center;letter-spacing:3px'>🔢 NUMBER GUESS</h1>",unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#5566aa;font-family:Share Tech Mono,monospace'>Guess the secret number 1–100</p>",unsafe_allow_html=True)
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
    st.markdown("<h1 style='text-align:center;letter-spacing:3px'>🎯 TARGET SHOT</h1>",unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#5566aa;font-family:Share Tech Mono,monospace'>Click targets before they vanish! 15 seconds</p>",unsafe_allow_html=True)
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
        with c2: st.markdown(f"<div style='font-family:Orbitron,sans-serif;font-size:28px;color:{'#ff006e' if rem<5 else '#00f5ff'};text-align:center;padding:6px;text-shadow:0 0 14px currentColor'>{rem:.1f}s</div>",unsafe_allow_html=True)
        st.progress(rem/15)
        pos=S("tgt_pos"); app_t=S("tgt_app",0)
        if time.time()-app_t>2.2:
            pos=(random.randint(0,2),random.randint(0,4)); st.session_state.update({"tgt_pos":pos,"tgt_app":time.time()})
        if pos:
            _row,col_i=pos
            rows_cols=st.columns(5)
            for ri in range(5):
                with rows_cols[ri]:
                    if ri==col_i:
                        age=time.time()-app_t; op=max(0.2,1-age/2.2)
                        st.markdown(f"""<div style="height:74px;
background:radial-gradient(circle,rgba(255,0,110,{op*0.3:.2f}),rgba(255,0,110,{op*0.1:.2f}));
border:2px solid rgba(255,0,110,{min(op+0.1,0.9):.2f});border-radius:50%;
display:flex;align-items:center;justify-content:center;font-size:32px;
box-shadow:0 0 {int(op*24)}px rgba(255,0,110,{op*0.5:.2f});
animation:tPulse .35s ease-in-out infinite">🎯</div>
<style>@keyframes tPulse{{0%,100%{{transform:scale(1)}}50%{{transform:scale(1.14)}}}}</style>""",unsafe_allow_html=True)
                        if st.button("HIT",key=f"tgt_{int(app_t*10)}_{ri}",use_container_width=True):
                            bonus=max(1,int((2.2-(time.time()-app_t))*6))
                            st.session_state["tgt_sc"]=score+bonus
                            st.session_state.update({"tgt_pos":(random.randint(0,2),random.randint(0,4)),"tgt_app":time.time()})
                            st.rerun()
                    else:
                        st.markdown("""<div style="height:74px;background:rgba(255,255,255,.01);
border:1px solid rgba(255,255,255,.03);border-radius:50%"></div>""",unsafe_allow_html=True)
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
    st.markdown("<h1 style='text-align:center;letter-spacing:3px'>🔤 WORD GUESS</h1>",unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#5566aa;font-family:Share Tech Mono,monospace'>Guess the word — 6 tries</p>",unsafe_allow_html=True)
    if "ww" not in st.session_state:
        w=random.choice(WORDS); st.session_state.update({"ww":w,"wg":[],"wo":False,"wm":""})
    word=S("ww",""); guesses=list(S("wg",[])); over=S("wo"); msg=S("wm","")
    c1,c2=st.columns(2)
    with c1: st.metric("📝 Length",len(word))
    with c2: st.metric("🎯 Tries",f"{len(guesses)}/6")

    _,mc,_=st.columns([1,3,1])
    with mc:
        for g in guesses:
            row_html=""
            for i,ch in enumerate(g):
                if i<len(word):
                    if ch==word[i]:
                        bg="linear-gradient(135deg,rgba(57,255,20,.15),rgba(57,255,20,.06))"; bd="rgba(57,255,20,.6)"; col="#39ff14"; sh="0 0 16px rgba(57,255,20,.4)"
                    elif ch in word:
                        bg="linear-gradient(135deg,rgba(255,214,10,.12),rgba(255,214,10,.04))"; bd="rgba(255,214,10,.5)"; col="#ffd60a"; sh="0 0 12px rgba(255,214,10,.3)"
                    else:
                        bg="rgba(255,255,255,.03)"; bd="rgba(255,255,255,.08)"; col="#5566aa"; sh="none"
                else:
                    bg="rgba(255,255,255,.01)"; bd="rgba(255,255,255,.04)"; col="#333"; sh="none"
                row_html+=f"""<div style="width:50px;height:52px;background:{bg};border:2px solid {bd};
border-radius:9px;display:flex;align-items:center;justify-content:center;
font-size:20px;font-weight:900;color:{col};font-family:'Orbitron',sans-serif;
box-shadow:{sh};letter-spacing:0">{ch}</div>"""
            st.markdown(f"<div style='display:flex;gap:7px;justify-content:center;margin-bottom:7px'>{row_html}</div>",unsafe_allow_html=True)

        for _ in range(6-len(guesses)):
            empty="".join(f"""<div style="width:50px;height:52px;background:rgba(255,255,255,.02);
border:1px solid rgba(255,255,255,.07);border-radius:9px"></div>""" for _ in range(len(word)))
            st.markdown(f"<div style='display:flex;gap:7px;justify-content:center;margin-bottom:7px'>{empty}</div>",unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)
    if msg:
        cls="ok" if "Win" in msg else ("err" if "word was" in msg else "inf")
        st.markdown(f"<div class='{cls}' style='padding:11px'>{msg}</div>",unsafe_allow_html=True)
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
    with c1: inp=st.text_input("Enter guess:",max_chars=len(word),key="wwin",label_visibility="collapsed").upper().strip()
    with c2:
        st.markdown('<div class="bg">',unsafe_allow_html=True)
        if st.button("🎯 Guess",use_container_width=True,key="wwok"):
            if len(inp)!=len(word): st.session_state["wm"]=f"⚠️ Must be {len(word)} letters!"
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
    st.markdown("<div style='color:#5566aa;font-size:11px;text-align:center;margin-top:8px;font-family:Share Tech Mono,monospace'>🟩 Correct position | 🟨 Wrong position | ⬜ Not in word</div>",unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
#  PONG 2P
# ═══════════════════════════════════════════════════════
def page_pong2p():
    st.markdown("<h1 style='text-align:center;letter-spacing:3px'>🏓 PONG — 2 PLAYERS</h1>",unsafe_allow_html=True)
    st.markdown("<div class='inf'>Player 1: W/S  ·  Player 2: ↑/↓  ·  First to 7 wins!</div>",unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    _,col,_=st.columns([1,10,1])
    with col:
        components.html("""<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>*{margin:0;padding:0;box-sizing:border-box}body{background:#04040f;display:flex;flex-direction:column;align-items:center;padding:10px;user-select:none}@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&display=swap');canvas{border:2px solid rgba(0,245,255,.2);border-radius:12px;box-shadow:0 0 40px rgba(0,245,255,.08);display:block}.ov{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);background:linear-gradient(145deg,rgba(4,4,20,.97),rgba(8,8,28,.97));border:1px solid rgba(0,245,255,.4);border-radius:16px;padding:24px 32px;text-align:center;backdrop-filter:blur(20px)}.ov h2{color:#00f5ff;font-family:'Orbitron',sans-serif;font-size:18px;margin-bottom:8px;text-shadow:0 0 16px rgba(0,245,255,.7)}.ov p{color:#8899bb;font-size:12px;margin-bottom:14px;font-family:monospace}.ov button{background:linear-gradient(135deg,rgba(0,245,255,.2),rgba(0,245,255,.06));color:#00f5ff;border:1px solid rgba(0,245,255,.5);padding:9px 22px;border-radius:8px;cursor:pointer;font-family:'Orbitron',sans-serif;font-size:12px;font-weight:700}.wrap{position:relative}</style></head><body>
<div class="wrap"><canvas id="c" width="560" height="340"></canvas><div class="ov" id="ov"><h2>🏓 2-PLAYER PONG</h2><p>P1: W/S | P2: ↑/↓<br>First to 7 wins!</p><button onclick="start()">▶ PLAY</button></div></div>
<script>
const W=560,H=340,PW=11,PH=70,BR=7;const cv=document.getElementById('c'),ctx=cv.getContext('2d');
let p1y,p2y,bx,by,vx,vy,s1,s2,run,raf,keys={},trail=[],parts=[];
function start(){document.getElementById('ov').style.display='none';p1y=H/2-PH/2;p2y=H/2-PH/2;bx=W/2;by=H/2;let a=(Math.random()*.7+.15)*Math.PI*(Math.random()<.5?1:-1);vx=Math.cos(a)*3.8;vy=Math.sin(a)*3.8;s1=s2=0;run=true;trail=[];parts=[];if(raf)cancelAnimationFrame(raf);loop();}
document.addEventListener('keydown',e=>{keys[e.code]=true;if(['KeyW','KeyS','ArrowUp','ArrowDown'].includes(e.code))e.preventDefault();});document.addEventListener('keyup',e=>keys[e.code]=false);
function loop(){if(!run)return;update();draw();raf=requestAnimationFrame(loop);}
function update(){if(keys['KeyW'])p1y=Math.max(0,p1y-5.5);if(keys['KeyS'])p1y=Math.min(H-PH,p1y+5.5);if(keys['ArrowUp'])p2y=Math.max(0,p2y-5.5);if(keys['ArrowDown'])p2y=Math.min(H-PH,p2y+5.5);bx+=vx;by+=vy;if(by<=BR||by>=H-BR){vy=-vy;spark(bx,by,'#ffd60a');}if(bx<=17+PW&&by>=p1y&&by<=p1y+PH){vx=Math.abs(vx)*1.03;vy+=(by-(p1y+PH/2))*.09;spark(bx,by,'#00f5ff');}if(bx>=W-17-PW&&by>=p2y&&by<=p2y+PH){vx=-Math.abs(vx)*1.03;vy+=(by-(p2y+PH/2))*.09;spark(bx,by,'#ff006e');}trail.unshift({x:bx,y:by,l:12});if(trail.length>14)trail.pop();trail.forEach(t=>t.l--);trail=trail.filter(t=>t.l>0);parts=parts.filter(p=>p.l>0);parts.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.l--;p.vx*=.92;});if(bx<0){s2++;if(s2>=7){end('Player 2 Wins! 🎉');return;}reset();}if(bx>W){s1++;if(s1>=7){end('Player 1 Wins! 🎉');return;}reset();}}
function spark(x,y,c){for(let i=0;i<8;i++)parts.push({x,y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,l:18,c});}
function reset(){bx=W/2;by=H/2;let a=(Math.random()*.7+.15)*Math.PI*(Math.random()<.5?1:-1);vx=Math.cos(a)*(3.8+Math.max(s1,s2)*.18);vy=Math.sin(a)*3.8;trail=[];}
function end(msg){run=false;cancelAnimationFrame(raf);document.getElementById('ov').querySelector('h2').textContent=msg;document.getElementById('ov').querySelector('p').textContent='P1: '+s1+' | P2: '+s2;document.getElementById('ov').style.display='block';}
function draw(){ctx.fillStyle='#04040f';ctx.fillRect(0,0,W,H);ctx.setLineDash([8,8]);ctx.strokeStyle='rgba(255,255,255,.05)';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(W/2,0);ctx.lineTo(W/2,H);ctx.stroke();ctx.setLineDash([]);ctx.font='bold 30px Orbitron,monospace';ctx.textAlign='center';ctx.fillStyle='rgba(0,245,255,.9)';ctx.shadowBlur=14;ctx.shadowColor='rgba(0,245,255,.6)';ctx.fillText(s1,W/2-75,40);ctx.fillStyle='rgba(255,0,110,.9)';ctx.shadowColor='rgba(255,0,110,.6)';ctx.fillText(s2,W/2+75,40);ctx.shadowBlur=0;trail.forEach((t,i)=>{ctx.globalAlpha=t.l/12*.45;ctx.fillStyle='#ffd60a';ctx.beginPath();ctx.arc(t.x,t.y,BR*t.l/12,0,Math.PI*2);ctx.fill();});ctx.globalAlpha=1;parts.forEach(p=>{ctx.globalAlpha=p.l/18;ctx.fillStyle=p.c;ctx.shadowBlur=4;ctx.shadowColor=p.c;ctx.beginPath();ctx.arc(p.x,p.y,2.5,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;});ctx.globalAlpha=1;[{x:15,y:p1y,c:'#00f5ff'},{x:W-15-PW,y:p2y,c:'#ff006e'}].forEach(p=>{let g=ctx.createLinearGradient(p.x,0,p.x+PW,0);g.addColorStop(0,p.c+'88');g.addColorStop(.5,p.c);g.addColorStop(1,p.c+'88');ctx.fillStyle=g;ctx.shadowBlur=16;ctx.shadowColor=p.c;ctx.beginPath();ctx.roundRect(p.x,p.y,PW,PH,5);ctx.fill();ctx.shadowBlur=0;});let bg2=ctx.createRadialGradient(bx-2,by-2,1,bx,by,BR);bg2.addColorStop(0,'#fff');bg2.addColorStop(.5,'#ffd60a');bg2.addColorStop(1,'#ff8800');ctx.fillStyle=bg2;ctx.shadowBlur=20;ctx.shadowColor='rgba(255,214,10,.9)';ctx.beginPath();ctx.arc(bx,by,BR,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;}
ctx.fillStyle='#04040f';ctx.fillRect(0,0,W,H);
</script></body></html>""", height=390, scrolling=False)

# ═══════════════════════════════════════════════════════
#  TIC-TAC-TOE 2P
# ═══════════════════════════════════════════════════════
def page_ttt2p():
    st.markdown("<h1 style='text-align:center;letter-spacing:3px'>❌ TIC-TAC-TOE — 2P</h1>",unsafe_allow_html=True)
    if "tb2" not in st.session_state:
        st.session_state.update({"tb2":[""]*9,"turn2":"X","tw2":{"X":0,"O":0},"to2":False,"ts2":""})
    b=st.session_state["tb2"]; turn=S("turn2","X"); wins=S("tw2",{"X":0,"O":0}); over=S("to2"); msg=S("ts2","")
    c1,c2,c3=st.columns(3)
    with c1: st.metric("❌ Player 1",wins.get("X",0))
    with c2: st.metric("⭕ Player 2",wins.get("O",0))
    with c3:
        col=("#00f5ff" if turn=="X" else "#ff006e")
        st.markdown(f"<div style='text-align:center;font-family:Orbitron,sans-serif;font-size:18px;color:{col};padding:10px;text-shadow:0 0 12px {col}'>{'❌ P1' if turn=='X' else '⭕ P2'}</div>",unsafe_allow_html=True)
    if msg:
        cls="ok" if "Wins" in msg else "inf"
        st.markdown(f"<div class='{cls}' style='font-size:15px;padding:12px;margin-bottom:12px'>{msg}</div>",unsafe_allow_html=True)
    _,mc,_=st.columns([1,2,1])
    with mc:
        for row in range(3):
            rc=st.columns(3)
            for ci in range(3):
                idx=row*3+ci
                with rc[ci]:
                    cell=b[idx]
                    if cell=="X":
                        st.markdown("""<div style="height:86px;background:linear-gradient(145deg,rgba(0,245,255,.1),rgba(0,245,255,.03));border:2px solid rgba(0,245,255,.55);border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:42px;font-weight:900;color:#00f5ff;text-shadow:0 0 20px rgba(0,245,255,.9);box-shadow:0 0 18px rgba(0,245,255,.1);animation:xPop .25s cubic-bezier(.34,1.56,.64,1)">✕</div>""",unsafe_allow_html=True)
                    elif cell=="O":
                        st.markdown("""<div style="height:86px;background:linear-gradient(145deg,rgba(255,0,110,.1),rgba(255,0,110,.03));border:2px solid rgba(255,0,110,.55);border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:42px;font-weight:900;color:#ff006e;text-shadow:0 0 20px rgba(255,0,110,.9);box-shadow:0 0 18px rgba(255,0,110,.1);animation:oPop .25s cubic-bezier(.34,1.56,.64,1)">○</div>""",unsafe_allow_html=True)
                    elif not over:
                        st.markdown("""<style>div.tttCell2 .stButton>button{height:86px!important;min-height:86px!important;background:linear-gradient(145deg,rgba(191,95,255,.05),rgba(191,95,255,.01))!important;border:1px solid rgba(191,95,255,.18)!important;border-radius:14px!important;font-size:0!important;transition:all .18s!important;}div.tttCell2 .stButton>button:hover{background:rgba(191,95,255,.12)!important;border-color:rgba(191,95,255,.5)!important;box-shadow:0 0 18px rgba(191,95,255,.18)!important;transform:scale(1.04)!important;}</style>""",unsafe_allow_html=True)
                        st.markdown('<div class="tttCell2">',unsafe_allow_html=True)
                        if st.button(" ",key=f"tt2_{idx}_{sum(1 for x in b if x)}",use_container_width=True):
                            b[idx]=turn; w=_tw(b)
                            if w:
                                wins[w]=wins.get(w,0)+1; st.session_state["tw2"]=wins
                                st.session_state.update({"ts2":f"{'❌ Player 1' if w=='X' else '⭕ Player 2'} Wins! 🎉","to2":True,"tb2":b})
                                earn(30); give_xp(15)
                            elif ""not in b: st.session_state.update({"ts2":"🤝 Draw!","to2":True,"tb2":b})
                            else: st.session_state.update({"turn2":"O" if turn=="X" else "X","tb2":b})
                            st.rerun()
                        st.markdown('</div>',unsafe_allow_html=True)
                    else:
                        st.markdown("""<div style="height:86px;background:rgba(255,255,255,.01);border:1px solid rgba(255,255,255,.04);border-radius:14px"></div>""",unsafe_allow_html=True)
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
    st.markdown("<h1 style='text-align:center;letter-spacing:3px'>🎲 DICE RACE — 2P</h1>",unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#5566aa;font-family:Share Tech Mono,monospace'>First to 100 wins! Roll or Hold each turn.</p>",unsafe_allow_html=True)
    if "dc2" not in st.session_state:
        st.session_state.update({"dc2":{"sc":[0,0],"turn":0,"cur":0,"dice":None,"over":False}})
    g=dict(st.session_state["dc2"]); sc=list(g["sc"]); turn=g["turn"]; cur=g["cur"]; over=g["over"]
    FACES=["","⚀","⚁","⚂","⚃","⚄","⚅"]
    cc=["#00f5ff","#ff006e"]
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
    st.markdown(f"<div class='inf' style='font-size:15px;padding:12px'>Turn: <b style='color:{cc[turn]}'>Player {turn+1}</b> &nbsp;·&nbsp; Current bank: <b style='color:{cc[turn]}'>{cur}</b></div>",unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    if g["dice"]:
        st.markdown(f"<div style='text-align:center;font-size:76px;filter:drop-shadow(0 0 16px {cc[turn]}80);animation:diceRoll .2s ease-out'>{FACES[g['dice']]}</div><style>@keyframes diceRoll{{from{{transform:rotate(-15deg) scale(.8)}}to{{transform:rotate(0) scale(1)}}}}</style>",unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    c1,c2,_=st.columns([1,1,1])
    with c1:
        if st.button("🎲 Roll",use_container_width=True,key="dc2r"):
            d=random.randint(1,6); g["dice"]=d
            if d==1: g["cur"]=0; g["turn"]=1-turn; g["dice"]=d
            else:
                g["cur"]=cur+d
                if sc[turn]+g["cur"]>=100:
                    sc[turn]+=g["cur"]; g["sc"]=sc; g["over"]=True
            st.session_state["dc2"]=g; st.rerun()
    with c2:
        st.markdown('<div class="bg">',unsafe_allow_html=True)
        if st.button("✋ Hold",use_container_width=True,key="dc2h",disabled=cur==0):
            sc[turn]+=cur; g["sc"]=sc; g["cur"]=0; g["turn"]=1-turn; g["dice"]=None
            st.session_state["dc2"]=g; st.rerun()
        st.markdown('</div>',unsafe_allow_html=True)
    for i in range(2):
        st.markdown(f"<div style='font-size:12px;color:{cc[i]};margin:8px 0 3px;font-family:Share Tech Mono,monospace'>Player {i+1}: {sc[i]}/100</div>",unsafe_allow_html=True)
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
    st.markdown("<h1 style='text-align:center;letter-spacing:3px'>💣 MINESWEEPER — 2P</h1>",unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#5566aa;font-family:Share Tech Mono,monospace'>Take turns revealing cells. Most safe cells wins!</p>",unsafe_allow_html=True)
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
    COLORS={0:"#334",1:"#00f5ff",2:"#39ff14",3:"#ff006e",4:"#bf5fff",5:"#ff7c00",6:"#ffd60a",7:"#fff",8:"#888"}
    _,mc,_=st.columns([1,6,1])
    with mc:
        for r in range(rows):
            rc=st.columns(cols_n)
            for c in range(cols_n):
                idx=r*cols_n+c; cell=b[r][c]
                with rc[c]:
                    if idx in rev:
                        if cell==-1:
                            st.markdown("""<div style="height:34px;background:linear-gradient(135deg,rgba(255,0,110,.18),rgba(255,0,110,.05));border:1px solid rgba(255,0,110,.45);border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:14px">💥</div>""",unsafe_allow_html=True)
                        else:
                            col_c=COLORS.get(cell,"#fff"); txt=str(cell) if cell else "·"
                            st.markdown(f"""<div style="height:34px;background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.06);border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;color:{col_c};font-family:Share Tech Mono,monospace">{txt}</div>""",unsafe_allow_html=True)
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
                                    cur2=stack.pop()
                                    if cur2 in rev: continue
                                    rev.add(cur2); gained+=1
                                    cr2,cc3=cur2//cols_n,cur2%cols_n
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
    st.markdown(f"""<div style="text-align:center;margin-bottom:22px">
<h1 style="letter-spacing:3px">🛒 UPGRADE SHOP</h1>
<div style="display:inline-flex;align-items:center;gap:12px;padding:12px 24px;
  background:linear-gradient(135deg,rgba(255,214,10,.1),rgba(255,214,10,.03));
  border:1px solid rgba(255,214,10,.35);border-radius:12px;margin-top:8px;
  box-shadow:0 0 24px rgba(255,214,10,.08)">
  <span style="font-size:24px">💰</span>
  <span style="font-family:'Orbitron',sans-serif;font-size:24px;font-weight:900;color:#ffd60a;
    text-shadow:0 0 12px rgba(255,214,10,.7)">{coins:,}</span>
  <span style="color:#5566aa;font-size:12px;font-family:Share Tech Mono,monospace">coins available</span>
</div></div>""", unsafe_allow_html=True)

    by_game={}
    for uid,item in SHOP.items(): by_game.setdefault(item["game"],[]).append((uid,item))
    tab_order=["Global","Snake","Flappy","Memory","Clicker","Slots","XO","Pong"]
    tabs=st.tabs([f" {g} " for g in tab_order if g in by_game])
    for ti,game in enumerate([g for g in tab_order if g in by_game]):
        with tabs[ti]:
            items=by_game[game]
            cols=st.columns(min(len(items),3))
            for i,(uid,item) in enumerate(items):
                cnt=oc(uid); mx=item["max"]; maxed=cnt>=mx; can=coins>=item["price"] and not maxed
                col_="#39ff14" if maxed else("#ffd60a" if can else "#5566aa")
                bg_=f"linear-gradient(145deg,rgba(57,255,20,.06),rgba(57,255,20,.01))" if maxed else "linear-gradient(145deg,rgba(255,255,255,.03),rgba(0,0,0,.2))"
                brd_="rgba(57,255,20,.4)" if maxed else("rgba(255,214,10,.32)" if can else "rgba(255,255,255,.06)")
                badge=(f"<div style='position:absolute;top:8px;right:8px;background:rgba(57,255,20,.15);border:1px solid rgba(57,255,20,.45);border-radius:5px;padding:2px 7px;font-size:9px;color:#39ff14;font-weight:700;font-family:Orbitron,sans-serif;letter-spacing:1px'>MAX</div>") if maxed else \
                      (f"<div style='position:absolute;top:8px;right:8px;background:rgba(0,245,255,.1);border:1px solid rgba(0,245,255,.3);border-radius:5px;padding:2px 7px;font-size:9px;color:#00f5ff;font-family:Share Tech Mono,monospace'>{cnt}/{mx}</div>") if cnt else ""
                with cols[i%3]:
                    st.markdown(f"""<div style="background:{bg_};border:1px solid {brd_};border-radius:14px;
padding:18px;text-align:center;margin-bottom:8px;min-height:145px;position:relative;
box-shadow:0 4px 20px rgba(0,0,0,.3){',0 0 20px rgba(57,255,20,.1)' if maxed else ''};
transition:all .2s ease;">
{badge}
<div style="font-size:32px;margin-bottom:8px;filter:drop-shadow(0 0 10px {col_}60)">{item['icon']}</div>
<div style="font-weight:700;font-size:13px;color:{col_};margin-bottom:4px;font-family:'Orbitron',sans-serif;letter-spacing:.5px">{item['name']}</div>
<div style="color:#5566aa;font-size:11px;margin-bottom:10px;line-height:1.5;font-family:'Rajdhani',sans-serif">{item['desc']}</div>
<div style="font-family:'Orbitron',sans-serif;font-size:14px;font-weight:900;
  color:{'#39ff14' if maxed else '#ffd60a'};text-shadow:0 0 8px {'rgba(57,255,20,.5)' if maxed else 'rgba(255,214,10,.5)'}">{'MAX ✓' if maxed else f'💰 {item["price"]:,}'}</div>
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
        st.markdown("<h3 style='font-size:14px;letter-spacing:2px'>🎒 MY UPGRADES</h3>",unsafe_allow_html=True)
        b2="".join(f"<span style='display:inline-flex;padding:5px 12px;"
                  f"background:linear-gradient(135deg,rgba(57,255,20,.07),rgba(57,255,20,.02));"
                  f"border:1px solid rgba(57,255,20,.3);border-radius:14px;font-size:11px;"
                  f"font-weight:700;color:#39ff14;margin:3px;font-family:Rajdhani,sans-serif;"
                  f"box-shadow:0 0 10px rgba(57,255,20,.07)'>{SHOP[uid]['icon']} {SHOP[uid]['name']}"
                  f"{' ×'+str(v) if v>1 else ''}</span>"
                  for uid,v in owned.items() if uid in SHOP)
        st.markdown(f"<div style='display:flex;flex-wrap:wrap;gap:3px'>{b2}</div>",unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<h3 style='font-size:14px;letter-spacing:2px'>💰 HOW TO EARN COINS</h3>",unsafe_allow_html=True)
    tips=[("🐍 Snake","Play & set high scores"),("🐦 Flappy","Pass pipes"),("🧠 Memory","Fewer moves = more coins"),
          ("❌ XO","Win vs AI = 50 coins"),("👆 Clicker","Clicks × 2"),("🎰 Slots","Match symbols"),
          ("🏓 Pong","Beat the AI"),("💣 Mines","Clear the field = 80 coins"),("🎯 Targets","Hit targets"),("🎲 Dice","Win race")]
    cols=st.columns(5)
    for i,(ico,tip) in enumerate(tips):
        with cols[i%5]:
            st.markdown(f"""<div style="background:linear-gradient(145deg,rgba(0,245,255,.03),rgba(0,0,0,.2));
border:1px solid rgba(0,245,255,.08);border-radius:10px;padding:12px;text-align:center;margin-bottom:8px">
<div style="font-size:22px;margin-bottom:5px">{ico}</div>
<div style="color:#5566aa;font-size:10px;font-family:'Rajdhani',sans-serif">{tip}</div></div>""",unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
#  ROUTER
# ═══════════════════════════════════════════════════════
ROUTES = {
    "lobby":       page_lobby,
    "snake":       page_snake,
    "flappy":      page_flappy,
    "memory":      page_memory,
    "ttt":         page_ttt,
    "clicker":     page_clicker,
    "slots":       page_slot,
    "pong":        page_pong,
    "minesweeper": page_minesweeper,
    "guess":       page_guess,
    "targets":     page_targets,
    "wordgame":    page_wordgame,
    "pong2p":      page_pong2p,
    "ttt2p":       page_ttt2p,
    "dice2p":      page_dice2p,
    "ms2p":        page_ms2p,
    "shop":        page_shop,
}

def main():
    inject_css()
    init()
    top_nav()
    page=S("page","lobby")
    ROUTES.get(page, page_lobby)()

if __name__=="__main__":
    main()
