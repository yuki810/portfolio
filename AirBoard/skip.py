#ブラウザ開く用
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
options = Options()
options.add_argument('--autoplay-policy=no-user-gesture-required')

#ブラウザ開く用
from telnetlib import EC
import chromedriver_binary
# ChromeOptionsを設定
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

driver = webdriver.Chrome("/usr/local/bin/chromedriver", chrome_options = options)
driver.set_window_position(1000,0)
driver.set_window_size(950,1150) 
driver.get("https://www.youtube.com/")

while(True):     
    if len(driver.find_elements_by_class_name('ytp-ad-skip-button-container')) > 0:
        if driver.find_element_by_class_name('ytp-ad-skip-button-container').get_attribute('style') != "display: none;":
            driver.find_element_by_class_name('ytp-ad-skip-button').click()