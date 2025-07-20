from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import threading
import json
import os
def run_view_bot(username, password, reel_url, watch_seconds=5,numviews=50):
    mobile_emulation = {
        "deviceName": "iPhone X"  # ممكن تغيره لـ "Pixel 2" أو "Galaxy S5"
    }
    options = Options()
    options.add_experimental_option("mobileEmulation", mobile_emulation)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=400,800")
    # options.add_argument("--headless")  # شغل ده لو عايز من غير نافذة

    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(5)

        username_input = driver.find_element(By.NAME, "username")
        password_input = driver.find_element(By.NAME, "password")
        username_input.send_keys(username)
        password_input.send_keys(password)
        time.sleep(1)
        login_button = driver.find_element(By.XPATH, "//div[@role='button' and @aria-label='Log in']")
        login_button.click()
        time.sleep(8)

        for view in range(numviews):
            try:
                not_now_btn = driver.find_element(By.XPATH, "//div[contains(text(),'Not now')]")
                not_now_btn.click()
                time.sleep(3)
            except:
                pass
            driver.get(reel_url)
            time.sleep(2)
            print(f"📱 {username} is watching the reel on mobile view...")
            time.sleep(watch_seconds)


    except Exception as e:
        print(f"❌ {username} Error:", e)

    finally:
        driver.quit()


# ========== بيانات الحسابات ==========

accounts : list
with open(f'data.json', 'r') as json_file:
    data=json.load(json_file)
    accounts=data["accounts"]

REEL_URL = "https://www.instagram.com/reel/DMU_Pf0MHmu/?igsh=MTM2ZHVuZDVwMDA4/"

# ========== تشغيل كل حساب في Thread ==========
threads = []

for acc in accounts:
    t = threading.Thread(
        target=run_view_bot,
        args=(acc["username"], acc["password"], REEL_URL)
    )
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("🎉 All threads finished.")
