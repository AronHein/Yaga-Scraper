import schedule
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from config import Config
from database import DatabaseManager
from mail import EmailSender


class Scraper:
    def __init__(self):
        self.stop_scraping = False
        self.is_first_run = True
        self.config = Config()
        self.db_manager = DatabaseManager()
        self.email_sender = EmailSender()
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')

    def scroll_down(self, driver):
        """
        Scroll down the page to load more content.
        """
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait for new content to load
        except Exception as e:
            print(f"Error while scrolling: {e}")

    def scrape_yaga_website(self):
        """
        Scrape items from the Yaga website and store new items in the database.
        """
        driver = webdriver.Chrome(options=self.options)
        url = self.config.get_url()
        items = []
        max_items = self.config.get_max_items()

        try:
            driver.get(url)
            while not self.stop_scraping:
                elements_before_scroll = len(driver.find_elements(By.CLASS_NAME, 'MuiGrid-item'))
                self.scroll_down(driver)
                elements_after_scroll = len(driver.find_elements(By.CLASS_NAME, 'MuiGrid-item'))

                # Check if more items are loaded
                if elements_before_scroll == elements_after_scroll:
                    break

                elements = driver.find_elements(By.CLASS_NAME, 'MuiGrid-item')
                if not elements:
                    print("No items found.")
                    return

                for element in elements:
                    if len(items) >= max_items:
                        print(f"There are more than {max_items} items found. Please narrow down your search parameters.")
                        self.stop_scraping = True
                        break

                    try:
                        link_element = element.find_element(By.CSS_SELECTOR, 'a.no-style')
                        price_element = element.find_element(By.CSS_SELECTOR, 'div.price-container > h5.price')

                        item = {
                            "link": link_element.get_attribute('href'),
                            "price": price_element.text.strip()[:-2]
                        }

                        try:
                            brand_element = element.find_element(By.CSS_SELECTOR, '.brand-container h5.details')
                            item["brand"] = brand_element.text.strip()
                        except Exception as e:
                            item["brand"] = None

                        items.append(item)
                    except Exception as e:
                        print(f"Error extracting item details: {e}")

        except Exception as e:
            print(f"Error loading page: {e}")

        finally:
            driver.quit()

        new_items = self.db_manager.save_new_items(items, max_items)
        if new_items and not self.is_first_run:
            self.email_sender.send_email(new_items)
        if self.is_first_run:
            self.is_first_run = False

        print(f"Total new items: {len(new_items)}")

    def run(self):
        """
        Run the scraper on a schedule.
        """
        self.db_manager.init_db()
        self.scrape_yaga_website()

        interval_minutes = self.config.get_schedule_interval()
        schedule.every(interval_minutes).minutes.do(self.scrape_yaga_website)

        # Keep the script running
        while not self.stop_scraping:
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    scraper = Scraper()
    scraper.run()
