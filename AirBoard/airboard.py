import cv2

#自分で作った関数
import func

#ブラウザ開く用
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
options = Options()
options.add_argument('--autoplay-policy=no-user-gesture-required')

# For webcam input:
cap = cv2.VideoCapture(0)

mode = "hand"
app = "movie"
change = "app"

driver = webdriver.Chrome("/usr/local/bin/chromedriver", chrome_options = options)
driver.set_window_position(1000,0)
driver.set_window_size(950,1150)

while(1):
  #ハンドモード
  if mode == "hand":
    mode, app, change = func.hand(cap, driver, app, change)
  #キーボードモード
  elif mode == "keyboard":
    mode, app, change = func.keyboard(cap,driver, app)