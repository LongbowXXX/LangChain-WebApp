# 開発環境

## ツール
PyCharm 2023.3.3 (Professional Edition)

## Python
Python 3.11

## Pycharm の起動オプションに文字エンコードを設定する

Shift２回押しで開く検索画面で`vmoptions`を検索し、`pycharm64.exe.vmoptions` を開く。
下記の行を追加する。
```
-Dfile.encoding=UTF-8
```
