#座標取得用
import pyautogui
#ブラウザ開く用
from selenium import webdriver


#ウィンドウサイズ調整
driver = webdriver.Chrome("/usr/local/bin/chromedriver")
driver.set_window_position(1000,0)
driver.set_window_size(950,1150)
driver.get("https://www.google.co.jp")
print("進むボタンにカーソルを合わせてo+ENTERを押してください")
key1 = input()
if key1 == "o":
    next_x, next_y  = pyautogui.position()
    print(pyautogui.position())
    print("戻るボタンにカーソルを合わせてo+ENTERを押してください")
    key2 = input()
    if key2 == "o":
        back_x, back_y = pyautogui.position()
        print(pyautogui.position())
        print("上矢印にカーソルを合わせてo+ENTERを押してください")
        key3 = input()
        if key3 == "o":
            up_x, up_y = pyautogui.position()
            print(pyautogui.position())
            print("下矢印にカーソルを合わせてo+ENTERを押してください")
            key4 = input()
            if key4 == "o":
                down_x, down_y = pyautogui.position()
                print(pyautogui.position())

                f = open('searchconst.txt', mode='w')
                f.write("{}\n".format(next_x))
                f.write("{}\n".format(next_y))
                f.write("{}\n".format(back_x))
                f.write("{}\n".format(back_y))
                f.write("{}\n".format(up_x))
                f.write("{}\n".format(up_y))
                f.write("{}\n".format(down_x))
                f.write("{}\n".format(down_y))
                f.close()