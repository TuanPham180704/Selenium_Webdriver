
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def test_duckduckgo_search_success():
    driver = webdriver.Chrome()
    try:
        driver.get("https://duckduckgo.com/")
        box = driver.find_element(By.NAME, "q")
        box.send_keys("Selenium WebDriver Python")
        box.send_keys(Keys.RETURN)
        time.sleep(8)
        results = driver.find_elements(By.CSS_SELECTOR, "a.result__a")
        assert len(results) >= 3
    finally:
        driver.quit()

def test_duckduckgo_search_failure():
    driver = webdriver.Chrome()
    try:
        driver.get("https://duckduckgo.com/")
        box = driver.find_element(By.NAME, "q")
        box.send_keys("asdasdasd1234567890!@#$")
        box.send_keys(Keys.RETURN)
        time.sleep(8)     
        results = driver.find_elements(By.CSS_SELECTOR, "a.result__a")
        assert len(results) < 0, f"Expected negative results, got {len(results)}"
    finally:
        driver.quit()


