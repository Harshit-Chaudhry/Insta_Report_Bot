import time
import random
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def human_delay(min_sec=7, max_sec=10):
    time.sleep(random.uniform(min_sec, max_sec))


class InstagramBot:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = self._create_driver()

    def _create_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-blink-features=AutomationControlled")
        return webdriver.Chrome(options=options)

    def login(self):
        self.driver.get("https://www.instagram.com/accounts/login/")
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        human_delay()

        self.driver.find_element(By.NAME, "username").send_keys(self.username)
        self.driver.find_element(By.NAME, "password").send_keys(self.password)

        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        human_delay()
        print("✅ Logged in successfully!")

    def get_about_this_account(self, target_username):
        info = {}
        try:
            self.driver.get(f"https://www.instagram.com/{target_username}/")
            human_delay()

            options_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "svg[aria-label='Options']"))
            )
            options_button.click()
            human_delay()

            about_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'About this account')]"))
            )
            about_button.click()
            human_delay()

            try:
                date_label = WebDriverWait(self.driver, 8).until(
                    EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Date joined')]"))
                )
                date_value = date_label.find_element(By.XPATH, "following-sibling::span").text
                info["Date Joined"] = date_value
            except:
                print("⚠️ 'Date Joined' not found")
                info["Date Joined"] = None

            try:
                country_label = WebDriverWait(self.driver, 8).until(
                    EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Account based in')]"))
                )
                country_value = country_label.find_element(By.XPATH, "following-sibling::span").text
                info["Country"] = country_value
            except:
                print("⚠️ 'Country' not found")
                info["Country"] = None

            print("\n📄 About This Account Info:")
            for k, v in info.items():
                print(f"{k}: {v}")

            filename = f"{target_username}.json"
            with open(filename, "w") as f:
                json.dump(info, f, indent=4)
            print(f"💾 Info saved to {filename}")

            try:
                close_btn = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[text()='Close']"))
                )
                close_btn.click()
                human_delay()
            except:
                print("⚠️ Couldn't close popup.")

        except Exception as e:
            print(f"⚠️ Failed to fetch account info: {e}")
            self.driver.save_screenshot(f"{target_username}_error.png")

        return info

    def close(self):
        human_delay()
        self.driver.quit()
        print("🛑 Driver closed.")


if __name__ == "__main__":
    USERNAME = "it_pvt_cell"
    PASSWORD = "%jQ-UtLpV/h7d:%"
    TARGET_ACCOUNT = "sajid91502024"

    bot = InstagramBot(USERNAME, PASSWORD)

    try:
        bot.login()
        bot.get_about_this_account(TARGET_ACCOUNT)
    finally:
        bot.close()
