[中文版本](README.md)
[English Version](README_EN.md)
[Japanese Version](README_JP.md)

# FoolPyWebView
超级简单的python webview库 支持 文件拖拽 窗口透明 等 这些都是 pywebview 做不到的
可以做很多很酷的效果 比如窗口出现和退出时候的css特效 这些也是 pywebview所不支持的 但 pywebview很轻量级 我这个是基于pyqt QtWebEngineWidgets
FoolPyWebView 是一个基于 PyQt5 的 QtWebEngineWidgets 进行二次封装的库。这个库的主要目标是提供一个与 JavaScript 和 Python 之间无缝互通的平台，无论是 JavaScript 调用 Python，还是 Python 调用 JavaScript，它都能完全支持。其返回值对对象、字典、数组等类型的支持也非常完整。此外，FoolPyWebView 还重写了 dragEvent，从而实现了拖拽文件并获取文件路径的功能。它还支持多窗口操作，并且用户可以在 HTML 中设置 #fool-drag，让 DOM 支持拖拽移动窗口。

## 功能特性

- **无缝数据交互**：完全支持 JavaScript 和 Python 之间的数据无缝互通，无论是 JavaScript 调用 Python，还是 Python 调用 JavaScript。

- **类型兼容性**：返回的数据类型支持包括对象、字典、数组等在内的多种类型。

- **拖拽文件功能**：重写了 dragEvent 实现了拖拽文件并获取文件路径的功能。

- **拖拽移动屏幕**：用户可以在 HTML 中设置 #fool-drag，让 DOM 支持拖拽移动屏幕。

- **多窗口支持**：能够满足用户对于多窗口操作的需求。

## 即将添加的特性

1. **实时数据同步**：我们计划添加类似于 Vuex 的实时数据同步功能。

2. **多窗口管理系统**：我们正在开发一个多窗口管理系统，可以管理窗口之间的父子关系。

3. **预制 HTML 组件**：我们将推出预制的 HTML 组件，如导航栏 (nav)。

## 安装

你可以通过 pip 来安装 FoolPyWebView：

```bash
pip install FoolPyWebView
```

## 使用

以下是一个简单的 FoolPyWebView 的使用示例：

```python
# 请看example文件夹
```

## 开源许可证

本项目采用 MIT 许可证。详情请查阅 [LICENSE](LICENSE) 文件。

## 贡献

如果你想对这个项目做出贡献，欢迎提交 pull request 或者在 issue 区提出你的问题或建议。

## 支持

如果你在使用过程中遇到任何问题，或者有任何疑问，都可以通过提交 issue 来向我们寻求帮助。我们会尽快回应你的请求。

---

希望 FoolPyWebView 能够帮助你更好地进行 Python 和 JavaScript 之间的交互！
