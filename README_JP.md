- [中文版本](README.md)
- [English Version](README_EN.md)
- [Japanese Version](README_JP.md)

# FoolPyWebView

FoolPyWebViewは、非常にシンプルなPythonのwebviewライブラリで、ファイルのドラッグ、ウィンドウの透明化など、pywebviewがサポートしていない機能を提供します。ウィンドウの表示と終了時のCSSエフェクトなど、多くのクールな効果を作成することができます。これらはpywebviewがサポートしていない機能です。pywebviewは軽量な一方、FoolPyWebViewはPyQt5のQtWebEngineWidgetsに基づいています。

FoolPyWebViewは、PyQt5のQtWebEngineWidgetsを二次的に包装したライブラリです。このライブラリの主な目的は、JavaScriptとPythonの間でシームレスに相互作用できるプラットフォームを提供することです。JavaScriptがPythonを呼び出すか、PythonがJavaScriptを呼び出すか、どちらも完全にサポートしています。また、オブジェクト、辞書、配列などのタイプの戻り値も完全にサポートしています。さらに、FoolPyWebViewはdragEventを書き直して、ファイルをドラッグしてファイルパスを取得する機能を実装しました。また、複数ウィンドウの操作をサポートしており、ユーザーはHTMLで#fool-dragを設定して、DOMがウィンドウのドラッグ移動をサポートするようにすることができます。

## 機能特性

- **シームレスなデータ交互作用**：JavaScriptとPythonの間のデータ交互作用を完全にサポートしています。JavaScriptがPythonを呼び出すか、PythonがJavaScriptを呼び出すか、どちらも対応しています。

- **タイプ互換性**：戻り値のデータタイプは、オブジェクト、辞書、配列など、さまざまなタイプをサポートしています。

- **ファイルドラッグ機能**：dragEventを書き直して、ファイルをドラッグしてファイルパスを取得する機能を実装しました。

- **ドラッグ移動画面**：ユーザーはHTMLで#fool-dragを設定し、DOMがドラッグ移動画面をサポートするようにできます。

- **マルチウィンドウサポート**：マルチウィンドウ操作のユーザー要件を満たすことができます。

## 追加予定の特性

1. **リアルタイムデータ同期**：Vuexのようなリアルタイムデータ同期機能を追加する予定です。

2. **マルチウィンドウ管理システム**：ウィンドウ間の親子関係を管理するマルチウィンドウ管理システムを開発中です。

3. **プリファブのHTMLコンポーネント**：navバーなどのプリファブのHTMLコンポーネントを導入する予定です。

## インストール

pipを使ってFoolPyWebViewをインストールすることができます：

```bash
pip install FoolPyWebView
```

## 使用法

以下は、FoolPyWebViewの使用例です：

```python
# exampleフォルダをご覧ください
```

## ライセンス

このプロジェクトはMITライセンスでライセンスされています。詳細は[LICENSE](LICENSE)ファイルをご覧ください。

## 貢献

このプロジェククトに貢献したい場合は、プルリクエストを送信するか、問題セクションでご質問や提案をお寄せください。

## サポート

使用中に問題が発生した場合、または質問がある場合は、問題を提出して私たちからのヘルプを求めることができます。私たちはできるだけ早くご要望に対応します。

---

FoolPyWebViewがPythonとJavaScriptの間の相互作用をより良くサポートする助けとなることを願っています！