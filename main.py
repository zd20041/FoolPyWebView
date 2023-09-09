from modules.FoolWebView import FoolWebView

class jsAPi():
    def __init__(self) -> None:
        pass

    def message(self, message, intstr):
        print("test",message, intstr)
        return "123"

    
if __name__ == "__main__":
    fool_web_view = FoolWebView(title="窗口标题", width=1200, height=650, icon="1.png", js_api=jsAPi)
    fool_web_view.start(debug=True)