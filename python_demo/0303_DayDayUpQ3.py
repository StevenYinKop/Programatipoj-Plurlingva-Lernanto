# 0303_DayDayUpQ3.py
base = 1.0
factor = 0.01
for i in range(365):
    if i % 7 in [0, 6]:
        base *= (1 - factor)
    else:
        base *= (1 + factor)
print("{:.2f}".format(base))
