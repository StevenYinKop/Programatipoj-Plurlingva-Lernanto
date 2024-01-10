import turtle
def drawGap():
    turtle.penup()
    turtle.fd(3)
    turtle.pendown()

def drawLine(draw):
    drawGap()
    turtle.pendown() if draw else turtle.penup()
    turtle.fd(20)
    drawGap()
    turtle.right(90)

def drawElement(ele):
    drawLine(ele in ['2', '3', '4', '5', '6', '8', '9', 'a', 'b', 'd', 'e', 'f'])
    drawLine(ele in ['0', '1', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'd'])
    drawLine(ele in ['0', '2', '3', '5', '6', '8', '9', 'b', 'c', 'd', 'e'])
    drawLine(ele in ['0', '2', '6', '8', 'a', 'b', 'c', 'd', 'e', 'f'])
    turtle.left(90)
    drawLine(ele in ['0', '4', '5', '6', '8', '9', 'a', 'b', 'c', 'e', 'f'])
    drawLine(ele in ['0', '2', '3', '5', '6', '7', '8', '9', 'a', 'c', 'e', 'f'])
    drawLine(ele in ['0', '1', '2', '3', '4', '7', '8', '9', 'a', 'd'])
    # drawLine(ele in [0, 2, 3, 4, 5, 6, 8, 9, 'a', 'b', 'd', 'e', 'f'])

turtle.setup(1000, 600)
turtle.hideturtle()
turtle.penup()
turtle.goto(-450, 0)
for i in 'abcdefg1234567890':
    drawElement(i)
    turtle.right(180)
    turtle.penup()
    turtle.fd(20)
turtle.done()