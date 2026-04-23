import streamlit as st

st.title("🐍 Snake + Shop Edition")

html_code = """
<!DOCTYPE html>
<html>
<body style="text-align:center; font-family:sans-serif; background:#111; color:white;">

<h2 id="score">נקודות: 0 | שיא: 0</h2>

<button onclick="startGame()">התחל משחק</button>
<button onclick="toggleShop()">🛒 חנות</button>

<br><br>

<canvas id="game" width="420" height="420"
style="background:#000; border:3px solid #444;"></canvas>

<div id="shop" style="display:none; margin-top:10px; background:#222; padding:10px;">
  <h3>🛒 חנות שדרוגים</h3>
  <button onclick="buy('speed')">שדרוג מהירות (-נקודות ליותר שליטה)</button><br><br>
  <button onclick="buy('shield')">שדרוג מגן (יותר חיים)</button><br><br>
  <button onclick="buy('bonus')">שדרוג בונוס (+נקודות יותר חזק)</button>
</div>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

const grid = 20;

let snake, dx, dy, apple;
let score, highscore = localStorage.getItem("hs") || 0;
let speed, running;

let upgrades = {
  speed: 0,
  shield: 0,
  bonus: 0
};

function randomPos(){
  return Math.floor(Math.random()*20)*grid;
}

function reset(){
  snake = [{x:200,y:200}];
  dx = grid;
  dy = 0;
  apple = {x:randomPos(), y:randomPos()};
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

function buy(type){
  if(type==="speed" && score>=5){
    score -= 5;
    upgrades.speed++;
  }
  if(type==="shield" && score>=7){
    score -= 7;
    upgrades.shield++;
  }
  if(type==="bonus" && score>=10){
    score -= 10;
    upgrades.bonus++;
  }
  updateUI();
}

// 🎮 שליטה חלקה
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

// 🎬 אנימציה חלקה יותר
function loop(){
  if(!running)return;

  const head = {x:snake[0].x+dx, y:snake[0].y+dy};

  if(head.x<0||head.y<0||head.x>=420||head.y>=420){
    if(upgrades.shield>0){
      upgrades.shield--;
    } else {
      gameOver(); return;
    }
  }

  for(let c of snake){
    if(c.x===head.x && c.y===head.y){
      if(upgrades.shield>0){
        upgrades.shield--;
        break;
      } else {
        gameOver(); return;
      }
    }
  }

  snake.unshift(head);

  if(head.x===apple.x && head.y===apple.y){
    score += 1 + upgrades.bonus;
    apple={x:randomPos(), y:randomPos()};
    if(speed>50) speed -= 1;
    updateUI();
  } else {
    snake.pop();
  }

  // ציור חלק
  ctx.fillStyle="#000";
  ctx.fillRect(0,0,420,420);

  // גריד עדין
  ctx.strokeStyle="#111";
  for(let i=0;i<420;i+=20){
    ctx.beginPath();ctx.moveTo(i,0);ctx.lineTo(i,420);ctx.stroke();
    ctx.beginPath();ctx.moveTo(0,i);ctx.lineTo(420,i);ctx.stroke();
  }

  // נחש עם אפקט זוהר
  snake.forEach((c,i)=>{
    ctx.fillStyle=i===0?"#00ff99":"#00cc66";
    ctx.fillRect(c.x,c.y,grid-2,grid-2);
  });

  // תפוח עם glow
  ctx.shadowBlur=10;
  ctx.shadowColor="red";
  ctx.fillStyle="red";
  ctx.fillRect(apple.x,apple.y,grid-2,grid-2);
  ctx.shadowBlur=0;

  setTimeout(loop,speed);
}
</script>

</body>
</html>
"""

st.components.v1.html(html_code, height=650)
