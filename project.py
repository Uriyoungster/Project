import streamlit as st

st.title("🐍 משחק הנחש")

html_code = """
<!DOCTYPE html>
<html>
<head>
<style>
  canvas { background: black; display: block; margin: auto; }
  body { text-align: center; color: white; }
</style>
</head>
<body>

<h2 id="score">ניקוד: 0</h2>
<canvas id="game" width="400" height="400"></canvas>

<script>
let canvas = document.getElementById("game");
let ctx = canvas.getContext("2d");

let grid = 20;
let count = 0;
let speed = 8;

let snake = [{x: 160, y: 160}];
let dx = grid;
let dy = 0;

let apple = {
  x: Math.floor(Math.random() * 20) * grid,
  y: Math.floor(Math.random() * 20) * grid
};

let score = 0;

document.addEventListener("keydown", function(e) {
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

function gameLoop() {
  requestAnimationFrame(gameLoop);

  if (++count < speed) return;
  count = 0;

  ctx.clearRect(0,0,canvas.width,canvas.height);

  snake[0].x += dx;
  snake[0].y += dy;

  // קירות
  if (snake[0].x < 0 || snake[0].x >= canvas.width ||
      snake[0].y < 0 || snake[0].y >= canvas.height) {
    alert("הפסדת! ניקוד: " + score);
    location.reload();
  }

  // תפוח
  if (snake[0].x === apple.x && snake[0].y === apple.y) {
    score++;
    document.getElementById("score").innerText = "ניקוד: " + score;

    // מהירות עולה
    if (speed > 2) speed--;

    apple.x = Math.floor(Math.random() * 20) * grid;
    apple.y = Math.floor(Math.random() * 20) * grid;

  } else {
    snake.pop();
  }

  // ציור נחש
  ctx.fillStyle = "lime";
  snake.forEach(function(cell, index) {
    ctx.fillRect(cell.x, cell.y, grid-2, grid-2);

    if (index === 0) {
      for (let i = index + 1; i < snake.length; i++) {
        if (cell.x === snake[i].x && cell.y === snake[i].y) {
          alert("נפסלת! ניקוד: " + score);
          location.reload();
        }
      }
    }
  });

  snake.unshift({x: snake[0].x, y: snake[0].y});

  // ציור תפוח
  ctx.fillStyle = "red";
  ctx.fillRect(apple.x, apple.y, grid-2, grid-2);
}

requestAnimationFrame(gameLoop);
</script>

</body>
</html>
"""

st.components.v1.html(html_code, height=500)
