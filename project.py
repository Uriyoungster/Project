import streamlit as st
import random
import time

st.title("🐍 משחק הנחש")

# הגדרות התחלתיות
width = 20
height = 20

if "snake" not in st.session_state:
    st.session_state.snake = [(10, 10)]
    st.session_state.direction = (0, 1)
    st.session_state.food = (random.randint(0, width-1), random.randint(0, height-1))
    st.session_state.game_over = False

# כפתורי שליטה
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("⬅️"):
        st.session_state.direction = (-1, 0)
with col2:
    if st.button("⬆️"):
        st.session_state.direction = (0, -1)
    if st.button("⬇️"):
        st.session_state.direction = (0, 1)
with col3:
    if st.button("➡️"):
        st.session_state.direction = (1, 0)

# עדכון המשחק
if not st.session_state.game_over:
    head = st.session_state.snake[0]
    dx, dy = st.session_state.direction
    new_head = (head[0] + dx, head[1] + dy)

    # בדיקת התנגשויות
    if (
        new_head in st.session_state.snake
        or new_head[0] < 0 or new_head[0] >= width
        or new_head[1] < 0 or new_head[1] >= height
    ):
        st.session_state.game_over = True
    else:
        st.session_state.snake.insert(0, new_head)

        if new_head == st.session_state.food:
            st.session_state.food = (
                random.randint(0, width-1),
                random.randint(0, height-1)
            )
        else:
            st.session_state.snake.pop()

# ציור הלוח
board = ""
for y in range(height):
    for x in range(width):
        if (x, y) == st.session_state.food:
            board += "🍎"
        elif (x, y) in st.session_state.snake:
            board += "🟩"
        else:
            board += "⬛"
    board += "\n"

st.text(board)

# סיום משחק
if st.session_state.game_over:
    st.error("הפסדת 😢")
    if st.button("התחל מחדש"):
        st.session_state.clear()

# רענון אוטומטי
time.sleep(0.3)
st.rerun()
