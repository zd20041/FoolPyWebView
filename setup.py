from setuptools import setup, find_packages

setup(
    name="FoolPyWebView",  # 你的包名，PyPI 上需要唯一
    version="1.5.0",  # 你的包的版本号
    author="zd2004",  # 作者名
    author_email="samuraizd@outlook.com",  # 作者邮箱
    description="超简单的pywebview UI库 支持py和js的相互通信 支持文件拖拽",  # 项目简短描述
    long_description=open('README_EN.md', 'r', encoding='utf-8').read(),  # 项目长描述，通常是读取 README 文件
    long_description_content_type="text/markdown",  # 长描述的格式，如果你的 README 是 Markdown 格式的，这里就应设为 text/markdown
    url="https://github.com/zd20041/FoolPyWebView",  # 项目的代码仓库 URL
    include_package_data=True, # 自动打包文件夹内所有数据
    install_requires=["PyQtWebEngine", "PyQt5"],  # 你的项目所依赖的第三方库
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],  # 一些分类信息
    python_requires='>=3.6',  # 你的包所需要的最低 Python 版本
)