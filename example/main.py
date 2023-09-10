# import FoolPyWebView 
from FoolPyWebView import FoolWebView



def js_callback(result):
    print(type(result))
    print("js_callback", result)


class pyAPi():
    def __init__(self) -> None:
        pass


    def message(self, message, intstr):
        print("msg",message, intstr)
        return "msg"
    

    def run_js_fn(self):
        fool_web_view.exec_js_fn(fn="test_pyfn",args=["123"], callback=js_callback)
    

    def addWindow(self):
        t_window_propers = {
            "title": "Fool Web View",
        }
        # 添加窗口
        fool_web_view.create_window(load="index.html", window_propers= t_window_propers)
        return "123"
    



# 文件拖入回调函数
def dragFileFn(path):
    print(path)


if __name__ == '__main__':
    fool_web_view = FoolWebView(title="窗口标题", load="index.html",background_color=None ,width=1200, height=650, icon="1.png", py_api=pyAPi)
    fool_web_view.setDragFileFn(dragFileFn) # 设置文件拖入回调函数
    fool_web_view.start(debug=True)