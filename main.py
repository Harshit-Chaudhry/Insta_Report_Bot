from scraper1 import InstagramScraper, InstagramCredentials, ScraperConfig
from scraper2 import InstagramBot
from report import report_account # Import the report function
import time
import random


def main():
    # Step 1: Scrape usernames from hashtags
    credentials = InstagramCredentials(
        username="it_pvt_cell",
        password="%jQ-UtLpV/h7d:%"  # Use the correct password
    )

    config = ScraperConfig.get_default_config()
    scraper = InstagramScraper(
        credentials=credentials,
        hashtags=config["hashtags"],
        scroll_count=config["scroll_count"],
        max_posts_per_hashtag=config["max_posts_per_hashtag"]
    )

    scraper.initialize_driver()
    scraper.login()
    scraper.collect_usernames()
    scraper.driver.quit()

    usernames = list(scraper.all_usernames)
    print(f"\n🌍 STEP 2: Filtering Pakistani Accounts ({len(usernames)} users total)")

    # Step 2: Filter Pakistani accounts
    info_scraper = InstagramBot(credentials.username, "%jQ-UtLpV/h7d:%")
    pakistani_users = []

    try:
        info_scraper.login()
        for user in usernames:
            print(f"🔍 Checking account origin: {user}")
            info = info_scraper.get_about_this_account(user)  # ✅ FIXED
            if info.get("Country", "").lower() == "pakistan":
                print(f"✅ Pakistani user found: {user}")
                pakistani_users.append(user)
                # --- Report the account ---
                profile_url = f"https://www.instagram.com/{user}/"
                print(f"🚩 Reporting account: {user}")
                report_account(info_scraper.driver, profile_url)
                print(f"🏁 Finished reporting attempt for: {user}")
                # --- End Reporting ---
            else:
                print(f"⛔ Not Pakistani: {user}")
            time.sleep(random.uniform(7, 10)) # Adjusted delay after check/report
    finally:
        info_scraper.close()

    # Save filtered usernames
    output_file = "pakistani_usernames.txt"
    with open(output_file, "w") as f:
        for user in pakistani_users:
            f.write(user + "\n")
    print(f"\n💾 Saved {len(pakistani_users)} Pakistani usernames to {output_file}")


if __name__ == "__main__":
    main()
