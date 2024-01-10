#0503_koch.py
import turtle
def koch(size, n):
    if n == 0:
        turtle.fd(size)
    else:
        for angle in [0, 60, -120, 60]:
            turtle.left(angle)
            koch(size / 3, n - 1)
turtle.setup(600, 600)
turtle.pensize(2)
turtle.penup()
turtle.goto(-200, 200)
turtle.pendown()
turtle.hideturtle()
for angle in range(3):
    koch(400, 3)
    turtle.right(120)
turtle.done()