import streamlit as st

st.title("🐍 Snake - Power Shop Edition")

html_code = """
<!DOCTYPE html>
<html>
<body style="text-align:center; font-family:sans-serif; background:#111; color:white;">

<h2 id="score">נקודות: 0 | שיא: 0</h2>

<button onclick="startGame()">התחל משחק</button>
<button onclick="toggleShop()">🛒 חנות כוחות</button>

<br><br>

<canvas id="game" width="420" height="420"
style="background:#000; border:3px solid #444;"></canvas>

<div id="shop" style="display:none; margin-top:10px; background:#222; padding:10px;">
  <h3>🛒 חנות שדרוג כוחות</h3>

  <p>❄️ Slow Upgrade - מחיר: 5 נקודות</p>
  <button onclick="buy('slow')">שדרג האטה</button>

  <p>🔵 Bonus Upgrade - מחיר: 7 נקודות</p>
  <button onclick="buy('bonus')">שדרג בונוס</button>

  <p>🛡️ Shield Upgrade - מחיר: 10 נקודות</p>
  <button onclick="buy('shield')">שדרג מגן</button>
</div>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

const grid = 20;

let snake, dx, dy, apple, power;
let score, highscore = localStorage.getItem("hs") || 0;
let speed, running;

let powerLevel = {
  slow: 1,
  bonus: 1,
  shield: 1
};

function randomPos(){
  return Math.floor(Math.random()*20)*grid;
}

function reset(){
  snake = [{x:200,y:200}];
  dx = grid;
  dy = 0;
  apple = {x:randomPos(), y:randomPos()};
  power = null;
  score = 0;
  speed = 120;
  running = true;
  updateUI();
}

function updateUI(){
  document.getElementById("score").innerText =
    "נקודות: " + score + " | שיא: " + highscore;
}

function startGame(){
  reset();
  loop();
}

function toggleShop(){
  let s = document.getElementById("shop");
  s.style.display = (s.style.display==="none")?"block":"none";
}

// 🛒 חנות שמשדרגת כוחות אמיתיים
function buy(type){
  if(type==="slow" && score>=5){
    score -= 5;
    powerLevel.slow++;
  }
  if(type==="bonus" && score>=7){
    score -= 7;
    powerLevel.bonus++;
  }
  if(type==="shield" && score>=10){
    score -= 10;
    powerLevel.shield++;
  }
  updateUI();
}

// 🎮 שליטה
document.addEventListener("keydown", e=>{
  if(["ArrowLeft","ArrowRight","ArrowUp","ArrowDown"].includes(e.key))
    e.preventDefault();

  if(e.key==="ArrowLeft" && dx===0){dx=-grid;dy=0;}
  if(e.key==="ArrowRight"&& dx===0){dx=grid;dy=0;}
  if(e.key==="ArrowUp"&& dy===0){dx=0;dy=-grid;}
  if(e.key==="ArrowDown"&& dy===0){dx=0;dy=grid;}
});

function gameOver(){
  running=false;
  if(score>highscore){
    highscore=score;
    localStorage.setItem("hs",highscore);
  }
  alert("הפסדת! ניקוד: "+score);
}

// 💥 יצירת כוח עם השפעה לפי שדרוגים
function spawnPower(){
  if(!power && Math.random()<0.08){
    const types=["slow","bonus","shield"];
    power={
      x:randomPos(),
      y:randomPos(),
      type:types[Math.floor(Math.random()*types.length)]
    };
  }
}

function applyPower(type){
  if(type==="slow"){
    speed += 15 / powerLevel.slow;
  }

  if(type==="bonus"){
    score += 1 * powerLevel.bonus;
  }

  if(type==="shield"){
    snake.unshift({x:snake[0].x, y:snake[0].y}); // חיזוק גוף
  }

  updateUI();
}

function loop(){
  if(!running)return;

  const head = {x:snake[0].x+dx, y:snake[0].y+dy};

  if(head.x<0||head.y<0||head.x>=420||head.y>=420){
    gameOver(); return;
  }

  for(let c of snake){
    if(c.x===head.x && c.y===head.y){
      gameOver(); return;
    }
  }

  snake.unshift(head);

  if(head.x===apple.x && head.y===apple.y){
    score++;
    apple={x:randomPos(), y:randomPos()};
    if(speed>50) speed-=1;
    updateUI();
  } else {
    snake.pop();
  }

  spawnPower();

  if(power && head.x===power.x && head.y===power.y){
    applyPower(power.type);
    power=null;
  }

  // ציור
  ctx.clearRect(0,0,420,420);

  snake.forEach((c,i)=>{
    ctx.fillStyle=i===0?"#00ff99":"#00aa66";
    ctx.fillRect(c.x,c.y,grid-2,grid-2);
  });

  ctx.fillStyle="red";
  ctx.fillRect(apple.x,apple.y,grid-2,grid-2);

  if(power){
    const colors={
      slow:"cyan",
      bonus:"blue",
      shield:"gold"
    };
    ctx.fillStyle=colors[power.type];
    ctx.fillRect(power.x,power.y,grid-2,grid-2);
  }

  setTimeout(loop,speed);
}
</script>

</body>
</html>
"""

st.components.v1.html(html_code, height=650)
