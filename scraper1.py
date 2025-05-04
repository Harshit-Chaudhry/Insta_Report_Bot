import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class InstagramCredentials:
    def __init__(self, username, password):
        self.username = username
        self.password = password


class InstagramScraper:

    def __init__(self, credentials, hashtags, scroll_count=5, max_posts_per_hashtag=10):
        self.credentials = credentials
        self.hashtags = hashtags
        self.scroll_count = scroll_count
        self.max_posts_per_hashtag = max_posts_per_hashtag
        self.driver = None
        self.all_usernames = set()

    def initialize_driver(self):
        options = uc.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        self.driver = uc.Chrome(options=options)
        print("🚀 Chrome driver initialized.")

    def login(self):
        self.driver.get("https://www.instagram.com/accounts/login/")
        print("🌐 Navigated to login page.")
        time.sleep(random.uniform(3, 5))

        try:
            user_input = self._wait_for_element(By.NAME, "username", timeout=20)
            if not user_input:
                raise Exception("Login failed: Username input field not found.")

            pass_input = self.driver.find_element(By.NAME, "password")

            print("🔑 Typing credentials...")
            user_input.send_keys(self.credentials.username)
            time.sleep(random.uniform(1, 2))
            pass_input.send_keys(self.credentials.password)
            time.sleep(random.uniform(1, 3))
            pass_input.send_keys(Keys.RETURN)

            print("⏳ Submitted login credentials. Waiting for page redirect...")
            try:
                WebDriverWait(self.driver, 25).until(
                    EC.url_changes("https://www.instagram.com/accounts/login/")
                )
            except Exception:
                 pass


            current_url = self.driver.current_url
            print(f"🔗 Current URL after wait: {current_url}")

            if "challenge" in current_url:
                print("❌ Login failed: Checkpoint/verification required.")
                self.driver.save_screenshot("login_challenge.png")
                print("📸 Screenshot saved as login_challenge.png")
                raise Exception("Login failed: Checkpoint/verification required.")
            elif "login" in current_url and "session_expired" not in current_url:
                print("❌ Login failed: Still on login page (likely incorrect credentials or other issue).")
                self.driver.save_screenshot("login_failed.png")
                print("📸 Screenshot saved as login_failed.png")
                raise Exception("Login failed: Still on login page.")
            elif "instagram.com" not in current_url:
                 print(f"❌ Login failed: Unexpected URL: {current_url}")
                 self.driver.save_screenshot("login_unexpected_url.png")
                 print("📸 Screenshot saved as login_unexpected_url.png")
                 raise Exception(f"Login failed: Unexpected URL: {current_url}")


            print("✅ Login successful.")

        except Exception as e:
             print(f"💥 An error occurred during login: {e}")
             raise

    def _wait_for_element(self, by, value, timeout=15):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
        except Exception:
            return None

    def _wait_for_elements(self, by, value, timeout=15):
        try:
             return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located((by, value))
            )
        except Exception:
            return []

    def _scroll_page(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(2, 4))

    def _get_links_from_hashtag_page(self, hashtag, link_pattern, element_selector):
        links = set()
        url = f"https://www.instagram.com/explore/tags/{hashtag}/"
        print(f"   L Navigating to: {url}")
        self.driver.get(url)

        main_element = self._wait_for_element(By.XPATH, "//main", timeout=25)
        if not main_element:
             print(f"   L ⚠️ Could not find main content area for #{hashtag}. Skipping.")
             return links
        time.sleep(random.uniform(4, 7))

        print(f"  L Scrolling and finding links incrementally for #{hashtag}...")

        for i in range(self.scroll_count + 1):
            try:
                link_elements = main_element.find_elements(By.CSS_SELECTOR, element_selector)
            except Exception as find_err:
                 print(f"  L ⚠️ Error finding elements with selector '{element_selector}' during scroll {i+1}: {find_err}")
                 link_elements = []

            scroll_found_count = 0
            for link_element in link_elements:
                try:
                    href = link_element.get_attribute("href")
                    if href and link_pattern in href and href.startswith("https://www.instagram.com") and href not in links:
                        links.add(href)
                        scroll_found_count += 1
                except Exception as e:
                     if "stale element reference" not in str(e).lower():
                          print(f"  L ⚠️ Error getting href from element during scroll {i+1}: {e}")

            print(f"  L Pass {i+1}/{self.scroll_count + 1}: Found {scroll_found_count} new links. Total unique: {len(links)}")

            if i < self.scroll_count:
                print(f"  L Scrolling down ({i+1}/{self.scroll_count})...")
                self._scroll_page()
                time.sleep(random.uniform(1, 3))


        print(f"  L Finished scrolling/searching. Found {len(links)} total potential links matching '{link_pattern}' for #{hashtag}")
        return links


    def _get_username_from_page(self, url, username_selector):
        username = None
        try:
            print(f"     U Navigating to: {url}")
            self.driver.get(url)
            user_element = self._wait_for_element(By.XPATH, username_selector, timeout=20)

            if user_element:
                href = user_element.get_attribute("href")
                if href:
                    parts = href.strip('/').split('/')
                    if len(parts) >= 3 and parts[-2] == 'www.instagram.com':
                         username = parts[-1]
                         print(f"    U Extracted username: {username}")
                    else:
                         potential_username = parts[-1]
                         if potential_username and potential_username not in ['p', 'reel', 'explore', 'accounts', '']:
                             username = potential_username
                             print(f"    U Extracted potential username (fallback): {username} from {href}")
                         else:
                             print(f"    U ⚠️ Could not reliably extract username from href: {href}")
            else:
                print(f"    U ⚠️ Username element not found with selector '{username_selector}' on page: {url}")
                try:
                    filename = f"error_username_{url.split('/')[-2]}.png"
                    self.driver.save_screenshot(filename)
                    print(f"    U 📸 Screenshot saved as {filename}")
                except Exception as ss_err:
                    print(f"    U ⚠️ Could not save screenshot: {ss_err}")


        except Exception as e:
            print(f"    U 💥 Error processing page {url} for username: {e}")
        finally:
             time.sleep(random.uniform(1, 3))
             return username


    def get_reel_usernames(self, hashtag):
        print(f"  R Searching reels for #{hashtag}...")
        usernames = set()
        reel_link_selector = "main > div > div a[href*='/reel/']"
        reel_links = self._get_links_from_hashtag_page(hashtag, "/reel/", reel_link_selector)

        username_selector_on_reel = "//article//header//a[@role='link' and normalize-space(text())]"

        processed_count = 0
        if not reel_links:
             print(f"  R No reel links found to process for #{hashtag}.")
             return usernames

        print(f"  R Processing {min(len(reel_links), self.max_posts_per_hashtag)} reel links for #{hashtag}...")
        for link in list(reel_links):
             if processed_count >= self.max_posts_per_hashtag:
                 print(f"  R Reached max posts limit ({self.max_posts_per_hashtag}) for reels.")
                 break
             username = self._get_username_from_page(link, username_selector_on_reel)
             if username and username not in usernames:
                 print(f"  R 👤 Found reel user: {username}")
                 usernames.add(username)
             processed_count += 1
        print(f"  R Finished processing reels for #{hashtag}. Found {len(usernames)} unique users.")
        return usernames

    def get_post_usernames(self, hashtag):
        print(f"  P Searching posts for #{hashtag}...")
        usernames = set()
        post_link_selector = "main > div > div a[href*='/p/']"
        post_links = self._get_links_from_hashtag_page(hashtag, "/p/", post_link_selector)

        username_selector_on_post = "//article//header//a[@role='link' and normalize-space(text())]"

        processed_count = 0
        if not post_links:
             print(f"  P No post links found to process for #{hashtag}.")
             return usernames

        print(f"  P Processing {min(len(post_links), self.max_posts_per_hashtag)} post links for #{hashtag}...")
        for link in list(post_links):
            if processed_count >= self.max_posts_per_hashtag:
                 print(f"  P Reached max posts limit ({self.max_posts_per_hashtag}) for posts.")
                 break
            username = self._get_username_from_page(link, username_selector_on_post)
            if username and username not in usernames:
                print(f"  P 👤 Found post user: {username}")
                usernames.add(username)
            processed_count += 1
        print(f"  P Finished processing posts for #{hashtag}. Found {len(usernames)} unique users.")
        return usernames

    def collect_usernames(self):
        self.all_usernames = set()
        print("\n--- Starting Username Collection ---")
        for tag in self.hashtags:
            print(f"\n🔍 Processing Hashtag: #{tag}")
            reel_usernames = self.get_reel_usernames(tag)
            self.all_usernames.update(reel_usernames)
            print(f"  > Reel users found for #{tag}: {len(reel_usernames)}")
            time.sleep(random.uniform(2, 5))

            post_usernames = self.get_post_usernames(tag)
            self.all_usernames.update(post_usernames)
            print(f"  > Post users found for #{tag}: {len(post_usernames)}")
            print(f"  > Total unique users after #{tag}: {len(self.all_usernames)}")
            time.sleep(random.uniform(4, 7))

        print(f"\n--- Finished Username Collection ---")
        print(f"✅ Total unique usernames collected across all hashtags: {len(self.all_usernames)}")
        self.save_usernames("all_scraped_usernames.txt")


    def save_usernames(self, filename="all_scraped_usernames.txt"):
        print(f"\n💾 Saving {len(self.all_usernames)} usernames to {filename}...")
        try:
            with open(filename, "w", encoding='utf-8') as f:
                for user in sorted(list(self.all_usernames)):
                    f.write(user + "\n")
            print(f"💾 Usernames successfully saved to {filename}")
        except Exception as e:
            print(f"💾💥 Error saving usernames to {filename}: {e}")

    def run(self):
        try:
            self.initialize_driver()
            self.login()
            self.collect_usernames()
        finally:
            if self.driver:
                print("🛑 Closing driver...")
                try:
                    self.driver.quit()
                    print("🛑 Driver closed.")
                except Exception as e:
                     print(f"⚠️ Error during driver.quit(): {e}")


class ScraperConfig:

    DEFAULT_HASHTAGS = ["meme", "indiapak"]
    DEFAULT_SCROLL_COUNT = 3
    DEFAULT_MAX_POSTS = 5

    @classmethod
    def get_default_config(cls):
        return {
            "hashtags": cls.DEFAULT_HASHTAGS,
            "scroll_count": cls.DEFAULT_SCROLL_COUNT,
            "max_posts_per_hashtag": cls.DEFAULT_MAX_POSTS
        }


if __name__ == "__main__":
    print("--- Running scraper1.py Standalone ---")
    credentials = InstagramCredentials(
        username="it_pvt_cell",
        password="KYU_BATAUN"
    )

    config = ScraperConfig.get_default_config()

    scraper = InstagramScraper(
        credentials=credentials,
        hashtags=config["hashtags"],
        scroll_count=config["scroll_count"],
        max_posts_per_hashtag=config["max_posts_per_hashtag"]
    )

    scraper.run()
    print("--- Standalone Run Finished ---")