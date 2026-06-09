arr1 = [12, 134, 146, 104, 119, 124, 161, 107,83 , 113]
arr2 = [7,70,118,101, 85, 112, 132, 94]
# 取较短数组作为检验对象
y = []
if len(arr1) < len(arr2):
    y.extend(arr1)
else:
    y.extend(arr2)
#两组数据合在一起
c = arr1 + arr2 
#排序
c.sort()
# 建立两个数组，分别为"c":表示两个数组合并后排序后的数组;"a":表示序列号;"b":表示对应序列号的秩
# 表示序列号
a = []  
# 表示对应序列号的秩
b = []  
for i in range(1, len(c) + 1):
    a.append(i)
    b.append(i)
k = len(c) - 1
# 设立一个旗帜，如果发现排序有多个相同数则使第二位到最后一位的相同数的秩均等于第一位的秩值，跳过遍历。
flag = 0
for i in range(k):
    # 首先依次判断排好序后的数组内相邻位置的元素的值是否相等
    if c[i] != c[i + 1]:
        i += 1
        continue
    else:
        # 如果发现有相邻位置的元素的值相等，则从此位置开始向后遍历直到出现不相等的值。
        for n in range(i + 1, k + 1):
            if flag == 0:
                if c[i] == c[n]:
                    continue
                else:
                    # 计算有多少个元素的秩相等
                    for p in range(i, n):
                        # 首相加末项乘以项数除以二，之后再求这些位的平均值。
                        s = (((i + n + 1) * (n - i)) / 2) 
                        b[p] = s / (n - i)
                        flag = n - i - 2
                    break
            if flag != 0:
                b[n] = b[n - 1]
                flag = flag - 1
                # 每跳过一次遍历，旗帜的值减一
                break
print("两个序列合并排好序为:", c)
print("两个序列合并排好序的秩为:", b)
print("较短数组y为：", y)
T = 0
# 所求秩的和初始值为0
t = []
# 新建一个数组表示初始输入的较短的数组中对应位置的秩的值
lenth1 = len(y)
lenth2 = len(c)
i = 0
while i < lenth1:
    # 首先看要比较的值是否为初始两个数组内的最大值，如果是，则直接计入最大值的秩，如果不是，则继续检验。
    if y[i] ==c[k]:
        T += b[k]
        t.append(b[k])
        i += 1
        continue
    else:
        for m in range(lenth2):
            # 判断初始较短数组中的值在排好序的“c”数组中的具体位置。
            if y[i] < c[m]:
                T += b[m - 1]
                t.append(b[m - 1])
                break
        i += 1
# 数组t中所显示的值一一对应为初始较短数组中每个值的秩。
print('秩和为', T, 'y中数据的秩分别为', t)
k1 = 31
k2 = 65
# 根据拒绝域判断
if k1 < T < k2:  
    print('接受原假设')
else:
    print('拒绝原假设')

