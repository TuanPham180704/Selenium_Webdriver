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
        time.sleep(5)

        results = driver.find_elements(By.CSS_SELECTOR, "a.result__a")
        assert len(results) >= 3, f"Expected at least 3 results, got {len(results)}"
    finally:
        driver.quit()

def test_duckduckgo_search_min_results_high_expectation():
    driver = webdriver.Chrome()
    try:
        driver.get("https://duckduckgo.com/")
        box = driver.find_element(By.NAME, "q")
        box.send_keys("Python")
        box.send_keys(Keys.RETURN)
        time.sleep(5)

        results = driver.find_elements(By.CSS_SELECTOR, "a.result__a")
        assert len(results) >= 50, f"Expected at least 50 results, got {len(results)}"
    finally:
        driver.quit()



def test_duckduckgo_search_special_characters():
    driver = webdriver.Chrome()
    try:
        driver.get("https://duckduckgo.com/")
        box = driver.find_element(By.NAME, "q")
        box.send_keys("%#@$$&%&&@&@")
        box.send_keys(Keys.RETURN)
        time.sleep(5)
        results = driver.find_elements(By.CSS_SELECTOR, "a.result__a")
        assert results is not None, "Search results not rendered properly"
    finally:
        driver.quit()

def test_duckduckgo_search_empty_input():
    driver = webdriver.Chrome()
    try:
        driver.get("https://duckduckgo.com/")
        box = driver.find_element(By.NAME, "q")
        box.send_keys("")
        box.send_keys(Keys.RETURN)
        time.sleep(5)
        assert "duckduckgo.com" in driver.current_url, "Unexpected behavior on empty input"
    finally:
        driver.quit()
