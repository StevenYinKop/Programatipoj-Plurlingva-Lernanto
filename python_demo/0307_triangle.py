# num = eval(input(""))

def fun(num):
    i = 1
    while (i <= num):
        print(("*" * i).center(num, " "))
        i += 2
    print()

fun(1)
fun(3)
fun(5)
fun(7)
fun(9)
fun(11)
fun(13)