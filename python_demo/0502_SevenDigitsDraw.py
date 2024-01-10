#0502_SevenDigitsDraw.py
import turtle, time
def drawGap():
    turtle.penup()
    turtle.fd(10)
def drawLine(draw):
    drawGap()
    turtle.pendown() if draw else turtle.penup()
    turtle.fd(40)
    drawGap()
    turtle.right(90)
def drawDigit(digit):
    drawLine(digit in [2,3,4,5,6,8,9])
    drawLine(digit in [0,1,3,4,5,6,7,8,9])
    drawLine(digit in [0,2,3,5,6,8,9])
    drawLine(digit in [0,2,6,8])
    turtle.left(90)
    drawLine(digit in [0,4,5,6,8,9])
    drawLine(digit in [0,2,3,5,6,7,8,9])
    drawLine(digit in [0,1,2,3,4,7,8,9])
    turtle.left(180)
    turtle.penup()
def drawDate(date):
    print(date)
    turtle.pencolor("cyan")
    for i in date:
        if i == '-':
            turtle.write("年")
            turtle.pencolor("green")
        elif i == '=':
            turtle.write("月")
            turtle.pencolor("red")
        elif i == '+':
            turtle.write("日")
            turtle.pencolor("blue")
        else:
            drawDigit(eval(i))
        turtle.fd(20)
def main():
    turtle.hideturtle()
    turtle.setup(800, 350, 200, 200)
    turtle.penup()
    turtle.fd(-300)
    turtle.pensize(5)
    drawDate(time.strftime("%Y-%m=%d+").format(time.gmtime))
    turtle.done()
main()

