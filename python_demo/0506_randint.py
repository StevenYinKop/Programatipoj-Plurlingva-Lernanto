import random

def genpwd(length):
    range = [10 ** (length - 1), 10 ** length]
    return random.randint(range[0], range[1])

length = eval(input())
random.seed(17)
for i in range(3):
    print(genpwd(length))
