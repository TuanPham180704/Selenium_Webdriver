import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class PythonOrgSearch(unittest.TestCase):
    
    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_search_in_google_org(self):
        driver = self.driver
        driver.get("http://www.google.com")
        self.assertIn("Google",driver.title)
        elem = driver.find_element(By.NAME,"q")
        elem.send_keys("TuanDev")
        elem.send_keys(Keys.RETURN)
        self.assertNotIn("No result found.", driver.page_source)


    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
        
