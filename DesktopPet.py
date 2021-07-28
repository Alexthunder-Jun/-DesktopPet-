import os
from PyQt5 import QtCore
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = "Lib\site-packages\PyQt5\Qt\plugins"
#导入QT
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtNetwork import QTcpSocket, QHostAddress
# 导入常用组件
from ctypes import *
from threading import Thread
# 使用调色板等
import win32gui, win32ui, win32con, win32api
import time
import random
# 导入爬虫所需包
from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
#导入机器人所需的包
import sys
import speech_recognition as sr
import urllib3
import pygame
import urllib.request
import json
from aip import AipSpeech
import warnings
warnings.filterwarnings("ignore")
#解释一下为什么有的方法参数列表中有“event：指外部操作促使，并不是代码传参

'''机器人窗口'''
class RoboWin(QWidget):
    def __init__(self):
        super(RoboWin, self).__init__()
        self.setWindowTitle('比丢的聊天室')
        self.resize(500, 450)
        #self.setWindowFlags(Qt.FramelessWindowHint)  # 去边框
        #self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.browser = QTextBrowser(self)
        self.browser.setStyleSheet("background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,stop:0 #ACD6FF,stop:1 #FFECEC);border-radius:10px;height: calc(95vh);position: relative;padding: 30px 0;border:5px solid #92B0DD;"
        "box-shadow: 0 1px 4px rgba(0, 0, 0, 0.27), 0 0 40px rgba(0, 0, 0, 0.06) inset;")
        # palette = QPalette()                                                                                                                                           
        # palette.setBrush(QPalette.Background,QBrush(QPixmap(":素材\背景.花.png")))
        # self.browser.setPalette(palette)
        self.edit = QTextEdit(self)
        self.edit.setStyleSheet("background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,stop:0 #FFECEC,stop:1 #ACD6FF);border-radius:10px;position: absolute;bottom: 1vh;left: auto;right: auto;height: 10px;width: 100%;z-index: 999;border:3px solid #92B0DD;")
        self.splitter = QSplitter(self)
        self.splitter.setOrientation(Qt.Vertical)
        self.splitter.addWidget(self.browser)
        self.splitter.addWidget(self.edit)
        self.splitter.setSizes([350, 100])
    
        self.send_btn = QPushButton('Send', self)
        self.send_btn.setStyleSheet("QPushButton "
"{"
   " font-family:Microsoft Yahei;"
    "font:20px;"
    "color:white;"
    "background-color:rgb(14 , 150 , 254);"
    "border-radius:8px;"
"}"
"QPushButton:hover"
"{"
    "background-color:rgb(44 , 137 , 255);"
"}"

"QPushButton:pressed"
"{"
    "background-color:rgb(14 , 135 , 228);"
    "padding-left:3px;"
    "padding-top:3px;"
"}")
        self.close_btn = QPushButton('Close', self)
        self.close_btn.setStyleSheet("QPushButton "
"{"
   " font-family:Microsoft Yahei;"
    "font:20px;"
    "color:white;"
    "background-color:rgb(14 , 150 , 254);"
    "border-radius:8px;"
"}"
"QPushButton:hover"
"{"
    "background-color:rgb(44 , 137 , 255);"
"}"

"QPushButton:pressed"
"{"
    "background-color:rgb(14 , 135 , 228);"
    "padding-left:3px;"
    "padding-top:3px;"
"}")
        self.voice_btn = QPushButton('Voive', self)
        self.voice_btn.setStyleSheet("QPushButton "
"{"
   " font-family:Microsoft Yahei;"
    "font:20px;"
    "color:white;"
    "background-color:rgb(14 , 150 , 254);"
    "border-radius:8px;"
"}"
"QPushButton:hover"
"{"
    "background-color:rgb(44 , 137 , 255);"
"}"

"QPushButton:pressed"
"{"
    "background-color:rgb(14 , 135 , 228);"
    "padding-left:3px;"
    "padding-top:3px;"
"}")
        # self.voisend_btn = QPushButton('SendVoi',self)  终止录音并发送

        self.h_layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()

        self.layout_init()
        self.signal_init()

        # 声明Ai和User的言语，但暂时使用别的方法替代
        # self.Aispeech = ''

        # API设置
        # Baidu Speech API
        APP_ID = '24592750'
        API_KEY = 'mbgVrXAyFtDsoEXgDSKTNMLC'
        SECRET_KEY = 'Huaf52VqpkocCawALTGOMlFPPgr3G6DI'

        self.client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

        # Turing API
        self.TURING_KEY = "ef383efdf98b448f8768be238b924071"
        self.API_URL = "http://openapi.tuling123.com/openapi/api/v2"

    # 百度语音转文字
    def listen(self):
        with open('recording.wav', 'rb') as f:
            audio_data = f.read()

        result = self.client.asr(audio_data, 'wav', 16000, {
            'dev_pid': 1536,
        })

        text_input = result["result"][0]

        print("我说: " + text_input)
        style = '<p style="font-size:15px;font-family:FZShuTi;color:red">'
        p = '</p>'
        self.browser.append(f'User: {style}{text_input}{p}')
        self.Robot_think(text_input)  # 已经在此处执行了图灵处理相当于自动连接

    # 图灵处理
    def Robot_think(self, text_input):
        req = {
            "perception":
                {
                    "inputText":
                        {
                            "text": text_input
                        },

                    "selfInfo":
                        {
                            "location":
                                {
                                    "city": "青岛",
                                    "province": "山东",
                                    "street": "珠江路"
                                }
                        }
                },
            "userInfo":
                {
                    "apiKey": self.TURING_KEY,
                    "userId": "123123"
                }
        }
        # print(req)
        # 将字典格式的req编码为utf8
        req = json.dumps(req).encode('utf8')
        # print(req)

        http_post = urllib.request.Request(self.API_URL, data=req, headers={'content-type': 'application/json'})
        response = urllib.request.urlopen(http_post)
        response_str = response.read().decode('utf8')
        # print(response_str)
        response_dic = json.loads(response_str)
        # print(response_dic)

        intent_code = response_dic['intent']['code']
        results_text = response_dic['results'][0]['values']['text']
        print("AI说: " + results_text)
        # self.Aispeech = results_text
        self.browser.append('比丢: {}'.format(results_text))
        self.du_say(results_text)
        self.play_mp3('robot.mp3')

    # 文字转语音
    def du_say(self, results_text):
        # per 3是汉子 4是妹子，spd 是语速，vol 是音量
        result = self.client.synthesis(results_text, 'zh', 1, {
            'vol': 5, 'per': 4, 'spd': 4
        })
        # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
        if not isinstance(result, dict):
            with open('robot.mp3', 'wb') as f:
                f.write(result)

    # 播放Mp3文件
    def play_mp3(self, file):
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(1)
        pygame.mixer.music.stop()
        pygame.mixer.quit()

    # 信号连接初始化，具有特色的逻辑
    def signal_init(self):
        self.send_btn.clicked.connect(self.write_data_slot)
        self.close_btn.clicked.connect(self.close_slot)
        self.voice_btn.clicked.connect(self.voice_slot)
        # self.voisend_btn.clicked.connect(self.send_voice_slot)

    # 功能模块
    def close_slot(self):
        self.close()

    # def open_voice_slot(self):
    #     self.record_pushButton.setEnabled(False)
    #     self.timer.start(999)
    #     self.t_record = Thread(target=self.record)
    #     self.t_record.start()

    # 此模块一次性处理了所有语音模块的活，相当于集成。
    def voice_slot(self):
        # self.voice_btn.setEnabled(False)
        # self.voice_btn.setText('说话中')   暂时还未调试成功

        r = sr.Recognizer()  # 识别器
        with sr.Microphone(sample_rate=16000) as source:
            print("please say something")
            audio = r.listen(source)

        with open("recording.wav", "wb") as f:
            f.write(audio.get_wav_data())  # 写入文件

        self.listen()

        # self.voice_btn.setEnabled(True)

    # def send_voice_slot(self):
    #         if self.pa is None:
    #             QMessageBox.information(self, '提示', '目前没有录音', QMessageBox.Close)
    #             return
    #         else:
    #             self.pause_flag = True

    def closeEvent(self, event):
        event.accept()

    def layout_init(self):
        self.h_layout.addStretch(1)
        self.h_layout.addWidget(self.voice_btn)
        # self.h_layout.addWidget(self.voisend_btn)
        self.h_layout.addWidget(self.close_btn)
        self.h_layout.addWidget(self.send_btn)
        self.v_layout.addWidget(self.splitter)
        self.v_layout.addLayout(self.h_layout)
        self.setLayout(self.v_layout)

    def write_data_slot(self):
        self.message = self.edit.toPlainText()
        self.browser.append('User: {}'.format(self.message))
        self.Robot_think(self.message)
        self.edit.clear()
    #设置发送消息快捷键为大键盘上的ctrl + enter
    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Return:
            self.write_data_slot()


'''实现浏览器功能的类'''
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 设置窗口标题
        self.setWindowTitle('简易浏览器')
        # 设置窗口大小900*600
        self.resize(1300, 700)
        self.show()

        # 创建tabwidget（多标签页面）
        self.tabWidget = QTabWidget()
        self.tabWidget.setTabShape(QTabWidget.Triangular)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.close_Tab)
        self.setCentralWidget(self.tabWidget)

        # 第一个tab页面
        self.webview = WebEngineView(self)  # self必须要有，是将主窗口作为参数，传给浏览器
        self.webview.load(QUrl("http://www.baidu.com"))
        self.create_tab(self.webview)

        # 使用QToolBar创建导航栏，并使用QAction创建按钮
        # 添加导航栏
        navigation_bar = QToolBar('Navigation')
        # 设定图标的大小
        navigation_bar.setIconSize(QSize(16, 16))
        # 添加导航栏到窗口中
        self.addToolBar(navigation_bar)

        # QAction类提供了抽象的用户界面action，这些action可以被放置在窗口部件中
        # 添加前进、后退、停止加载和刷新的按钮
        back_button = QAction(QIcon('素材\Icon\houtui.png'), 'Back', self)
        next_button = QAction(QIcon('素材\Icon\qianjin.png'), 'Forward', self)
        stop_button = QAction(QIcon('素材\Icon\close.png'), 'stop', self)
        reload_button = QAction(QIcon('素材\Icon\shuaxin.png'), 'reload', self)

        # 绑定事件
        back_button.triggered.connect(self.webview.back)
        next_button.triggered.connect(self.webview.forward)
        stop_button.triggered.connect(self.webview.stop)
        reload_button.triggered.connect(self.webview.reload)

        # 将按钮添加到导航栏上
        navigation_bar.addAction(back_button)
        navigation_bar.addAction(next_button)
        navigation_bar.addAction(stop_button)
        navigation_bar.addAction(reload_button)

        # 添加URL地址栏
        self.urlbar = QLineEdit()
        # 让地址栏能响应回车按键信号
        self.urlbar.returnPressed.connect(self.navigate_to_url)

        navigation_bar.addSeparator()
        navigation_bar.addWidget(self.urlbar)

        # 让浏览器相应url地址的变化
        self.webview.urlChanged.connect(self.renew_urlbar)

    # 显示地址
    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == '':
            q.setScheme('http')
        self.webview.setUrl(q)

    # 响应输入的地址
    def renew_urlbar(self, q):
        # 将当前网页的链接更新到地址栏
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    # 创建tab页面
    def create_tab(self, webview):
        self.tab = QWidget()
        self.tabWidget.addTab(self.tab, "新建页面")
        self.tabWidget.setCurrentWidget(self.tab)

        # 渲染到页面
        self.Layout = QHBoxLayout(self.tab)
        self.Layout.setContentsMargins(0, 0, 0, 0)
        self.Layout.addWidget(webview)

    # 关闭tab页面
    def close_Tab(self, index):
        if self.tabWidget.count() > 1:
            self.tabWidget.removeTab(index)
        else:
            self.close()  # 当只有1个tab时，关闭主窗口


# 创建浏览器，重写重写createwindow方法实现页面连接的点击跳转
class WebEngineView(QWebEngineView):

    def __init__(self, mainwindow, parent=None):
        super(WebEngineView, self).__init__(parent)
        self.mainwindow = mainwindow

    # 重写createwindow()
    def createWindow(self, QWebEnginePage_WebWindowType):
        new_webview = WebEngineView(self.mainwindow)
        self.mainwindow.create_tab(new_webview)
        return new_webview

'''实现登录登出的气泡弹窗功能的类'''
#气泡样式
class Bubble(object):
    def setupUi(self, Dialog):
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QRect(0, 0, 151, 51))
        font = QtGui.QFont()
        font.setFamily("方正舒体")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
# 在这里设置气泡的stylesheet
        self.pushButton.setStyleSheet("background-color:rgb(250, 255, 213);\n"
"border-style:none;\n"
"padding:8px;\n"
"border-radius:25px;")

# 创建静态变量的装饰器，参考 https://www.jianshu.com/p/3ed1037b7c18
def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate
#实现气泡功能
class TipUi(QDialog):
    def __init__(self, text:str, parent=None):
# 设置气泡窗ui
        super().__init__(parent)
        self.ui = Bubble()
        self.ui.setupUi(self)
# 设置定时器，用于动态调节窗口透明度
        self.timer = QTimer()
# 设置气泡在屏幕上的位置，水平居中，垂直屏幕80%位置
        desktop = QApplication.desktop()
        self.setGeometry(QRect(int(desktop.width() / 2 - 75), int(desktop.height() * 0.8), 152, 50))
# 显示的文本
        self.ui.pushButton.setText(text)
# 设置隐藏标题栏、无边框、隐藏任务栏图标、始终置顶
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
# 设置窗口透明背景
        self.setAttribute(Qt.WA_TranslucentBackground, True)
# 窗口关闭自动退出，一定要加，否则无法退出
        self.setAttribute(Qt.WA_QuitOnClose, True)
# 用来计数的参数
        self.windosAlpha = 0
# 设置定时器25ms，1600ms记64个数
        self.timer.timeout.connect(self.hide_windows)
        self.timer.start(25)

# 槽函数
    def hide_windows(self):
        self.timer.start(25)
    # 前750ms设置透明度不变，后850ms透明度线性变化
        if self.windosAlpha <= 30:
            self.setWindowOpacity(1.0)
        else:
            self.setWindowOpacity(1.882 - 0.0294 * self.windosAlpha)
        self.windosAlpha += 1
# 差不多3秒自动退出

# 静态方法创建气泡提示
    @staticmethod
    @static_vars(tip=None)
    def show_tip(text):
        TipUi.show_tip.tip = TipUi(text)
        TipUi.show_tip.tip.show()

'''主程序窗口'''
class DemoWin(QMainWindow):
    def __init__(self):
        super(DemoWin, self).__init__()
        #预定义关于自由落体的参数
        self.desktop = QApplication.desktop()
        self.autoFalling = False
        self.initUI()

        # 初始化，不规则窗口
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)  #设置半透明背景
        self.repaint()

        #爬取天气数据并写入天气文件
        chrome_options =Options()
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=chrome_options)
        xweather = '//*[@id="sfr-app"]/div/div[2]/div/div[2]/div/div[1]/div[1]/p[1]/span[2]'
        url = "http://weathernew.pae.baidu.com/weathernew/pc?query=%E5%B1%B1%E4%B8%9C%E9%9D%92%E5%B2%9B%E5%A4%A9%E6%B0%94&srcid=4982&city_name=%E9%9D%92%E5%B2%9B&province_name=%E5%B1%B1%E4%B8%9C"
        self.driver.get(url)
        lists=self.driver.find_elements_by_xpath(xweather)
        with open("./素材/weather.txt",'w') as w:
            for each in lists:
                ht = bs(each.get_attribute('innerHTML'),'lxml')
                w.write(ht.text.replace(' ','').replace('\n','|'))

        # 是否跟随鼠标
        self.is_follow_mouse = False
        self.move(1650,20)
        #按下时出现菜单栏&喜爱值
        with open("./素材/data.txt", "r") as f:
            text = f.read()
            self.sentence = text.split("\n")

        #喜爱值框
        self.pbar.setStyleSheet('''border: 2px solid grey;background-color:red;border-radius: 10px;text-align: right;color: transparent; } QProgressBar:chunk{ background-color:white;margin:0.5px}''')
        self.pbar.setInvertedAppearance(True)
        self.doAction(self)

        # 设置托盘选项
        iconpath="./素材/托盘.png"
        eyepath="./素材/Icon/eye.png"

        #右键菜单
        quit_action = QAction(u'退出', self, triggered=self.quit)
        quit_action.setIcon(QIcon(iconpath))
        showwin = QAction(u'显示', self, triggered=self.showwin)
        showwin.setIcon(QIcon(eyepath))
        self.tray_icon_menu = QMenu(self)
        self.tray_icon_menu.addAction(showwin)
        self.tray_icon_menu.addAction(quit_action)
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(iconpath))
        self.tray_icon.setContextMenu(self.tray_icon_menu)
        self.tray_icon.show()
        #窗口透明程度
        self.setWindowOpacity(1)
        # 对话框
        QToolTip.setFont(QFont('楷体', 14))
        y = ['不要随便摸人家啦', '每次见到主人都很开心呀', '话说最近主人都没理我诶', '再摸我的话小心我生气了', '恭喜发财大吉大利']
        self.setToolTip(random.choice(y))
        # 每隔一段时间做个动作
        self.timer = QTimer()
        self.timer.timeout.connect(self.randomAct)
        self.timer.start(5000)
        self.condition = 0
        self.talk_condition=0

        # 每隔一段时间讲一句话
        self.timer1 = QTimer()
        self.timer1.timeout.connect(self.talk)
        self.timer1.start(5000)

        self.pet1 = []
        for i in os.listdir("./素材/biu"):
            self.pet1.append("./素材/biu/" + i)   #此处注意易让图片消失

        self.pet2 = []
        for k in os.listdir("./素材/Cloth0"):
            self.pet2.append("./素材/Cloth0/" + k)
        self.pet3 = []
        for j in os.listdir("./素材/Cloth1"):
            self.pet3.append("./素材/Cloth1/" + j)
        self.pet4 = []
        for l in os.listdir("./素材/Cloth2"):
            self.pet4.append("./素材/Cloth2/" + l)
        self.pet5 = []
        for o in os.listdir("./素材/Cloth3"):
            self.pet5.append("./素材/Cloth3/" + o)
        self.pet6 = []
        for p in os.listdir("./素材/Cloth4"):
            self.pet6.append("./素材/Cloth4/" + p)

        #建立可隐藏的工具栏
        self.tb = self.addToolBar("Interact")
        self.tb.setStyleSheet("border:none;")
        #隐藏工具栏
        self.tb.hide()

        # 喂食模块
        Feed = QAction(QIcon("./素材/Icon/喂食cooked.png"), "Feed", self)
        Feed.triggered.connect(self.FeedFood)
        self.tb.addAction(Feed)
        # 聊天模块
        Chat = QAction(QIcon("./素材/Icon/聊天cooked.png"), "Chat", self)
        Chat.triggered.connect(self.Have_Chat)
        self.tb.addAction(Chat)
        # 查询天气模块
        Weather = QAction(QIcon("./素材/Icon/天气cooked.png"), "Weather", self)
        Weather.triggered.connect(self.Check_Weather)
        self.tb.addAction(Weather)
        # 更衣模块
        Cloth = QAction(QIcon("./素材/Icon/更衣cooked.png"), "Cloth", self)
        Cloth.triggered.connect(self.Change_Cloth)
        self.tb.addAction(Cloth)
        
    '''浮现与隐藏模块'''
    #工具栏和的浮现
    def TShow(self):
        self.tb.show()
    #工具栏的隐藏
    def THide(self):
        self.tb.hide()
    #喜爱值的浮现与隐藏
    def LShow(self):
        self.pbar.show()
        self.emo_label.show()
    def LHide(self):
        self.pbar.hide()
        self.emo_label.hide()

    #功能模组
    def Have_Chat(self):
        if self.step > 10:
            self.step -= 5
        self.robochat = RoboWin()
        self.robochat.show()
        # self.chile_Win.exec_()

    def Check_Weather(self):
        if self.step > 10:
            self.step -= 5
        #打开爬取的天气数据的txt文件进行输出
        with open("./素材/weather.txt",'r') as we:
            texts = we.read()
            self.label1.setText(texts)

    def Change_Cloth(self):
        # 每隔一段时间做个动作
        if self.step > 10:
            self.step -= 5
        n = [self.randomAct0,self.randomAct1,self.randomAct2,self.randomAct3,self.randomAct4]
        self.timer = QTimer()
        m = random.choice(n)
        self.timer.timeout.connect(m)
        self.timer.start(5000)
        self.condition = 0
        self.talk_condition=0

    def initUI(self):
        # 将窗口设置为动图大小  label1:文字冒泡，label：动画
        self.resize(600, 600)
        self.label1 = QLabel("", self)
        self.label1.setStyleSheet("font:15pt '楷体';border-width: 1px;color:blue;")  # 设置边框
        self.label1.move(0,50)
        # 使用label来显示动画
        self.label = QLabel("", self)
        self.label.move(100,100)
        # label大小设置为动画大小
        self.label.setFixedSize(200, 200)    #gif尺寸
        self.label2 = QLabel("", self)
        self.label2.setFixedSize(250,250)
        self.label2.move(67,-35)
        self.label.move(100,100)
        self.label1.raise_()
        # 设置动画路径
        self.movie = QMovie("./素材/biu/biu12.gif")
        #宠物大小
        self.movie.setScaledSize(QSize(200, 200))
        # 将动画添加到label中
        self.label.setMovie(self.movie)
        # 开始播放动画
        self.movie.start()
        #透明窗口
        #self.setWindowOpacity(1)
        # 添加窗口标题
        self.setWindowTitle("GIFDemo")

        #喜爱值模块   emo_label:表情放置区
        self.pix1 = QPixmap('./素材\emoji\emoji1.png')
        self.pix2 = QPixmap('./素材\emoji\emoji2.png')
        self.pix3 = QPixmap('./素材\emoji\emoji3.png')
        self.pix4 = QPixmap('./素材\emoji\emoji4.png')
        self.pix6 = QPixmap('./素材\emoji\emoji6.png')
        self.pix7= QPixmap('./素材\emoji\emoji17png')
        self.pbar = QProgressBar(self)
        self.pbar.setRange(0, 100)
        #self.pbar.setGeometry(100, 500, 200, 25)
        self.pbar.move(100, 300)
        self.pbar.resize(180,20)
        self.timer3 = QBasicTimer()
        self.step = 0
        self.emo_label = QLabel(self)
        self.emo_label.setFixedSize(50, 50)
        self.emo_label.setScaledContents(True)  #自适应窗口大小
        self.emo_label.move(50, 290)
        self.LHide()

    '''喜爱值相关配件'''
    def timerEvent(self, value):
        if self.step >= 1000:
            self.timer3.stop()
            return
        if self.step <= 25:
            self.emo_label.setPixmap(self.pix1)
        elif self.step <= 50:
            self.emo_label.setPixmap(self.pix4)
        elif self.step <= 60:
            self.emo_label.setPixmap(self.pix7)
        elif self.step <= 75:
            self.emo_label.setPixmap(self.pix3)
        elif self.step <= 90:
            self.emo_label.setPixmap(self.pix2)
        elif self.step <= 99:
            self.emo_label.setPixmap(self.pix6)
        self.step = self.step + 0.1
        self.pbar.setValue(self.step)
        time.sleep(0.1)

    def doAction(self, value):
        if self.timer3.isActive():
            self.timer3.stop()
        else:
            self.timer3.start(1000, self)

    def FeedFood(self, value):
        if self.step > 10:
            self.step -= 5
        self.movie = QMovie("./素材/biu/biu3.gif")
        #宠物大小
        self.movie.setScaledSize(QSize(200, 200))
        # 将动画添加到label中
        self.label.setMovie(self.movie)
        # 开始播放动画
        self.movie.start()
    def Change_emo(self, value):
        if self.step <= 50:
            self.emo_label.setPixmap(self.pix)
        elif self.step > 50:
            self.emo_label.setPixmap(self.pix2)

    '''自由落体功能实现'''
    def fallingBody(self, posX, posY):
        """宠物自由落体, posX, posY 是起始的位置"""
        rect = self.desktop.availableGeometry()
        while self.pos().y() < rect.height() - 290:
            self.move(posX, posY)
            QApplication.processEvents()
            time.sleep(0.01)
            posY += 10

    '''窗口跟随鼠标功能实现'''
    #鼠标左键按下时, 宠物将和鼠标位置绑定
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_follow_mouse = True
            self.mouse_drag_pos = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))
            self.movie = QMovie("./素材/biu/biu10.gif")
            # 宠物大小
            self.movie.setScaledSize(QSize(200, 200))
            # 将动画添加到label中
            self.label.setMovie(self.movie)
            # 开始播放动画
            self.movie.start()
    #鼠标移动, 则宠物也移动
    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.is_follow_mouse:
            self.move(event.globalPos() - self.mouse_drag_pos)
            event.accept()
    #鼠标释放时, 取消绑定
    def mouseReleaseEvent(self, event):
        self.is_follow_mouse = False
        self.setCursor(QCursor(Qt.ArrowCursor))
        #释放时实现自由落体功能
        if self.autoFalling == True:
            self.fallingBody(event.globalPos().x(), event.globalPos().y())

    def enterEvent(self, event):  # 鼠标移进时调用
        #print('鼠标移入')
        self.setCursor(Qt.ClosedHandCursor)
        self.TShow() 
        self.LShow() # 设置鼠标形状。需要from PyQt5.QtGui import QCursor,from PyQt5.QtCore import Qt
        '''
        各种鼠标样式类型
        Qt.PointingHandCursor   指向手            Qt.WaitCursor  旋转的圆圈
        ArrowCursor   正常箭头                 Qt.ForbiddenCursor 红色禁止圈
        Qt.BusyCursor      箭头+旋转的圈      Qt.WhatsThisCursor   箭头+问号
        Qt.CrossCursor      十字              Qt.SizeAllCursor    箭头十字
        Qt.UpArrowCursor 向上的箭头            Qt.SizeBDiagCursor  斜向上双箭头
        Qt.IBeamCursor   I形状                 Qt.SizeFDiagCursor  斜向下双箭头
        Qt.SizeHorCursor  水平双向箭头          Qt.SizeVerCursor  竖直双向箭头
        Qt.SplitHCursor                        Qt.SplitVCursor  
        Qt.ClosedHandCursor   非指向手          Qt.OpenHandCursor  展开手
        '''
        # self.unsetCursor()   #取消设置的鼠标形状

    #鼠标离开时延迟十秒后触发隐藏功能
    def leaveEvent(self,event):
        self.TShow() 
        self.LShow() 
        self.timer2 = QTimer()
        self.timer2.singleShot(10000,self.THide)  # 10秒后触发
        self.timer2.singleShot(10000,self.LHide)  

    '''实现一键截屏的组件'''
    def Shotscreen(self,filename):
        hwnd = 0  # 窗口的编号，0号表示当前活跃窗口
        # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
        hwndDC = win32gui.GetWindowDC(hwnd)
        # 根据窗口的DC获取mfcDC
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        # mfcDC创建可兼容的DC
        saveDC = mfcDC.CreateCompatibleDC()
        # 创建bigmap准备保存图片
        saveBitMap = win32ui.CreateBitmap()
        # 获取监控器信息
        MoniterDev = win32api.EnumDisplayMonitors(None, None)
        w = MoniterDev[0][2][2]
        h = MoniterDev[0][2][3]
        # print w,h　　　#图片大小
        # 为bitmap开辟空间
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
        # 高度saveDC，将截图保存到saveBitmap中
        saveDC.SelectObject(saveBitMap)
        # 截取从左上角（0，0）长宽为（w，h）的图片
        saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
        saveBitMap.SaveBitmapFile(saveDC, filename)

    '''一键锁屏功能组件'''
    def closefun(self):
        HWND_BROADCAST = 0xffff
        WM_SYSCOMMAND = 0x0112
        SC_MONITORPOWER = 0xF170
        MonitorPowerOff = 2
        SW_SHOW = 5
        windll.user32.PostMessageW(HWND_BROADCAST, WM_SYSCOMMAND,
                               SC_MONITORPOWER, MonitorPowerOff)

        shell32 = windll.LoadLibrary("shell32.dll")
        shell32.ShellExecuteW(None,'open', 'rundll32.exe',
                            'USER32,LockWorkStation','',SW_SHOW)
    def contextMenuEvent(self, event):
        netpath = r"素材\Icon\net.png"
        exitpath = "素材\Icon\shutdown.png"
        hidepath = "素材\Icon\隐藏.png"
        suopath = "素材\Icon\锁屏.png"
        shotpath = "素材\Icon\截图.png"
        fallpath = r"素材\Icon\fall.png"
        menu = QMenu(self)
        search = QAction(QIcon(netpath),'浏览器',menu)
        search.triggered.connect(self.searchaction)
        shotscreen = QAction(QIcon(shotpath),'一键截屏',menu)
        shotscreen.triggered.connect(self.shotscreenaction)
        close = QAction(QIcon(suopath),'一键锁屏',menu)
        close.triggered.connect(self.closeaction)
        fall = QAction(QIcon(fallpath),"关闭自由落体" if self.autoFalling else "开启自由落体",menu)
        fall.triggered.connect(self.fallaction)
        hide = QAction(QIcon(hidepath),'隐藏',menu)
        hide.triggered.connect(self.hideaction)
        quitAction = QAction(QIcon(exitpath),'退出',menu)
        quitAction.triggered.connect(self.quitaction)
        menu.addAction(search)
        menu.addAction(shotscreen)
        menu.addAction(close)
        menu.addAction(fall)
        menu.addAction(hide)
        menu.addAction(quitAction)
        menu.exec_(self.mapToGlobal(event.pos()))
    def fallaction(self):
        self.autoFalling = 1-self.autoFalling
    def quitaction(self):
        TipUi.show_tip('退出成功')
        self.timer3 = QTimer()
        self.timer3.singleShot(1600,qApp.quit) 
    def hideaction(self):
        TipUi.show_tip('隐藏成功')
        self.setWindowOpacity(0)
    #启动浏览器控件
    def searchaction(self):
        browser = MainWindow()
        browser.show()
    def closeaction(self):
        self.closefun()
    def shotscreenaction(self):
        self.Shotscreen('jieping.jpg')
    '''退出程序'''
    def quit(self):
        self.close()
        sys.exit()

    '''显示'''
    def showwin(self):
        TipUi.show_tip('欢迎回来')
        self.setWindowOpacity(1)

    '''动作库'''
    def randomAct0(self):
        if not self.condition:
            # print("状态变更")
            # print(random.choice(self.pet1))
            self.movie = QMovie(random.choice(self.pet2))
            # 宠物大小
            self.movie.setScaledSize(QSize(200, 200))
            # 将动画添加到label中
            self.label.setMovie(self.movie)
            # 开始播放动画
            self.movie.start()
            self.condition=1
        else:
            # print("状态还原")
            # 设置动画路径
            self.movie = QMovie("素材\Cloth0\Cloth14cooked.gif")
            # 宠物大小
            self.movie.setScaledSize(QSize(200, 200))
            # 将动画添加到label中
            self.label.setMovie(self.movie)
            # 开始播放动画
            self.movie.start()
            self.condition=0
    def randomAct1(self):
        if not self.condition:
            # print("状态变更")
            # print(random.choice(self.pet1))
            self.movie = QMovie(random.choice(self.pet3))
            # 宠物大小
            self.movie.setScaledSize(QSize(200, 200))
            # 将动画添加到label中
            self.label.setMovie(self.movie)
            # 开始播放动画
            self.movie.start()
            self.condition=1
        else:
            # print("状态还原")
            # 设置动画路径
            self.movie = QMovie("素材\Cloth1\Cloth10cooked.gif")
            # 宠物大小
            self.movie.setScaledSize(QSize(200, 200))
            # 将动画添加到label中
            self.label.setMovie(self.movie)
            # 开始播放动画
            self.movie.start()
            self.condition=0
    def randomAct2(self):
        if not self.condition:
            # print("状态变更")
            # print(random.choice(self.pet1))
            self.movie = QMovie(random.choice(self.pet4))
            # 宠物大小
            self.movie.setScaledSize(QSize(200, 200))
            # 将动画添加到label中
            self.label.setMovie(self.movie)
            # 开始播放动画
            self.movie.start()
            self.condition=1
        else:
            # print("状态还原")
            # 设置动画路径
            self.movie = QMovie("素材\Cloth2\Cloth9cooked.gif")
            # 宠物大小
            self.movie.setScaledSize(QSize(200, 200))
            # 将动画添加到label中
            self.label.setMovie(self.movie)
            # 开始播放动画
            self.movie.start()
            self.condition=0
    def randomAct3(self):
        if not self.condition:
            # print("状态变更")
            # print(random.choice(self.pet1))
            self.movie = QMovie(random.choice(self.pet5))
            # 宠物大小
            self.movie.setScaledSize(QSize(200, 200))
            # 将动画添加到label中
            self.label.setMovie(self.movie)
            # 开始播放动画
            self.movie.start()
            self.condition=1
        else:
            # print("状态还原")
            # 设置动画路径
            self.movie = QMovie("素材\Cloth3\Cloth3cooked.gif")
            # 宠物大小
            self.movie.setScaledSize(QSize(200, 200))
            # 将动画添加到label中
            self.label.setMovie(self.movie)
            # 开始播放动画
            self.movie.start()
            self.condition=0
    def randomAct4(self):
        if not self.condition:
            # print("状态变更")
            # print(random.choice(self.pet1))
            self.movie = QMovie(random.choice(self.pet6))
            # 宠物大小
            self.movie.setScaledSize(QSize(200, 200))
            # 将动画添加到label中
            self.label.setMovie(self.movie)
            # 开始播放动画
            self.movie.start()
            self.condition=1
        else:
            # print("状态还原")
            # 设置动画路径
            self.movie = QMovie("素材\Cloth4\Cloth2cooked.gif")
            # 宠物大小
            self.movie.setScaledSize(QSize(200, 200))
            # 将动画添加到label中
            self.label.setMovie(self.movie)
            # 开始播放动画
            self.movie.start()
            self.condition=0

    '''随机做一个动作'''
    def randomAct(self):
        if not self.condition:
            # print("状态变更")
            # print(random.choice(self.pet1))
            self.movie = QMovie(random.choice(self.pet1))
            # 宠物大小
            self.movie.setScaledSize(QSize(200, 200))
            # 将动画添加到label中
            self.label.setMovie(self.movie)
            # 开始播放动画
            self.movie.start()
            self.condition=1
        else:
            # print("状态还原")
            # 设置动画路径
            self.movie = QMovie("./素材/biu/biu12.gif")
            # 宠物大小
            self.movie.setScaledSize(QSize(200, 200))
            # 将动画添加到label中
            self.label.setMovie(self.movie)
            # 开始播放动画
            self.movie.start()
            self.condition=0

    def talk(self):
        time = QDateTime.currentDateTime()
            # 设置系统时间显示格式
        timeDisplay = time.toString("hh:mm ")
        if not self.talk_condition:
            self.label2.setStyleSheet("border-image:url(./素材/Icon/气泡_cooked2.png)")
            self.label1.setText(random.choice(self.sentence))
            if timeDisplay=="06:00 ":
                self.label1.setText("早上好")
            if timeDisplay=="12:00 ":
                self.label1.setText("中午好")
            if timeDisplay=="18:00 ":
                self.label1.setText("晚上好")
            self.label1.setWordWrap(True)
            self.label1.setStyleSheet("font: bold;font:12pt '方正舒体';color:black;background-color:transparent")  # 设置边框
            self.label1.move(90,60)
            self.label1.adjustSize()
            self.talk_condition=1
        else:
            self.label1.setText("")
            self.label2.setText("")
            self.label2.setStyleSheet("")
            self.label1.adjustSize()
            self.talk_condition = 0



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("素材\托盘.png"))
    # 创建一个主窗口
    mainWin = DemoWin()
    # 显示
    mainWin.show()
    # 主循环
    TipUi.show_tip('欢迎回来')
    sys.exit(app.exec_())