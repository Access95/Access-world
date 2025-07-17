import turtle
import random
import time

# Set up screen
win = turtle.Screen()
win.title("Catch the Star ⭐ by Mastermind")
win.bgcolor("black")
win.setup(width=600, height=600)
win.tracer(0)

# Create player (basket)
player = turtle.Turtle()
player.shape("square")
player.color("white")
player.shapesize(stretch_wid=1, stretch_len=5)
player.penup()
player.goto(0, -250)

# Create star
star = turtle.Turtle()
star.shape("circle")
star.color("yellow")
star.penup()
star.goto(random.randint(-250, 250), 250)
star.speed(0)

# Score
score = 0

score_writer = turtle.Turtle()
score_writer.hideturtle()
score_writer.color("white")
score_writer.penup()
score_writer.goto(-280, 260)
score_writer.write(f"Score: {score}", font=("Arial", 16, "bold"))

# Move player
def go_left():
    x = player.xcor()
    if x > -250:
        player.setx(x - 30)

def go_right():
    x = player.xcor()
    if x < 250:
        player.setx(x + 30)

win.listen()
win.onkeypress(go_left, "Left")
win.onkeypress(go_right, "Right")

# Game loop
fall_speed = 3
while True:
    win.update()
    y = star.ycor()
    star.sety(y - fall_speed)

    # Reset star if it falls
    if star.ycor() < -300:
        star.goto(random.randint(-250, 250), 250)

    # Check collision
    if player.distance(star) < 40:
        score += 1
        fall_speed += 0.2  # Increase difficulty
        star.goto(random.randint(-250, 250), 250)
        score_writer.clear()
        score_writer.write(f"Score: {score}", font=("Arial", 16, "bold"))

    time.sleep(0.01)
