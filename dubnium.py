import os
import time
import pyautogui
from selenium import webdriver
from selenium_stealth import stealth
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from anticaptchaofficial.recaptchav2proxyless import *
from webdriver_manager.chrome import ChromeDriverManager


options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)


def browser_work(login, password):
    pyautogui.moveTo(pyautogui.size()[0] // 2, pyautogui.size()[1] // 2)

    driver = webdriver.Chrome(options=options,
                              service=Service(ChromeDriverManager().install()))

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True)

    url = ''  # site link that I parsed
    driver.get(url)

    login_form = driver.find_element(By.ID, 'username')
    login_form.send_keys(login)

    password_form = driver.find_element(By.ID, 'password')
    password_form.send_keys(password)

    driver.execute_script("window.scrollTo(0, 650)")

    sitekey = driver.find_element(By.CLASS_NAME, 'g-recaptcha').get_attribute('data-sitekey')

    solver = recaptchaV2Proxyless()
    solver.set_verbose(1)
    solver.set_key('secret-key')
    solver.set_website_url(url)
    solver.set_website_key(sitekey)

    g_response = solver.solve_and_return_solution()

    if g_response != 0:
        driver.execute_script(f"document.getElementById('g-recaptcha-response').innerHTML = '{g_response}'")
        driver.find_element(By.XPATH, '//*[@id="create"]/div/button').click()
        time.sleep(2)
        try:
            driver.find_element(By.XPATH, '//*[@id="layoutDefault_content"]/main/section[1]/div[1]/div/div[1]/h3')
            return 1  # captcha solved successfully
        except Exception:
            return 2  # repeat algorithm

    else:
        return solver.error_code


def create_user(login, password):
    return browser_work(login, password)


def data_update(path, new_path):
    data = logs = errors = ''
    today = '.'.join(datetime.now().strftime("%d %m").split())

    with open(path, 'r') as file:
        for line in file:
            login = line.split()[0]
            password = line.split()[1]

            result = browser_work(login, password)

            attempts = 1

            while result == 2 and attempts <= 3:
                time.sleep(10)
                result = browser_work(login, password)
                attempts += 1

            if result == 1:
                data += f'{login} {password}\n'
                logs += f'{login} {password} <---> successfully updated\n'
            else:
                logs += f'{login} {password} <---> error\n'
                errors += f'{login} {password} {today}\n'

    with open(f'D:/database/logs.txt', 'a') as log_file:
        log_file.write(logs)

    if len(errors) > 0:
        with open(f'D:/database/errors.txt', 'a') as err_file:
            err_file.write(errors)

    with open(new_path, 'a') as data_file:
        data_file.write(data)


def fix_errors():
    data = errors = ''
    today = '.'.join(datetime.now().strftime("%d %m").split())
    hour = int(time.strftime("%H", time.localtime()))
    path = 'D:/database/errors.txt'

    with open(path, 'r') as file:
        for line in file:
            login = line.split()[0]
            password = line.split()[1]
            result = create_user(login, password)
            if result == 1:
                data += f'{login} {password}\n'
            else:
                errors += f'{login} {password} {today}\n'

    if len(errors) > 0:
        with open(path, 'w') as file:
            file.write(errors)
    else:
        os.remove(path)

    if hour >= 20:
        file_date = datetime.now() + timedelta(days=9)
    else:
        file_date = datetime.now() + timedelta(days=8)

    file_date = '.'.join(file_date.strftime("%d %m").split())

    with open(f'D:/database/{file_date}.txt', 'a') as file:
        file.write(data)

    return len(errors)
