from selenium import webdriver
from selenium.webdriver.common.by import By
import pickle
from time import sleep
from tqdm import tqdm
from useragent_changer import UserAgent
import re

COOKIES_FILE = "cookies.pkl"
USER_AGENT = UserAgent("chrome").set()


def make_login():
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    # options.add_argument("--user-agent=" + USER_AGENT)
    driver = webdriver.Chrome(options=options)

    url = "https://www.pixiv.net"
    driver.get(url)

    msg = "ログインしたらEnter \n>"
    input(msg)

    # Cookie書き込み
    cookies = driver.get_cookies()
    pickle.dump(cookies, open(COOKIES_FILE, "wb"))

    driver.quit()


def hide_bookmark():
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    # options.add_argument("--user-agent=" + USER_AGENT)
    driver = webdriver.Chrome(options=options)
    url = "https://www.pixiv.net"

    driver.get(url)

    # Cookie読み込み
    cookies = pickle.load(open(COOKIES_FILE, "rb"))
    [driver.add_cookie(cookie) for cookie in cookies]
    driver.get(url)

    url = "https://www.pixiv.net/users/200469/bookmarks/artworks"

    xpathes = {
        "bookmark": '//*[@id="root"]/div[2]/div/div[3]/div/div/div[2]/div[3]/div[2]/div/section/div[1]/div[2]/div/span/span',
        "select_all": '//*[@id="root"]/div[2]/div/div[3]/div/div/div[2]/div[3]/div[2]/div/section/div[3]/div/div[1]/div[1]',
        "hide": '//*[@id="root"]/div[2]/div/div[3]/div/div/div[2]/div[3]/div[2]/div/section/div[3]/div/div[1]/div[4]/div/div',
        "length": '//*[@id="root"]/div[2]/div/div[3]/div/div/div[2]/div[3]/div[2]/div/section/div[1]/div/div/div/div/span',
    }

    for i in tqdm(range(100)):
        driver.get(url)
        sleep(1)
        length = driver.find_element(By.XPATH, xpathes["length"]).text
        length = int(re.sub(",", "", length))
        if length < 30:
            break
        driver.find_element(By.XPATH, xpathes["bookmark"]).click()
        driver.find_element(By.XPATH, xpathes["select_all"]).click()
        driver.find_element(By.XPATH, xpathes["hide"]).click()

    driver.quit()


def hide_follow():
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    # options.add_argument("--user-agent=" + USER_AGENT)
    driver = webdriver.Chrome(options=options)
    url = "https://www.pixiv.net"

    driver.get(url)

    # Cookie読み込み
    cookies = pickle.load(open(COOKIES_FILE, "rb"))
    [driver.add_cookie(cookie) for cookie in cookies]
    driver.get(url)

    url = "https://www.pixiv.net/users/200469/following"
    xpathes = {
        "three1": "",
        "hide": "/html/body/div[6]/div/div/div/div/div[2]",
    }
    driver.get(url)
    sleep(1)
    for _ in tqdm(range(1000)):
        for i in range(2, 10):
            xpath = f'//*[@id="root"]/div[2]/div/div[3]/div/div/div[2]/div[2]/div[2]/div/section/div[2]/div[1]/div/div[1]/div/div/div[{i}]/div/div/pixiv-icon'
            try:
                driver.find_element(By.XPATH, xpath).click()
                sleep(0.5)
                driver.find_element(By.XPATH, xpathes["hide"]).click()
                sleep(1)
                break
            except:
                pass


def main():
    # make_login()
    # hide_bookmark()
    hide_follow()


if __name__ == "__main__":
    main()
