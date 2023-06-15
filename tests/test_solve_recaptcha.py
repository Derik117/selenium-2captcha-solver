import json
import time

from pytest import MonkeyPatch
from selenium import webdriver
from selenium.webdriver.common.by import By
from twocaptcha import TwoCaptcha

import selenium_2captcha_solver
from selenium_2captcha_solver import solve_recaptchav2


def test_solve_recaptcha_success(
        two_captcha: TwoCaptcha,
        driver: webdriver.Chrome):
    driver.get('https://2captcha.com/demo/recaptcha-v2')
    recaptcha = driver.find_element(By.CLASS_NAME, 'g-recaptcha')
    solve_recaptchav2(two_captcha, driver, recaptcha)
    btn = driver.find_element(
        By.XPATH, '//*[@id="root"]/div/main/div/section/form/button[1]')
    btn.click()
    time.sleep(1)
    res = json.loads(driver.find_element(By.TAG_NAME, 'pre').text)
    assert res['success'], res


def test_solve_recaptcha_error(
        monkeypatch: MonkeyPatch,
        two_captcha: TwoCaptcha,
        driver: webdriver.Chrome):
    def mock_solve_captcha(*args, **kwargs):
        return {'code': 123}
    monkeypatch.setattr(
        selenium_2captcha_solver.solver,
        '_solve_captcha',
        mock_solve_captcha)
    driver.get('https://2captcha.com/demo/recaptcha-v2')
    recaptcha = driver.find_element(By.CLASS_NAME, 'g-recaptcha')
    solve_recaptchav2(two_captcha, driver, recaptcha)
    btn = driver.find_element(
        By.XPATH, '//*[@id="root"]/div/main/div/section/form/button[1]')
    btn.click()
    time.sleep(1)
    res = driver.find_element(By.TAG_NAME, 'aside').text
    assert res == 'reCAPTCHA solved incorrectly, please try again.'
