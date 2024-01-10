#0305_ProgressBarQ1.py
import time
scale = 50
print("开始执行".center(scale // 2, "-"))
start = time.perf_counter()
for i in range(scale + 1):
    a = "*" * i
    b = "." * (scale - i)
    c = (i / scale) * 100
    print("\r{:3.0f}%[{} -> {}] {:.2f}s".format(c, a, b, time.perf_counter() - start), end="")
    time.sleep(0.1)
print("执行结束".center(scale // 2, "-"))