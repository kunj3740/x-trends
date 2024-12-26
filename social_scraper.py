from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime
import uuid
import pymongo
from pymongo import MongoClient
import time
from config import *

class SocialMediaScraper:
    def __init__(self):
        self.mongo_client = MongoClient(MONGODB_URI)
        self.topics_db = self.mongo_client['social_topics']
        self.trending_collection = self.topics_db['trending']

    def initialize_browser(self):
        chrome_config = webdriver.ChromeOptions()
        chrome_config.add_argument('--no-sandbox')
        chrome_config.add_argument('--disable-dev-shm-usage')
        chrome_config.add_argument('--disable-gpu')
        chrome_config.add_argument('--window-size=1920,1080')
        chrome_config.add_argument('--start-maximized')
        return webdriver.Chrome(options=chrome_config)

    def authenticate_user(self, browser):
        try:
            browser.get('https://x.com/i/flow/login')
            time.sleep(5)

            username_field = WebDriverWait(browser, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]'))
            )
            username_field.send_keys(TWITTER_USERNAME)

            continue_btn = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']"))
            )
            continue_btn.click()
            time.sleep(3)

            password_field = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password"]'))
            )
            password_field.send_keys(TWITTER_PASSWORD)

            signin_btn = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Log in']"))
            )
            signin_btn.click()
            time.sleep(5)

        except Exception as e:
            print(f"Authentication error: {str(e)}")
            raise

    def fetch_trending_topics(self):
        browser = None
        try:
            browser = self.initialize_browser()
            self.authenticate_user(browser)
            time.sleep(10)

            trending_container = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-label="Timeline: Trending now"]'))
            )

            topic_elements = trending_container.find_elements(By.CSS_SELECTOR, '[data-testid="trend"]')
            topics_list = []
            topics_found = 0

            for element in topic_elements[:5]:
                try:
                    topic_text = None
                    text_spans = element.find_elements(By.CSS_SELECTOR, 'span[dir="ltr"]')
                    
                    for span in text_spans:
                        text = span.text.strip()
                        if text and not text.startswith("Trending"):
                            topic_text = text
                            break

                    if not topic_text:
                        text_divs = element.find_elements(By.CSS_SELECTOR, 'div[dir="ltr"]')
                        for div in text_divs:
                            text = div.text.strip()
                            if text and not text.startswith("Trending"):
                                topic_text = text
                                break

                    if topic_text:
                        topics_list.append(topic_text)
                        topics_found += 1

                except Exception as e:
                    print(f"Topic extraction error: {str(e)}")
                    continue

            while len(topics_list) < 5:
                topics_list.append("No topic available")

            record = {
                '_id': str(uuid.uuid4()),
                'topicname1': topics_list[0],
                'topicname2': topics_list[1],
                'topicname3': topics_list[2],
                'topicname4': topics_list[3],
                'topicname5': topics_list[4],
                'timestamp': datetime.now(),
                'ip_address': "127.0.0.1"
            }

            self.trending_collection.insert_one(record)
            return record

        except Exception as e:
            print(f"Trending topics error: {str(e)}")
            raise

        finally:
            if browser:
                browser.quit()