# 根据数据集绘制图形

## 1. 定义数据文件格式(接口)
300, 0, 144, 1, 0, 0

2. 编写程序, 根据文件接口解析参数绘制图形
```python
import turtle as t
t.title("自动绘制轨迹")
t.setup(800, 600, 0, 0)
t.pencolor("red")
t.pensize(5)
datalist = []
f.open("data.txt")
for line in f:
    line = line.replace("\n", "")
    datalist.append(list(map(eval, line.split(","))))
f.close()
# 自动绘制
for i in range(len(datalist)):
    t.pencolor(datalist[i][3], datalist[i][4], datalist[i][5])
    t.fd(datalist[i][0])
    if datalist[i][1]:
        t.right(datalist[i][2])
    else:
        t.left(datalist[i][2])

3. 编制数据文件



自动化思维: