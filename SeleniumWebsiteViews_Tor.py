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

# global variable index of dict to consume
index = 0


class viewBot:

    def __init__(self):
        print("starting ...")
        # To use Tor's SOCKS proxy server with chrome, include the socks protocol in the scheme with the --proxy-server option
        # PROXY = "socks5://127.0.0.1:9150" # IP:PORT or HOST:PORT
        try:
            os.system("sudo fuser -k 9050/tcp")
            tor_launcher = process.launch_tor_with_config(
                config={
                    "ControlPort": "9051",
                    "ExitNodes":
                    "{in}"  # currently only india, further https://sccmrookie.blogspot.com/2016/03/tor-country-codes-list.html
                }, )
        except OSError:
            print(
                "Please terminate the running tor process in task manager(optional), Press Ctrl+C to stop the program"
            )
            raise
        PROXY = "socks5://127.0.0.1:9050"  # IP:PORT or HOST:PORT
        self.chrome_options = Options()
        self.chrome_options.add_argument("--disable-extensions")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--no-sandbox")  # linux only
        self.chrome_options.add_argument("--proxy-server=%s" % PROXY)
        self.chrome_options.add_argument("--window-size=1920,1080")
        self.chrome_options.add_experimental_option("excludeSwitches",
                                                    ["enable-automation"])
        self.chrome_options.add_experimental_option("useAutomationExtension",
                                                    False)
        # # configure Chrome profile to automatically reject cookies
        # self.chrome_options.add_experimental_option(
        #     "prefs", {"profile.default_content_setting_values.cookies": 2}
        # )
        # self.chrome_options.add_argument("--headless")
        # chrome_options.headless = True # also works
        sleep(0.1)
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=self.chrome_options,
        )
        stealth(
            driver,
            user_agent=
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36",
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

            print(url)

            index += 1
            if index > len(list(url_status_test.keys())) - 1:
                index = 0

            if url_status_test[url][1] > 1:
                driver.delete_all_cookies()
                driver.get(url)
                sleep(url_status_test[url][0])
                url_status_test[url][1] -= 1
                driver.close()
                return True
            else:
                return True
        except Exception as e:
            print(e)
            return False


try:
    while True:
        viewBot()
except Exception as e:
    print(str(e))
