# 0304_DayDayUpQ4.py
def dayUp(df):
    base = 1.0
    for i in range(365):
        if i % 7 in [0, 6]:
            base *= (1 - 0.01)
        else:
            base *= (1 + df)
    return base

df = 0.01
daydayUp = 1.01 ** 365
while dayUp(df) < daydayUp:
    df += 0.001
print("{:.3f}".format(df))
