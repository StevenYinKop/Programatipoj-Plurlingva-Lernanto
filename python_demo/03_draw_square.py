#draw_square.py
from turtle import *
setup(650, 650, 0, 0)
pensize(2)
pu()
goto(-50, -50)
pd()
for i in range(4):
    seth(i * 90)
    fd(100)
seth(0)
done()