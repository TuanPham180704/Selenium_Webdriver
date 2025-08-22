from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert
import time

driver = webdriver.Chrome()
driver.get("https://www.w3schools.com/tags/tryit.asp?filename=tryhtml_input_test")

driver.switch_to.frame("iframeResult")             
name_box = driver.find_element(By.NAME, "fname")    
name_box.send_keys("Tuan Dev")

select = Select(driver.find_element(By.NAME, "cars")) 
select.select_by_visible_text("Volvo")

driver.find_element(By.XPATH, "//input[@type='submit']").click()
time.sleep(2)
print(driver.get_cookies())  
driver.quit()
