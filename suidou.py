# ✅ Instagramクッキー保存＆自動ログイン付き完全版スクレイピングスクリプト

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pickle
import time
from pathlib import Path


# ===============================
# Step 1: Cookieを保存する関数（初回だけ実行）
# ===============================
def save_instagram_cookie():
    options = Options()
    # options.add_argument("--headless")  # 手動ログインなので無効
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)
    driver.get("https://www.instagram.com/accounts/login/")
    print("🔓 手動でログインしてください（最大90秒待ち）...")
    time.sleep(90)

    cookie_path = Path.home() / "instagram_cookies.pkl"
    with open(cookie_path, "wb") as f:
        pickle.dump(driver.get_cookies(), f)
        print(f"✅ Cookieを保存しました：{cookie_path}")

    driver.quit()


# ===============================
# Step 2: クッキーを使ってプロフィール情報を取得
# ===============================
def get_instagram_info_selenium(url):
    try:
        options = Options()
        # options.add_argument("--headless")  # 実運用時に有効化
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

        driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=options)
        wait = WebDriverWait(driver, 10)

        cookie_path = Path.home() / "instagram_cookies.pkl"
        driver.get("https://www.instagram.com/")

        if not cookie_path.exists():
            print("❌ Cookieファイルが存在しません。まず save_instagram_cookie() を実行してください。")
            driver.quit()
            return "", "", ""

        with open(cookie_path, "rb") as f:
            cookies = pickle.load(f)
            for cookie in cookies:
                driver.add_cookie(cookie)

        # Cookie反映後にプロフィールページへ移動
        driver.get(url)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "h2")))

        user_id = url.split("instagram.com/")[-1].strip("/").split("/")[0]

        # アカウント名
        try:
            name_element = wait.until(EC.presence_of_element_located((
                By.XPATH,
                '//span[@class="x1lliihq x1plvlek xryxfnj x1n2onr6 x1ji0vk5 x18bv5gf x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xvs91rp x1s688f x5n08af x10wh9bi xpm28yp x8viiok x1o7cslx"]'
            )))
            account_name = name_element.text.strip()
        except:
            account_name = ""

        # フォロワー数
        try:
            follower_element = wait.until(EC.presence_of_element_located((
                By.XPATH, '//ul/li[2]//a//span'
            )))
            followers = follower_element.text.strip()
        except:
            followers = ""

        driver.quit()
        return user_id, account_name, followers

    except Exception as e:
        print(f"❌ エラー: {url} - {e}")
        return "", "", ""


# ===============================
# Step 3: スプレッドシート更新関数
# ===============================
def update_sheet(json_key_path, sheet_id, worksheet_name):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        json_key_path, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(sheet_id).worksheet(worksheet_name)
    rows = sheet.get_all_values()

    for i, row in enumerate(rows[1:], start=2):
        url = row[0]
        if not url.startswith("https://www.instagram.com/"):
            continue
        if all(row[1:4]):
            continue

        user_id, name, followers = get_instagram_info_selenium(url)
        sheet.update_cell(i, 2, user_id)
        sheet.update_cell(i, 3, name)
        sheet.update_cell(i, 4, followers)
        print(f"✅ {i-1}件目: {user_id} | {name} | {followers}")
        time.sleep(2)


# ===============================
# 実行部分（必要に応じて切り替えてください）
# ===============================
if __name__ == "__main__":
    # 初回だけCookieを保存する
    # save_instagram_cookie()

    # Cookie保存後はこの関数だけでOK
    update_sheet(
        json_key_path="credentials.json",
        sheet_id="1kZx7utoZIAhvlNCArV1iijDT_BGYtryfq4lL0ZxcztM",
        worksheet_name="シート1"
    )
