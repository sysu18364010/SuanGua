# 写一个周易起卦程序，给自己生活以指导
# 首先是随机数生成，用0代表阴，1代表阳
# 起卦方法：先采用硬币起卦法，三个硬币，从下往上生成卦
# 导入需要的库
import random as r

# 同时抛掷3枚硬币，
# 两阴一阳为少阳（7表示），三阳为老阳（9表示），需变卦
# 两阳一阴为少阴（8表示），三阴为老阴（6表示），需变卦
# 因为加入顺序是无关的，我们让列表元素从小排到大，方便判断
YinYangDict = {'000':6,"011":8,"001":7,"111":9}
Gua = []
for i in range(6):
    num = []
    for j in range(3):
        num.append(r.randint(0,1))
    num.sort()
    Gua.insert(0,YinYangDict["%d%d%d"%(num[0],num[1],num[2])])
print(Gua)

# 变卦 老阴变阳，老阳变阴
YuanGua = ""
BianGua = ""
for y in Gua:
    if y == 6:
        YuanGua += '0'
        BianGua += '1'
    elif y == 9:
        YuanGua += '1'
        BianGua += '0'
    elif y == 7:
        YuanGua += '1'
        BianGua += '1' 
    else :
        YuanGua += '0'
        BianGua += '0'      
print(YuanGua,'--->',BianGua)