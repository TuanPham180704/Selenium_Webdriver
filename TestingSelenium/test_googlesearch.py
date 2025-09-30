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
def test_duckduckgo_logo_visible():
    driver = webdriver.Chrome()
    try:
        driver.get("https://duckduckgo.com/")
        logo = driver.find_element(By.CLASS_NAME, "header__logo")
        assert logo.is_displayed(), "Logo not visible on homepage"
    finally:
        driver.quit()


def test_duckduckgo_title_contains_keyword():
    driver = webdriver.Chrome()
    try:
        driver.get("https://duckduckgo.com/")
        query = "OpenAI"
        box = driver.find_element(By.NAME, "q")
        box.send_keys(query)
        box.send_keys(Keys.RETURN)
        time.sleep(5)
        assert query.lower() in driver.title.lower(), "Page title does not contain search query"
    finally:
        driver.quit()


def test_duckduckgo_first_result_clickable():
    driver = webdriver.Chrome()
    try:
        driver.get("https://duckduckgo.com/")
        box = driver.find_element(By.NAME, "q")
        box.send_keys("GitHub")
        box.send_keys(Keys.RETURN)
        time.sleep(5)
        first_result = driver.find_element(By.CSS_SELECTOR, "a.result__a")
        assert first_result.is_displayed() and first_result.is_enabled(), "First result is not clickable"
    finally:
        driver.quit()



def test_duckduckgo_back_navigation():
    driver = webdriver.Chrome()
    try:
        driver.get("https://duckduckgo.com/")
        box = driver.find_element(By.NAME, "q")
        box.send_keys("ReactJS")
        box.send_keys(Keys.RETURN)
        time.sleep(5)
        driver.back()
        time.sleep(5)
        assert "duckduckgo.com" in driver.current_url, "Back navigation did not return to DuckDuckGo"
    finally:
        driver.quit()


def test_duckduckgo_long_query():
    driver = webdriver.Chrome()
    try:
        driver.get("https://duckduckgo.com/")
        long_query = "a" * 1000
        box = driver.find_element(By.NAME, "q")
        box.send_keys(long_query)
        box.send_keys(Keys.RETURN)
        time.sleep(5)
        assert "q=" in driver.current_url, "Long query did not process correctly"
    finally:
        driver.quit()


def test_duckduckgo_instant_suggestions():
    driver = webdriver.Chrome()
    try:
        driver.get("https://duckduckgo.com/")
        box = driver.find_element(By.NAME, "q")
        box.send_keys("Python")
        time.sleep(5)
        suggestions = driver.find_elements(By.CSS_SELECTOR, ".search__autocomplete .acp")
        assert len(suggestions) > 0, "No instant suggestions appeared"
    finally:
        driver.quit()