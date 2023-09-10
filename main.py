from FoolPyWebView.FoolPyWebView import FoolWebView
from FoolPyWebView.FoolJsComps import getCookie, insertButton

class pyAPi():
    def __init__(self) -> None:
        pass

    def message(self, message, intstr):
        print("msg",message, intstr)
        return "msg"

    def insertButton_res(self, cookie):
        print("点击按钮>cookie>", cookie)


def init_fn(window):
    # 执行js
    window.runJavaScript("alert(document.title); window.py_fn.message('hello', 1); function test(a, b, c) { return a + b + c; }")

    # 执行js方法
    window.runJavaScriptFunc("test", [1, 2, 3], callback=lambda x: print("返回值>", x))

    # 获取cookie 快捷注入
    window.runJavaScript(getCookie(), callback=lambda x: print("cookie>", x))

    # 插入获取cookie按钮
    window.runJavaScript(insertButton("获取cookie", "insertButton_res"))


if __name__ == '__main__':
    webview = FoolWebView()
    webview.create_window(load="https://www.bilibili.com", window_propers={"title": "百度一下", "py_api": pyAPi, "init_fn": init_fn, "memory": True})