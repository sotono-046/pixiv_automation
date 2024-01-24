from selenium import webdriver
from selenium.webdriver.common.by import By
import pickle
from time import sleep
from tqdm import tqdm
from useragent_changer import UserAgent

COOKIES_FILE = "cookies.pkl"
USER_AGENT = UserAgent("chrome").set()


def make_login():
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--user-agent=" + USER_AGENT)
    driver = webdriver.Chrome(options=options)

    url = "https://www.pixiv.net"
    driver.get(url)

    msg = "ログインしたらEnter \n>"
    input(msg)

    # Cookie書き込み
    cookies = driver.get_cookies()
    pickle.dump(cookies, open(COOKIES_FILE, "wb"))

    driver.quit()


def get_login():
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--user-agent=" + USER_AGENT)
    driver = webdriver.Chrome(options=options)
    url = "https://www.pixiv.net"

    driver.get(url)

    # Cookie読み込み
    cookies = pickle.load(open(COOKIES_FILE, "rb"))
    [driver.add_cookie(cookie) for cookie in cookies]

    msg = "ログインできてたらEnter \n>"
    input(msg)

    url = "https://www.pixiv.net/users/200469/bookmarks/artworks"
    driver.get(url)

    xpathes = {
        "bookmark": '//*[@id="root"]/div[2]/div/div[3]/div/div/div[2]/div[3]/div[2]/div/section/div[1]/div[2]/div',
        "select_all": '//*[@id="root"]/div[2]/div/div[3]/div/div/div[2]/div[3]/div[2]/div/section/div[3]/div/div[1]/div[1]',
        "hide": '//*[@id="root"]/div[2]/div/div[3]/div/div/div[2]/div[3]/div[2]/div/section/div[3]/div/div[1]/div[4]/div/div',
    }

    for i in tqdm(range(10)):
        driver.find_element(By.XPATH, xpathes.bookmark).click
        sleep(2)
        driver.find_element(By.XPATH, xpathes.select_all).click
        sleep(2)
        driver.find_element(By.XPATH, xpathes.hide).click
        sleep(2)

    driver.quit()


def main():
    make_login()
    get_login()


if __name__ == "__main__":
    main()
