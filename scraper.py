import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from constants import *


def initialize_driver():
    browser = webdriver.Chrome()
    browser.maximize_window()
    wait = WebDriverWait(browser, 30)
    return browser, wait


def login_twitter(browser, wait):
    browser.get("https://twitter.com/login")
    print("waiting for the browser to load...")
    time.sleep(5)
    print("starting...")

    email_input = wait.until(
        EC.visibility_of_element_located((By.NAME, "text")))
    email_input.send_keys('razudira282@gmail.com')

    next_button = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//span[text()='Next']")))
    next_button.click()

    time.sleep(2)

    uname_input = wait.until(
        EC.visibility_of_element_located((By.NAME, "text")))
    uname_input.send_keys('benibokenda')

    next_button = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//span[text()='Next']")))
    next_button.click()

    password_input = wait.until(
        EC.visibility_of_element_located((By.NAME, "password")))
    password_input.send_keys('bethecoolguyya')

    login_button = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//span[text()='Log in']")))
    login_button.click()

    time.sleep(5)


def search(browser, username):
    # go to the user profile page
    base_url = u'https://twitter.com'
    url = f'{base_url}/{username}'

    browser.get(url)
    time.sleep(1)

    body = browser.find_element(By.TAG_NAME, 'body')

    while True:
        body.send_keys(Keys.PAGE_DOWN)

        tweet_contents = browser.find_elements(By.XPATH, TWEET_CONTENT_TEXT)
        print(
            f'number of tweet content containers found: {len(tweet_contents)}')
        for t in tweet_contents:
            print(f'<[[tweet]]: {t.text}>')

        tweet_unames = browser.find_elements(By.XPATH, TWEET_USERNAME_TEXT)
        print(f'number of tweet uname found: {len(tweet_unames)}')
        for t in tweet_unames:
            print(f'<[[posted by user]]: {t.text}>')

        time.sleep(2)


def run(config):
    browser, wait = initialize_driver()
    login_twitter(browser, wait)
    search(browser, config.Username)
