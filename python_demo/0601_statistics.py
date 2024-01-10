def getNum():
    nums = []
    iNumStr = input("请输入数字(回车结束)")
    while iNumStr != "":
        nums.append(eval(iNumStr))
        iNumStr = input("请输入数字(回车结束)")
    return nums
def mean(nums):
    s = 0.0
    for num in nums:
        s += num
    return s / len(nums)

def dev(nums, mean):
    sdev = 0.0
    for num in nums:
        sdev = sdev + (num - mean) ** 2
    return sdev / (len(nums) - 1) ** 0.5

def median(nums):
    sorted(nums)
    size = len(nums)
    if size % 2 == 0:
        med = (nums[size // 2 - 1] + nums[size // 2]) / 2
    else:
        med = nums[size // 2]
    return med
nums = getNum()
m = mean(nums)
print("平均值: {}, 方差: {:.2f}, 中位数: {}".format(m, dev(nums, m), median(nums)))

