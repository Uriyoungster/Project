import streamlit as st

st.title("🐍 משחק הנחש עם כוחות")

html_code = """
<!DOCTYPE html>
<html>
<body style="text-align:center; font-family:sans-serif;">

<h2 id="score">ניקוד: 0</h2>
<button onclick="startGame()">התחל משחק</button>

<br><br>

<canvas id="game" width="400" height="400"
style="background:black; border:2px solid gray;"></canvas>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

const grid = 20;
let snake, dx, dy, apple, power, score, speed, running;

function randomPos() {
  return Math.floor(Math.random() * 20) * grid;
}

function resetGame() {
  snake = [{x: 160, y: 160}];
  dx = grid;
  dy = 0;
  apple = {x: randomPos(), y: randomPos()};
  power = null;
  score = 0;
  speed = 120;
  running = true;
  document.getElementById("score").innerText = "ניקוד: 0";
}

function startGame() {
  resetGame();
  canvas.focus();
  gameLoop();
}

canvas.setAttribute("tabindex","0");

canvas.addEventListener("keydown", function(e) {
  if (e.key === "ArrowLeft" && dx === 0) {
    dx = -grid; dy = 0;
  } else if (e.key === "ArrowUp" && dy === 0) {
    dx = 0; dy = -grid;
  } else if (e.key === "ArrowRight" && dx === 0) {
    dx = grid; dy = 0;
  } else if (e.key === "ArrowDown" && dy === 0) {
    dx = 0; dy = grid;
  }
});

function spawnPower() {
  if (!power && Math.random() < 0.1) {
    const types = ["slow", "bonus", "shrink"];
    power = {
      x: randomPos(),
      y: randomPos(),
      type: types[Math.floor(Math.random() * types.length)]
    };
  }
}

function gameLoop() {
  if (!running) return;

  const head = {x: snake[0].x + dx, y: snake[0].y + dy};

  // קירות
  if (head.x < 0 || head.y < 0 || head.x >= 400 || head.y >= 400) {
    alert("הפסדת! ניקוד: " + score);
    running = false;
    return;
  }

  // פגיעה בעצמך
  for (let cell of snake) {
    if (cell.x === head.x && cell.y === head.y) {
      alert("נפסלת! ניקוד: " + score);
      running = false;
      return;
    }
  }

  snake.unshift(head);

  // תפוח רגיל
  if (head.x === apple.x && head.y === apple.y) {
    score++;
    document.getElementById("score").innerText = "ניקוד: " + score;

    if (speed > 40) speed -= 5;

    apple = {x: randomPos(), y: randomPos()};
  } else {
    snake.pop();
  }

  // יצירת כוח
  spawnPower();

  // אכילת כוח
  if (power && head.x === power.x && head.y === power.y) {
    if (power.type === "slow") {
      speed += 20;
    } else if (power.type === "bonus") {
      score += 5;
    } else if (power.type === "shrink") {
      snake.splice(-3);
    }

    document.getElementById("score").innerText = "ניקוד: " + score;
    power = null;
  }

  // ציור
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // נחש
  ctx.fillStyle = "lime";
  snake.forEach(cell => {
    ctx.fillRect(cell.x, cell.y, grid-2, grid-2);
  });

  // תפוח
  ctx.fillStyle = "red";
  ctx.fillRect(apple.x, apple.y, grid-2, grid-2);

  // כוח
  if (power) {
    if (power.type === "slow") ctx.fillStyle = "yellow";
    if (power.type === "bonus") ctx.fillStyle = "blue";
    if (power.type === "shrink") ctx.fillStyle = "purple";

    ctx.fillRect(power.x, power.y, grid-2, grid-2);
  }

  setTimeout(gameLoop, speed);
}

</script>

</body>
</html>
"""

st.components.v1.html(html_code, height=550)
