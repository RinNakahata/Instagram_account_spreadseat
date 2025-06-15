# 📸 Instagramアカウント情報収集 & Googleスプレッドシート自動入力スクリプト

Instagramアカウントの表示名・ユーザーID・フォロワー数を自動で取得し、Googleスプレッドシートに書き込むPythonスクリプトです。

---

## ✅ 機能概要

- InstagramアカウントのURLリストをスプレッドシートに記載
- Pythonで各アカウントにアクセスし、以下情報を取得：
  - アカウント名（表示名）
  - ユーザーID（URLから抽出）
  - フォロワー数（単位変換含む）
- Googleスプレッドシートに自動で追記

---

## 🛠 使用技術

| 技術          | 用途                          |
|---------------|-------------------------------|
| Python        | スクリプト本体                |
| Selenium      | InstagramのHTMLスクレイピング |
| ChromeDriver  | ブラウザ操作                  |
| gspread       | Googleスプレッドシート操作    |
| oauth2client  | Google認証                    |

---

## 💡 事前準備

1. Python環境を用意（推奨: Python 3.9〜）
2. 下記ライブラリをインストール：

```bash
pip install selenium gspread oauth2client webdriver-manager
```

3. Google Cloud Consoleでサービスアカウントを作成し、`credentials.json` を取得  
4. 対象スプレッドシートを作成し、1列目にInstagramのURLを入力  
5. スプレッドシートの編集権限にサービスアカウントのメールアドレスを追加

---

## 🔐 Cookie認証について

Instagramはログインしないと情報が取得できない仕様のため、ログイン済みのCookieを `.pkl` 形式で保存し、再利用します。

以下のコードを事前に実行してください：

```python
from selenium import webdriver
import pickle

driver = webdriver.Chrome()
driver.get("https://www.instagram.com/")
input("ログイン後、Enterを押してください")
pickle.dump(driver.get_cookies(), open("instagram_cookies.pkl", "wb"))
driver.quit()
```

---

## 🚀 実行方法

```bash
python script.py
```

- `credentials.json` および `instagram_cookies.pkl` はスクリプトと同じフォルダに配置してください  
- スプレッドシートIDとシート名は `script.py` 内で指定できます

---

## 📂 ディレクトリ構成

```
project/
├── script.py
├── credentials.json
├── instagram_cookies.pkl
└── README.md
```

---

## ⚠️ 注意事項

- 本スクリプトはInstagramの利用規約を尊重し、過剰なアクセスは避ける設計です  
- DOM構造が変更されると、スクリプトが動作しなくなる場合があります  
- 商用利用は自己責任でお願いします

---

## 📘 ライセンス

MIT License

---

## ✨ 今後の拡張予定

- 投稿数や画像URLの取得
- スプレッドシートとの自動連携（トリガー設定）
- TikTokやX（旧Twitter）など他SNS対応
