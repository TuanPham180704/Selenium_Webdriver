import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class TestFacebookLogin(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def test_login_invalid(self):
        driver = self.driver
        driver.get("https://www.facebook.com/")

        # Nhập email và password sai
        driver.find_element(By.ID, "email").send_keys("phamtuan180704@gmail.com")
        driver.find_element(By.ID, "pass").send_keys("Tuandev18")
        driver.find_element(By.NAME, "login").click()

        time.sleep(3)  # chờ load

        # Kiểm tra thông báo lỗi xuất hiện
        self.assertTrue("The password that you've entered is incorrect" in driver.page_source 
                        or "Invalid username" in driver.page_source
                        or "mật khẩu bạn nhập" in driver.page_source)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()

time.sleep(10)
