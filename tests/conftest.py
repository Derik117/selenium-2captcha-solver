import pytest
from dotenv import dotenv_values
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from twocaptcha import TwoCaptcha

CONFIG = dotenv_values()


@pytest.fixture
def driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument("--headless=new")
    return webdriver.Chrome(options=options)


@pytest.fixture
def two_captcha() -> TwoCaptcha:
    api_key = CONFIG.get('2CAPTCHA_API_KEY')
    if api_key is None:
        raise AttributeError("Please specify 2CAPTCHA_API_KEY in env")
    return TwoCaptcha(apiKey=api_key)
