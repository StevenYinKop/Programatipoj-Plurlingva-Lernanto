# 06_draw_windmill.py
import turtle as t
t.pensize(2)
for i in range(4):
    t.left(45)
    t.fd(150)
    t.left(90)
    t.circle(150, 45)
    t.left(90)
    t.fd(150)
    t.left(180)
t.seth(135)
t.done()