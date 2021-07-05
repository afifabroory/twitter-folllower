import sys
import time
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def login(driver, login_method=[], password=''):

    if (password == '') or (len(login_method) == 0):
        driver.quit()
        sys.exit('login(): login_method and password argument cannot empty!')
    elif len(login_method) > 3:
        driver.quit()
        sys.exit(f'login(): login_method length expected max 3, but {len(login_method)} were given!')

    is_success = lambda driver: not re.search('.*email_disabled.*', driver.current_url)
    is_login_url = lambda driver, LOGIN_URL: re.search(f'^{LOGIN_URL}$', driver.current_url)

    LOGIN_SELECTOR = 'div.css-1dbjc4n:nth-child({0})>label:nth-child(1)>div:nth-child(1)'\
               '>div:nth-child(2)>div:nth-child(1)>input:nth-child(1)'
    LOGIN_URL = 'https://twitter.com/login' 

    while True:
        if is_login_url(driver, LOGIN_URL) == None and is_success(driver):
            driver.get(LOGIN_URL)
            continue

        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, LOGIN_SELECTOR.format(6))))

        username_field = driver.find_element_by_css_selector(LOGIN_SELECTOR.format(6))
        password_field = driver.find_element_by_css_selector(LOGIN_SELECTOR.format(7))
        
        username_field.send_keys(login_method[0])
        password_field.send_keys(password)

        driver.find_element_by_css_selector('div.css-18t94o4').click() # Login button

        if is_success(driver): break
        elif len(login_method) == 0: 
            driver.quit()
            sys.exit('login(): Failed to login by given method')
        
        login_method.pop(0)
        time.sleep(3)

def get_follower(driver, username=''):

    if username == '':
        driver.quit()
        sys.exit('get_follower(): username cannot empty string!')

    TWITTER_URL = f'https://twitter.com/{username}/followers'
    driver.get(TWITTER_URL)
    
    FOLLOWER_LIST = ('div>div>div:nth-child(2)>'
                    'section>div:nth-child(2)>div>div')
    FOLLOWER_SELECTOR = FOLLOWER_LIST + (':nth-child({})>div>div>div>' 
        'div:nth-child(2)>div>div>a>div>div:nth-child(2)>div>span')
    
    USER_LIST = []
    while len(USER_LIST) <= 1000:
        WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, FOLLOWER_SELECTOR.format(10))))
        total = len(driver.find_elements_by_css_selector(FOLLOWER_LIST)) # Return follower list 
        
        for i in range(1, total+1):
            try:
                user = driver.find_element_by_css_selector(FOLLOWER_SELECTOR.format(i))
                USER_LIST.append(user.text)
            except:
                break

            
        driver.execute_script('window.scrollTo(scrollY, scrollMaxY/1.15)')
        time.sleep(5)

        if len(USER_LIST)%100 == 0: time.sleep(900)


    os.system('cls')
    return USER_LIST

import os
os.system('cls')

with webdriver.Firefox() as driver:
    login(driver) 
    print(get_follower(driver))
    driver.quit()