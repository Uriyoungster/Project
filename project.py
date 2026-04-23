import streamlit as st

st.title("🐍 Snake Ultra")

html_code = """
<!DOCTYPE html>
<html>
<body style="text-align:center; font-family:sans-serif; background:#111; color:white;">

<h2 id="score">ניקוד: 0 | שיא: 0</h2>
<button onclick="startGame()">התחל משחק</button>
<button onclick="togglePause()">⏸️ Pause</button>

<br><br>

<canvas id="game" width="420" height="420"
style="background:#000; border:3px solid #555;"></canvas>

<div id="gameover" style="display:none; font-size:24px; margin-top:10px;">
💀 Game Over
</div>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

const grid = 20;
const size = 20;

let snake, dx, dy, apple, power;
let score, highscore = localStorage.getItem("snakeHigh") || 0;
let speed, running, paused, shield, turbo;

function randomPos() {
  return Math.floor(Math.random() * size) * grid;
}

function resetGame() {
  snake = [{x: 200, y: 200}];
  dx = grid;
  dy = 0;
  apple = {x: randomPos(), y: randomPos()};
  power = null;
  score = 0;
  speed = 120;
  running = true;
  paused = false;
  shield = 0;
  turbo = 0;

  document.getElementById("gameover").style.display = "none";
  updateScore();
}

function updateScore() {
  document.getElementById("score").innerText =
    "ניקוד: " + score + " | שיא: " + highscore;
}

function startGame() {
  resetGame();
  gameLoop();
}

function togglePause() {
  paused = !paused;
}

// 🎮 שליטה
document.addEventListener("keydown", function(e) {
  if(["ArrowUp","ArrowDown","ArrowLeft","ArrowRight","w","a","s","d"].includes(e.key)) {
    e.preventDefault();
  }

  if ((e.key === "ArrowLeft" || e.key==="a") && dx === 0) {
    dx = -grid; dy = 0;
  } else if ((e.key === "ArrowUp" || e.key==="w") && dy === 0) {
    dx = 0; dy = -grid;
  } else if ((e.key === "ArrowRight" || e.key==="d") && dx === 0) {
    dx = grid; dy = 0;
  } else if ((e.key === "ArrowDown" || e.key==="s") && dy === 0) {
    dx = 0; dy = grid;
  }
});

// כוחות
function spawnPower() {
  if (!power && Math.random() < 0.08) {
    const types = ["slow","bonus","shrink","shield","turbo"];
    power = {
      x: randomPos(),
      y: randomPos(),
      type: types[Math.floor(Math.random()*types.length)]
    };
  }
}

function applyPower(type) {
  if (type === "slow") speed += 20;
  if (type === "bonus") score += 5;

  if (type === "shrink") {
    if (snake.length > 5) {
      snake.splice(-Math.min(3, snake.length-1));
    }
  }

  if (type === "shield") shield = 10;
  if (type === "turbo") turbo = 10;

  updateScore();
}

// ציור גריד
function drawGrid() {
  ctx.strokeStyle = "#222";
  for (let i=0;i<420;i+=20) {
    ctx.beginPath();
    ctx.moveTo(i,0); ctx.lineTo(i,420); ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(0,i); ctx.lineTo(420,i); ctx.stroke();
  }
}

function gameOver() {
  running = false;
  document.getElementById("gameover").style.display = "block";

  if (score > highscore) {
    highscore = score;
    localStorage.setItem("snakeHigh", highscore);
  }
}

function gameLoop() {
  if (!running) return;
  if (paused) {
    setTimeout(gameLoop, 100);
    return;
  }

  const head = {x: snake[0].x + dx, y: snake[0].y + dy};

  // קירות
  if (head.x < 0 || head.y < 0 || head.x >= 420 || head.y >= 420) {
    if (shield > 0) {
      shield--;
    } else {
      gameOver();
      return;
    }
  }

  // עצמי
  for (let cell of snake) {
    if (cell.x === head.x && cell.y === head.y) {
      if (shield > 0) {
        shield--;
        break;
      } else {
        gameOver();
        return;
      }
    }
  }

  snake.unshift(head);

  // תפוח
  if (head.x === apple.x && head.y === apple.y) {
    score++;
    if (speed > 50) speed -= 2;
    apple = {x: randomPos(), y: randomPos()};
    updateScore();
  } else {
    snake.pop();
  }

  spawnPower();

  if (power && head.x === power.x && head.y === power.y) {
    applyPower(power.type);
    power = null;
  }

  // אפקטים
  if (turbo > 0) {
    turbo--;
  }
  if (shield > 0) {
    shield--;
  }

  // ציור
  ctx.clearRect(0,0,canvas.width,canvas.height);

  drawGrid();

  // נחש
  ctx.fillStyle = turbo>0 ? "orange" : "lime";
  snake.forEach(c => ctx.fillRect(c.x, c.y, grid-2, grid-2));

  // תפוח
  ctx.fillStyle = "red";
  ctx.fillRect(apple.x, apple.y, grid-2, grid-2);

  // כוח
  if (power) {
    const colors = {
      slow:"cyan",
      bonus:"blue",
      shrink:"purple",
      shield:"gold",
      turbo:"orange"
    };
    ctx.fillStyle = colors[power.type];
    ctx.fillRect(power.x, power.y, grid-2, grid-2);
  }

  setTimeout(gameLoop, turbo>0 ? speed/2 : speed);
}
</script>

</body>
</html>
"""

st.components.v1.html(html_code, height=650)
