import os
import sys
import json
from PyQt5.QtCore import QUrl, Qt, pyqtSlot, QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5.QtWebChannel import QWebChannel
import socket
import random


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
    def test(self, value):
        print(value)
        return "test"
    

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




def check_port(port, host='localhost'):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
            return False
        except socket.error as e:
            return True



class CreatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.webview = QWebEngineView(self)
        self.setCentralWidget(self.webview)

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

    
    def runJavaScript(self, js, callback=None):
        """
        没有返回数据处理
        """
        self.webview.page().runJavaScript(js, callback) if callback else self.webview.page().runJavaScript(js)

    def runJavaScriptFunc(self, func, args_list, callback=None):
        """
        调用方法 有返回数据处理 转化为python数据
        """
        def callback_self(result):
            json_data = json.loads(result)['data']
            if callback:
                callback(json_data)
        tmp = {
            "method": func,
            "args": args_list
        }
        js = f"window.py_call_js({json.dumps(tmp)})"
        self.runJavaScript(js, callback_self)


class FoolWebView:
    def __init__(self, window_propers=None):
        self.app = QApplication(sys.argv)
        self.windows = []
        # 默认window样式
        self.window_propers = {
            "title": "FoolWebView",
            "width": 1200,
            "height": 650,
            "background_color": "#ffffff", 
            "icon": None, # 图标
            "noborder": False, # 无边框
            "resizable": True, # 允许调整窗口大小
            "on_top": False, # 窗口置顶
            "py_api": None,
            "init_fn": None, # 初始化函数 当webview一切准备就绪后执行
            "drag_file_callback": None, # 文件拖入回调函数
            "debug": False,
            "memory": False # webview是否保存历史记录 本地存储 cookie等
        }
        if window_propers:
            self.window_propers.update(window_propers)


    def create_window(self, load, window_propers=None):
        window = CreatWindow()

        # 加载页面
        if "http" in load:
            window.webview.load(QUrl(load))
        else:
            window.webview.load(QUrl.fromLocalFile(load))

        # 设置窗口属性
        if window_propers:
            tmp_window_propers = self.window_propers.copy()
            tmp_window_propers.update(window_propers)
        else:
            tmp_window_propers = self.window_propers

        # 设置webview是否保存历史记录 本地存储 cookie等
        if not tmp_window_propers["memory"]:
            profile = QWebEngineProfile.defaultProfile()
            profile.setPersistentCookiesPolicy(QWebEngineProfile.NoPersistentCookies) # 清除cookie
            profile.setHttpCacheType(QWebEngineProfile.NoCache) # 清除缓存
            profile.setPersistentStoragePath("") # 清除本地存储
            profile.setCachePath("") # 清除缓存
            # 清除cookie
            profile.cookieStore().deleteAllCookies()
            # 清除本地存储
            profile.clearAllVisitedLinks()
        else:
            pass

            

        # 设置文件拖入回调函数
        if tmp_window_propers["drag_file_callback"]:
            callback["dragFileCallback"] = tmp_window_propers["drag_file_callback"]

        # 设置标题
        window.setWindowTitle(tmp_window_propers["title"])

        # 设置窗口大小
        window.resize(tmp_window_propers["width"], tmp_window_propers["height"])

        # 设置窗口图标
        if tmp_window_propers["icon"]:
            window.setWindowIcon(QIcon(tmp_window_propers["icon"]))

        # 设置窗口背景颜色
        window.setStyleSheet("background-color: %s;" % tmp_window_propers["background_color"])

        # 设置窗口无边框
        if tmp_window_propers["noborder"]:
            window.setWindowFlags(Qt.FramelessWindowHint)

        # 设置窗口可调整大小
        if not tmp_window_propers["resizable"]:
            window.setFixedSize(tmp_window_propers["width"], tmp_window_propers["height"])

        # 设置窗口置顶
        if tmp_window_propers["on_top"]:
            window.setWindowFlags(Qt.WindowStaysOnTopHint)

        # 设置窗口调试模式
        if tmp_window_propers["debug"]:
            # 生成端口 从9222开始
            port = random.randint(9222, 9999)
            # 查看端口是否被占用
            while check_port(port):
                port = random.randint(9222, 9999)
            # 设置调试模式
            os.environ["QTWEBENGINE_REMOTE_DEBUGGING"] = str(port)

        # 设置窗口py_api
        if tmp_window_propers["py_api"]:
            channel = QWebChannel(window.webview.page())
            backend = Backend(window.webview, tmp_window_propers["py_api"])
            channel.registerObject('backend', backend)
            window.webview.page().setWebChannel(channel)

        def init_window():
            inject_success = 0

            def inject_success_signal(result):
                nonlocal inject_success
                inject_success += 1
                if inject_success == 3:
                    # 到此位置 window已经初始化完毕 这里可以执行一些初始化操作
                    if tmp_window_propers["init_fn"]:
                        tmp_window_propers["init_fn"](window)

            # 注入js qwebchannel.js
            if tmp_window_propers["py_api"]:
                current_path = os.path.dirname(os.path.abspath(__file__))
                qwebchannel_js = os.path.join(current_path, "qwebchannel.js")
                with open(qwebchannel_js, "r", encoding="utf-8") as f:
                    js = f.read()
                    window.webview.page().runJavaScript(js, inject_success_signal)
                # 注入js FoolCom.js
                foolcom_js = os.path.join(current_path, "FoolCom.js")
                with open(foolcom_js, "r", encoding="utf-8") as f:
                    js = f.read()
                    window.webview.page().runJavaScript(js, inject_success_signal)
                # 获取py_api的所有方法
                py_api_methods = [method for method in dir(tmp_window_propers["py_api"]) if not method.startswith("__")]
                # 执行js代码
                window.webview.page().runJavaScript(f"window.add_pyfn("+str(py_api_methods)+")", inject_success_signal)
                
            window.show()


        # 加载完成后执行
        window.webview.loadFinished.connect(lambda: init_window())

        self.windows.append(window)

        if len(self.windows) == 1:
            sys.exit(self.app.exec())

    

