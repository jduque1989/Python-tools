from selenium import webdriver
import time 
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-software-rasterizer')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=Options)

driver.get("https://dermalife.co")
print(driver.title)
driver.quit()

