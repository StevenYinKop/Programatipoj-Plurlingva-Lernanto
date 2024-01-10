# 0302_DayDayUpQ2.py
factor = 0.005
print("向上: {:.2f}, 向下: {:.2f}".format((1+factor)**365, (1-factor)**365))
factor = 0.01
print("向上: {:.2f}, 向下: {:.2f}".format((1+factor)**365, (1-factor)**365))