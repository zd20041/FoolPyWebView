import os
import sys
import json
from PyQt5.QtCore import QUrl, Qt, pyqtSlot, QObject
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton, QWidget, QHBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel



# 回调方法
callback = {
    "dragFileCallback": None
}



class Backend(QObject):
    def __init__(self, view, py_api=None):
        super(Backend, self).__init__()
        self.view = view
        self.py_api = None
        if py_api:
            self.py_api = py_api()
        


    @pyqtSlot(str, result=str)
    def handle(self, value):
        try:
            json_data = json.loads(value)
            method = json_data["method"]
            args = json_data["args"]
            res = getattr(self.py_api, method)(*args)
            typeres = type(res).__name__
            return json.dumps({"type": str(typeres), "value": res})
        except Exception as e:
            print(e)
            return json.dumps({"type": "str", "value": str(e)})

    @pyqtSlot(str)
    def moveWindow(self, str_xy):
        x, y = str_xy.split("&")
        tx = self.view.parent().pos().x()
        ty = self.view.parent().pos().y()
        self.view.parent().move(tx + int(x), ty + int(y))


    


class WebEngineView(QWebEngineView):
    def __init__(self, *args, **kwargs):
        super(WebEngineView, self).__init__(*args, **kwargs)
        self.setAcceptDrops(True)
        self.page().setBackgroundColor(QColor(Qt.GlobalColor.transparent))

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if callback["dragFileCallback"]:
                    callback["dragFileCallback"](url.toLocalFile())
            event.acceptProposedAction()
        else:
            super().dropEvent(event)


class MainWindow(QMainWindow):
    def __init__(self, load=None, window_propers=None):
        super(MainWindow, self).__init__()
        self.browser = WebEngineView()
        if "http" in load:
            self.browser.setUrl(QUrl(load))
        else:
            load = os.path.abspath(load)
            self.browser.load(QUrl.fromLocalFile(load))

        # 背景颜色
        if not window_propers["background_color"]:
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        else:
            self.setStyleSheet(f"background-color: {window_propers['background_color']};")

        # 窗口置顶
        if window_propers["on_top"]:
            self.setWindowFlag(Qt.WindowStaysOnTopHint)


        # # 无边框
        if window_propers["noborder"]:
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # 设置标题
        self.setWindowTitle(window_propers["title"])

        # 设置宽高
        self.resize(window_propers["width"], window_propers["height"])

        # 设置图标
        if window_propers["icon"]:
            self.setWindowIcon(QIcon(window_propers["icon"]))

        # 允许调整窗口大小
        self.setMouseTracking(window_propers["resizable"])


        self.backend = Backend(self.browser, py_api=window_propers["py_api"])
        self.channel = QWebChannel()
        self.channel.registerObject('backend', self.backend)
        self.browser.page().setWebChannel(self.channel)

        self.setCentralWidget(self.browser)

        self.browser.loadFinished.connect(self.init) # 加载完成事件



    def create_py_api(self):
        if not self.backend.py_api:
            return
        # 注入js文件
        with open("FoolCom.js", "r", encoding="utf-8") as f:
            js = f.read()
            self.browser.page().runJavaScript(js)
        # 获取py_api的所有方法
        py_api_methods = [method for method in dir(self.backend.py_api) if not method.startswith("__")]

        # 执行js代码
        self.browser.page().runJavaScript(f"window.add_pyfn("+str(py_api_methods)+")")

    def init(self):
        self.create_py_api()
        self.show()

    
class JsResultHolder:
    def __init__(self):
        self.result = None

    def set_result(self, result):
        self.result = result

    


class FoolWebView:
    def __init__(self, title="Fool Web View", load=None, width=1200, height=650, background_color = "#ffffff", noborder=False, resizable=True,on_top=False ,icon=None, py_api=None):
        self.app = QApplication(sys.argv)
        self.py_api = py_api # py_api
        os.environ["QTWEBENGINE_REMOTE_DEBUGGING"] = "9222"
        # 默认window样式
        self.window_propers = {
            "title": title,
            "load": load,
            "width": width,
            "height": height,
            "background_color": background_color,
            "icon": icon,
            "noborder": noborder, # 无边框
            "resizable": resizable, # 允许调整窗口大小
            "on_top": on_top, # 窗口置顶
            "py_api": py_api,
        }

        self.windows = []
        self.window = MainWindow(load=load, window_propers=self.window_propers)
        self.windows.append(self.window)


    
    def setDragFileFn(self, fn): # 设置文件拖入回调函数
        global callback
        callback["dragFileCallback"] = fn

    def create_window(self, load=None, window_propers=None):
        if window_propers:
            tmp_window_propers = self.window_propers.copy()
            tmp_window_propers.update(window_propers)
        else:
            tmp_window_propers = self.window_propers

        window = MainWindow(load = load, window_propers = tmp_window_propers)
        self.windows.append(window)

    




    # 执行js方法
    def exec_js_fn(self, fn, args, window=0, callback=None):
        # self.windows[window].browser.page().runJavaScript(f"window.{fn}({js_params})",callback)
        def callback_self(result):
            json_data = json.loads(result)['data']
            if callback:
                callback(json_data)

        tmp = {
            "method": fn,
            "args": args
        }
        self.windows[window].browser.page().runJavaScript(f"window.py_call_js({json.dumps(tmp)})", callback_self)



    
    def start(self, debug=False):
        if debug:
            self.create_window(load="http://127.0.0.1:9222", window_propers={"title": "Fool Web View Debugger", "width": 700, "height": 500, "background_color": "#ffffff", "noborder": False, "resizable": True, "icon": None, "py_api": None, "on_top": True})

        sys.exit(self.app.exec())



