
// ---------------------------------- js注册py通信 ---------------------------------------
new QWebChannel(qt.webChannelTransport, function (channel) {
    window.backend = channel.objects.backend;
});
// ---------------------------------------------------------------------------------------------

// ---------------------------------- 处理py的返回结果类型 ---------------------------------------
const handle_reply = function (reply) {
    let json_reply = JSON.parse(reply);;
    let type_ = json_reply["type"];
    let value = json_reply["value"];
    return value;
}
// ---------------------------------------------------------------------------------------------

// ---------------------------------- 映射py方法到js ---------------------------------------
const py_fn = {}

const add_pyfn = function (fn_name_list) {
    for (let fn_name of fn_name_list) {
        py_fn[fn_name] = function (...args) {
            return new Promise(function (resolve, reject) {
                window.backend.handle(JSON.stringify({ "method": fn_name, "args": args }), function (reply) {
                    resolve(handle_reply(reply));
                });
            }.bind(this));
        }
    }
}
window.add_pyfn = add_pyfn; // 暴露给外部使用 添加python的方法
window.py_fn = py_fn;
// -------------------------------------------------------------------------------------------------------------

// py调用js方法
const py_call_js = function (json_data) {
    return JSON.stringify({data: window[json_data["method"]](...json_data["args"])});
}

window.py_call_js = py_call_js;

// ---------------------------------- 添加nav拖拽 ---------------------------------------
const add_drag = (name) => {
    let drag = document.querySelectorAll(name);
    if (drag.length == 0) {
        console.log("drag is null");
        return;
    }
    for (let drag_ of drag) {
        drag_.onmousedown = async (e) => {
            let x = e.clientX;
            let y = e.clientY;
            let dx = 0;
            let dy = 0;
            document.onmousemove = function (e) {
                dx = (e.clientX - x)
                dy = (e.clientY - y)
                window.backend.moveWindow(`${dx}&${dy}`);
            }
            document.onmouseup = function () {
                document.onmousemove = null;
                document.onmouseup = null;
            }
        }
    }
}
// -------------------------------------------------------------------------------------------------------------



// ---------------------------------- 初始化方法 ---------------------------------------
window.FoolJsInit = async () => {
    add_drag("#fool-drag") // 添加拖拽
}
// -------------------------------------------------------------------------------------------------------------



var event_ = new Event("FoolJsReady");
window.dispatchEvent(event_);




