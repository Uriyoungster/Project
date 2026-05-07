"""
🎮 ARCADE GALAXY v6 — Fixed Edition
Run: pip install streamlit && streamlit run project.py
"""
import streamlit as st
import streamlit.components.v1 as components
import random, time

st.set_page_config(page_title="🎮 Arcade Galaxy", page_icon="🎮",
                   layout="wide", initial_sidebar_state="collapsed")

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

def init():
    D = {"coins":500,"level":1,"xp":0,"ach":[],"owned":{},
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

def inject_css():
    st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;600;700&family=Share+Tech+Mono&display=swap');
:root{
  --bg:#04040f;--card:#080818;--card2:#0c0c20;
  --cyan:#00f5ff;--pink:#ff006e;--gold:#ffd60a;
  --green:#39ff14;--purple:#bf5fff;--orange:#ff7c00;
  --blue:#4488ff;--dim:#aabbdd;--fg:#e8ecff;
}
html,body,.stApp{background:var(--bg)!important;font-family:'Rajdhani',sans-serif!important;color:var(--fg)!important;}
.stApp{background-image:radial-gradient(ellipse 80% 50% at 20% 20%,rgba(0,245,255,.06),transparent),radial-gradient(ellipse 60% 40% at 80% 80%,rgba(191,95,255,.05),transparent)!important;}
.main .block-container{padding:0 16px 32px!important;max-width:100%!important;}
section[data-testid="stSidebar"]{display:none!important;}
h1,h2,h3{font-family:'Orbitron',sans-serif!important;color:var(--cyan)!important;font-size:22px!important;}
p,div,span,label{color:var(--fg)!important;}
.stButton>button{
  background:linear-gradient(135deg,rgba(0,245,255,.12),rgba(0,245,255,.04))!important;
  color:#00f5ff!important;border:1px solid rgba(0,245,255,.4)!important;
  border-radius:8px!important;font-family:'Rajdhani',sans-serif!important;
  font-weight:700!important;font-size:15px!important;letter-spacing:.5px!important;
  transition:all .18s!important;
}
.stButton>button:hover{background:rgba(0,245,255,.22)!important;border-color:var(--cyan)!important;box-shadow:0 0 20px rgba(0,245,255,.3)!important;transform:translateY(-2px)!important;}
.stButton>button:active{transform:translateY(0) scale(.99)!important;}
.stButton>button:disabled{opacity:.25!important;transform:none!important;}
.bg .stButton>button{background:linear-gradient(135deg,rgba(255,214,10,.15),rgba(255,214,10,.05))!important;color:#ffd60a!important;border-color:rgba(255,214,10,.5)!important;}
.bg .stButton>button:hover{background:rgba(255,214,10,.25)!important;box-shadow:0 0 20px rgba(255,214,10,.35)!important;}
.br .stButton>button{background:linear-gradient(135deg,rgba(255,0,110,.15),rgba(255,0,110,.05))!important;color:#ff006e!important;border-color:rgba(255,0,110,.5)!important;}
.br .stButton>button:hover{background:rgba(255,0,110,.25)!important;}
.bG .stButton>button{background:linear-gradient(135deg,rgba(57,255,20,.12),rgba(57,255,20,.04))!important;color:#39ff14!important;border-color:rgba(57,255,20,.4)!important;}
.bG .stButton>button:hover{background:rgba(57,255,20,.22)!important;}
.bp .stButton>button{background:linear-gradient(135deg,rgba(191,95,255,.12),rgba(191,95,255,.04))!important;color:#bf5fff!important;border-color:rgba(191,95,255,.4)!important;}
[data-testid="metric-container"]{background:linear-gradient(135deg,rgba(0,245,255,.06),rgba(0,0,0,.3))!important;border:1px solid rgba(0,245,255,.2)!important;border-radius:10px!important;padding:12px!important;}
[data-testid="metric-container"] label{color:#aabbdd!important;font-size:12px!important;font-family:'Share Tech Mono',monospace!important;letter-spacing:1px!important;}
[data-testid="metric-container"] [data-testid="stMetricValue"]{color:#00f5ff!important;font-family:'Orbitron',sans-serif!important;font-size:24px!important;text-shadow:0 0 12px rgba(0,245,255,.5)!important;}
.ok{padding:12px 16px;background:linear-gradient(135deg,rgba(57,255,20,.1),rgba(57,255,20,.03));border:1px solid rgba(57,255,20,.5);border-radius:10px;color:#39ff14!important;font-weight:700;text-align:center;font-family:'Rajdhani',sans-serif;font-size:16px;}
.err{padding:12px 16px;background:linear-gradient(135deg,rgba(255,0,110,.1),rgba(255,0,110,.03));border:1px solid rgba(255,0,110,.5);border-radius:10px;color:#ff006e!important;font-weight:700;text-align:center;font-family:'Rajdhani',sans-serif;font-size:16px;}
.inf{padding:12px 16px;background:linear-gradient(135deg,rgba(0,245,255,.08),rgba(0,245,255,.02));border:1px solid rgba(0,245,255,.35);border-radius:10px;color:#00f5ff!important;text-align:center;font-family:'Rajdhani',sans-serif;font-size:15px;}
.warn{padding:12px 16px;background:linear-gradient(135deg,rgba(255,214,10,.09),rgba(255,214,10,.02));border:1px solid rgba(255,214,10,.4);border-radius:10px;color:#ffd60a!important;text-align:center;font-family:'Rajdhani',sans-serif;font-size:15px;}
.stProgress>div>div>div{background:linear-gradient(90deg,var(--cyan),var(--purple),var(--pink))!important;border-radius:4px!important;}
.stProgress>div>div{background:rgba(255,255,255,.06)!important;border-radius:4px!important;}
hr{border:none!important;border-top:1px solid rgba(0,245,255,.1)!important;margin:20px 0!important;}
#MainMenu,footer,.stDeployButton{display:none!important;}
header[data-testid="stHeader"]{display:none!important;}
.stTabs [data-baseweb="tab-list"]{background:rgba(255,255,255,.03)!important;border-radius:8px!important;padding:3px!important;border:1px solid rgba(0,245,255,.15)!important;}
.stTabs [data-baseweb="tab"]{font-family:'Rajdhani',sans-serif!important;font-weight:700!important;font-size:14px!important;color:#aabbdd!important;border-radius:6px!important;}
.stTabs [aria-selected="true"]{background:linear-gradient(135deg,rgba(0,245,255,.18),rgba(0,245,255,.06))!important;color:#00f5ff!important;box-shadow:0 0 12px rgba(0,245,255,.2)!important;}
[data-testid="column"]{padding:0 4px!important;}
.stNumberInput input{background:rgba(0,245,255,.06)!important;border:1px solid rgba(0,245,255,.3)!important;border-radius:8px!important;color:#e8ecff!important;font-family:'Share Tech Mono',monospace!important;font-size:16px!important;}
.stTextInput input{background:rgba(0,245,255,.06)!important;border:1px solid rgba(0,245,255,.3)!important;border-radius:8px!important;color:#e8ecff!important;font-family:'Orbitron',sans-serif!important;letter-spacing:3px!important;text-transform:uppercase!important;font-size:16px!important;}
.stSlider [data-baseweb="slider"] div[role="slider"]{background:var(--gold)!important;box-shadow:0 0 10px var(--gold)!important;}
.stSelectbox select,.stSelectbox [data-baseweb="select"] div{background:rgba(0,245,255,.06)!important;border-color:rgba(0,245,255,.3)!important;color:#e8ecff!important;font-size:15px!important;}
::-webkit-scrollbar{width:4px;}::-webkit-scrollbar-track{background:var(--bg);}::-webkit-scrollbar-thumb{background:rgba(0,245,255,.2);border-radius:2px;}
</style>""", unsafe_allow_html=True)

def top_nav():
    lv=S("level",1); coins=S("coins",0); xpv=S("xp",0); need=lv*120
    pct=int(xpv/need*100)
    st.markdown(f"""<div style="display:flex;align-items:center;justify-content:space-between;
  padding:10px 24px;background:linear-gradient(180deg,rgba(4,4,20,.97),rgba(4,4,15,.92));
  border-bottom:1px solid rgba(0,245,255,.12);backdrop-filter:blur(20px);
  position:sticky;top:0;z-index:999;margin-bottom:20px;box-shadow:0 4px 30px rgba(0,0,0,.5)">
  <div style="display:flex;align-items:center;gap:12px">
    <div style="font-size:34px;filter:drop-shadow(0 0 14px rgba(0,245,255,.9))">🎮</div>
    <div>
      <div style="font-family:'Orbitron',sans-serif;font-size:20px;font-weight:900;
        background:linear-gradient(90deg,#00f5ff,#bf5fff,#ff006e);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;
        background-size:200%;animation:gradShift 4s linear infinite;letter-spacing:4px">ARCADE GALAXY</div>
      <div style="font-size:10px;color:#aabbdd;letter-spacing:3px;margin-top:-2px">ULTIMATE EDITION</div>
    </div>
  </div>
  <div style="display:flex;align-items:center;gap:10px">
    <div style="background:linear-gradient(135deg,rgba(255,214,10,.15),rgba(255,214,10,.05));
      border:1px solid rgba(255,214,10,.5);border-radius:10px;padding:8px 16px;
      display:flex;align-items:center;gap:8px">
      <span style="font-size:18px">💰</span>
      <span style="font-family:'Orbitron',sans-serif;font-size:18px;font-weight:900;color:#ffd60a;
        text-shadow:0 0 12px rgba(255,214,10,.7)">{coins:,}</span>
    </div>
    <div style="background:linear-gradient(135deg,rgba(0,245,255,.1),rgba(0,245,255,.03));
      border:1px solid rgba(0,245,255,.25);border-radius:10px;padding:8px 14px;min-width:100px">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">
        <span style="font-family:'Orbitron',sans-serif;font-size:11px;color:#00f5ff;font-weight:700">LV {lv}</span>
        <span style="font-size:9px;color:#aabbdd;font-family:'Share Tech Mono',monospace">{xpv}/{need}</span>
      </div>
      <div style="background:rgba(255,255,255,.06);border-radius:3px;height:4px;overflow:hidden">
        <div style="background:linear-gradient(90deg,#00f5ff,#bf5fff);width:{pct}%;height:100%;border-radius:3px"></div>
      </div>
    </div>
  </div>
</div>
<style>@keyframes gradShift{{0%{{background-position:0%}}100%{{background-position:200%}}}}</style>""", unsafe_allow_html=True)
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
    ("paintrace","🎨","Paint Race","#ffd60a","Cover the most tiles!",None,"1P"),
    ("wordgame","🔤","Word Guess","#bf5fff","Guess the 5-letter word!",None,"1P"),
    ("pong2p","🏓","Pong (2P)","#00f5ff","Two players, one keyboard",None,"2P"),
    ("ttt2p","❌","Tic-Tac-Toe 2P","#bf5fff","Two players on same screen",None,"2P"),
    ("dice2p","🎲","Dice Race 2P","#ffd60a","First to 100 wins!",None,"2P"),
    ("sumo2p","🥊","Sumo Push 2P","#ff006e","Push your opponent off!",None,"2P"),
]

def page_lobby():
    st.markdown("""<div style="text-align:center;padding:16px 0 30px">
<div style="font-size:64px;display:inline-block;filter:drop-shadow(0 0 20px rgba(0,245,255,.9))">🎮</div>
<h1 style="font-family:'Orbitron',sans-serif;font-size:36px;font-weight:900;margin:10px 0 6px;
  background:linear-gradient(90deg,#00f5ff,#bf5fff,#ff006e,#ffd60a,#00f5ff);background-size:400%;
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:sh 5s linear infinite;letter-spacing:4px">ARCADE GALAXY</h1>
<p style="color:#aabbdd;letter-spacing:4px;font-size:13px;margin:0">15 GAMES · 2-PLAYER · UPGRADES</p>
</div>
<style>@keyframes sh{0%{background-position:0%}100%{background-position:400%}}</style>""", unsafe_allow_html=True)

    lv=S("level",1); xpv=S("xp",0); need=lv*120
    c1,c2,c3,c4=st.columns(4)
    with c1: st.metric("💎 Level",lv)
    with c2: st.metric("💰 Coins",f"{S('coins',0):,}")
    with c3: st.metric("🏆 Achievements",len(S("ach",[])))
    with c4:
        total=sum(S(k,0) for k in["snake_pl","flappy_pl","mem_pl","ttt_pl","click_ses","slot_sp","pong_pl"])
        st.metric("🎮 Games Played",total)
    st.markdown("<br>",unsafe_allow_html=True)

    st.markdown("""<div style="display:flex;align-items:center;gap:12px;margin-bottom:16px">
<div style="height:1px;flex:1;background:linear-gradient(90deg,transparent,rgba(0,245,255,.3))"></div>
<span style="font-family:'Orbitron',sans-serif;font-size:13px;color:#00f5ff;letter-spacing:3px">🕹️ SINGLE PLAYER</span>
<div style="height:1px;flex:1;background:linear-gradient(90deg,rgba(0,245,255,.3),transparent)"></div>
</div>""", unsafe_allow_html=True)

    sp_games=[g for g in GAME_CARDS if g[6]=="1P"]
    cols=st.columns(4)
    for i,g in enumerate(sp_games):
        key,ico,name,col,desc,hi_key,_=g
        hi_val=S(hi_key,0) if hi_key else ""
        with cols[i%4]:
            best_str=f"Best: {hi_val}" if hi_val else "Play to set record"
            st.markdown(f"""<div style="background:linear-gradient(145deg,{col}12,rgba(4,4,20,.95));
border:1px solid {col}40;border-radius:14px;text-align:center;padding:18px 10px 14px;margin-bottom:6px;
position:relative;overflow:hidden">
<div style="position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,{col}90,transparent)"></div>
<div style="font-size:40px;margin-bottom:8px;filter:drop-shadow(0 0 12px {col}80)">{ico}</div>
<div style="font-family:'Orbitron',sans-serif;font-size:12px;font-weight:900;color:{col};margin-bottom:4px;letter-spacing:1px">{name}</div>
<div style="color:#aabbdd;font-size:12px;margin-bottom:10px">{desc}</div>
<div style="font-size:10px;color:{col}aa;font-family:'Share Tech Mono',monospace">{best_str}</div>
</div>""", unsafe_allow_html=True)
            if st.button(f"▶ Play", key=f"lobby_{key}", use_container_width=True):
                nav(key); st.rerun()

    st.markdown("<br>",unsafe_allow_html=True)
    st.markdown("""<div style="display:flex;align-items:center;gap:12px;margin-bottom:16px">
<div style="height:1px;flex:1;background:linear-gradient(90deg,transparent,rgba(255,0,110,.3))"></div>
<span style="font-family:'Orbitron',sans-serif;font-size:13px;color:#ff006e;letter-spacing:3px">👥 TWO PLAYERS</span>
<div style="height:1px;flex:1;background:linear-gradient(90deg,rgba(255,0,110,.3),transparent)"></div>
</div>""", unsafe_allow_html=True)

    mp_games=[g for g in GAME_CARDS if g[6]=="2P"]
    cols2=st.columns(4)
    for i,g in enumerate(mp_games):
        key,ico,name,col,desc,_,__=g
        with cols2[i%4]:
            st.markdown(f"""<div style="background:linear-gradient(145deg,{col}12,rgba(4,4,20,.95));
border:1px solid {col}40;border-radius:14px;text-align:center;padding:18px 10px 14px;margin-bottom:6px;
position:relative;overflow:hidden">
<div style="position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,{col}90,transparent)"></div>
<div style="font-size:40px;margin-bottom:8px;filter:drop-shadow(0 0 12px {col}80)">{ico}</div>
<div style="font-family:'Orbitron',sans-serif;font-size:12px;font-weight:900;color:{col};margin-bottom:4px;letter-spacing:1px">{name}</div>
<div style="color:#aabbdd;font-size:12px;margin-bottom:10px">{desc}</div>
<div style="font-size:10px;color:{col}aa;font-family:'Share Tech Mono',monospace">👥 Local Multiplayer</div>
</div>""", unsafe_allow_html=True)
            if st.button(f"▶ Play", key=f"lobby_{key}", use_container_width=True):
                nav(key); st.rerun()

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
        st.markdown("<h3 style='font-size:15px;letter-spacing:2px'>🏆 ACHIEVEMENTS</h3>",unsafe_allow_html=True)
        b="".join(f"<span style='display:inline-flex;padding:6px 14px;background:linear-gradient(135deg,rgba(255,214,10,.1),rgba(255,214,10,.03));border:1px solid rgba(255,214,10,.35);border-radius:16px;font-size:12px;font-weight:700;color:#ffd60a;margin:3px;font-family:Rajdhani,sans-serif'>{a}</span>" for a in achs[-15:])
        st.markdown(f"<div style='display:flex;flex-wrap:wrap;gap:3px'>{b}</div>",unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
#  SNAKE — fixed (no undefined vars in JS template)
# ═══════════════════════════════════════════════════════
def page_snake():
    st.markdown("<h1 style='text-align:center;letter-spacing:3px'>🐍 SNAKE</h1>",unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#aabbdd;font-family:Share Tech Mono,monospace;font-size:14px'>ARROW KEYS or WASD to move</p>",unsafe_allow_html=True)
    lives=1+oc("snake_life")
    wall_pass="true" if has("snake_wall") else "false"
    magnet="true" if has("snake_magnet") else "false"
    hi=S("snake_hi",0)
    ups=[]
    if lives>1: ups.append(f"💚 {lives} lives")
    if has("snake_wall"): ups.append("🌀 Wall pass")
    if has("snake_magnet"): ups.append("🧲 Magnet")
    if ups: st.markdown(f"<div class='inf'>{'  |  '.join(ups)}</div>",unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    _,col,_=st.columns([1,10,1])
    with col:
        snake_html = """<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>*{margin:0;padding:0;box-sizing:border-box}
body{background:#04040f;display:flex;flex-direction:column;align-items:center;padding:10px;user-select:none;font-family:'Share Tech Mono',monospace}
.hud{display:flex;gap:10px;margin-bottom:10px;flex-wrap:wrap;justify-content:center}
.h{background:linear-gradient(135deg,rgba(57,255,20,.1),rgba(57,255,20,.03));border:1px solid rgba(57,255,20,.4);border-radius:8px;padding:6px 16px;color:#39ff14;font-size:13px;font-weight:700}
canvas{border:2px solid rgba(57,255,20,.3);border-radius:12px;box-shadow:0 0 40px rgba(57,255,20,.1);display:block}
.ov{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
background:linear-gradient(145deg,rgba(4,4,20,.97),rgba(8,8,28,.97));
border:1px solid rgba(57,255,20,.5);border-radius:16px;padding:28px 36px;
text-align:center;min-width:200px;backdrop-filter:blur(20px)}
.ov h2{color:#39ff14;font-family:'Orbitron',sans-serif;font-size:20px;margin-bottom:10px;text-shadow:0 0 16px rgba(57,255,20,.8)}
.ov p{color:#aabbdd;font-size:13px;margin-bottom:16px}
.ov button{background:linear-gradient(135deg,rgba(57,255,20,.2),rgba(57,255,20,.06));color:#39ff14;border:1px solid rgba(57,255,20,.5);padding:10px 24px;border-radius:8px;cursor:pointer;font-family:'Orbitron',sans-serif;font-size:13px;font-weight:700;transition:all .18s}
.ov button:hover{background:rgba(57,255,20,.3);box-shadow:0 0 20px rgba(57,255,20,.3)}
.wrap{position:relative}</style></head><body>
<div class="hud">
  <div class="h">SCORE: <span id="sc">0</span></div>
  <div class="h">BEST: <span id="hi">HI_PLACEHOLDER</span></div>
  <div class="h">LIVES: <span id="lv">LV_PLACEHOLDER</span></div>
  <div class="h">SPEED: <span id="sp">1</span></div>
</div>
<div class="wrap"><canvas id="c"></canvas>
<div class="ov" id="ov"><h2>🐍 SNAKE</h2><p>Arrow keys or WASD to move</p>
<button onclick="startGame()">▶ PLAY</button></div></div>
<script>
const G=22,C=20;
const WP=WALLPASS_PLACEHOLDER,MAG=MAGNET_PLACEHOLDER,ML=LIVES_PLACEHOLDER;
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
cv.width=cv.height=G*C;
let sn,dir,nd,food,bon,score,lives2,spd,loop,run,parts,trail;
function startGame(){
  document.getElementById('ov').style.display='none';
  sn=[{x:11,y:11},{x:10,y:11},{x:9,y:11}];
  dir={x:1,y:0};nd={x:1,y:0};
  score=0;lives2=ML;spd=1;parts=[];bon=null;trail=[];run=true;
  document.getElementById('sc').textContent=0;
  document.getElementById('lv').textContent=ML;
  document.getElementById('sp').textContent=1;
  placeFood();if(loop)clearInterval(loop);loop=setInterval(update,155);
}
document.addEventListener('keydown',function(e){
  var k={ArrowUp:{x:0,y:-1},ArrowDown:{x:0,y:1},ArrowLeft:{x:-1,y:0},ArrowRight:{x:1,y:0},
    KeyW:{x:0,y:-1},KeyS:{x:0,y:1},KeyA:{x:-1,y:0},KeyD:{x:1,y:0}};
  var n=k[e.code];
  if(n&&(n.x!=-dir.x||n.y!=-dir.y)){nd=n;e.preventDefault();}
});
function placeFood(){
  var p;
  do{p={x:Math.floor(Math.random()*G),y:Math.floor(Math.random()*G)};}
  while(sn.some(function(s){return s.x===p.x&&s.y===p.y;}));
  food=p;
}
function spark(x,y,c,n){
  n=n||10;
  for(var i=0;i<n;i++)parts.push({x:x*C+C/2,y:y*C+C/2,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,l:30,c:c,r:Math.random()*3+1});
}
function update(){
  if(!run)return;
  dir={x:nd.x,y:nd.y};
  var h={x:sn[0].x+dir.x,y:sn[0].y+dir.y};
  if(WP){h.x=(h.x+G)%G;h.y=(h.y+G)%G;}
  else if(h.x<0||h.x>=G||h.y<0||h.y>=G){die();return;}
  if(sn.slice(1).some(function(s){return s.x===h.x&&s.y===h.y;})){die();return;}
  if(MAG){
    var dx=food.x-h.x,dy=food.y-h.y;
    if(Math.abs(dx)+Math.abs(dy)<=4){
      if(dx)food.x+=dx>0?-1:1;else if(dy)food.y+=dy>0?-1:1;
    }
  }
  trail.push({x:sn[0].x*C+C/2,y:sn[0].y*C+C/2,l:8});
  if(trail.length>12)trail.shift();
  sn.unshift(h);
  var grew=false;
  if(h.x===food.x&&h.y===food.y){
    score+=10;grew=true;
    spark(food.x,food.y,'#39ff14',12);
    placeFood();
    document.getElementById('sc').textContent=score;
    var ns=1+Math.floor(score/60);
    if(ns>spd){spd=ns;clearInterval(loop);loop=setInterval(update,Math.max(60,155-spd*22));document.getElementById('sp').textContent=spd;}
  }
  if(!grew)sn.pop();
  parts=parts.filter(function(p){return p.l>0;});
  parts.forEach(function(p){p.x+=p.vx;p.y+=p.vy;p.l--;p.vy+=.08;p.vx*=.97;});
  trail=trail.filter(function(t){return t.l>0;});
  trail.forEach(function(t){t.l--;});
  draw();
}
function die(){
  lives2--;
  document.getElementById('lv').textContent=lives2;
  spark(sn[0].x,sn[0].y,'#ff006e',20);
  if(lives2<=0){
    run=false;clearInterval(loop);
    var hs=parseInt(document.getElementById('hi').textContent)||0;
    if(score>hs)document.getElementById('hi').textContent=score;
    var ov=document.getElementById('ov');
    ov.querySelector('h2').textContent='💀 GAME OVER';
    ov.querySelector('p').textContent='Score: '+score;
    ov.style.display='block';
  }else{
    sn=[{x:11,y:11},{x:10,y:11},{x:9,y:11}];
    dir={x:1,y:0};nd={x:1,y:0};trail=[];
  }
}
function rr(x,y,w,h,r){
  ctx.beginPath();ctx.moveTo(x+r,y);ctx.lineTo(x+w-r,y);ctx.quadraticCurveTo(x+w,y,x+w,y+r);
  ctx.lineTo(x+w,y+h-r);ctx.quadraticCurveTo(x+w,y+h,x+w-r,y+h);ctx.lineTo(x+r,y+h);
  ctx.quadraticCurveTo(x,y+h,x,y+h-r);ctx.lineTo(x,y+r);ctx.quadraticCurveTo(x,y,x+r,y);ctx.closePath();
}
function draw(){
  ctx.fillStyle='#04040f';ctx.fillRect(0,0,G*C,G*C);
  ctx.strokeStyle='rgba(57,255,20,.04)';ctx.lineWidth=.5;
  for(var i=0;i<=G;i++){
    ctx.beginPath();ctx.moveTo(i*C,0);ctx.lineTo(i*C,G*C);ctx.stroke();
    ctx.beginPath();ctx.moveTo(0,i*C);ctx.lineTo(G*C,i*C);ctx.stroke();
  }
  ctx.globalAlpha=1;
  trail.forEach(function(t){
    ctx.globalAlpha=t.l/8*.3;ctx.fillStyle='#39ff14';
    ctx.beginPath();ctx.arc(t.x,t.y,2,0,Math.PI*2);ctx.fill();
  });ctx.globalAlpha=1;
  parts.forEach(function(p){
    ctx.globalAlpha=p.l/30;ctx.fillStyle=p.c;ctx.shadowBlur=6;ctx.shadowColor=p.c;
    ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
  });ctx.globalAlpha=1;
  var t2=Date.now()/300;
  ctx.save();ctx.translate(food.x*C+C/2,food.y*C+C/2);
  ctx.scale(1+Math.sin(t2)*.18,1+Math.sin(t2)*.18);
  ctx.shadowBlur=20;ctx.shadowColor='#39ff14';ctx.fillStyle='#39ff14';
  ctx.beginPath();ctx.arc(0,0,C/2-2,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='rgba(255,255,255,.35)';ctx.beginPath();ctx.arc(-2,-2,C/5,0,Math.PI*2);ctx.fill();
  ctx.shadowBlur=0;ctx.restore();
  sn.forEach(function(seg,i){
    ctx.save();
    var ratio=i/sn.length;
    var baseG=215-ratio*90;
    if(i===0){ctx.shadowBlur=16;ctx.shadowColor='rgba(57,255,20,.9)';ctx.fillStyle='#fff';}
    else{ctx.fillStyle='rgba(0,'+Math.round(baseG)+',255,.9)';}
    var pd=i===0?1:2,rd=i===0?5:3;
    rr(seg.x*C+pd,seg.y*C+pd,C-pd*2,C-pd*2,rd);ctx.fill();
    if(i===0){
      ctx.shadowBlur=0;ctx.fillStyle='#04040f';
      ctx.beginPath();ctx.arc(seg.x*C+C*.3+dir.y*C*.2,seg.y*C+C*.3-dir.x*C*.2,2.2,0,Math.PI*2);ctx.fill();
      ctx.beginPath();ctx.arc(seg.x*C+C*.7-dir.y*C*.2,seg.y*C+C*.3-dir.x*C*.2,2.2,0,Math.PI*2);ctx.fill();
    }
    ctx.restore();
  });
}
ctx.fillStyle='#04040f';ctx.fillRect(0,0,G*C,G*C);
</script></body></html>"""
        snake_html = snake_html.replace("HI_PLACEHOLDER", str(hi))
        snake_html = snake_html.replace("LV_PLACEHOLDER", str(lives))
        snake_html = snake_html.replace("WALLPASS_PLACEHOLDER", wall_pass)
        snake_html = snake_html.replace("MAGNET_PLACEHOLDER", magnet)
        snake_html = snake_html.replace("LIVES_PLACEHOLDER", str(lives))
        components.html(snake_html, height=G*C+100, scrolling=False)

    st.markdown("---")
    c1,c2=st.columns(2)
    with c1: st.metric("🏆 Best",S("snake_hi",0))
    with c2: st.metric("🎮 Games",S("snake_pl",0))

# ═══════════════════════════════════════════════════════
#  FLAPPY — no new game button at bottom
# ═══════════════════════════════════════════════════════
def page_flappy():
    st.markdown("<h1 style='text-align:center;letter-spacing:3px'>🐦 FLAPPY BIRD</h1>",unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#aabbdd;font-family:Share Tech Mono,monospace;font-size:14px'>SPACE or CLICK to flap</p>",unsafe_allow_html=True)
    sh=oc("flappy_shield"); gap=110+oc("flappy_gap")*15
    slow_ps=1.7 if has("flappy_slow") else 2.5
    hi=S("flappy_hi",0)
    if sh or has("flappy_slow") or has("flappy_gap"):
        gap_count=oc("flappy_gap")
        parts2=list(filter(None,[
            f'🛡 {sh} shields' if sh else '',
            '🐌 Slow pipes' if has("flappy_slow") else '',
            f'🔓 Gap +{gap_count*15}' if has("flappy_gap") else '',
        ]))
        st.markdown(f"<div class='inf'>{'  |  '.join(parts2)}</div>",unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    _,col,_=st.columns([1,8,1])
    with col:
        flappy_html = """<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>*{margin:0;padding:0;box-sizing:border-box}
body{background:#04040f;display:flex;flex-direction:column;align-items:center;padding:10px;user-select:none;font-family:'Share Tech Mono',monospace}
.hud{display:flex;gap:10px;margin-bottom:10px}
.h{background:linear-gradient(135deg,rgba(255,214,10,.1),rgba(255,214,10,.03));border:1px solid rgba(255,214,10,.4);border-radius:8px;padding:6px 16px;color:#ffd60a;font-size:13px;font-weight:700}
canvas{border:2px solid rgba(255,214,10,.35);border-radius:12px;box-shadow:0 0 40px rgba(255,214,10,.1);cursor:pointer;display:block}
.ov{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
background:linear-gradient(145deg,rgba(4,4,20,.97),rgba(8,8,28,.97));
border:1px solid rgba(255,214,10,.5);border-radius:16px;padding:28px 36px;text-align:center;min-width:200px;backdrop-filter:blur(20px)}
.ov h2{color:#ffd60a;font-family:'Orbitron',sans-serif;font-size:20px;margin-bottom:10px;text-shadow:0 0 16px rgba(255,214,10,.8)}
.ov p{color:#aabbdd;font-size:13px;margin-bottom:16px}
.ov button{background:linear-gradient(135deg,rgba(255,214,10,.2),rgba(255,214,10,.06));color:#ffd60a;border:1px solid rgba(255,214,10,.5);padding:10px 24px;border-radius:8px;cursor:pointer;font-family:'Orbitron',sans-serif;font-size:13px;font-weight:700;transition:all .18s}
.ov button:hover{background:rgba(255,214,10,.3)}
.wrap{position:relative}</style></head><body>
<div class="hud">
  <div class="h">SCORE: <span id="sc">0</span></div>
  <div class="h">BEST: <span id="hi">HI_PH</span></div>
  <div class="h">🛡 <span id="sh">SH_PH</span></div>
</div>
<div class="wrap"><canvas id="c" width="340" height="460"></canvas>
<div class="ov" id="ov">
  <h2 id="ot">🐦 FLAPPY BIRD</h2>
  <p>SPACE or click to flap</p>
  <button onclick="startGame()">▶ PLAY</button>
</div></div>
<script>
var W=340,H=460,BR=13,PS=SLOWPS_PH,GAP=GAP_PH,ISH=SH_PH2;
var cv=document.getElementById('c'),ctx=cv.getContext('2d');
var bird,pipes,score,frame,run,raf,shL,parts3,stars,clouds;
function mkBg(){
  stars=[];for(var i=0;i<70;i++)stars.push({x:Math.random()*W,y:Math.random()*H*.72,r:Math.random()*1.5+.3,s:Math.random()*.2+.06,b:Math.random()});
  clouds=[];for(var i=0;i<5;i++)clouds.push({x:Math.random()*W,y:20+Math.random()*80,w:40+Math.random()*60,s:Math.random()*.3+.1});
}
function startGame(){
  document.getElementById('ov').style.display='none';
  bird={x:75,y:H/2,vy:0,rot:0};pipes=[];score=0;frame=0;run=true;shL=ISH;parts3=[];
  document.getElementById('sc').textContent='0';
  document.getElementById('sh').textContent=shL;
  if(raf)cancelAnimationFrame(raf);mkBg();loop();
}
function flap(){if(run){bird.vy=-7.2;}}
cv.addEventListener('click',flap);
document.addEventListener('keydown',function(e){if(e.code==='Space'){flap();e.preventDefault();}});
function loop(){if(!run)return;update();draw();raf=requestAnimationFrame(loop);}
function update(){
  frame++;bird.vy+=.35;bird.y+=bird.vy;bird.rot=Math.min(Math.max(bird.vy*3.5,-35),90);
  parts3=parts3.filter(function(p){return p.l>0;});
  parts3.forEach(function(p){p.x+=p.vx;p.y+=p.vy;p.l--;});
  stars.forEach(function(s){s.x-=s.s;if(s.x<0){s.x=W;s.y=Math.random()*H*.72;}});
  clouds.forEach(function(c){c.x-=c.s;if(c.x+c.w<0)c.x=W+c.w;});
  if(frame%85===0)pipes.push({x:W,th:55+Math.random()*(H-GAP-105),ok:false});
  pipes.forEach(function(p){p.x-=PS;});
  pipes=pipes.filter(function(p){return p.x>-55;});
  pipes.forEach(function(p){
    if(!p.ok&&p.x+45<bird.x){
      p.ok=true;score++;document.getElementById('sc').textContent=score;
    }
    if(bird.x+BR>p.x&&bird.x-BR<p.x+46&&(bird.y-BR<p.th||bird.y+BR>p.th+GAP)){
      if(shL>0){shL--;document.getElementById('sh').textContent=shL;}
      else die();
    }
  });
  if(bird.y+BR>H-28||bird.y-BR<0)die();
}
function die(){
  run=false;cancelAnimationFrame(raf);
  var hs=parseInt(document.getElementById('hi').textContent)||0;
  if(score>hs)document.getElementById('hi').textContent=score;
  document.getElementById('ot').textContent='💥 CRASHED!';
  document.getElementById('ov').querySelector('p').textContent='Score: '+score;
  document.getElementById('ov').style.display='block';
}
function drawPipe(x,th){
  var g=ctx.createLinearGradient(x,0,x+46,0);
  g.addColorStop(0,'#0d3d12');g.addColorStop(.4,'#1a6b20');g.addColorStop(1,'#0d3d12');
  ctx.fillStyle=g;ctx.fillRect(x,0,46,th);ctx.fillRect(x,th+GAP,46,H-(th+GAP));
  ctx.fillStyle='#1e8026';ctx.fillRect(x-5,th-18,56,18);ctx.fillRect(x-5,th+GAP,56,18);
}
function draw(){
  ctx.fillStyle='#02020a';ctx.fillRect(0,0,W,H);
  stars.forEach(function(s){
    ctx.globalAlpha=.3+Math.sin(frame*.04+s.b*6)*.3;ctx.fillStyle='#fff';
    ctx.beginPath();ctx.arc(s.x,s.y,s.r,0,Math.PI*2);ctx.fill();
  });ctx.globalAlpha=1;
  pipes.forEach(function(p){drawPipe(p.x,p.th);});
  ctx.fillStyle='#101a10';ctx.fillRect(0,H-28,W,28);
  ctx.fillStyle='rgba(57,255,20,.2)';ctx.fillRect(0,H-28,W,2);
  ctx.save();ctx.translate(bird.x,bird.y);ctx.rotate(bird.rot*Math.PI/180);
  if(shL>0){
    ctx.beginPath();ctx.arc(0,0,BR+9,0,Math.PI*2);
    ctx.strokeStyle='rgba(0,245,255,.7)';ctx.lineWidth=2;ctx.stroke();
  }
  ctx.shadowBlur=14;ctx.shadowColor='rgba(255,214,10,.8)';
  var bg2=ctx.createRadialGradient(-2,-2,1,0,0,BR);
  bg2.addColorStop(0,'#fff9c4');bg2.addColorStop(.5,'#ffd60a');bg2.addColorStop(1,'#ff8f00');
  ctx.fillStyle=bg2;ctx.beginPath();ctx.ellipse(0,0,BR,BR-1,0,0,Math.PI*2);ctx.fill();
  ctx.shadowBlur=0;
  ctx.fillStyle='#fff';ctx.beginPath();ctx.arc(5.5,-2,3.5,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='#1a0a00';ctx.beginPath();ctx.arc(6.5,-2,2,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='#ff6600';ctx.beginPath();ctx.moveTo(BR+1,0);ctx.lineTo(BR+7,1.5);ctx.lineTo(BR+1,-2);ctx.fill();
  ctx.restore();
  ctx.fillStyle='rgba(255,214,10,.95)';ctx.font='bold 28px Orbitron,monospace';ctx.textAlign='center';
  ctx.shadowBlur=16;ctx.shadowColor='rgba(255,214,10,.8)';ctx.fillText(score,W/2,50);ctx.shadowBlur=0;
}
mkBg();ctx.fillStyle='#04040f';ctx.fillRect(0,0,W,H);
</script></body></html>"""
        flappy_html = flappy_html.replace("HI_PH", str(hi))
        flappy_html = flappy_html.replace("SH_PH", str(sh)).replace("SH_PH2", str(sh))
        flappy_html = flappy_html.replace("SLOWPS_PH", str(slow_ps))
        flappy_html = flappy_html.replace("GAP_PH", str(gap))
        components.html(flappy_html, height=520, scrolling=False)

    st.markdown("---")
    c1,c2=st.columns(2)
    with c1: st.metric("🏆 Best",S("flappy_hi",0))
    with c2: st.metric("🎮 Games",S("flappy_pl",0))

# ═══════════════════════════════════════════════════════
#  MEMORY — canvas only, no button grid below
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
    st.markdown("<p style='text-align:center;color:#aabbdd;font-family:Share Tech Mono,monospace;font-size:14px'>Click tiles to flip — find all pairs!</p>",unsafe_allow_html=True)
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

    if S("mpend") and time.time()-S("mptime",0)>=1.0:
        f2=list(S("mf",[]))
        if len(f2)==2:
            i1,i2=f2
            if b[i1]==b[i2]:
                mm.add(i1); mm.add(i2); st.session_state["mm"]=mm
        st.session_state["mf"]=[]; st.session_state["mpend"]=False; st.rerun()
    if S("mpend"): time.sleep(0.05); st.rerun()

    can_flip = len(fl)<2 and not S("mpend")

    mm_list = list(mm)
    fl_list = list(fl)
    emj_js = "[" + ",".join('"' + EMJ[b[i]] + '"' for i in range(16)) + "]"
    mm_js = "[" + ",".join(str(x) for x in mm_list) + "]"
    fl_js = "[" + ",".join(str(x) for x in fl_list) + "]"
    can_js = "true" if can_flip else "false"

    # Render card grid — clicking sends to Streamlit via hidden form pattern
    # We render each card as a clickable div with streamlit buttons underneath styled to fill the card
    for row in range(4):
        btn_cols = st.columns(4)
        for col_i in range(4):
            idx = row*4 + col_i
            with btn_cols[col_i]:
                if idx in mm:
                    em = EMJ[b[idx]]
                    st.markdown(f"""<div style="height:80px;background:linear-gradient(135deg,rgba(57,255,20,.12),rgba(57,255,20,.04));
border:2px solid rgba(57,255,20,.6);border-radius:12px;display:flex;align-items:center;
justify-content:center;font-size:32px;box-shadow:0 0 16px rgba(57,255,20,.2);margin-bottom:4px;
animation:matchPop .4s ease">{em}</div>
<style>@keyframes matchPop{{0%{{transform:scale(.8)}}60%{{transform:scale(1.08)}}100%{{transform:scale(1)}}}}</style>""",unsafe_allow_html=True)
                elif idx in fl:
                    em = EMJ[b[idx]]
                    st.markdown(f"""<div style="height:80px;background:linear-gradient(135deg,rgba(0,245,255,.12),rgba(0,245,255,.04));
border:2px solid rgba(0,245,255,.6);border-radius:12px;display:flex;align-items:center;
justify-content:center;font-size:32px;box-shadow:0 0 16px rgba(0,245,255,.2);margin-bottom:4px">{em}</div>""",unsafe_allow_html=True)
                elif not can_flip:
                    st.markdown("""<div style="height:80px;background:linear-gradient(135deg,rgba(191,95,255,.06),rgba(191,95,255,.02));
border:1px solid rgba(191,95,255,.2);border-radius:12px;display:flex;align-items:center;
justify-content:center;font-size:22px;color:rgba(191,95,255,.3);font-family:Orbitron,sans-serif;font-weight:900;margin-bottom:4px">?</div>""",unsafe_allow_html=True)
                else:
                    st.markdown("""<style>div.memCard .stButton>button{
height:80px!important;min-height:80px!important;font-size:22px!important;
background:linear-gradient(135deg,rgba(191,95,255,.1),rgba(191,95,255,.03))!important;
border:1px solid rgba(191,95,255,.35)!important;border-radius:12px!important;
color:rgba(191,95,255,.6)!important;font-weight:900!important;font-family:'Orbitron',sans-serif!important;
transition:all .15s!important;margin-bottom:4px!important;}
div.memCard .stButton>button:hover{background:rgba(191,95,255,.18)!important;border-color:rgba(191,95,255,.7)!important;
box-shadow:0 0 18px rgba(191,95,255,.25)!important;transform:scale(1.04)!important;color:rgba(191,95,255,.9)!important;}
</style>""",unsafe_allow_html=True)
                    st.markdown('<div class="memCard">',unsafe_allow_html=True)
                    if st.button("?", key=f"mc_{idx}_{mv}_{len(mm)}", use_container_width=True):
                        fl.append(idx); st.session_state["mf"]=fl
                        if len(fl)==2:
                            st.session_state["mov"]=mv+1
                            st.session_state["mpend"]=True
                            st.session_state["mptime"]=time.time()
                        st.rerun()
                    st.markdown('</div>',unsafe_allow_html=True)

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
#  TIC-TAC-TOE 1P — consistent cell sizes
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

CELL_STYLE = """<style>
div.tttCell .stButton>button{
  height:96px!important;min-height:96px!important;width:100%!important;
  background:linear-gradient(145deg,rgba(191,95,255,.08),rgba(191,95,255,.02))!important;
  border:1px solid rgba(191,95,255,.25)!important;border-radius:14px!important;
  font-size:0!important;transition:all .15s!important;
}
div.tttCell .stButton>button:hover{
  background:rgba(191,95,255,.16)!important;border-color:rgba(191,95,255,.6)!important;
  box-shadow:0 0 18px rgba(191,95,255,.2)!important;transform:scale(1.03)!important;
}
</style>"""

def _ttt_cell_x():
    return """<div style="height:96px;
background:linear-gradient(145deg,rgba(0,245,255,.12),rgba(0,245,255,.04));
border:2px solid rgba(0,245,255,.6);border-radius:14px;
display:flex;align-items:center;justify-content:center;
font-size:48px;font-weight:900;color:#00f5ff;
text-shadow:0 0 20px rgba(0,245,255,.9);
box-shadow:0 0 18px rgba(0,245,255,.12)">✕</div>"""

def _ttt_cell_o():
    return """<div style="height:96px;
background:linear-gradient(145deg,rgba(255,0,110,.12),rgba(255,0,110,.04));
border:2px solid rgba(255,0,110,.6);border-radius:14px;
display:flex;align-items:center;justify-content:center;
font-size:48px;font-weight:900;color:#ff006e;
text-shadow:0 0 20px rgba(255,0,110,.9);
box-shadow:0 0 18px rgba(255,0,110,.12)">○</div>"""

def _ttt_cell_empty_over():
    return """<div style="height:96px;background:rgba(255,255,255,.01);
border:1px solid rgba(255,255,255,.05);border-radius:14px"></div>"""

def page_ttt():
    st.markdown("<h1 style='text-align:center;letter-spacing:3px'>❌ TIC-TAC-TOE</h1>",unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#aabbdd;font-family:Share Tech Mono,monospace;font-size:14px'>YOU = X (cyan) · AI = O (pink)</p>",unsafe_allow_html=True)
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

    _,mc,_=st.columns([1,2,1])
    with mc:
        for row in range(3):
            rc=st.columns(3)
            for ci in range(3):
                idx=row*3+ci; cell=b[idx]
                with rc[ci]:
                    if cell=="X":
                        st.markdown(_ttt_cell_x(), unsafe_allow_html=True)
                    elif cell=="O":
                        st.markdown(_ttt_cell_o(), unsafe_allow_html=True)
                    elif not ov:
                        st.markdown(CELL_STYLE, unsafe_allow_html=True)
                        st.markdown('<div class="tttCell">', unsafe_allow_html=True)
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
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(_ttt_cell_empty_over(), unsafe_allow_html=True)

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
  text-shadow:0 0 30px {'rgba(255,0,110,.8)' if danger else 'rgba(0,245,255,.8)'}">{rem:.1f}</div>
<div style="color:#aabbdd;font-size:12px;font-family:Share Tech Mono,monospace">SECONDS REMAINING</div>
</div>""",unsafe_allow_html=True)
        st.progress(rem/dur)
        if rem<=0: st.session_state["cks"]="done"; st.rerun()

    col_c="#ff006e" if state=="playing" else("#39ff14" if state=="done" else "#aabbdd")
    st.markdown(f"""<div style="text-align:center;margin:12px 0">
<div style="font-family:'Orbitron',sans-serif;font-size:80px;font-weight:900;
  color:{col_c};text-shadow:0 0 40px {col_c}90">{cnt}</div>
<div style="color:#aabbdd;font-size:13px;font-family:Share Tech Mono,monospace">CLICKS</div>
</div>""",unsafe_allow_html=True)

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
div.ckB .stButton>button{background:linear-gradient(145deg,rgba(255,0,110,.25),rgba(255,0,110,.08))!important;
border:2px solid rgba(255,0,110,.7)!important;color:#ff006e!important;
font-size:24px!important;height:120px!important;font-weight:900!important;letter-spacing:2px!important;
box-shadow:0 0 30px rgba(255,0,110,.2)!important;font-family:'Orbitron',sans-serif!important;}
div.ckB .stButton>button:active{transform:scale(.94)!important;}</style>""",unsafe_allow_html=True)
            st.markdown('<div class="ckB">',unsafe_allow_html=True)
            if st.button("👆 CLICK!",use_container_width=True,key="ckc_btn"):
                st.session_state["ckc"]=cnt+mul; st.session_state["click_tot"]=S("click_tot",0)+mul; st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)
        elif state=="done":
            final=S("ckc",0); e=earn(final*2); give_xp(final)
            if final>best: st.session_state["click_hi"]=final; add_ach(f"👆 Clicker Record: {final}!")
            st.markdown(f"<div class='ok' style='margin-bottom:12px;font-size:15px'>{final} clicks! +{e} coins</div>",unsafe_allow_html=True)
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
#  SLOT MACHINE — with roll animation, higher bet limit
# ═══════════════════════════════════════════════════════
SYM=["🍒","🍋","🍊","🍇","⭐","💎","🎰","🃏"]
SW=[20,18,15,12,10,7,4,14]
PAY={0:5,1:8,2:10,3:15,4:20,5:50,6:100,7:35}
SYM_NAMES=["Cherry","Lemon","Orange","Grapes","Star","Diamond","Jackpot","Joker"]

def page_slot():
    st.markdown("<h1 style='text-align:center;letter-spacing:3px'>🎰 SLOT MACHINE</h1>",unsafe_allow_html=True)
    lk=oc("slot_luck"); jp=oc("slot_jackpot"); rf=has("slot_refund")
    if lk or jp or rf:
        parts4=list(filter(None,[f"🍀 Luck +{lk}" if lk else "",f"💰 Jackpot x{2**jp}" if jp else "",f"↩ Refund" if rf else ""]))
        st.markdown(f"<div class='inf'>{'  |  '.join(parts4)}</div>",unsafe_allow_html=True)
    if "slr" not in st.session_state:
        st.session_state.update({"slr":[6,6,6],"slres":"","slbet":50,"sl_spinning":False,"sl_frame":0})

    reels=st.session_state["slr"]; res=S("slres",""); coins=S("coins",0)
    iw="Won" in res or "Jackpot" in res; ijp="Jackpot" in res
    spinning=S("sl_spinning",False)
    frame_n=S("sl_frame",0)

    r0,r1,r2=reels

    # Slot display with CSS animation when spinning
    spin_anim = "animation:reelSpin .08s steps(1) infinite;" if spinning else ""
    components.html(f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&display=swap');
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:transparent;display:flex;justify-content:center;align-items:center;padding:12px;font-family:'Orbitron',sans-serif}}
.machine{{background:linear-gradient(160deg,#1a0800,#240c00,#1a0800);
  border:2px solid {'rgba(255,214,10,.85)' if iw else 'rgba(255,124,0,.4)'};
  border-radius:20px;padding:22px 28px;max-width:440px;width:100%;
  box-shadow:{'0 0 50px rgba(255,214,10,.4)' if iw else '0 0 20px rgba(255,124,0,.1)'};
  {'animation:jackpotFlash .4s infinite;' if ijp else ''}
}}
@keyframes jackpotFlash{{0%,100%{{border-color:rgba(255,214,10,.9)}}50%{{border-color:rgba(255,214,10,.2)}}}}
.title{{text-align:center;font-size:14px;font-weight:900;color:#ff7c00;text-shadow:0 0 16px rgba(255,124,0,.8);letter-spacing:5px;margin-bottom:16px}}
.reels-wrap{{display:flex;gap:14px;justify-content:center;background:linear-gradient(145deg,rgba(0,0,0,.7),rgba(10,5,0,.6));border-radius:14px;padding:16px;border:1px solid rgba(255,124,0,.15)}}
.reel{{flex:1;max-width:100px;aspect-ratio:1;border-radius:12px;display:flex;align-items:center;justify-content:center;
  background:linear-gradient(145deg,#1a0800,#0f0500);
  border:2px solid {'rgba(255,214,10,.6)' if iw else 'rgba(255,124,0,.25)'};
  font-size:{'24px' if spinning else '50px'};overflow:hidden;
  {'animation:reelSpin .12s steps(1) infinite;' if spinning else ''}
  box-shadow:{'0 0 24px rgba(255,214,10,.3)' if iw else 'inset 0 4px 12px rgba(0,0,0,.4)'};
  {'animation:reelWin .5s cubic-bezier(.34,1.56,.64,1);' if iw and not spinning else ''}
}}
@keyframes reelSpin{{0%{{background:#1a1000}}25%{{background:#0f2000}}50%{{background:#200010}}75%{{background:#001020}}100%{{background:#1a1000}}}}
@keyframes reelWin{{0%{{transform:scale(.8)}}60%{{transform:scale(1.1)}}100%{{transform:scale(1)}}}}
.win-line{{height:3px;margin:12px 0;background:linear-gradient(90deg,transparent,{'#ffd60a' if iw else 'rgba(255,124,0,.2)'},transparent);{'box-shadow:0 0 12px #ffd60a;' if iw else ''}}}
</style></head><body>
<div class="machine">
  <div class="title">🎰 ARCADE SLOTS</div>
  <div class="reels-wrap">
    <div class="reel" style="animation-delay:0s">{'🎲' if spinning else SYM[r0]}</div>
    <div class="reel" style="animation-delay:.04s">{'🎲' if spinning else SYM[r1]}</div>
    <div class="reel" style="animation-delay:.08s">{'🎲' if spinning else SYM[r2]}</div>
  </div>
  <div class="win-line"></div>
</div>
</body></html>""", height=200, scrolling=False)

    st.markdown("<br>",unsafe_allow_html=True)
    if res and not spinning:
        cls="ok" if iw else "err"
        icon = "🎉" if ijp else ("✅" if iw else "😔")
        st.markdown(f"<div class='{cls}' style='font-size:15px;padding:12px'>{icon} {res}</div>",unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)

    c1,c2=st.columns([3,1])
    with c1:
        maxbet=max(50,min(5000,coins)) if coins>=50 else 50
        bet=st.slider("Bet 💰",50,maxbet,min(S("slbet",50),maxbet),50,key="slsl")
        st.session_state["slbet"]=bet
    with c2: st.metric("Balance",f"{coins:,}")

    _,c2b,_=st.columns([1,2,1])
    with c2b:
        st.markdown("""<style>div.spB .stButton>button{background:linear-gradient(135deg,rgba(255,124,0,.25),rgba(255,124,0,.08))!important;
border:2px solid rgba(255,124,0,.6)!important;color:#ff7c00!important;
font-size:18px!important;height:60px!important;font-weight:900!important;letter-spacing:3px!important;
font-family:'Orbitron',sans-serif!important;}</style>""",unsafe_allow_html=True)
        st.markdown('<div class="spB">',unsafe_allow_html=True)
        if spinning:
            if st.button("⏳ SPINNING...",use_container_width=True,key="slsp2",disabled=True): pass
            time.sleep(0.06); _spin(bet,lk,jp,rf); st.rerun()
        else:
            if st.button("🎰  SPIN!",use_container_width=True,key="slsp",disabled=coins<bet):
                st.session_state["sl_spinning"]=True; st.rerun()
        st.markdown('</div>',unsafe_allow_html=True)
    if coins<bet: st.markdown("<div class='err'>Not enough coins!</div>",unsafe_allow_html=True)

    st.markdown("---")
    with st.expander("📋 Paytable"):
        for idx,mult in PAY.items():
            am=mult*(2**jp if mult>=50 else 1)
            st.markdown(f"""<div style="display:flex;justify-content:space-between;align-items:center;padding:8px 14px;
background:linear-gradient(135deg,rgba(255,124,0,.05),transparent);border-radius:8px;margin-bottom:4px;border:1px solid rgba(255,124,0,.08)">
<span style="font-size:26px">{SYM[idx]*3}</span>
<span style="color:#aabbdd;font-size:13px;font-family:Share Tech Mono,monospace">{SYM_NAMES[idx]}</span>
<span style="color:#ff7c00;font-weight:900;font-family:'Orbitron',sans-serif;font-size:15px">×{am}</span></div>""",unsafe_allow_html=True)
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
    st.session_state["slr"]=r; st.session_state["sl_spinning"]=False
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

# ═══════════════════════════════════════════════════════
#  PONG 1P — speed increases per hit, no new game button
# ═══════════════════════════════════════════════════════
def page_pong():
    st.markdown("<h1 style='text-align:center;letter-spacing:3px'>🏓 PONG</h1>",unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#aabbdd;font-family:Share Tech Mono,monospace;font-size:14px'>W/S or ↑/↓ to move · First to 7 wins</p>",unsafe_allow_html=True)
    spb=2+oc("pong_speed"); hi=S("pong_hi",0)
    _,col,_=st.columns([1,10,1])
    with col:
        pong_html = """<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>*{margin:0;padding:0;box-sizing:border-box}
body{background:#04040f;display:flex;flex-direction:column;align-items:center;padding:10px;user-select:none;font-family:'Share Tech Mono',monospace}
canvas{border:2px solid rgba(0,245,255,.2);border-radius:12px;box-shadow:0 0 40px rgba(0,245,255,.08);display:block}
.ov{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
background:linear-gradient(145deg,rgba(4,4,20,.97),rgba(8,8,28,.97));
border:1px solid rgba(0,245,255,.5);border-radius:16px;padding:28px 36px;text-align:center;backdrop-filter:blur(20px)}
.ov h2{color:#00f5ff;font-family:'Orbitron',sans-serif;font-size:20px;margin-bottom:10px;text-shadow:0 0 16px rgba(0,245,255,.8)}
.ov p{color:#aabbdd;font-size:13px;margin-bottom:16px}
.ov button{background:linear-gradient(135deg,rgba(0,245,255,.2),rgba(0,245,255,.06));color:#00f5ff;border:1px solid rgba(0,245,255,.5);padding:10px 24px;border-radius:8px;cursor:pointer;font-family:'Orbitron',sans-serif;font-size:13px;font-weight:700;transition:all .18s}
.ov button:hover{background:rgba(0,245,255,.3)}
.wrap{position:relative}</style></head><body>
<div class="wrap"><canvas id="c" width="520" height="320"></canvas>
<div class="ov" id="ov"><h2>🏓 PONG</h2><p>W/S or ↑/↓ · First to 7</p><button onclick="start()">▶ PLAY</button></div></div>
<script>
var W=520,H=320,PW=10,PH=70,BR=7,BASE_SPD=SPB_PH;
var cv=document.getElementById('c'),ctx=cv.getContext('2d');
var p1y,p2y,bx,by,vx,vy,s1,s2,run,raf,keys={},trail=[],parts5=[],hitCount=0;
function start(){
  document.getElementById('ov').style.display='none';
  p1y=H/2-PH/2;p2y=H/2-PH/2;bx=W/2;by=H/2;hitCount=0;
  var a=(Math.random()*.5+.2)*Math.PI*(Math.random()<.5?1:-1);
  vx=Math.cos(a)*BASE_SPD;vy=Math.sin(a)*(BASE_SPD*.6);
  s1=s2=0;run=true;trail=[];parts5=[];
  if(raf)cancelAnimationFrame(raf);loop();
}
document.addEventListener('keydown',function(e){keys[e.code]=true;if(['KeyW','KeyS','ArrowUp','ArrowDown'].includes(e.code))e.preventDefault();});
document.addEventListener('keyup',function(e){keys[e.code]=false;});
function loop(){if(!run)return;update();draw();raf=requestAnimationFrame(loop);}
function update(){
  if(keys['KeyW']||keys['ArrowUp'])p1y=Math.max(0,p1y-5.5);
  if(keys['KeyS']||keys['ArrowDown'])p1y=Math.min(H-PH,p1y+5.5);
  var cy=p2y+PH/2;
  if(by<cy-4)p2y=Math.max(0,p2y-4.8);
  else if(by>cy+4)p2y=Math.min(H-PH,p2y+4.8);
  bx+=vx;by+=vy;
  if(by<=BR){by=BR;vy=Math.abs(vy);spark(bx,by,'#ffd60a');}
  if(by>=H-BR){by=H-BR;vy=-Math.abs(vy);spark(bx,by,'#ffd60a');}
  // Player paddle hit
  if(vx<0&&bx<=22+PW&&bx>=16&&by>=p1y&&by<=p1y+PH){
    hitCount++;var spd=BASE_SPD+hitCount*0.18;
    var relY=(by-(p1y+PH/2))/(PH/2);
    var angle=relY*0.85;
    vx=Math.abs(Math.cos(angle)*spd);
    vy=Math.sin(angle)*spd;
    bx=22+PW+1;spark(bx,by,'#00f5ff');
  }
  // AI paddle hit
  if(vx>0&&bx>=W-22-PW&&bx<=W-16&&by>=p2y&&by<=p2y+PH){
    hitCount++;var spd2=BASE_SPD+hitCount*0.18;
    var relY2=(by-(p2y+PH/2))/(PH/2);
    var angle2=relY2*0.85;
    vx=-Math.abs(Math.cos(angle2)*spd2);
    vy=Math.sin(angle2)*spd2;
    bx=W-22-PW-1;spark(bx,by,'#ff006e');
  }
  trail.unshift({x:bx,y:by,l:12});if(trail.length>14)trail.pop();
  trail.forEach(function(t){t.l--;});trail=trail.filter(function(t){return t.l>0;});
  parts5=parts5.filter(function(p){return p.l>0;});
  parts5.forEach(function(p){p.x+=p.vx;p.y+=p.vy;p.l--;p.vx*=.92;});
  if(bx<0){s2++;hitCount=0;if(s2>=7){endGame('AI Wins!');return;}reset();}
  if(bx>W){s1++;hitCount=0;if(s1>=7){endGame('You Win! 🎉');return;}reset();}
}
function spark(x,y,c){for(var i=0;i<10;i++)parts5.push({x:x,y:y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,l:20,c:c});}
function reset(){
  bx=W/2;by=H/2;hitCount=0;
  var a=(Math.random()*.5+.2)*Math.PI*(Math.random()<.5?1:-1);
  vx=Math.cos(a)*BASE_SPD;vy=Math.sin(a)*(BASE_SPD*.6);trail=[];
}
function endGame(msg){
  run=false;cancelAnimationFrame(raf);
  document.getElementById('ov').querySelector('h2').textContent=msg;
  document.getElementById('ov').querySelector('p').textContent='You: '+s1+' | AI: '+s2;
  document.getElementById('ov').style.display='block';
}
function draw(){
  ctx.fillStyle='#04040f';ctx.fillRect(0,0,W,H);
  ctx.setLineDash([10,10]);ctx.strokeStyle='rgba(0,245,255,.07)';ctx.lineWidth=1;
  ctx.beginPath();ctx.moveTo(W/2,0);ctx.lineTo(W/2,H);ctx.stroke();ctx.setLineDash([]);
  ctx.font='bold 32px Orbitron,monospace';ctx.textAlign='center';
  ctx.fillStyle='rgba(0,245,255,.9)';ctx.shadowBlur=14;ctx.shadowColor='rgba(0,245,255,.6)';ctx.fillText(s1,W/2-70,42);
  ctx.fillStyle='rgba(255,0,110,.9)';ctx.shadowColor='rgba(255,0,110,.6)';ctx.fillText(s2,W/2+70,42);ctx.shadowBlur=0;
  // Speed indicator
  ctx.font='10px monospace';ctx.fillStyle='rgba(255,214,10,.5)';ctx.textAlign='center';
  ctx.fillText('spd: '+(BASE_SPD+hitCount*0.18).toFixed(1),W/2,H-8);
  trail.forEach(function(t){
    ctx.globalAlpha=t.l/12*.5;ctx.fillStyle='#ffd60a';
    ctx.beginPath();ctx.arc(t.x,t.y,BR*(t.l/12),0,Math.PI*2);ctx.fill();
  });ctx.globalAlpha=1;
  parts5.forEach(function(p){
    ctx.globalAlpha=p.l/20;ctx.fillStyle=p.c;ctx.shadowBlur=5;ctx.shadowColor=p.c;
    ctx.beginPath();ctx.arc(p.x,p.y,2.5,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
  });ctx.globalAlpha=1;
  [{x:16,y:p1y,c:'#00f5ff'},{x:W-16-PW,y:p2y,c:'#ff006e'}].forEach(function(p){
    var g=ctx.createLinearGradient(p.x,0,p.x+PW,0);
    g.addColorStop(0,p.c+'88');g.addColorStop(.5,p.c);g.addColorStop(1,p.c+'88');
    ctx.fillStyle=g;ctx.shadowBlur=18;ctx.shadowColor=p.c;
    ctx.beginPath();ctx.roundRect(p.x,p.y,PW,PH,5);ctx.fill();ctx.shadowBlur=0;
  });
  var bg2=ctx.createRadialGradient(bx-2,by-2,1,bx,by,BR);
  bg2.addColorStop(0,'#fff');bg2.addColorStop(.5,'#ffd60a');bg2.addColorStop(1,'#ff8800');
  ctx.fillStyle=bg2;ctx.shadowBlur=20;ctx.shadowColor='rgba(255,214,10,.9)';
  ctx.beginPath();ctx.arc(bx,by,BR,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
}
ctx.fillStyle='#04040f';ctx.fillRect(0,0,W,H);
</script></body></html>"""
        pong_html = pong_html.replace("SPB_PH", str(spb))
        components.html(pong_html, height=370, scrolling=False)
    st.markdown("---")
    c1,c2=st.columns(2)
    with c1: st.metric("🏆 Best",S("pong_hi",0))
    with c2: st.metric("🎮 Games",S("pong_pl",0))

# ═══════════════════════════════════════════════════════
#  MINESWEEPER — animated Google-style
# ═══════════════════════════════════════════════════════
def page_minesweeper():
    st.markdown("<h1 style='text-align:center;letter-spacing:3px'>💣 MINESWEEPER</h1>",unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#aabbdd;font-family:Share Tech Mono,monospace;font-size:14px'>Click a cell to reveal · Right-click context: use Flag button</p>",unsafe_allow_html=True)

    if "ms_b" not in st.session_state:
        _ms_init()

    c1,c2,c3=st.columns(3)
    with c1: pass
    with c2: diff=st.selectbox("Difficulty",["Easy (6×6, 7 mines)","Normal (8×8, 10 mines)","Hard (10×10, 18 mines)"],key="ms_diff",label_visibility="visible")
    with c3: pass

    b=st.session_state["ms_b"]; rev=st.session_state["ms_rev"]; flags=st.session_state["ms_flag"]
    rows=S("ms_rows",8); cols_n=S("ms_cols",8); mines=S("ms_mines",10); over=S("ms_over"); win=S("ms_win")
    safe_total=rows*cols_n-mines; rev_safe=sum(1 for i in rev if b[i//cols_n][i%cols_n]!=-1)

    c1,c2,c3,c4=st.columns(4)
    with c1: st.metric("💣 Mines Left",mines-len(flags))
    with c2: st.metric("✅ Safe Found",f"{rev_safe}/{safe_total}")
    with c3: st.metric("🚩 Flags",len(flags))
    with c4:
        _,mc2,_=st.columns([1,3,1])
        with mc2:
            st.markdown('<div class="br">',unsafe_allow_html=True)
            if st.button("🔄 New",use_container_width=True,key="msnew"):
                d=S("ms_diff","Normal (8×8, 10 mines)")
                if "6×6" in d: _ms_init(6,6,7)
                elif "10×10" in d: _ms_init(10,10,18)
                else: _ms_init(8,8,10)
                st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)

    if over:
        if win: st.markdown("<div class='ok' style='font-size:16px;padding:14px;margin:10px 0'>🎉 Field cleared! 💰 +80 coins</div>",unsafe_allow_html=True)
        else: st.markdown("<div class='err' style='font-size:16px;padding:14px;margin:10px 0'>💥 BOOM! Hit a mine!</div>",unsafe_allow_html=True)

    COLORS={1:"#00f5ff",2:"#39ff14",3:"#ff006e",4:"#bf5fff",5:"#ff7c00",6:"#ffd60a",7:"#fff",8:"#aaa"}

    # Render the grid with animation styles
    st.markdown("""<style>
.ms-cell{transition:all .15s cubic-bezier(.34,1.56,.64,1);cursor:pointer;}
div.msReveal .stButton>button{
  height:44px!important;min-height:44px!important;font-size:13px!important;font-weight:700!important;
  background:linear-gradient(135deg,rgba(0,245,255,.08),rgba(0,245,255,.02))!important;
  border:1px solid rgba(0,245,255,.25)!important;border-radius:8px!important;
  color:#aabbdd!important;letter-spacing:0!important;padding:0!important;
  transition:all .12s!important;
}
div.msReveal .stButton>button:hover{background:rgba(0,245,255,.18)!important;border-color:rgba(0,245,255,.5)!important;transform:scale(1.06)!important;}
div.msFlag .stButton>button{
  height:44px!important;min-height:44px!important;font-size:13px!important;
  background:linear-gradient(135deg,rgba(255,214,10,.1),rgba(255,214,10,.03))!important;
  border:1px solid rgba(255,214,10,.35)!important;border-radius:8px!important;
  color:#ffd60a!important;transition:all .12s!important;
}
div.msFlag .stButton>button:hover{background:rgba(255,214,10,.2)!important;transform:scale(1.06)!important;}
div.msFlagRemove .stButton>button{
  height:44px!important;min-height:44px!important;font-size:13px!important;
  background:linear-gradient(135deg,rgba(255,0,110,.1),rgba(255,0,110,.03))!important;
  border:1px solid rgba(255,0,110,.35)!important;border-radius:8px!important;
  color:#ff006e!important;
}
</style>""",unsafe_allow_html=True)

    _,mc,_=st.columns([1,6,1])
    with mc:
        for r in range(rows):
            rc=st.columns(cols_n)
            for c in range(cols_n):
                idx=r*cols_n+c; cell=b[r][c]
                with rc[c]:
                    if idx in rev:
                        if cell==-1:
                            st.markdown("""<div style="height:44px;background:linear-gradient(135deg,rgba(255,0,110,.25),rgba(255,0,110,.08));
border:2px solid rgba(255,0,110,.6);border-radius:8px;display:flex;align-items:center;
justify-content:center;font-size:20px;animation:mineExplode .3s ease;margin-bottom:2px">💥</div>
<style>@keyframes mineExplode{0%{transform:scale(.5);opacity:.5}60%{transform:scale(1.2)}100%{transform:scale(1)}}</style>""",unsafe_allow_html=True)
                        elif cell==0:
                            st.markdown("""<div style="height:44px;background:rgba(57,255,20,.05);
border:1px solid rgba(57,255,20,.15);border-radius:8px;display:flex;align-items:center;
justify-content:center;font-size:12px;color:rgba(57,255,20,.3);animation:cellReveal .2s ease;margin-bottom:2px">·</div>
<style>@keyframes cellReveal{0%{transform:scale(.8);opacity:0}100%{transform:scale(1);opacity:1}}</style>""",unsafe_allow_html=True)
                        else:
                            col_c=COLORS.get(cell,"#fff")
                            st.markdown(f"""<div style="height:44px;background:rgba(255,255,255,.04);
border:1px solid rgba(255,255,255,.1);border-radius:8px;display:flex;align-items:center;
justify-content:center;font-size:15px;font-weight:900;color:{col_c};
font-family:'Orbitron',sans-serif;text-shadow:0 0 8px {col_c};animation:cellReveal .2s ease;margin-bottom:2px">{cell}</div>""",unsafe_allow_html=True)
                    elif idx in flags:
                        st.markdown("""<div style="height:44px;background:linear-gradient(135deg,rgba(255,214,10,.12),rgba(255,214,10,.04));
border:1px solid rgba(255,214,10,.5);border-radius:8px;display:flex;align-items:center;
justify-content:center;font-size:20px;margin-bottom:2px">🚩</div>""",unsafe_allow_html=True)
                        if not over:
                            st.markdown('<div class="msFlagRemove">',unsafe_allow_html=True)
                            if st.button("✕",key=f"msu_{idx}_{len(rev)}",use_container_width=True):
                                flags.discard(idx); st.session_state["ms_flag"]=flags; st.rerun()
                            st.markdown('</div>',unsafe_allow_html=True)
                    elif not over:
                        col1b,col2b=st.columns(2)
                        with col1b:
                            st.markdown('<div class="msReveal">',unsafe_allow_html=True)
                            if st.button("·",key=f"msr_{idx}_{len(rev)}",use_container_width=True):
                                _ms_rev(idx,b,rev,flags,rows,cols_n,mines)
                            st.markdown('</div>',unsafe_allow_html=True)
                        with col2b:
                            st.markdown('<div class="msFlag">',unsafe_allow_html=True)
                            if st.button("🚩",key=f"msf_{idx}_{len(rev)}",use_container_width=True):
                                flags.add(idx); st.session_state["ms_flag"]=flags; st.rerun()
                            st.markdown('</div>',unsafe_allow_html=True)
                    else:
                        st.markdown("""<div style="height:44px;background:rgba(255,255,255,.01);
border:1px solid rgba(255,255,255,.04);border-radius:8px;margin-bottom:2px"></div>""",unsafe_allow_html=True)

def _ms_init(rows=8,cols=8,mines=10):
    board=[[0]*cols for _ in range(rows)]
    mset=set(random.sample(range(rows*cols),mines))
    for p in mset: board[p//cols][p%cols]=-1
    for r in range(rows):
        for c in range(cols):
            if board[r][c]==-1: continue
            board[r][c]=sum(1 for dr in[-1,0,1] for dc in[-1,0,1] if 0<=r+dr<rows and 0<=c+dc<cols and board[r+dr][c+dc]==-1)
    st.session_state.update({"ms_b":board,"ms_rev":set(),"ms_flag":set(),"ms_rows":rows,"ms_cols":cols,"ms_mines":mines,"ms_over":False,"ms_win":False})

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
#  NUMBER GUESS — wider ranges, more coins
# ═══════════════════════════════════════════════════════
def page_guess():
    st.markdown("<h1 style='text-align:center;letter-spacing:3px'>🔢 NUMBER GUESS</h1>",unsafe_allow_html=True)
    if "gn" not in st.session_state:
        st.session_state.update({"gn":random.randint(1,1000),"gatt":0,"gover":False,"gfeed":"","g_lo":1,"g_hi":1000,"g_range":1000})

    ranges={"1–100":100,"1–500":500,"1–1000":1000,"1–10000":10000}
    sel=st.selectbox("Range",list(ranges.keys()),index=2,key="grange_sel")
    rng=ranges[sel]
    if rng != S("g_range",1000):
        st.session_state.update({"gn":random.randint(1,rng),"gatt":0,"gover":False,"gfeed":"","g_lo":1,"g_hi":rng,"g_range":rng})

    mx={"1–100":8,"1–500":10,"1–1000":12,"1–10000":15}[sel]
    gn=S("gn"); att=S("gatt",0); feed=S("gfeed",""); over=S("gover")

    c1,c2,c3=st.columns(3)
    with c1: st.metric("🎯 Attempts",f"{att}/{mx}")
    with c2: st.metric("📊 Range",f"{S('g_lo',1)}–{S('g_hi',rng)}")
    with c3: st.metric("💰 Prize",f"{max(50,(mx-att)*30)}")

    if over:
        won="Win" in feed
        st.markdown(f"<div class='{'ok' if won else 'err'}' style='font-size:17px;padding:14px'>{feed}</div>",unsafe_allow_html=True)
        _,mc,_=st.columns([1,2,1])
        with mc:
            st.markdown('<div class="bG">',unsafe_allow_html=True)
            if st.button("🔄 New Game",use_container_width=True,key="gnnew"):
                st.session_state.update({"gn":random.randint(1,rng),"gatt":0,"gover":False,"gfeed":"","g_lo":1,"g_hi":rng})
                st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)
        return

    if feed: st.markdown(f"<div class='inf' style='font-size:15px;padding:12px'>{feed}</div>",unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    c1,c2=st.columns([3,1])
    with c1: guess=st.number_input("Your guess:",1,rng,rng//2,key="gin",label_visibility="visible")
    with c2:
        st.markdown("<br>",unsafe_allow_html=True)
        st.markdown('<div class="bg">',unsafe_allow_html=True)
        if st.button("🎯 Guess",use_container_width=True,key="gok"):
            st.session_state["gatt"]=att+1
            if guess==gn:
                e=earn(max(50,(mx-att)*30)); give_xp(50)
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
                st.session_state["g_hi"]=min(S("g_hi",rng),guess-1)
            st.rerun()
        st.markdown('</div>',unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
#  PAINT RACE — new game replacing Target Shot
# ═══════════════════════════════════════════════════════
def page_paintrace():
    st.markdown("<h1 style='text-align:center;letter-spacing:3px'>🎨 PAINT RACE</h1>",unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#aabbdd;font-family:Share Tech Mono,monospace;font-size:14px'>Paint tiles by clicking them! Most painted in 20s wins</p>",unsafe_allow_html=True)

    GRID_W, GRID_H = 10, 8
    TOTAL = GRID_W * GRID_H

    if "pr_state" not in st.session_state:
        st.session_state.update({"pr_state":"idle","pr_grid":[0]*TOTAL,"pr_t":0,"pr_score":0,"pr_hi":0,"pr_color":0})

    state=S("pr_state"); grid=list(S("pr_grid",[])); hi=S("pr_hi",0)
    colors=["#ff006e","#00f5ff","#39ff14","#ffd60a","#bf5fff","#ff7c00"]
    color_names=["Pink","Cyan","Green","Gold","Purple","Orange"]

    if state=="idle":
        c1,c2=st.columns(2)
        with c1: st.metric("🏆 Best",hi)
        with c2: st.metric("🎨 Colors",len(colors))
        st.markdown("<br>",unsafe_allow_html=True)
        _,mc,_=st.columns([1,2,1])
        with mc:
            st.markdown('<div class="br">',unsafe_allow_html=True)
            if st.button("🎨 Start Painting!",use_container_width=True,key="pr_go"):
                st.session_state.update({"pr_state":"playing","pr_grid":[0]*TOTAL,"pr_t":time.time(),"pr_score":0,"pr_color":random.randint(1,len(colors))})
                st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)
        return

    if state=="playing":
        el=time.time()-S("pr_t",0); rem=max(0,20-el)
        if rem<=0:
            score=sum(1 for x in grid if x>0)
            st.session_state.update({"pr_state":"done","pr_score":score})
            st.rerun()

        cur_col=S("pr_color",1)
        c1,c2,c3=st.columns(3)
        with c1: st.metric("🎨 Painted",sum(1 for x in grid if x>0))
        with c2: st.metric("⬜ Empty",sum(1 for x in grid if x==0))
        with c3:
            danger=rem<5
            st.markdown(f"<div style='font-family:Orbitron,sans-serif;font-size:28px;color:{'#ff006e' if danger else '#ffd60a'};text-align:center;padding:6px;text-shadow:0 0 12px currentColor;font-weight:900'>{rem:.1f}s</div>",unsafe_allow_html=True)
        st.progress(rem/20)

        # Color picker
        st.markdown(f"<div style='color:#aabbdd;font-size:13px;margin:8px 0 4px;font-family:Rajdhani,sans-serif'>🎨 Current color: <b style='color:{colors[cur_col-1]}'>{color_names[cur_col-1]}</b></div>",unsafe_allow_html=True)
        ccols=st.columns(len(colors))
        for ci,cc in enumerate(colors):
            with ccols[ci]:
                border="3px solid white" if ci+1==cur_col else f"1px solid {cc}55"
                st.markdown(f"""<div style="height:28px;background:{cc};border-radius:6px;border:{border};cursor:pointer;margin-bottom:4px"></div>""",unsafe_allow_html=True)
                if st.button(f"●",key=f"prc_{ci}",use_container_width=True):
                    st.session_state["pr_color"]=ci+1; st.rerun()

        # Grid
        st.markdown("<br>",unsafe_allow_html=True)
        for r in range(GRID_H):
            gcols=st.columns(GRID_W)
            for c in range(GRID_W):
                idx=r*GRID_W+c
                with gcols[c]:
                    cv=grid[idx]
                    if cv>0:
                        bc=colors[cv-1]
                        st.markdown(f"""<div style="height:38px;background:{bc};border-radius:6px;
border:1px solid {bc}aa;box-shadow:0 0 8px {bc}66;margin-bottom:2px"></div>""",unsafe_allow_html=True)
                    else:
                        st.markdown("""<style>div.prCell .stButton>button{height:38px!important;min-height:38px!important;
background:rgba(255,255,255,.04)!important;border:1px solid rgba(255,255,255,.1)!important;
border-radius:6px!important;font-size:0!important;transition:all .1s!important;margin-bottom:2px!important;}
div.prCell .stButton>button:hover{background:rgba(255,255,255,.15)!important;transform:scale(1.08)!important;}</style>""",unsafe_allow_html=True)
                        st.markdown('<div class="prCell">',unsafe_allow_html=True)
                        if st.button("·",key=f"pr_{idx}_{sum(1 for x in grid if x>0)}",use_container_width=True):
                            grid[idx]=cur_col; st.session_state["pr_grid"]=grid; st.rerun()
                        st.markdown('</div>',unsafe_allow_html=True)
        time.sleep(0.08); st.rerun()

    if state=="done":
        score=S("pr_score",0); e=earn(score*5); give_xp(score*2)
        if score>hi: st.session_state["pr_hi"]=score; add_ach(f"🎨 Paint Record: {score}!")
        st.markdown(f"<div class='ok' style='font-size:17px;padding:16px'>🎉 Painted {score}/{TOTAL} tiles! +{e} coins</div>",unsafe_allow_html=True)

        # Show final grid
        for r in range(GRID_H):
            gcols=st.columns(GRID_W)
            for c2 in range(GRID_W):
                idx=r*GRID_W+c2
                with gcols[c2]:
                    cv=grid[idx]
                    bc=colors[cv-1] if cv>0 else "#111"
                    st.markdown(f"""<div style="height:30px;background:{bc};border-radius:4px;margin-bottom:2px"></div>""",unsafe_allow_html=True)

        st.markdown("<br>",unsafe_allow_html=True)
        _,mc,_=st.columns([1,2,1])
        with mc:
            st.markdown('<div class="bG">',unsafe_allow_html=True)
            if st.button("🔄 Play Again",use_container_width=True,key="pr_again"):
                st.session_state.update({"pr_state":"idle","pr_grid":[0]*TOTAL}); st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
#  WORD GUESS — real Wordle keyboard input, fixed coloring
# ═══════════════════════════════════════════════════════
WORDS=["PYTHON","LASER","PIXEL","BLAST","CYBER","QUEST","STORM","SWORD",
       "FLAME","GHOST","QUEEN","BRAVE","CRISP","SHINY","PRIME","LUNAR",
       "BLOCK","CLOCK","DREAM","FROST","GRAPE","HONEY","IVORY","JOLLY",
       "KNIFE","LEMON","MAGIC","NINJA","OCEAN","PEACE","QUICK","RAZOR",
       "TIGER","ULTRA","VIVID","WATER","XENON","YACHT","ZEBRA","SHINE"]

def _wordle_colors(guess, word):
    """Correct Wordle coloring — handles duplicate letters properly."""
    result = ['gray'] * len(guess)
    word_remaining = list(word)
    # First pass: mark greens
    for i, ch in enumerate(guess):
        if i < len(word) and ch == word[i]:
            result[i] = 'green'
            word_remaining[i] = None
    # Second pass: mark yellows
    for i, ch in enumerate(guess):
        if result[i] == 'green':
            continue
        if ch in word_remaining:
            result[i] = 'yellow'
            word_remaining[word_remaining.index(ch)] = None
    return result

def page_wordgame():
    st.markdown("<h1 style='text-align:center;letter-spacing:3px'>🔤 WORD GUESS</h1>",unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#aabbdd;font-family:Share Tech Mono,monospace;font-size:14px'>Type your 5-letter guess · Enter to submit · Backspace to delete</p>",unsafe_allow_html=True)

    if "ww" not in st.session_state:
        w=random.choice([x for x in WORDS if len(x)==5])
        st.session_state.update({"ww":w,"wg":[],"wo":False,"wm":"","wcur":""})
    word=S("ww",""); guesses=list(S("wg",[])); over=S("wo"); msg=S("wm",""); cur=S("wcur","")

    c1,c2=st.columns(2)
    with c1: st.metric("📝 Word Length",len(word))
    with c2: st.metric("🎯 Tries",f"{len(guesses)}/6")

    # Color map for keyboard
    letter_colors={}
    for g in guesses:
        cols_w=_wordle_colors(g, word)
        for i,ch in enumerate(g):
            prev=letter_colors.get(ch,'unused')
            nc=cols_w[i]
            if nc=='green': letter_colors[ch]='green'
            elif nc=='yellow' and prev!='green': letter_colors[ch]='yellow'
            elif prev not in ('green','yellow'): letter_colors[ch]='gray'

    # Board
    _,mc,_=st.columns([1,3,1])
    with mc:
        for gi in range(6):
            row_html=""
            if gi < len(guesses):
                g=guesses[gi]; cols_w=_wordle_colors(g, word)
                for i,ch in enumerate(g):
                    nc=cols_w[i]
                    if nc=='green':
                        bg="linear-gradient(135deg,rgba(57,255,20,.2),rgba(57,255,20,.08))"; bd="rgba(57,255,20,.7)"; col2="#39ff14"
                    elif nc=='yellow':
                        bg="linear-gradient(135deg,rgba(255,214,10,.2),rgba(255,214,10,.08))"; bd="rgba(255,214,10,.6)"; col2="#ffd60a"
                    else:
                        bg="rgba(255,255,255,.04)"; bd="rgba(255,255,255,.12)"; col2="#667799"
                    row_html+=f"""<div style="width:52px;height:54px;background:{bg};border:2px solid {bd};
border-radius:9px;display:flex;align-items:center;justify-content:center;
font-size:22px;font-weight:900;color:{col2};font-family:'Orbitron',sans-serif;
animation:flipIn .4s ease {i*0.1:.1f}s both">{ch}</div>"""
            elif gi == len(guesses) and not over:
                # Current input row
                for i in range(5):
                    ch = cur[i] if i < len(cur) else ""
                    active = i == len(cur) and len(cur) < 5
                    bd = "rgba(0,245,255,.7)" if active else ("rgba(0,245,255,.4)" if ch else "rgba(255,255,255,.12)")
                    row_html+=f"""<div style="width:52px;height:54px;background:rgba(0,245,255,.05);border:2px solid {bd};
border-radius:9px;display:flex;align-items:center;justify-content:center;
font-size:22px;font-weight:900;color:#e8ecff;font-family:'Orbitron',sans-serif;
{'animation:cursorBlink .8s ease-in-out infinite;' if active else ''}
transition:border-color .1s">{ch}</div>"""
            else:
                for i in range(5):
                    row_html+="""<div style="width:52px;height:54px;background:rgba(255,255,255,.02);
border:1px solid rgba(255,255,255,.06);border-radius:9px"></div>"""
            st.markdown(f"""<div style='display:flex;gap:7px;justify-content:center;margin-bottom:7px'>{row_html}</div>""",unsafe_allow_html=True)

    st.markdown("""<style>
@keyframes flipIn{0%{transform:scaleY(0);opacity:0}50%{transform:scaleY(1.1)}100%{transform:scaleY(1);opacity:1}}
@keyframes cursorBlink{0%,100%{border-color:rgba(0,245,255,.7)}50%{border-color:rgba(0,245,255,.2)}}
</style>""",unsafe_allow_html=True)

    # On-screen keyboard
    rows_kb=[["Q","W","E","R","T","Y","U","I","O","P"],
             ["A","S","D","F","G","H","J","K","L"],
             ["ENTER","Z","X","C","V","B","N","M","⌫"]]
    st.markdown("<br>",unsafe_allow_html=True)
    color_map={'green':'rgba(57,255,20,.4)','yellow':'rgba(255,214,10,.35)','gray':'rgba(100,100,120,.4)','unused':'rgba(0,245,255,.1)'}
    border_map={'green':'rgba(57,255,20,.8)','yellow':'rgba(255,214,10,.7)','gray':'rgba(100,100,120,.4)','unused':'rgba(0,245,255,.3)'}
    text_map={'green':'#39ff14','yellow':'#ffd60a','gray':'#667799','unused':'#aabbdd'}

    if not over:
        for kb_row in rows_kb:
            kb_cols=st.columns(len(kb_row))
            for ki,key in enumerate(kb_row):
                with kb_cols[ki]:
                    lc=letter_colors.get(key,'unused')
                    bg=color_map[lc]; bd=border_map[lc]; tc=text_map[lc]
                    is_wide=key in ("ENTER","⌫")
                    st.markdown(f"""<style>
div.kb_{ki}_{ord(key[0])} .stButton>button{{
height:44px!important;background:{bg}!important;border:1px solid {bd}!important;
border-radius:7px!important;color:{tc}!important;font-weight:700!important;
font-family:'Orbitron',sans-serif!important;font-size:{'10px' if is_wide else '13px'}!important;
padding:0!important;letter-spacing:0!important;transition:all .1s!important;}}
div.kb_{ki}_{ord(key[0])} .stButton>button:hover{{background:{bg.replace('rgba','rgba').replace(', 0.',', 0.6')}!important;transform:scale(1.05)!important;}}
</style>""",unsafe_allow_html=True)
                    st.markdown(f'<div class="kb_{ki}_{ord(key[0])}">',unsafe_allow_html=True)
                    if st.button(key,key=f"kb_{key}_{len(guesses)}_{len(cur)}",use_container_width=True):
                        if key=="⌫":
                            if cur: st.session_state["wcur"]=cur[:-1]; st.rerun()
                        elif key=="ENTER":
                            if len(cur)==5:
                                guesses.append(cur); st.session_state["wg"]=guesses; st.session_state["wcur"]=""
                                if cur==word:
                                    e=earn(max(20,(6-len(guesses)+1)*40)); give_xp(50)
                                    st.session_state["wm"]=f"🎉 Win! +{e} coins"; st.session_state["wo"]=True; add_ach("🔤 Word Master!")
                                elif len(guesses)>=6:
                                    st.session_state["wm"]=f"😔 The word was: {word}"; st.session_state["wo"]=True
                                st.rerun()
                            else:
                                st.session_state["wm"]=f"⚠️ Need 5 letters!"
                                st.rerun()
                        elif len(cur)<5:
                            st.session_state["wcur"]=cur+key; st.rerun()
                    st.markdown('</div>',unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)
    if msg:
        cls="ok" if "Win" in msg else ("err" if "word was" in msg else "warn")
        st.markdown(f"<div class='{cls}' style='padding:11px;font-size:15px'>{msg}</div>",unsafe_allow_html=True)

    if over:
        st.markdown("<br>",unsafe_allow_html=True)
        _,mc2,_=st.columns([1,2,1])
        with mc2:
            st.markdown('<div class="bG">',unsafe_allow_html=True)
            if st.button("🔄 New Word",use_container_width=True,key="wwnew"):
                w=random.choice([x for x in WORDS if len(x)==5])
                st.session_state.update({"ww":w,"wg":[],"wo":False,"wm":"","wcur":""}); st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
#  PONG 2P — fixed angles, variable speed
# ═══════════════════════════════════════════════════════
def page_pong2p():
    st.markdown("<h1 style='text-align:center;letter-spacing:3px'>🏓 PONG — 2 PLAYERS</h1>",unsafe_allow_html=True)
    st.markdown("<div class='inf' style='font-size:15px'>Player 1: W/S  ·  Player 2: ↑/↓  ·  First to 7 wins!</div>",unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    _,col,_=st.columns([1,10,1])
    with col:
        components.html("""<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>*{margin:0;padding:0;box-sizing:border-box}body{background:#04040f;display:flex;flex-direction:column;align-items:center;padding:10px;user-select:none;font-family:'Share Tech Mono',monospace}
canvas{border:2px solid rgba(0,245,255,.2);border-radius:12px;box-shadow:0 0 40px rgba(0,245,255,.08);display:block}
.ov{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);background:linear-gradient(145deg,rgba(4,4,20,.97),rgba(8,8,28,.97));border:1px solid rgba(0,245,255,.5);border-radius:16px;padding:28px 36px;text-align:center;backdrop-filter:blur(20px)}
.ov h2{color:#00f5ff;font-family:'Orbitron',sans-serif;font-size:20px;margin-bottom:10px;text-shadow:0 0 16px rgba(0,245,255,.8)}
.ov p{color:#aabbdd;font-size:13px;margin-bottom:16px}
.ov button{background:linear-gradient(135deg,rgba(0,245,255,.2),rgba(0,245,255,.06));color:#00f5ff;border:1px solid rgba(0,245,255,.5);padding:10px 24px;border-radius:8px;cursor:pointer;font-family:'Orbitron',sans-serif;font-size:13px;font-weight:700}
.wrap{position:relative}</style></head><body>
<div class="wrap"><canvas id="c" width="560" height="340"></canvas>
<div class="ov" id="ov"><h2>🏓 2-PLAYER PONG</h2><p>P1: W/S | P2: ↑/↓<br>First to 7 wins!</p><button onclick="start()">▶ PLAY</button></div></div>
<script>
var W=560,H=340,PW=11,PH=70,BR=7,BASE=4.0;
var cv=document.getElementById('c'),ctx=cv.getContext('2d');
var p1y,p2y,bx,by,vx,vy,s1,s2,run,raf,keys={},trail=[],parts6=[],hits=0;
function start(){
  document.getElementById('ov').style.display='none';
  p1y=H/2-PH/2;p2y=H/2-PH/2;bx=W/2;by=H/2;hits=0;
  var a=(Math.random()*.5+.25)*Math.PI*(Math.random()<.5?1:-1);
  vx=Math.cos(a)*BASE;vy=Math.sin(a)*(BASE*.65);
  s1=s2=0;run=true;trail=[];parts6=[];
  if(raf)cancelAnimationFrame(raf);loop();
}
document.addEventListener('keydown',function(e){keys[e.code]=true;if(['KeyW','KeyS','ArrowUp','ArrowDown'].includes(e.code))e.preventDefault();});
document.addEventListener('keyup',function(e){keys[e.code]=false;});
function loop(){if(!run)return;update();draw();raf=requestAnimationFrame(loop);}
function update(){
  if(keys['KeyW'])p1y=Math.max(0,p1y-5.5);
  if(keys['KeyS'])p1y=Math.min(H-PH,p1y+5.5);
  if(keys['ArrowUp'])p2y=Math.max(0,p2y-5.5);
  if(keys['ArrowDown'])p2y=Math.min(H-PH,p2y+5.5);
  bx+=vx;by+=vy;
  if(by<=BR){by=BR;vy=Math.abs(vy);spark(bx,by,'#ffd60a');}
  if(by>=H-BR){by=H-BR;vy=-Math.abs(vy);spark(bx,by,'#ffd60a');}
  if(vx<0&&bx<=17+PW&&bx>=11&&by>=p1y&&by<=p1y+PH){
    hits++;var spd=BASE+hits*0.15;
    var rel=(by-(p1y+PH/2))/(PH/2);
    var ang=rel*0.8;
    vx=Math.abs(Math.cos(ang)*spd);vy=Math.sin(ang)*spd;
    bx=17+PW+1;spark(bx,by,'#00f5ff');
  }
  if(vx>0&&bx>=W-17-PW&&bx<=W-11&&by>=p2y&&by<=p2y+PH){
    hits++;var spd2=BASE+hits*0.15;
    var rel2=(by-(p2y+PH/2))/(PH/2);
    var ang2=rel2*0.8;
    vx=-Math.abs(Math.cos(ang2)*spd2);vy=Math.sin(ang2)*spd2;
    bx=W-17-PW-1;spark(bx,by,'#ff006e');
  }
  trail.unshift({x:bx,y:by,l:12});if(trail.length>14)trail.pop();
  trail.forEach(function(t){t.l--;});trail=trail.filter(function(t){return t.l>0;});
  parts6=parts6.filter(function(p){return p.l>0;});
  parts6.forEach(function(p){p.x+=p.vx;p.y+=p.vy;p.l--;p.vx*=.92;});
  if(bx<0){s2++;hits=0;if(s2>=7){end('Player 2 Wins! 🎉');return;}reset();}
  if(bx>W){s1++;hits=0;if(s1>=7){end('Player 1 Wins! 🎉');return;}reset();}
}
function spark(x,y,c){for(var i=0;i<8;i++)parts6.push({x:x,y:y,vx:(Math.random()-.5)*6,vy:(Math.random()-.5)*6,l:18,c:c});}
function reset(){bx=W/2;by=H/2;hits=0;var a=(Math.random()*.5+.25)*Math.PI*(Math.random()<.5?1:-1);vx=Math.cos(a)*BASE;vy=Math.sin(a)*(BASE*.65);trail=[];}
function end(msg){run=false;cancelAnimationFrame(raf);document.getElementById('ov').querySelector('h2').textContent=msg;document.getElementById('ov').querySelector('p').textContent='P1: '+s1+' | P2: '+s2;document.getElementById('ov').style.display='block';}
function draw(){
  ctx.fillStyle='#04040f';ctx.fillRect(0,0,W,H);
  ctx.setLineDash([8,8]);ctx.strokeStyle='rgba(255,255,255,.05)';ctx.lineWidth=1;
  ctx.beginPath();ctx.moveTo(W/2,0);ctx.lineTo(W/2,H);ctx.stroke();ctx.setLineDash([]);
  ctx.font='bold 32px Orbitron,monospace';ctx.textAlign='center';
  ctx.fillStyle='rgba(0,245,255,.95)';ctx.shadowBlur=14;ctx.shadowColor='rgba(0,245,255,.6)';ctx.fillText(s1,W/2-80,42);
  ctx.fillStyle='rgba(255,0,110,.95)';ctx.shadowColor='rgba(255,0,110,.6)';ctx.fillText(s2,W/2+80,42);ctx.shadowBlur=0;
  ctx.font='10px monospace';ctx.fillStyle='rgba(255,214,10,.5)';ctx.textAlign='center';
  ctx.fillText('speed: '+(BASE+hits*0.15).toFixed(1),W/2,H-8);
  trail.forEach(function(t){ctx.globalAlpha=t.l/12*.45;ctx.fillStyle='#ffd60a';ctx.beginPath();ctx.arc(t.x,t.y,BR*t.l/12,0,Math.PI*2);ctx.fill();});ctx.globalAlpha=1;
  parts6.forEach(function(p){ctx.globalAlpha=p.l/18;ctx.fillStyle=p.c;ctx.shadowBlur=4;ctx.shadowColor=p.c;ctx.beginPath();ctx.arc(p.x,p.y,2.5,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;});ctx.globalAlpha=1;
  [{x:15,y:p1y,c:'#00f5ff'},{x:W-15-PW,y:p2y,c:'#ff006e'}].forEach(function(p){
    var g=ctx.createLinearGradient(p.x,0,p.x+PW,0);g.addColorStop(0,p.c+'88');g.addColorStop(.5,p.c);g.addColorStop(1,p.c+'88');
    ctx.fillStyle=g;ctx.shadowBlur=16;ctx.shadowColor=p.c;ctx.beginPath();ctx.roundRect(p.x,p.y,PW,PH,5);ctx.fill();ctx.shadowBlur=0;
  });
  var bg3=ctx.createRadialGradient(bx-2,by-2,1,bx,by,BR);bg3.addColorStop(0,'#fff');bg3.addColorStop(.5,'#ffd60a');bg3.addColorStop(1,'#ff8800');
  ctx.fillStyle=bg3;ctx.shadowBlur=20;ctx.shadowColor='rgba(255,214,10,.9)';ctx.beginPath();ctx.arc(bx,by,BR,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
}
ctx.fillStyle='#04040f';ctx.fillRect(0,0,W,H);
</script></body></html>""", height=390, scrolling=False)

# ═══════════════════════════════════════════════════════
#  TIC-TAC-TOE 2P — consistent cell sizes
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
        col2="#00f5ff" if turn=="X" else "#ff006e"
        st.markdown(f"<div style='text-align:center;font-family:Orbitron,sans-serif;font-size:18px;font-weight:700;color:{col2};padding:10px;text-shadow:0 0 12px {col2}'>{'❌ Player 1' if turn=='X' else '⭕ Player 2'}</div>",unsafe_allow_html=True)
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
                        st.markdown(_ttt_cell_x(), unsafe_allow_html=True)
                    elif cell=="O":
                        st.markdown(_ttt_cell_o(), unsafe_allow_html=True)
                    elif not over:
                        st.markdown(CELL_STYLE, unsafe_allow_html=True)
                        st.markdown('<div class="tttCell">', unsafe_allow_html=True)
                        if st.button(" ",key=f"tt2_{idx}_{sum(1 for x in b if x)}",use_container_width=True):
                            b[idx]=turn; w=_tw(b)
                            if w:
                                wins[w]=wins.get(w,0)+1; st.session_state["tw2"]=wins
                                st.session_state.update({"ts2":f"{'❌ Player 1' if w=='X' else '⭕ Player 2'} Wins! 🎉","to2":True,"tb2":b})
                                earn(30); give_xp(15)
                            elif ""not in b: st.session_state.update({"ts2":"🤝 Draw!","to2":True,"tb2":b})
                            else: st.session_state.update({"turn2":"O" if turn=="X" else "X","tb2":b})
                            st.rerun()
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(_ttt_cell_empty_over(), unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    _,c2b,_=st.columns([1,2,1])
    with c2b:
        st.markdown('<div class="bG">',unsafe_allow_html=True)
        if st.button("🔄 New Round",use_container_width=True,key="tt2n"):
            st.session_state.update({"tb2":[""]*9,"turn2":"X","to2":False,"ts2":""}); st.rerun()
        st.markdown('</div>',unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
#  DICE RACE 2P
# ═══════════════════════════════════════════════════════
def page_dice2p():
    st.markdown("<h1 style='text-align:center;letter-spacing:3px'>🎲 DICE RACE — 2P</h1>",unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#aabbdd;font-family:Share Tech Mono,monospace;font-size:14px'>First to 100 wins! Roll or Hold each turn.</p>",unsafe_allow_html=True)
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
        st.markdown(f"<div style='text-align:center;font-size:80px;filter:drop-shadow(0 0 16px {cc[turn]}80);animation:diceRoll .2s ease-out'>{FACES[g['dice']]}</div><style>@keyframes diceRoll{{from{{transform:rotate(-15deg) scale(.8)}}to{{transform:rotate(0) scale(1)}}}}</style>",unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    c1,c2,_=st.columns([1,1,1])
    with c1:
        if st.button("🎲 Roll",use_container_width=True,key="dc2r"):
            d=random.randint(1,6); g["dice"]=d
            if d==1: g["cur"]=0; g["turn"]=1-turn
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
        st.markdown(f"<div style='font-size:13px;color:{cc[i]};margin:8px 0 3px;font-family:Share Tech Mono,monospace;font-weight:700'>Player {i+1}: {sc[i]}/100</div>",unsafe_allow_html=True)
        st.progress(min(sc[i]/100,1.0))

# ═══════════════════════════════════════════════════════
#  SUMO PUSH 2P — new creative 2P game
# ═══════════════════════════════════════════════════════
def page_sumo2p():
    st.markdown("<h1 style='text-align:center;letter-spacing:3px'>🥊 SUMO PUSH — 2P</h1>",unsafe_allow_html=True)
    st.markdown("<div class='inf' style='font-size:15px'>P1: A/D to move · P2: ←/→ to move · Push your opponent off the platform! First to 5 wins!</div>",unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    _,col,_=st.columns([1,10,1])
    with col:
        components.html("""<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>*{margin:0;padding:0;box-sizing:border-box}body{background:#04040f;display:flex;flex-direction:column;align-items:center;padding:10px;user-select:none;font-family:'Orbitron',sans-serif}
canvas{border:2px solid rgba(255,0,110,.2);border-radius:12px;box-shadow:0 0 40px rgba(255,0,110,.08);display:block}
.ov{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);background:linear-gradient(145deg,rgba(4,4,20,.97),rgba(8,8,28,.97));border:1px solid rgba(255,0,110,.5);border-radius:16px;padding:28px 36px;text-align:center;backdrop-filter:blur(20px)}
.ov h2{color:#ff006e;font-family:'Orbitron',sans-serif;font-size:20px;margin-bottom:10px;text-shadow:0 0 16px rgba(255,0,110,.8)}
.ov p{color:#aabbdd;font-size:13px;margin-bottom:16px}
.ov button{background:linear-gradient(135deg,rgba(255,0,110,.2),rgba(255,0,110,.06));color:#ff006e;border:1px solid rgba(255,0,110,.5);padding:10px 24px;border-radius:8px;cursor:pointer;font-family:'Orbitron',sans-serif;font-size:13px;font-weight:700}
.wrap{position:relative}</style></head><body>
<div class="wrap"><canvas id="c" width="560" height="340"></canvas>
<div class="ov" id="ov"><h2>🥊 SUMO PUSH</h2><p>P1: A/D &nbsp;|&nbsp; P2: ←/→<br>Push opponent off the edge!<br>First to 5 wins!</p><button onclick="start()">▶ PLAY</button></div></div>
<script>
var W=560,H=340;
var cv=document.getElementById('c'),ctx=cv.getContext('2d');
var p1,p2,s1,s2,run,raf,keys={},parts7=[],frame=0;
var PLAT={x:80,w:400,y:260,h:18};
var PR=24; // player radius
function makeP(x,color,dir){return{x:x,y:PLAT.y-PR,vx:0,color:color,dir:dir,grounded:true,w:0};}
function start(){
  document.getElementById('ov').style.display='none';
  p1=makeP(PLAT.x+80,  '#00f5ff', 1);
  p2=makeP(PLAT.x+PLAT.w-80,'#ff006e',-1);
  if(!s1)s1=0;if(!s2)s2=0;
  run=true;parts7=[];frame=0;
  if(raf)cancelAnimationFrame(raf);loop();
}
document.addEventListener('keydown',function(e){keys[e.code]=true;['KeyA','KeyD','ArrowLeft','ArrowRight'].forEach(function(k){if(e.code===k)e.preventDefault();});});
document.addEventListener('keyup',function(e){keys[e.code]=false;});
function loop(){if(!run)return;update();draw();raf=requestAnimationFrame(loop);}
function update(){
  frame++;
  // P1 controls
  var p1acc=0,p2acc=0;
  if(keys['KeyA'])p1acc=-0.55;
  if(keys['KeyD'])p1acc=0.55;
  if(keys['ArrowLeft'])p2acc=-0.55;
  if(keys['ArrowRight'])p2acc=0.55;
  p1.vx+=p1acc;p2.vx+=p2acc;
  // Friction
  p1.vx*=0.78;p2.vx*=0.78;
  // Clamp speed
  p1.vx=Math.max(-7,Math.min(7,p1.vx));
  p2.vx=Math.max(-7,Math.min(7,p2.vx));
  p1.x+=p1.vx;p2.x+=p2.vx;
  // Collision between players
  var dx=p2.x-p1.x;
  var dist=Math.abs(dx);
  if(dist<PR*2+4){
    var overlap=PR*2+4-dist;
    var push=overlap*0.25+Math.abs(p1.vx-p2.vx)*0.3;
    if(dx>0){p1.vx-=push;p2.vx+=push*0.5;}
    else{p1.vx+=push;p2.vx-=push*0.5;}
    // Impact particles
    if(Math.abs(p1.vx)>2)spark((p1.x+p2.x)/2,p1.y,'#ffd60a');
  }
  // Check fall off
  var platL=PLAT.x,platR=PLAT.x+PLAT.w;
  if(p1.x<platL-PR||p1.x>platR+PR){
    spark(p1.x,p1.y,'#00f5ff');
    s2++;checkEnd();return;
  }
  if(p2.x<platL-PR||p2.x>platR+PR){
    spark(p2.x,p2.y,'#ff006e');
    s1++;checkEnd();return;
  }
  // Keep on platform vertically
  p1.y=PLAT.y-PR;p2.y=PLAT.y-PR;
  parts7=parts7.filter(function(p){return p.l>0;});
  parts7.forEach(function(p){p.x+=p.vx;p.y+=p.vy;p.vy+=0.15;p.l--;p.vx*=0.9;});
}
function spark(x,y,c){for(var i=0;i<14;i++)parts7.push({x:x,y:y,vx:(Math.random()-.5)*8,vy:-Math.random()*6-2,l:35,c:c,r:Math.random()*4+2});}
function checkEnd(){
  run=false;cancelAnimationFrame(raf);
  var winner=s1>=5?'Player 1 Wins! 🎉':'Player 2 Wins! 🎉';
  if(s1<5&&s2<5){
    // Just reset round
    setTimeout(function(){
      p1=makeP(PLAT.x+80,'#00f5ff',1);
      p2=makeP(PLAT.x+PLAT.w-80,'#ff006e',-1);
      run=true;raf=requestAnimationFrame(loop);
    },600);
    return;
  }
  document.getElementById('ov').querySelector('h2').textContent=winner;
  document.getElementById('ov').querySelector('p').textContent='P1: '+s1+' | P2: '+s2;
  document.getElementById('ov').style.display='block';
  s1=0;s2=0;
}
function draw(){
  ctx.fillStyle='#04040f';ctx.fillRect(0,0,W,H);
  // Stars bg
  ctx.fillStyle='rgba(255,255,255,.3)';
  for(var i=0;i<40;i++){
    var sx=(i*137+frame*.2)%W,sy=(i*97+frame*.1)%H*.6;
    ctx.beginPath();ctx.arc(sx,sy,.8,0,Math.PI*2);ctx.fill();
  }
  // Platform
  var pg=ctx.createLinearGradient(PLAT.x,PLAT.y,PLAT.x,PLAT.y+PLAT.h);
  pg.addColorStop(0,'#334466');pg.addColorStop(1,'#1a2233');
  ctx.fillStyle=pg;ctx.beginPath();ctx.roundRect(PLAT.x,PLAT.y,PLAT.w,PLAT.h,6);ctx.fill();
  ctx.strokeStyle='rgba(0,245,255,.3)';ctx.lineWidth=1.5;ctx.stroke();
  // Edge danger zones
  ctx.fillStyle='rgba(255,0,110,.15)';ctx.fillRect(PLAT.x,PLAT.y,30,PLAT.h);
  ctx.fillRect(PLAT.x+PLAT.w-30,PLAT.y,30,PLAT.h);
  // Scores
  ctx.font='bold 28px Orbitron,monospace';ctx.textAlign='center';
  ctx.fillStyle='rgba(0,245,255,.9)';ctx.shadowBlur=12;ctx.shadowColor='rgba(0,245,255,.6)';ctx.fillText(s1,120,50);
  ctx.fillStyle='rgba(255,0,110,.9)';ctx.shadowColor='rgba(255,0,110,.6)';ctx.fillText(s2,W-120,50);ctx.shadowBlur=0;
  ctx.font='11px monospace';ctx.fillStyle='rgba(255,255,255,.4)';ctx.fillText('FIRST TO 5',W/2,50);
  // Particles
  parts7.forEach(function(p){
    ctx.globalAlpha=p.l/35;ctx.fillStyle=p.c;ctx.shadowBlur=6;ctx.shadowColor=p.c;
    ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
  });ctx.globalAlpha=1;
  // Players
  [p1,p2].forEach(function(p){
    if(!p)return;
    // Shadow
    ctx.fillStyle='rgba(0,0,0,.4)';ctx.beginPath();ctx.ellipse(p.x,PLAT.y+2,PR*.8,6,0,0,Math.PI*2);ctx.fill();
    // Body glow
    ctx.shadowBlur=18;ctx.shadowColor=p.color;
    // Body gradient
    var rg=ctx.createRadialGradient(p.x-PR*.3,p.y-PR*.3,2,p.x,p.y,PR);
    rg.addColorStop(0,'#fff');rg.addColorStop(.4,p.color);rg.addColorStop(1,p.color+'88');
    ctx.fillStyle=rg;ctx.beginPath();ctx.arc(p.x,p.y,PR,0,Math.PI*2);ctx.fill();
    ctx.shadowBlur=0;
    // Eyes
    var ex=p.vx>0?6:-6;
    ctx.fillStyle='#04040f';ctx.beginPath();ctx.arc(p.x+ex,p.y-6,4,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='#fff';ctx.beginPath();ctx.arc(p.x+ex+1,p.y-7,1.5,0,Math.PI*2);ctx.fill();
    // Speed indicator
    if(Math.abs(p.vx)>1){
      ctx.fillStyle=p.color;ctx.font='bold 10px monospace';ctx.textAlign='center';
      ctx.fillText(p.vx>0?'>>>':'<<<',p.x,p.y+PR+14);
    }
    // Charge indicator
    var spd=Math.abs(p.vx)/7;
    if(spd>0.1){
      ctx.beginPath();ctx.arc(p.x,p.y,PR+5,0,Math.PI*2*spd);
      ctx.strokeStyle=p.color+'aa';ctx.lineWidth=2;ctx.stroke();
    }
  });
}
ctx.fillStyle='#04040f';ctx.fillRect(0,0,W,H);
var s1=0,s2=0;
</script></body></html>""", height=400, scrolling=False)

# ═══════════════════════════════════════════════════════
#  SHOP — bigger fonts, better visibility
# ═══════════════════════════════════════════════════════
def page_shop():
    coins=S("coins",0)
    st.markdown(f"""<div style="text-align:center;margin-bottom:22px">
<h1 style="letter-spacing:3px;font-size:28px">🛒 UPGRADE SHOP</h1>
<div style="display:inline-flex;align-items:center;gap:12px;padding:14px 28px;
  background:linear-gradient(135deg,rgba(255,214,10,.12),rgba(255,214,10,.04));
  border:1px solid rgba(255,214,10,.5);border-radius:12px;margin-top:10px">
  <span style="font-size:28px">💰</span>
  <span style="font-family:'Orbitron',sans-serif;font-size:28px;font-weight:900;color:#ffd60a;
    text-shadow:0 0 12px rgba(255,214,10,.7)">{coins:,}</span>
  <span style="color:#aabbdd;font-size:14px;font-family:Rajdhani,sans-serif;font-weight:700">coins available</span>
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
                if maxed: col_="#39ff14"; bg_="linear-gradient(145deg,rgba(57,255,20,.1),rgba(57,255,20,.03))"; brd_="rgba(57,255,20,.5)"
                elif can: col_="#ffd60a"; bg_="linear-gradient(145deg,rgba(255,214,10,.1),rgba(255,214,10,.03))"; brd_="rgba(255,214,10,.45)"
                else: col_="#aabbdd"; bg_="linear-gradient(145deg,rgba(255,255,255,.04),rgba(0,0,0,.2))"; brd_="rgba(255,255,255,.1)"
                badge=""
                if maxed: badge=f"<div style='position:absolute;top:10px;right:10px;background:rgba(57,255,20,.2);border:1px solid rgba(57,255,20,.6);border-radius:6px;padding:3px 9px;font-size:11px;color:#39ff14;font-weight:700;font-family:Orbitron,sans-serif'>MAX</div>"
                elif cnt: badge=f"<div style='position:absolute;top:10px;right:10px;background:rgba(0,245,255,.12);border:1px solid rgba(0,245,255,.4);border-radius:6px;padding:3px 9px;font-size:11px;color:#00f5ff;font-family:Share Tech Mono,monospace'>{cnt}/{mx}</div>"
                with cols[i%3]:
                    st.markdown(f"""<div style="background:{bg_};border:1px solid {brd_};border-radius:14px;
padding:20px 16px;text-align:center;margin-bottom:10px;min-height:165px;position:relative;">
{badge}
<div style="font-size:36px;margin-bottom:10px">{item['icon']}</div>
<div style="font-weight:700;font-size:15px;color:{col_};margin-bottom:6px;font-family:'Orbitron',sans-serif;letter-spacing:.5px">{item['name']}</div>
<div style="color:#aabbdd;font-size:13px;margin-bottom:12px;line-height:1.5;font-family:'Rajdhani',sans-serif">{item['desc']}</div>
<div style="font-family:'Orbitron',sans-serif;font-size:16px;font-weight:900;color:{'#39ff14' if maxed else '#ffd60a'};text-shadow:0 0 8px {'rgba(57,255,20,.5)' if maxed else 'rgba(255,214,10,.5)'}">{'✓ MAXED' if maxed else '💰 '+str(item['price'])}</div>
</div>""",unsafe_allow_html=True)
                    if not maxed:
                        label="🛒 Buy" if can else f"🔒 Need {item['price']-coins} more"
                        st.markdown(f'<div class="{"bg" if can else ""}">',unsafe_allow_html=True)
                        if st.button(label,key=f"sh_{uid}_{cnt}",use_container_width=True,disabled=not can):
                            ok,msg=buy_item(uid)
                            if ok: st.balloons(); st.rerun()
                        st.markdown('</div>',unsafe_allow_html=True)

    owned={k:v for k,v in S("owned",{}).items() if v>0}
    if owned:
        st.markdown("---")
        st.markdown("<h3 style='font-size:16px;letter-spacing:2px;color:#aabbdd'>🎒 MY UPGRADES</h3>",unsafe_allow_html=True)
        b2="".join(f"<span style='display:inline-flex;padding:7px 16px;background:linear-gradient(135deg,rgba(57,255,20,.1),rgba(57,255,20,.03));border:1px solid rgba(57,255,20,.4);border-radius:14px;font-size:13px;font-weight:700;color:#39ff14;margin:4px;font-family:Rajdhani,sans-serif'>{SHOP[uid]['icon']} {SHOP[uid]['name']}{' ×'+str(v) if v>1 else ''}</span>"
                  for uid,v in owned.items() if uid in SHOP)
        st.markdown(f"<div style='display:flex;flex-wrap:wrap;gap:4px'>{b2}</div>",unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<h3 style='font-size:16px;letter-spacing:2px;color:#aabbdd'>💰 HOW TO EARN COINS</h3>",unsafe_allow_html=True)
    tips=[("🐍","Snake","Play & set high scores"),("🐦","Flappy","Pass pipes"),("🧠","Memory","Fewer moves = more"),
          ("❌","XO","Win vs AI = 50 coins"),("👆","Clicker","Clicks × 2 coins"),("🎰","Slots","Match symbols"),
          ("🏓","Pong","Beat the AI"),("💣","Mines","Clear field = 80"),("🔢","Guess","Fewer guesses = more"),
          ("🎨","Paint","Tiles × 5 coins")]
    tip_cols=st.columns(5)
    for i,(ico,name,tip) in enumerate(tips):
        with tip_cols[i%5]:
            st.markdown(f"""<div style="background:rgba(0,245,255,.04);border:1px solid rgba(0,245,255,.1);border-radius:10px;padding:14px;text-align:center;margin-bottom:8px">
<div style="font-size:24px;margin-bottom:6px">{ico}</div>
<div style="color:#00f5ff;font-size:12px;font-weight:700;font-family:'Orbitron',sans-serif;margin-bottom:4px">{name}</div>
<div style="color:#aabbdd;font-size:12px;font-family:'Rajdhani',sans-serif">{tip}</div></div>""",unsafe_allow_html=True)

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
    "paintrace":   page_paintrace,
    "wordgame":    page_wordgame,
    "pong2p":      page_pong2p,
    "ttt2p":       page_ttt2p,
    "dice2p":      page_dice2p,
    "sumo2p":      page_sumo2p,
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
