import random
from selenium import webdriver
import os
from time import sleep
from collections import defaultdict
from selenium.webdriver.common.action_chains import ActionChains as ac
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager
import multiprocessing as mp

from joblib import Parallel, delayed
import multiprocessing as mp
from stem.control import Controller
from stem import Signal
from stem import process

import random

# global variable dict
# url => [secondstostay, iter_left, total_iter_per_day]
url_status = {
    "https://www.crezalo.com": [60, 250, 250],
    "https://www.crezalo.com/editprofile": [10, 20, 20],
    "https://www.crezalo.com/bankinfo": [2, 5, 5],
    "https://www.crezalo.com/orders": [5, 300, 300],
    "https://www.crezalo.com/revenue": [15, 350, 350],
    "https://www.crezalo.com/creatorprofile/?address=username":
    [10, 2500, 2500],
    "https://www.crezalo.com/kycapproval": [10, 10, 10],
    "https://www.crezalo.com/merch/?productid=productid": [10, 500, 500],
    "https://www.crezalo.com/videoplayer/?videoid=videoid": [60, 1300, 1300],
    "https://www.crezalo.com/course/?courseid=courseid": [20, 300, 300],
    "https://www.crezalo.com/checkout/?stage=0": [5, 400, 400],
    "https://www.crezalo.com/checkout/?stage=1": [2, 40, 40],
    "https://www.crezalo.com/checkout/?stage=2": [10, 80, 80],
    "https://info.crezalo.com": [32, 1000, 1000]
}

url_status_test = {
    "https://www.crezalo.com": [1, 250, 250],
    "https://www.crezalo.com/editprofile": [1, 20, 20],
    "https://www.crezalo.com/bankinfo": [1, 5, 5],
    "https://www.crezalo.com/orders": [1, 300, 300],
    "https://www.crezalo.com/revenue": [1, 350, 350],
    "https://www.crezalo.com/creatorprofile/?address=username":
    [1, 2500, 2500],
    "https://www.crezalo.com/kycapproval": [1, 10, 10],
    "https://www.crezalo.com/merch/?productid=productid": [1, 500, 500],
    "https://www.crezalo.com/videoplayer/?videoid=videoid": [1, 1300, 1300],
    "https://www.crezalo.com/course/?courseid=courseid": [1, 300, 300],
    "https://www.crezalo.com/checkout/?stage=0": [1, 400, 400],
    "https://www.crezalo.com/checkout/?stage=1": [1, 40, 40],
    "https://www.crezalo.com/checkout/?stage=2": [1, 80, 80],
    "https://info.crezalo.com": [1, 1000, 1000]
}

# with open('http_proxies.txt', "r") as f:
#     proxies = f.read().split("\n")

# global variable index of dict to consume
index = 0


class viewBot:

    def __init__(self):
        print("starting ...")
        # proxy = random.choice(proxies)
        # print(proxy)
        self.chrome_options = Options()
        self.chrome_options.add_argument("--no-sandbox")  # linux only
        self.chrome_options.add_argument("--disable-extensions")
        self.chrome_options.add_argument("--disable-gpu")
        # self.chrome_options.add_argument(f'--proxy-server={proxy}')
        self.chrome_options.add_argument("--window-size=1920,1080")
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_experimental_option("excludeSwitches",
                                                    ["enable-automation"])
        self.chrome_options.add_experimental_option("useAutomationExtension",
                                                    False)
        mobile_emulation = {"deviceName": "iPhone 6"}

        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36"

        if random.choices(population=[0, 1], weights=[0.25, 0.75])[0]:
            self.chrome_options.add_experimental_option(
                "mobileEmulation", mobile_emulation)
            user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1"
            print("On Mobile")
        else:
            print("On Desktop")
        # self.chrome_options.add_argument("--auto-open-devtools-for-tabs")
        # # configure Chrome profile to automatically reject cookies
        # self.chrome_options.add_experimental_option(
        #     "prefs", {"profile.default_content_setting_values.cookies": 2}
        # )
        # self.chrome_options.add_argument("--headless")
        # chrome_options.headless = True # also works
        # sleep(0.1)
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=self.chrome_options,
        )
        stealth(
            driver,
            user_agent=user_agent,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=False,
            run_on_insecure_origins=False,
        )
        self.viewBotCrawler(driver)

    def viewBotCrawler(self, driver):
        global url_status_test
        global index

        try:
            url = list(url_status_test.keys())[index]

            index += 1
            if index > len(list(url_status_test.keys())) - 1:
                index = 0

            print(url)
            if url_status_test[url][1] > 1:
                driver.delete_all_cookies()
                driver.get(url)
                sleep(url_status_test[url][0])
                url_status_test[url][1] -= 1
                driver.quit()
                print(url_status_test[url])
                return True
            else:
                driver.quit()
                print(url_status_test[url])
                return True
        except Exception as e:
            driver.quit()
            print(e)
            return False


try:
    while True:
        viewBot()
except Exception as e:
    print(str(e))
