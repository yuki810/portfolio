#座標取得用
import pyautogui
#コマンド実行用
import subprocess


#ウィンドウサイズ調整
pyautogui.click(32, 110)
subprocess.run(["wmctrl", "-i", "-r", "0x04800002", "-e", "0,1027,0,893,1050"])
#座標取得
print("再生ボタンにカーソルを合わせてo+ENTERを押してください")
key1 = input()
if key1 == "o":
    playbutton_x, playbutton_y  = pyautogui.position()
    print(pyautogui.position())
    print("進むボタンにカーソルを合わせてo+ENTERを押してください")
    key2 = input()
    if key2 == "o":
        nextbutton_x, nextbutton_y = pyautogui.position()
        print(pyautogui.position())
        print("戻るボタンにカーソルを合わせてo+ENTERを押してください")
        key3 = input()
        if key3 == "o":
            backbutton_x, backbutton_y = pyautogui.position()
            print(pyautogui.position())
            print("検索ボタンにカーソルを合わせてo+ENTERを押してください")
            key4 = input()
            if key4 == "o":
                searchbutton_x, searchbutton_y = pyautogui.position()
                print(pyautogui.position())
                print("検索バーにカーソルを合わせてo+ENTERを押してください")
                key5 = input()
                if key5 == "o":
                    searchbar_x, searchbar_y = pyautogui.position()
                    print(pyautogui.position())
                    print("検索バーの消去ボタンにカーソルを合わせてo+ENTERを押してください")
                    key6 = input()
                    if key6 == "o":
                        searchdelete_x, searchdelete_y = pyautogui.position()
                        print(pyautogui.position())
                        print("検索候補の再生ボタンにカーソルを合わせてo+ENTERを押してください")
                        key7 = input()
                        if key7 == "o":
                            firstsearch_x, firstsearch_y = pyautogui.position()
                            print(pyautogui.position())
                            print("musicアイコンにカーソルを合わせてo+ENTERを押してください")
                            key7 = input()
                            if key7 == "o":
                                aicon_x, aicon_y = pyautogui.position()
                                print(pyautogui.position())
                                f = open('musicconst.txt', mode='w')
                                f.write("{}\n".format(playbutton_x))
                                f.write("{}\n".format(playbutton_y))
                                f.write("{}\n".format(nextbutton_x))
                                f.write("{}\n".format(nextbutton_y))
                                f.write("{}\n".format(backbutton_x))
                                f.write("{}\n".format(backbutton_y))
                                f.write("{}\n".format(searchbutton_x))
                                f.write("{}\n".format(searchbutton_y))
                                f.write("{}\n".format(searchbar_x))
                                f.write("{}\n".format(searchbar_y))
                                f.write("{}\n".format(searchdelete_x))
                                f.write("{}\n".format(searchdelete_y))
                                f.write("{}\n".format(firstsearch_x))
                                f.write("{}\n".format(firstsearch_y))
                                f.write("{}\n".format(aicon_x))
                                f.write("{}\n".format(aicon_y))
                                f.close()