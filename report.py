from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random


def human_delay(min_sec=7, max_sec=10): # Adjusted delay
    time.sleep(random.uniform(min_sec, max_sec))


def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=options)
    return driver


def login_instagram(driver, username, password):
    driver.get("https://www.instagram.com/accounts/login/")
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    human_delay() # Use default 7-10s

    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")

    username_input.send_keys(username)
    password_input.send_keys(password)

    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()
    human_delay() # Use default 7-10s

    print("✅ Logged in successfully!")


def report_account(driver, profile_url):
    try:
        driver.get(profile_url)
        human_delay() # Use default 7-10s


        options_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "svg[aria-label='Options']"))
        )
        options_button.click()
        human_delay() # Use default 7-10s
        print("🔵 Clicked 'Options' button.")
    except Exception as e:
        print(f"⚠️ Error clicking 'Options' button: {e}")
        driver.quit()
        return

    
    try:
        report_button = WebDriverWait(driver, 20).until( 
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Report']"))
        )
        report_button.click()
        print("🔵 Clicked 'Report' button.")
    except Exception as e:
        print(f"⚠️ Error clicking 'Report' button: {e}")
        driver.quit()
        return

    
    try:
        report_account_button = WebDriverWait(driver, 20).until( 
            EC.element_to_be_clickable((By.XPATH, "//div[text()='Report Account']"))
        )
        report_account_button.click()
        print("🔵 Clicked 'Report Account'.")
    except Exception as e:
        print(f"⚠️ Error clicking 'Report Account' option: {e}")
        driver.quit()
        return

    
    try:
        reason_text_xpath = "//div[contains(text(), \"It's posting content that shouldn't be on Instagram\")]"
        reason_button = WebDriverWait(driver, 20).until( 
            EC.element_to_be_clickable((By.XPATH, reason_text_xpath))
        )
        reason_button.click()
        print("🔵 Selected reason: It's posting content that shouldn't be on Instagram")
    except Exception as e:
        print(f"⚠️ Error selecting reason: {e}")
        driver.quit()
        return

    
    try:
        false_info_button_xpath = "//div[contains(text(), 'False information')]"
        false_info_button = WebDriverWait(driver, 20).until( 
            EC.element_to_be_clickable((By.XPATH, false_info_button_xpath))
        )
        false_info_button.click()
        print("🔵 Clicked 'False Information' button.")
    except Exception as e:
        print(f"⚠️ Error clicking 'False Information' button: {e}")
        driver.quit()
        return

    
    try:
        
        close_button_xpath = "//button[contains(text(),'Close')]"
        close_button = WebDriverWait(driver, 20).until(  
            EC.element_to_be_clickable((By.XPATH, close_button_xpath))
        )
        close_button.click()
        print("🔵 Clicked 'Close' button.")
    except Exception as e:
        
        try:
            driver.execute_script("arguments[0].click();", close_button)
            print("🔵 Clicked 'Close' button using JavaScript.")
        except Exception as e:
            print(f"⚠️ Error clicking 'Close' button with JavaScript: {e}")
            driver.quit()
            return

if __name__ == "__main__":
    your_username = "KYU_BATAUN"
    your_password = "NOPE"
    target_account = "sajid91502024" 

    driver = create_driver()

    try:
        login_instagram(driver, your_username, your_password)
        report_account(driver, f"https://www.instagram.com/{target_account}/")
    finally:
        human_delay() # Use default 7-10s
        driver.quit()
