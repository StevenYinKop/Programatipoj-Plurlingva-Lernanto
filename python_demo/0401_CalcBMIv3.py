#0401_CalcBMIv3.py
weight, height = eval(input("请输入体重(公斤)/身高(米), 中间用英文逗号分隔, 如: 60,1.75: \n"))
bmi = weight / pow(height, 2)
print("你的BMI指数为: {:.2f}".format(bmi))
if (bmi < 18.5):
    who, nat = "偏瘦","偏瘦"
elif 18.5 <= bmi < 24:
    who, nat = "正常","正常"
elif 24 <= bmi < 25:
    who, nat = "正常", "偏胖"
elif 25 <= bmi < 28:
    who, nat = "偏胖", "偏胖"
elif 28 <= bmi < 30:
    who, nat = "偏胖", "肥胖"
else:
    who, nat = "肥胖", "肥胖"

print("国际: [{}], 国内: [{}]".format(who, nat))

