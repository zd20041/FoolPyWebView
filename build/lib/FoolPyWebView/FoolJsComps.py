# 提供一些快捷的 js 注入方法


# 返回cookie
def getCookie():
    return """
    (function() {
        var cookie = document.cookie;
        var cookieArr = cookie.split("; ");
        var cookieObj = {};
        for (var i = 0; i < cookieArr.length; i++) {
            var cookieItem = cookieArr[i].split("=");
            cookieObj[cookieItem[0]] = cookieItem[1];
        }
        return cookieObj;
    })();
        """


# 插入按钮 点击触发回调
def insertButton(text, insertButton_res):
    return """
    (function() {
        var btn = document.createElement("button");
        btn.innerHTML = "%s";
        btn.style.position = "fixed";
        btn.style.top = "50px";
        btn.style.left = "50px";
        btn.style.zIndex = "999999";
        btn.style.width = "100px";
        btn.style.height = "50px";
        btn.style.backgroundColor = "#fff";
        btn.style.border = "1px solid #000";
        btn.style.borderRadius = "5px";
        btn.onclick = function() {
            window.py_fn.%s(document.cookie);
        }
        document.body.appendChild(btn);
    })();
        """ % (text, insertButton_res)