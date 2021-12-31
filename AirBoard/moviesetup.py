#座標取得用
import pyautogui
#ブラウザ開く用
from selenium import webdriver

#多分いらん
#ウィンドウサイズ調整
driver = webdriver.Chrome("/usr/local/bin/chromedriver")
driver.set_window_position(1000,0)
driver.set_window_size(950,1150)
driver.get("https://www.youtube.com/")
#座標取得
print("再生ボタンにカーソルを合わせてo+ENTERを押してください")
key1 = input()
if key1 == "o":
    playbutton_x, playbutton_y  = pyautogui.position()
    print(pyautogui.position())
    #print("検索バーにカーソルを合わせてo+ENTERを押してください")
    key2 = input()
    if key2 == "o":
        searchbar_x, searchbar_y = pyautogui.position()
        print(pyautogui.position())
        #print("一番最初の検索候補にカーソルを合わせてo+ENTERを押してください")
        key3 = input()
        if key3 == "o":
            firstsearch_x, firstsearch_y = pyautogui.position()
            print(pyautogui.position())
            print("アイコンにカーソルを合わせてo+ENTERを押してください")
            key3 = input()
            if key3 == "o":
                aicon_x, aicon_y = pyautogui.position()
                print(pyautogui.position())

                f = open('movieconst.txt', mode='w')
                f.write("{}\n".format(playbutton_x))
                f.write("{}\n".format(playbutton_y))
                f.write("{}\n".format(searchbar_x))
                f.write("{}\n".format(searchbar_y))
                f.write("{}\n".format(firstsearch_x))
                f.write("{}\n".format(firstsearch_y))
                f.write("{}\n".format(aicon_x))
                f.write("{}\n".format(aicon_y))
                f.close()