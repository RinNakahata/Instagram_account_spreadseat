from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pickle
import time
from pathlib import Path

cookie_path = Path.home() / "instagram_cookies.pkl"

options = Options()
# options.add_argument("--headless")  # 手動ログインなのでヘッドレス不可
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)
driver.get("https://www.instagram.com/accounts/login/")
print("🔓 Instagramにログインしてください（90秒以内）...")

time.sleep(90)  # 自分でログイン＋2段階認証もここで済ませてください

with open(cookie_path, "wb") as f:
    pickle.dump(driver.get_cookies(), f)
    print(f"✅ Cookieを保存しました → {cookie_path}")

driver.quit()
