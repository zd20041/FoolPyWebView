new QWebChannel(qt.webChannelTransport, function (channel) {
    window.backend = channel.objects.backend;
});


// 处理返回值
const handle_reply = function (reply) {
    let json_reply = JSON.parse(reply);;
    let type_ = json_reply["type"];
    let value = json_reply["value"];
    return value;
}


const py_fn = {
    // message: function (...args) {
    //     return new Promise(function (resolve, reject) {
    //         window.backend.handle(JSON.stringify({ "method": this.message.name, "args": args }), function (reply) {
    //             resolve(handle_reply(reply));
    //         });
    //     }.bind(this));
    // },
    // test_dict: function (...args) {
    //     return new Promise(function (resolve, reject) {
    //         window.backend.handle(JSON.stringify({ "method": this.test_dict.name, "args": args }), function (reply) {
    //             resolve(handle_reply(reply));
    //         });
    //     }.bind(this));
    // },
    // test_list: function (...args) {
    //     return new Promise(function (resolve, reject) {
    //         window.backend.handle(JSON.stringify({ "method": this.test_list.name, "args": args }), function (reply) {
    //             resolve(handle_reply(reply));
    //         });
    //     }.bind(this));
    // }
}

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
window.add_pyfn = add_pyfn;
window.py_fn = py_fn;