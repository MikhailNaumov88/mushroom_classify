from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config import DRIVER_PATH

options = Options()

options.headless = True

driver = webdriver.Chrome(DRIVER_PATH , options=options)

driver.get("https://google.com/")
print(driver.title)
driver.quit()