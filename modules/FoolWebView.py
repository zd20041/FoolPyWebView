from PyQt5.QtCore import QObject, QUrl, Qt, QPoint,QSize, pyqtSlot
from PyQt5.QtGui import QMouseEvent, QColor,QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QLabel, QPushButton, QWidget, QHBoxLayout
import sys
import os
import json



class Backend(QObject):
    def __init__(self, view, js_api=None):
        super(Backend, self).__init__()
        self.view = view
        self.js_api = js_api()


    @pyqtSlot(str, result=str)
    def handle(self, value):
        try:
            json_data = json.loads(value)
            method = json_data["method"]
            args = json_data["args"]
            res = getattr(self.js_api, method)(*args)
            typeres = type(res).__name__
            return json.dumps({"type": str(typeres), "value": res})
        except Exception as e:
            print(e)
            return json.dumps({"type": "str", "value": str(e)})



# 格式转化器
def FormatConverter(type, value):
    if type == "int":
        return int(value)
    elif type == "float":
        return float(value)
    elif type == "bool":
        return bool(value)
    elif type == "str":
        return str(value)
    elif type == "list":
        return list(value)
    elif type == "dict":
        return dict(value)
    else:
        return value
    




class TitleBarButton(QPushButton):
    def __init__(self, text, color):
        super(TitleBarButton, self).__init__()
        self.setText(text)
        self.setFixedSize(QSize(35, 35))
        self.setStyleSheet(f"""
            QPushButton {{
                font-size: 20px;
                color: white;
                border-top-right-radius: 5px;
                border-top-left-radius: 0px; 
            }}
            QPushButton:hover {{
                background-color: {color};
            }}
        """)

class TitleBar(QWidget):
    def __init__(self, parent=None):
        super(TitleBar, self).__init__(parent)
        self.moving = False
        self.offset = QPoint()
        self.setFixedHeight(35)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
            background-color: #333; 
            color: white; 
            padding: 5px; 
            border-top-left-radius: 5px; 
            border-top-right-radius: 5px;
        """)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.title_label = QLabel()
        self.title_label.setText(parent.windowTitle())
        layout.addWidget(self.title_label)
        
        self.minimize_button = TitleBarButton("-", "#666666")
        self.minimize_button.clicked.connect(parent.showMinimized)
        layout.addWidget(self.minimize_button)

        self.close_button = TitleBarButton("×", "red")
        self.close_button.clicked.connect(parent.close)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.moving = True
            self.offset = event.globalPos() - self.parent().pos()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.moving and event.buttons() == Qt.LeftButton:
            self.parent().move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.moving = False


class WebView(QWebEngineView):
    def __init__(self, parent=None):
        super(WebView, self).__init__(parent)
        profile = QWebEngineProfile.defaultProfile()
        page = QWebEnginePage(profile, self)
        page.setBackgroundColor(QColor(Qt.transparent))
        self.setPage(page)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                print(url.toLocalFile())


class FoolWebView:
    def __init__(self, title="Fool Web View", width=1200, height=650, icon=None, js_api=None):
        self.app = QApplication(sys.argv)
        os.environ["QTWEBENGINE_REMOTE_DEBUGGING"] = "9222"

        self.main_widget = QWidget()
        self.main_widget.setWindowFlags(Qt.FramelessWindowHint)
        self.main_widget.setAttribute(Qt.WA_TranslucentBackground, True)
        self.main_widget.resize(width, height)
        self.main_widget.setWindowTitle(title)
        # 允许调整窗口大小
        self.main_widget.setMouseTracking(True)

        if icon:
            self.main_widget.setWindowIcon(QIcon(icon))

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.title_bar = TitleBar(self.main_widget)
        layout.addWidget(self.title_bar)

        self.view = WebView()

        self.backend = Backend(self.view, js_api)
        self.channel = QWebChannel()
        self.channel.registerObject('backend', self.backend)
        self.view.page().setWebChannel(self.channel)


        layout.addWidget(self.view)
        self.main_widget.setLayout(layout)

        # self.view.load(QUrl.fromLocalFile("/index.html")) http://127.0.0.1:5500/index.html
        self.view.load(QUrl("http://127.0.0.1:5500/index.html"))
        self.view.loadFinished.connect(self.init) 

    def create_js_api(self):
        # 注入js文件
        with open("FoolCom.js", "r", encoding="utf-8") as f:
            js = f.read()
            self.view.page().runJavaScript(js)

        # 获取js_api的所有方法
        js_api_methods = [method for method in dir(self.backend.js_api) if not method.startswith("__")]
        # print(js_api_methods)
        # 执行js代码
        self.view.page().runJavaScript(f"window.add_pyfn("+str(js_api_methods)+")")


    def init(self):
        self.create_js_api()
        self.main_widget.show()


        

    def start(self, debug=False):
        if debug:
            # 创建一个webview窗口 加载http://127.0.0.1:9222
            self.debugger = WebView()
            self.debugger.resize(700, 500)
            self.debugger.setWindowTitle("Fool Web View Debugger")
            self.debugger.load(QUrl("http://127.0.0.1:9222"))
            # 窗口置顶
            self.debugger.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.debugger.show()
            
        sys.exit(self.app.exec_())

        

