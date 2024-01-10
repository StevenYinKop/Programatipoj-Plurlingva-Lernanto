import re
f = open("./parseStr.txt", encoding="utf-8")
print(re.findall('/images/./../Servant\d{3}.jpg', f.read()))

# for line in f.read().split("\\n"):
#     for ele in line.split(","):
#         if (re.findall('./images/.*?/Servant\d{3}.jpg', ele)):
#             resFile.write(ele + '\n')
#             print(ele)