import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Fixture setup
@pytest.fixture
def setup():
    driver = webdriver.Chrome()  # Cần cài ChromeDriver sẵn
    driver.maximize_window()
    yield driver
    driver.quit()

# Test case: Login thành công
def test_login_valid(setup):
    driver = setup
    driver.get("https://opensource-demo.orangehrmlive.com/")

    # Nhập username và password đúng
    driver.find_element(By.NAME, "username").send_keys("Admin")
    driver.find_element(By.NAME, "password").send_keys("admin123")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Kiểm tra có vào Dashboard chưa
    assert "Dashboard" in driver.page_source

# Test case: Login sai
def test_login_invalid(setup):
    driver = setup
    driver.get("https://opensource-demo.orangehrmlive.com/")

    driver.find_element(By.NAME, "username").send_keys("WrongUser")
    driver.find_element(By.NAME, "password").send_keys("WrongPass")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Kiểm tra thông báo lỗi
    error_text = driver.find_element(By.CLASS_NAME, "oxd-alert-content-text").text
    assert "Invalid credentials" in error_text
