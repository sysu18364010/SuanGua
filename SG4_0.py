'''
写一个周易起卦程序，给自己生活以指导
首先是随机数生成，用0代表阴，1代表阳
起卦方法：先采用硬币起卦法，三个硬币，从下往上生成卦

1.0 实现起卦
同时抛掷3枚硬币，
两阴一阳为少阳（7表示），三阳为老阳（9表示），需变卦
两阳一阴为少阴（8表示），三阴为老阴（6表示），需变卦
因为加入顺序是无关的，我们让列表元素从小排到大，方便判断

2.0新增功能
接下来需要一个字典，可以索引对应的卦，这个留到明天吧
先3爻对应八卦，再两个卦再组合

3.0 新增功能
将卦封装成一个类
设置随机种子，保证时间一样，输入一样时，结果一样
利用朱熹解卦的方法，输出对应的卦辞爻辞

4.0 新增功能，实现可视化
实现可视化输入以及文字输出
'''


# 导入需要的库
import random as r
import datetime as d
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QInputDialog, QTextBrowser)
import sys
# from typing_extensions import Self
from yi_book import YinYangDict,G_8_dict,G_64_dict,book

class Gua():
    # 初始化函数
    def __init__(self,wish) -> None:
        self.gua = []
        self.wish = wish # 所求之事
        self.YuanGua = ''
        self.BianGua = ''
        self.turn_symbol_index_list = [] # 存储第几爻变爻
        self.not_turn_symbol_index_list = [] # 存储第几爻不变爻

    # 设置随机数种子，确保用户输入一样时，得到的随机数是一样的
    def _set_random_seed(self, time_seed_str):
        def _transfer_str_to_time_seed():
            user_input_str_bytes = time_seed_str.encode()
            inner_random_seed = 0
            for tmp_byte in user_input_str_bytes:
                inner_random_seed += tmp_byte
            return inner_random_seed
        random_seed = _transfer_str_to_time_seed()
        r.seed(random_seed)

    # 分析变爻数及变爻下标列表,这个需要改，方法不太一样
    def _get_turn_symbol_count_and_index_list(self, origin_hexagram, support_hexagram):
        turn_symbol_count = 0
        turn_symbol_index_list = []
        not_turn_symbol_index_list = []
        for index in range(len(origin_hexagram)):
            if origin_hexagram[index] != support_hexagram[index]:
                turn_symbol_count += 1
                turn_symbol_index_list.append(index)
            else:
                not_turn_symbol_index_list.append(index)
        return turn_symbol_count,turn_symbol_index_list,not_turn_symbol_index_list
    
    # 输入所求之事进行起卦
    def QiGua(self):
        # self.wish = input("请输入你所求之事：")
        today = d.datetime.now().__format__("%Y%m%d")
        time_seed_str = self.wish + today
        # 设置随机数种子，确保当天同样的输出得到的结果是一样的
        self._set_random_seed(time_seed_str)
        for _ in range(6):
            num = []
            for _ in range(3):
                num.append(r.randint(0,1))
            num.sort() # 因为阴阳卦只与数量有关，所以这里采用排序对应
            self.gua.insert(0,YinYangDict["%d%d%d"%(num[0],num[1],num[2])])
        print(self.gua)
        # 变卦 老阴变阳，老阳变阴
        YuanGua = ""
        BianGua = ""
        for n,y in enumerate(self.gua):
            if y == 6:
                YuanGua += '0'
                BianGua += '1'
                self.turn_symbol_index_list.append(n)
            elif y == 9:
                YuanGua += '1'
                BianGua += '0'
                self.turn_symbol_index_list.append(n)
            elif y == 7:
                YuanGua += '1'
                BianGua += '1' 
                self.not_turn_symbol_index_list.append(n)
            else :
                YuanGua += '0'
                BianGua += '0'
                self.not_turn_symbol_index_list.append(n)
        self.YuanGua = YuanGua
        self.BianGua = BianGua      
        print(YuanGua,'--->',BianGua)
        print(G_64_dict[YuanGua],'--->',G_64_dict[BianGua])
        print(self.turn_symbol_index_list)
    
    # 解卦，利用朱熹的方法进行解卦
    def JieGua(self):
        turn_symbol_count = len(self.turn_symbol_index_list) # 变爻的数目
        
        main_indicate = "" # 主爻辞
        support_indicate = "" # 次爻辞

        origin_hexagram_dict_key = self.YuanGua
        support_hexagram_dict_key = self.BianGua
        turn_symbol_index_list = self.turn_symbol_index_list
        not_turn_symbol_index_list = self.not_turn_symbol_index_list
        # 六爻皆不变者，占本卦卦辞
        if turn_symbol_count == 0:
            turn_symbol_desc = "六爻皆不变者，占本卦卦辞。"
            main_indicate = book[origin_hexagram_dict_key]["indicate"][0]
        # 一爻变者，以本卦变爻之辞占
        elif turn_symbol_count == 1:
            turn_symbol_desc = "一爻变者，以本卦变爻之辞占。"
            main_indicate = book[origin_hexagram_dict_key]["indicate"][turn_symbol_index_list[0]+1]
        # 二爻变者，则以本卦二变爻之辞占，而以上爻之辞为主
        elif turn_symbol_count == 2:
            turn_symbol_desc = "二爻变者，则以本卦二变爻之辞占，而以上爻之辞为主。"
            main_indicate = book[origin_hexagram_dict_key]["indicate"][turn_symbol_index_list[1]+1]
            support_indicate = book[origin_hexagram_dict_key]["indicate"][turn_symbol_index_list[0]+1]
        # 三爻变者，占本卦及之卦的卦辞，而以本卦为主
        elif turn_symbol_count == 3:
            turn_symbol_desc = "三爻变者，占本卦及之卦的卦辞，而以本卦为主。"
            main_indicate = book[origin_hexagram_dict_key]["indicate"][0]
            support_indicate = book[support_hexagram_dict_key]["indicate"][0]
        # 四爻变者，以之卦中二不变之爻辞占，以下爻为主
        elif turn_symbol_count == 4:
            turn_symbol_desc = "四爻变者，以之卦中二不变之爻辞占，以下爻为主。"
            main_indicate = book[origin_hexagram_dict_key]["indicate"][not_turn_symbol_index_list[0]+1]
            support_indicate = book[origin_hexagram_dict_key]["indicate"][not_turn_symbol_index_list[1]+1]
        # 五爻变者，以之卦中不变爻的爻辞占
        elif turn_symbol_count == 5:
            turn_symbol_desc = "五爻变者，以之卦中不变爻的爻辞占。"
            main_indicate = book[origin_hexagram_dict_key]["indicate"][not_turn_symbol_index_list[0]+1]
        # 六爻皆变者，以乾坤二用之辞占，并参考其之卦卦辞
        elif turn_symbol_count == 6:
            turn_symbol_desc = "六爻皆变者，以乾坤二用之辞占，并参考其之卦卦辞。"
            main_indicate = book[origin_hexagram_dict_key]["indicate"][7]
            support_indicate = book[support_hexagram_dict_key]["indicate"][0]
        return turn_symbol_desc,main_indicate,support_indicate

class GuaPaint(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(500,500,500,550) # 窗口位置大小
        self.setWindowTitle('必修算卦')

        self.bt1 = QPushButton('问天',self) # 输入按键
        self.bt1.move(225,50)

        self.tb = QTextBrowser(self) # 输出信息
        self.tb.move(20,100)

        self.show()

        self.bt1.clicked.connect(self.showDialog)
    def showDialog(self):
        sender = self.sender()
        if sender == self.bt1:
            text, ok = QInputDialog.getText(self, '问天', '请输入所求之事：')
            if ok:
                gua = Gua(text) 
                gua.QiGua()
                turn_symbol_desc, main_indicate, support_indicate = gua.JieGua()
                outText = f"说明：{turn_symbol_desc}\n主预言：{main_indicate}\n辅预言：{support_indicate}"
                self.tb.setText(outText)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = GuaPaint()
    sys.exit(app.exec_())