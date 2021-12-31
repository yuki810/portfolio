import cv2
import mediapipe as mp
import numpy
import time

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

#マウス・キーボード操作
import pyautogui
#pyautogui.PAUSE = 1
#検索入力・日本語用
import pyperclip
#コマンド実行用
import subprocess

#ブラウザ開く用
from telnetlib import EC
from selenium import webdriver
import chromedriver_binary
# ChromeOptionsを設定
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

#import psutil
#psutil.Process().nice(psutil.IDLE_PRIORITY_CLASS)
from threading import Timer

#定数
import const as C

#ひらがな表と濁点表のイメージを返す
def keyboard(cap, driver, app):
  staycount = 0
  text = ""
  urllist = []
  prev = [0,0]
  keyboardtype = "hiragana"
  flag = "stop"
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)

  appconst = []
  if app == "movie":
    appconst = C.movieconst
  elif app == "music":
    appconst = C.musicconst
  elif app == "search":
    appconst = C.searchconst

  with mp_hands.Hands(
      model_complexity=0,
      min_detection_confidence=0.7,
      min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
      #VideoCaptureオブジェクトのread()メソッドで動画のフレーム（コマ）をNumPy配列ndarrayとして取得できる。
      success, image = cap.read()
      subimage = numpy.copy(image)
      smallimage = numpy.copy(image)
      bigimage = numpy.copy(image)
      numimage = numpy.copy(image)

      if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        continue

      # To improve performance, optionally mark the image as not writeable to
      # pass by reference.
      image.flags.writeable = False
      image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
      results = hands.process(image)
      
      # Draw the hand annotations on the image.
      image.flags.writeable = True
      image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
      s = image.shape[:2]

      if app == "movie":
        if len(driver.find_elements_by_class_name('ytp-ad-skip-button-container')) > 0:
          if driver.find_element_by_class_name('ytp-ad-skip-button-container').get_attribute('style') != "display: none;":
            driver.find_element_by_class_name('ytp-ad-skip-button').click()
      
      #画面
      #ひらがな表
      hiraganaimage=cv2.imread("hiragana.png")
      image=cv2.addWeighted(image,0.3,cv2.flip(cv2.resize(hiraganaimage, dsize=(960, 540)),1),0.3,0)
      cv2.rectangle(image, pt1=(s[1]//12,s[0]//7), pt2=(s[1]*11//12, s[0]*6//7), color = (0,255,255), thickness = 1, lineType = 8,shift = 0)
      for i in range(2, 11):
        cv2.line(image, pt1=(s[1]*i//12,s[0]//7), pt2=(s[1]*i//12, s[0]*6//7), color = (0,255,255), thickness = 1, lineType = 8,shift = 0)
      for j in range(2, 6):
        cv2.line(image, (s[1]//12,s[0]*j//7), (s[1]*11//12, s[0]*j//7), (0,255,255), 1, 8, 0)
      #濁点ver
      dakutenimage=cv2.imread("dakuten.png")
      subimage=cv2.addWeighted(subimage,0.3,cv2.flip(cv2.resize(dakutenimage, dsize=(960, 540)),1),0.3,0)
      cv2.rectangle(subimage, pt1=(s[1]//12,s[0]//7), pt2=(s[1]*11//12, s[0]*6//7), color = (0,255,255), thickness = 1, lineType = 8,shift = 0)
      for i in range(2, 11):
        cv2.line(subimage, pt1=(s[1]*i//12,s[0]//7), pt2=(s[1]*i//12, s[0]*6//7), color = (0,255,255), thickness = 1, lineType = 8,shift = 0)
      for j in range(2, 6):
        cv2.line(subimage, (s[1]//12,s[0]*j//7), (s[1]*11//12, s[0]*j//7), (0,255,255), 1, 8, 0)
      #小文字
      alphabetsmallimage=cv2.imread("alphabet_small.png")
      smallimage=cv2.addWeighted(smallimage,0.3,cv2.flip(cv2.resize(alphabetsmallimage, dsize=(960, 540)),1),0.3,0)
      cv2.rectangle(smallimage, pt1=(s[1]//12,s[0]//7), pt2=(s[1]*11//12, s[0]*6//7), color = (0,255,255), thickness = 1, lineType = 8,shift = 0)
      for i in range(2, 11):
        cv2.line(smallimage, pt1=(s[1]*i//12,s[0]//7), pt2=(s[1]*i//12, s[0]*6//7), color = (0,255,255), thickness = 1, lineType = 8,shift = 0)
      for j in range(2, 6):
        cv2.line(smallimage, (s[1]//12,s[0]*j//7), (s[1]*11//12, s[0]*j//7), (0,255,255), 1, 8, 0)
      #大文字
      alphabetbigimage=cv2.imread("alphabet_big.png")
      bigimage=cv2.addWeighted(bigimage,0.3,cv2.flip(cv2.resize(alphabetbigimage, dsize=(960, 540)),1),0.3,0)
      cv2.rectangle(bigimage, pt1=(s[1]//12,s[0]//7), pt2=(s[1]*11//12, s[0]*6//7), color = (0,255,255), thickness = 1, lineType = 8,shift = 0)
      for i in range(2, 11):
        cv2.line(bigimage, pt1=(s[1]*i//12,s[0]//7), pt2=(s[1]*i//12, s[0]*6//7), color = (0,255,255), thickness = 1, lineType = 8,shift = 0)
      for j in range(2, 6):
        cv2.line(bigimage, (s[1]//12,s[0]*j//7), (s[1]*11//12, s[0]*j//7), (0,255,255), 1, 8, 0)

      #number
      #numberimage=cv2.imread("number.png")
      numberimage=cv2.imread("alphabet_small.png")
      numimage=cv2.addWeighted(numimage,0.3,cv2.flip(cv2.resize(numberimage, dsize=(960, 540)),1),0.3,0)
      cv2.rectangle(numimage, pt1=(s[1]//12,s[0]//7), pt2=(s[1]*11//12, s[0]*6//7), color = (0,255,255), thickness = 1, lineType = 8,shift = 0)
      for i in range(2, 11):
        cv2.line(numimage, pt1=(s[1]*i//12,s[0]//7), pt2=(s[1]*i//12, s[0]*6//7), color = (0,255,255), thickness = 1, lineType = 8,shift = 0)
      for j in range(2, 6):
        cv2.line(numimage, (s[1]//12,s[0]*j//7), (s[1]*11//12, s[0]*j//7), (0,255,255), 1, 8, 0)

      if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
          #普通のひらがな表
          if keyboardtype == "hiragana":
            #指のポインタ
            cv2.circle(image, (int(hand_landmarks.landmark[8].x*s[1]), int(hand_landmarks.landmark[8].y*s[0])), 10, (0,0,255), thickness=-1, lineType=cv2.LINE_8, shift=0)
            #指の動きに応じて文字選択
            for i in range(0,12):
              for j in range(0,6):
                if s[1]*i/12 <= hand_landmarks.landmark[8].x*s[1] and hand_landmarks.landmark[8].x*s[1] <= s[1]*(i+1)/12 and s[0]*j/7 <= hand_landmarks.landmark[8].y*s[0] and hand_landmarks.landmark[8].y*s[0] <= s[0]*(j+1)/7:
                  if (j != 0 and i != 0) or (j==0 and i==0) or (j==0 and i==11):
                    cv2.rectangle(image, pt1=(s[1]*i//12,s[0]*j//7), pt2=(s[1]*(i+1)//12, s[0]*(j+1)//7), color = (0,0,255), thickness = 1, lineType = 8,shift = 0)
                    if i == prev[0] and j == prev[1]:
                      staycount += 1
                    else:
                      staycount = 0
                    prev = [i, j]
                    #数秒滞在したら文字を取得・操作
                    if staycount > 20:
                      cv2.rectangle(image, pt1=(s[1]*i//12,s[0]*j//7), pt2=(s[1]*(i+1)//12, s[0]*(j+1)//7), color = (0,0,255), thickness = 4, lineType = 8,shift = 0)
                      if j == 0 and i == 0:
                        return "hand", app, "mode"
                      elif j== 0 and i == 11:
                        keyboardtype = "alphabet_small"
                      elif C.hiragana[i-1][j-1] == "濁点":
                        keyboardtype = "dakuten"
                      elif C.hiragana[i-1][j-1] == "DELETE":
                        text = text[:-1]
                      elif C.hiragana[i-1][j-1] == "ENTER":
                        if app == "movie":
                          search_bar = driver.find_element_by_name("search_query")
                          search_bar.click()
                          pyautogui.hotkey('ctrl', 'a')
                          pyautogui.press('delete')
                          search_bar.send_keys(text)
                          search_bar.submit()
                          count = 1
                          for elem_a in driver.find_elements_by_xpath('//a'):
                            if elem_a.get_attribute('id') == "video-title":
                              urllist.append(elem_a.get_attribute('href'))
                              print('{}:{}'.format(count, elem_a.get_attribute('title')))
                              count += 1
                            if count > 5:
                              break
                          keyboardtype = "number"
                          #driver.get(urllist[0])
                          text = ""
                        elif app == "music":
                          pyautogui.click(appconst[6], appconst[7])
                          pyautogui.click(appconst[8], appconst[9])
                          pyautogui.hotkey('ctrl', 'a')
                          pyautogui.press('delete')
                          pyperclip.copy(text)
                          pyautogui.hotkey('ctrl', 'v')
                          pyautogui.press('enter')
                          text = ""
                        elif app == "search":
                          search_bar = driver.find_element_by_name("q")
                          search_bar.click()
                          pyautogui.hotkey('ctrl', 'a')
                          pyautogui.press('delete')
                          search_bar.send_keys(text)
                          search_bar.submit()
                          count = 1
                          for elem_h3 in driver.find_elements_by_xpath('//a/h3'):
                            elem_a = elem_h3.find_element_by_xpath('..')
                            urllist.append(elem_a.get_attribute('href'))
                            print('{}:{}'.format(count, elem_h3.text))
                            count += 1
                          keyboardtype = "number"
                          #driver.get(urllist[0])
                          text = ""
                      else:
                        text += C.hiragana[i-1][j-1]
                      print(text)
                      staycount = 0
                    
          #濁点表
          elif keyboardtype == "dakuten":
            #指のポインタ
            cv2.circle(subimage, (int(hand_landmarks.landmark[8].x*s[1]), int(hand_landmarks.landmark[8].y*s[0])), 10, (0,0,255), thickness=-1, lineType=cv2.LINE_8, shift=0)
            #指の動きに応じて文字選択
            for i in range(0,12):
              for j in range(0,6):
                if s[1]*i/12 <= hand_landmarks.landmark[8].x*s[1] and hand_landmarks.landmark[8].x*s[1] <= s[1]*(i+1)/12 and s[0]*j/7 <= hand_landmarks.landmark[8].y*s[0] and hand_landmarks.landmark[8].y*s[0] <= s[0]*(j+1)/7:
                  if (j != 0 and i != 0) or (j==0 and i==0) or (j==0 and i==11):
                    cv2.rectangle(subimage, pt1=(s[1]*i//12,s[0]*j//7), pt2=(s[1]*(i+1)//12, s[0]*(j+1)//7), color = (0,0,255), thickness = 1, lineType = 8,shift = 0)
                    if i == prev[0] and j == prev[1]:
                      staycount += 1
                    else:
                      staycount = 0
                    prev = [i, j]
                    #クリックしたら文字を取得・操作
                    if staycount > 20:
                      cv2.rectangle(subimage, pt1=(s[1]*i//12,s[0]*j//7), pt2=(s[1]*(i+1)//12, s[0]*(j+1)//7), color = (0,0,255), thickness = 4, lineType = 8,shift = 0)
                      if j == 0 and i == 0:
                        return "hand", app, "mode"
                      elif j== 0 and i == 11:
                        keyboardtype = "alphabet_small"
                      elif C.dakuten[i-1][j-1] == "濁点":
                        keyboardtype = "hiragana"
                      elif C.dakuten[i-1][j-1] == "DELETE":
                        text = text[:-1]
                      elif C.dakuten[i-1][j-1] == "ENTER":
                        if app == "movie":
                          search_bar = driver.find_element_by_name("search_query")
                          search_bar.click()
                          pyautogui.hotkey('ctrl', 'a')
                          pyautogui.press('delete')
                          search_bar.send_keys(text)
                          search_bar.submit()
                          count = 1
                          for elem_a in driver.find_elements_by_xpath('//a'):
                            if elem_a.get_attribute('id') == "video-title":
                              urllist.append(elem_a.get_attribute('href'))
                              print('{}:{}'.format(count, elem_a.get_attribute('title')))
                              count += 1
                          keyboardtype = "number"
                          #driver.get(urllist[0])
                          text = ""
                        elif app == "music":
                          pyautogui.click(appconst[6], appconst[7])
                          pyautogui.click(appconst[8], appconst[9])
                          pyautogui.hotkey('ctrl', 'a')
                          pyautogui.press('delete')
                          pyperclip.copy(text)
                          pyautogui.hotkey('ctrl', 'v')
                          pyautogui.press('enter')
                          text = ""
                        elif app == "search":
                          search_bar = driver.find_element_by_name("q")
                          search_bar.click()
                          pyautogui.hotkey('ctrl', 'a')
                          pyautogui.press('delete')
                          search_bar.send_keys(text)
                          search_bar.submit()
                          count = 1
                          for elem_h3 in driver.find_elements_by_xpath('//a/h3'):
                            elem_a = elem_h3.find_element_by_xpath('..')
                            urllist.append(elem_a.get_attribute('href'))
                            print('{}:{}'.format(count, elem_h3.text))
                            count += 1
                          keyboardtype = "number"
                          #driver.get(urllist[0])
                          text = ""
                      else:
                        text += C.dakuten[i-1][j-1]
                      print(text)
                      staycount = 0

          #小文字
          elif keyboardtype == "alphabet_small":
            #指のポインタ
            cv2.circle(smallimage, (int(hand_landmarks.landmark[8].x*s[1]), int(hand_landmarks.landmark[8].y*s[0])), 10, (0,0,255), thickness=-1, lineType=cv2.LINE_8, shift=0)
            #指の動きに応じて文字選択
            for i in range(0,12):
              for j in range(0,6):
                if s[1]*i/12 <= hand_landmarks.landmark[8].x*s[1] and hand_landmarks.landmark[8].x*s[1] <= s[1]*(i+1)/12 and s[0]*j/7 <= hand_landmarks.landmark[8].y*s[0] and hand_landmarks.landmark[8].y*s[0] <= s[0]*(j+1)/7:
                  if (j != 0 and i != 0) or (j==0 and i==0) or (j==0 and i==11):
                    cv2.rectangle(smallimage, pt1=(s[1]*i//12,s[0]*j//7), pt2=(s[1]*(i+1)//12, s[0]*(j+1)//7), color = (0,0,255), thickness = 1, lineType = 8,shift = 0)
                    if i == prev[0] and j == prev[1]:
                      staycount += 1
                    else:
                      staycount = 0
                    prev = [i, j]
                    #クリックしたら文字を取得・操作
                    if staycount > 20:
                      cv2.rectangle(smallimage, pt1=(s[1]*i//12,s[0]*j//7), pt2=(s[1]*(i+1)//12, s[0]*(j+1)//7), color = (0,0,255), thickness = 4, lineType = 8,shift = 0)
                      if j == 0 and i == 0:
                        return "hand", app, "mode"
                      elif j== 0 and i == 11:
                        keyboardtype = "hiragana"
                      elif C.alphabet_small[i-1][j-1] == "大文字":
                        keyboardtype = "alphabet_big"
                      elif C.alphabet_small[i-1][j-1] == "DELETE":
                        text = text[:-1]
                      elif C.hiragana[i-1][j-1] == "ENTER":
                        if app == "movie":
                          search_bar = driver.find_element_by_name("search_query")
                          search_bar.click()
                          pyautogui.hotkey('ctrl', 'a')
                          pyautogui.press('delete')
                          search_bar.send_keys(text)
                          search_bar.submit()
                          count = 1
                          for elem_a in driver.find_elements_by_xpath('//a'):
                            if elem_a.get_attribute('id') == "video-title":
                              urllist.append(elem_a.get_attribute('href'))
                              print('{}:{}'.format(count, elem_a.get_attribute('title')))
                              count += 1
                          keyboardtype = "number"
                          #driver.get(urllist[0])
                          text = ""
                        elif app == "music":
                          pyautogui.click(appconst[6], appconst[7])
                          pyautogui.click(appconst[8], appconst[9])
                          pyautogui.hotkey('ctrl', 'a')
                          pyautogui.press('delete')
                          pyperclip.copy(text)
                          pyautogui.hotkey('ctrl', 'v')
                          pyautogui.press('enter')
                          text = ""
                        elif app == "search":
                          search_bar = driver.find_element_by_name("q")
                          search_bar.click()
                          pyautogui.hotkey('ctrl', 'a')
                          pyautogui.press('delete')
                          search_bar.send_keys(text)
                          search_bar.submit()
                          count = 1
                          for elem_h3 in driver.find_elements_by_xpath('//a/h3'):
                            elem_a = elem_h3.find_element_by_xpath('..')
                            urllist.append(elem_a.get_attribute('href'))
                            print('{}:{}'.format(count, elem_h3.text))
                            count += 1
                          keyboardtype = "number"
                          #driver.get(urllist[0])
                          text = ""
                      else:
                        text += C.alphabet_small[i-1][j-1]
                      print(text)
                      staycount = 0

          #大文字
          elif keyboardtype == "alphabet_big":
            #指のポインタ
            cv2.circle(bigimage, (int(hand_landmarks.landmark[8].x*s[1]), int(hand_landmarks.landmark[8].y*s[0])), 10, (0,0,255), thickness=-1, lineType=cv2.LINE_8, shift=0)
            #指の動きに応じて文字選択
            for i in range(0,12):
              for j in range(0,6):
                if s[1]*i/12 <= hand_landmarks.landmark[8].x*s[1] and hand_landmarks.landmark[8].x*s[1] <= s[1]*(i+1)/12 and s[0]*j/7 <= hand_landmarks.landmark[8].y*s[0] and hand_landmarks.landmark[8].y*s[0] <= s[0]*(j+1)/7:
                  if (j != 0 and i != 0) or (j==0 and i==0) or (j==0 and i==11):
                    cv2.rectangle(bigimage, pt1=(s[1]*i//12,s[0]*j//7), pt2=(s[1]*(i+1)//12, s[0]*(j+1)//7), color = (0,0,255), thickness = 1, lineType = 8,shift = 0)
                    if i == prev[0] and j == prev[1]:
                      staycount += 1
                    else:
                      staycount = 0
                    prev = [i, j]
                    #クリックしたら文字を取得・操作
                    if staycount > 20:
                      cv2.rectangle(bigimage, pt1=(s[1]*i//12,s[0]*j//7), pt2=(s[1]*(i+1)//12, s[0]*(j+1)//7), color = (0,0,255), thickness = 4, lineType = 8,shift = 0)
                      if j == 0 and i == 0:
                        return "hand", app, "mode"
                      elif j== 0 and i == 11:
                        keyboardtype = "hiragana"
                      elif C.alphabet_big[i-1][j-1] == "大文字":
                        keyboardtype = "alphabet_big"
                      elif C.alphabet_big[i-1][j-1] == "DELETE":
                        text = text[:-1]
                      elif C.hiragana[i-1][j-1] == "ENTER":
                        if app == "movie":
                          search_bar = driver.find_element_by_name("search_query")
                          search_bar.click()
                          pyautogui.hotkey('ctrl', 'a')
                          pyautogui.press('delete')
                          search_bar.send_keys(text)
                          search_bar.submit()
                          count = 1
                          for elem_a in driver.find_elements_by_xpath('//a'):
                            if elem_a.get_attribute('id') == "video-title":
                              urllist.append(elem_a.get_attribute('href'))
                              print('{}:{}'.format(count, elem_a.get_attribute('title')))
                              count += 1
                          keyboardtype = "number"
                          #driver.get(urllist[0])
                          text = ""
                        elif app == "music":
                          pyautogui.click(appconst[6], appconst[7])
                          pyautogui.click(appconst[8], appconst[9])
                          pyautogui.hotkey('ctrl', 'a')
                          pyautogui.press('delete')
                          pyperclip.copy(text)
                          pyautogui.hotkey('ctrl', 'v')
                          pyautogui.press('enter')
                          text = ""
                        elif app == "search":
                          search_bar = driver.find_element_by_name("q")
                          search_bar.click()
                          pyautogui.hotkey('ctrl', 'a')
                          pyautogui.press('delete')
                          search_bar.send_keys(text)
                          search_bar.submit()
                          count = 1
                          for elem_h3 in driver.find_elements_by_xpath('//a/h3'):
                            elem_a = elem_h3.find_element_by_xpath('..')
                            urllist.append(elem_a.get_attribute('href'))
                            print('{}:{}'.format(count, elem_h3.text))
                            count += 1
                          keyboardtype = "number"
                          #driver.get(urllist[0])
                          text = ""
                      else:
                        text += C.alphabet_big[i-1][j-1]
                      print(text)
                      staycount = 0
          #番号決め
          elif keyboardtype == "number":
            #指のポインタ
            cv2.circle(numimage, (int(hand_landmarks.landmark[8].x*s[1]), int(hand_landmarks.landmark[8].y*s[0])), 10, (0,0,255), thickness=-1, lineType=cv2.LINE_8, shift=0)
            #指の動きに応じて文字選択
            for i in range(0,12):
              for j in range(0,6):
                if s[1]*i/12 <= hand_landmarks.landmark[8].x*s[1] and hand_landmarks.landmark[8].x*s[1] <= s[1]*(i+1)/12 and s[0]*j/7 <= hand_landmarks.landmark[8].y*s[0] and hand_landmarks.landmark[8].y*s[0] <= s[0]*(j+1)/7:
                  if (j != 0 and i != 0) or (j==0 and i==0) or (j==0 and i==11):
                    cv2.rectangle(numimage, pt1=(s[1]*i//12,s[0]*j//7), pt2=(s[1]*(i+1)//12, s[0]*(j+1)//7), color = (0,0,255), thickness = 1, lineType = 8,shift = 0)
                    if i == prev[0] and j == prev[1]:
                      staycount += 1
                    else:
                      staycount = 0
                    prev = [i, j]
                    #クリックしたら文字を取得・操作
                    if staycount > 20:
                      cv2.rectangle(numimage, pt1=(s[1]*i//12,s[0]*j//7), pt2=(s[1]*(i+1)//12, s[0]*(j+1)//7), color = (0,0,255), thickness = 4, lineType = 8,shift = 0)
                      if j == 0 and i == 0:
                        return "hand", app, "mode"
                      elif j== 0 and i == 11:
                        keyboardtype = "hiragana"
                      elif C.hiragana[i-1][j-1] == "up":
                        pyautogui.click(1350, 40)
                        pyautogui.press('up')
                      elif C.hiragana[i-1][j-1] == "down":
                        pyautogui.click(1350, 40)
                        pyautogui.press('down')
                      elif C.number[i-1][j-1] == "DELETE":
                        text = text[:-1]
                      elif C.hiragana[i-1][j-1] == "ENTER":
                        driver.get(urllist[int(text)-1])
                        urllist = []
                        keyboardtype = "hiragana"
                      else:
                        text += C.number[i-1][j-1]
                      print(text)
                      staycount = 0

      # Flip the image horizontally for a selfie-view display.
      # 自撮りビューを表示するために水平方向反転
      if keyboardtype == "hiragana":
        cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
      elif keyboardtype == "dakuten":
        cv2.imshow('MediaPipe Hands', cv2.flip(subimage, 1))
      elif keyboardtype == "alphabet_small":
        cv2.imshow('MediaPipe Hands', cv2.flip(smallimage, 1))
      elif keyboardtype == "alphabet_big":
        cv2.imshow('MediaPipe Hands', cv2.flip(bigimage, 1))
      elif keyboardtype == "number":
        cv2.imshow('MediaPipe Hands', cv2.flip(numimage, 1))
      if cv2.waitKey(5) & 0xFF == 27:
        break
  cap.release()

def hand(cap, driver, app, change):
  lockflag = "unlocked"
  flag = "stop"
  playflag = "stop"
  count = 0
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)
  subprocess.run(["wmctrl", "-i", "-r", "0x04000006", "-e", "0,0,645,960,400"])

  #アプリ別定数・画面初期化
  appconst = []
  if app == "movie":
    appconst = C.movieconst
  elif app == "music":
    appconst = C.musicconst
  elif app == "search":
    appconst = C.searchconst    

  if change == "app":
    if app == "movie":
      driver.set_window_position(1000,0)
      driver.set_window_size(950,1150)
      driver.get("https://www.youtube.com/")
    elif app == "music":
      pyautogui.click(appconst[14], appconst[15])
      subprocess.run(["wmctrl", "-i", "-r", "0x04a00002", "-e", "0,1027,0,893,1050"])
    elif app == "search":
      driver.set_window_position(1000,0)
      driver.set_window_size(950,1150)
      driver.get("https://www.google.co.jp")



  with mp_hands.Hands(
      model_complexity=0,
      min_detection_confidence=0.7,
      min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
      success, image = cap.read()
      subimage = numpy.copy(image)

      if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        continue

      # To improve performance, optionally mark the image as not writeable to
      # pass by reference.
      image.flags.writeable = False
      image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
      results = hands.process(image)
      
      # Draw the hand annotations on the image.
      image.flags.writeable = True
      image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
      s = image.shape[:2]

      #処理領域を指定
      roi = (s[1]//12, s[0]//7, s[1]*9//12, s[0]*6//7)

      # ROI領域を抜き出し、抜き出した部分を動画に置き換え
      # [top:bottom, left:right] 順序
      s_roi = image[roi[1]: roi[3], roi[0]: roi[2]]
      
      #画面
      #unlock用
      if app == "movie":
        movieimage=cv2.imread("movie.png")
        movieimage=cv2.flip(cv2.resize(cv2.imread("movie.png"), dsize=(960, 540)),1)
        #　出力画像の同じ箇所に埋め込み
        movieimage[roi[1]: roi[3], roi[0]: roi[2]] = s_roi
        image = movieimage
        if len(driver.find_elements_by_class_name('ytp-ad-skip-button-container')) > 0:
          if driver.find_element_by_class_name('ytp-ad-skip-button-container').get_attribute('style') != "display: none;":
            driver.find_element_by_class_name('ytp-ad-skip-button').click()
      elif app == "music":
        musicimage=cv2.flip(cv2.resize(cv2.imread("music.png"), dsize=(960, 540)),1)
        #　出力画像の同じ箇所に埋め込み
        musicimage[roi[1]: roi[3], roi[0]: roi[2]] = s_roi
        image = musicimage
      elif app == "search":
        searchimage=cv2.flip(cv2.resize(cv2.imread("search.png"), dsize=(960, 540)),1)
        #　出力画像の同じ箇所に埋め込み
        searchimage[roi[1]: roi[3], roi[0]: roi[2]] = s_roi
        image = searchimage

      cv2.line(image, pt1=(s[1]*1//12,0), pt2=(s[1]*1//12, s[0]), color = (0,0,0), thickness = 1, lineType = 8,shift = 0)
      cv2.line(image, pt1=(s[1]*9//12,0), pt2=(s[1]*9//12, s[0]), color = (0,0,0), thickness = 1, lineType = 8,shift = 0)
      cv2.line(image, pt1=(s[1]*10//12,0), pt2=(s[1]*10//12, s[0]), color = (0,0,0), thickness = 1, lineType = 8,shift = 0)
      cv2.line(image, pt1=(0,s[0]//7), pt2=(s[1]*10//12, s[0]//7), color = (0,0,0), thickness = 1, lineType = 8,shift = 0)
      cv2.line(image, pt1=(0,s[0]*6//7), pt2=(s[1]*10//12, s[0]*6//7), color = (0,0,0), thickness = 1, lineType = 8,shift = 0)
      cv2.line(image, pt1=(s[1]*10//12,s[0]//3), pt2=(s[1], s[0]//3), color = (0,0,0), thickness = 1, lineType = 8,shift = 0)
      cv2.line(image, pt1=(s[1]*10//12,s[0]*2//3), pt2=(s[1], s[0]*2//3), color = (0,0,0), thickness = 1, lineType = 8,shift = 0)


      #lock用
      lockimage=cv2.flip(cv2.resize(cv2.imread("lock.png"), dsize=(960, 540)),1)
      #　出力画像の同じ箇所に埋め込み
      lockimage[roi[1]: roi[3], roi[0]: roi[2]] = s_roi
      subimage = lockimage

      cv2.line(subimage, pt1=(s[1]*1//12,0), pt2=(s[1]*1//12, s[0]), color = (0,0,0), thickness = 1, lineType = 8,shift = 0)
      cv2.line(subimage, pt1=(s[1]*9//12,0), pt2=(s[1]*9//12, s[0]), color = (0,0,0), thickness = 1, lineType = 8,shift = 0)
      cv2.line(subimage, pt1=(s[1]*10//12,0), pt2=(s[1]*10//12, s[0]), color = (0,0,0), thickness = 1, lineType = 8,shift = 0)
      cv2.line(subimage, pt1=(0,s[0]//7), pt2=(s[1]*10//12, s[0]//7), color = (0,0,0), thickness = 1, lineType = 8,shift = 0)
      cv2.line(subimage, pt1=(0,s[0]*6//7), pt2=(s[1]*10//12, s[0]*6//7), color = (0,0,0), thickness = 1, lineType = 8,shift = 0)
      cv2.line(subimage, pt1=(s[1]*10//12,s[0]//3), pt2=(s[1], s[0]//3), color = (0,0,0), thickness = 1, lineType = 8,shift = 0)
      cv2.line(subimage, pt1=(s[1]*10//12,s[0]*2//3), pt2=(s[1], s[0]*2//3), color = (0,0,0), thickness = 1, lineType = 8,shift = 0)



      if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
          #認識中
          if lockflag == "unlocked":
            #左、下が正
            #キーボードモード(緑)
            if round(hand_landmarks.landmark[3].y, 2) > round(hand_landmarks.landmark[4].y, 2) and round(hand_landmarks.landmark[7].x, 2) > round(hand_landmarks.landmark[8].x, 2) and \
               round(hand_landmarks.landmark[11].x, 2) < round(hand_landmarks.landmark[12].x, 2) and round(hand_landmarks.landmark[15].x, 2) < round(hand_landmarks.landmark[16].x, 2) and \
               round(hand_landmarks.landmark[19].x, 2) > round(hand_landmarks.landmark[20].x, 2):
              cv2.rectangle(image, pt1=(0,s[0]*6//7), pt2=(s[1]//12, s[0]), color = (0,0,255), thickness = 4, lineType = 8,shift = 0)
              if flag == "modechange":
                count += 1
              if count > 25:
                cv2.rectangle(image, pt1=(0,s[0]*6//7), pt2=(s[1]//12, s[0]), color = (0,0,255), thickness = 8, lineType = 8,shift = 0)
                if app == "movie" or app == "search":
                  count = 0
                  return "keyboard", app, "mode"
              flag = "modechange"
            #左を指しているとき(水色)
            elif round(hand_landmarks.landmark[5].y, 1) == round(hand_landmarks.landmark[6].y, 1) and round(hand_landmarks.landmark[5].x, 2) <= round(hand_landmarks.landmark[6].x, 2) and \
                 round(hand_landmarks.landmark[12].x, 3) < round(hand_landmarks.landmark[11].x, 3) and \
                 round(hand_landmarks.landmark[16].x, 3) < round(hand_landmarks.landmark[15].x, 3) and \
                 round(hand_landmarks.landmark[20].x, 3) < round(hand_landmarks.landmark[19].x, 3):
              cv2.rectangle(image, pt1=(s[1]*9//12,s[0]//7), pt2=(s[1]*10//12, s[0]*6//7), color = (255,255,0), thickness = 4, lineType = 8,shift = 0)
              if flag == "back":
                count += 1
              if count > 25:
                cv2.rectangle(image, pt1=(s[1]*9//12,s[0]//7), pt2=(s[1]*10//12, s[0]*6//7), color = (255,255,0), thickness = 8, lineType = 8,shift = 0)
                if app == "movie":
                  pyautogui.click(1350, 40)
                  pyautogui.press('left')
                elif app == "music":
                  pyautogui.click(appconst[4], appconst[5])
                elif app == "search":
                  pyautogui.click(appconst[2], appconst[3])
                count = 0
              flag = "back"
            #右を指しているとき(緑)
            elif round(hand_landmarks.landmark[5].y, 1) == round(hand_landmarks.landmark[6].y, 1) and round(hand_landmarks.landmark[5].x, 2) > round(hand_landmarks.landmark[6].x, 2) and \
                 round(hand_landmarks.landmark[12].x, 3) > round(hand_landmarks.landmark[11].x, 3) and \
                 round(hand_landmarks.landmark[16].x, 3) > round(hand_landmarks.landmark[15].x, 3) and \
                 round(hand_landmarks.landmark[20].x, 3) > round(hand_landmarks.landmark[19].x, 3):
              cv2.rectangle(image, pt1=(0,s[0]//7), pt2=(s[1]//12, s[0]*6//7), color = (0,255,0), thickness = 4, lineType = 8,shift = 0)
              if flag == "next":
                count += 1
              if count > 25:
                cv2.rectangle(image, pt1=(0,s[0]//7), pt2=(s[1]//12, s[0]*6//7), color = (0,255,0), thickness = 8, lineType = 8,shift = 0)
                if app == "movie":
                  pyautogui.click(1350, 40)
                  pyautogui.press('right')
                elif app == "music":
                  pyautogui.click(appconst[2], appconst[3])
                elif app == "search":
                  pyautogui.click(appconst[0], appconst[1])
                count = 0
              flag = "next"
            #アプリ変更
            #search(4)
            elif  round(hand_landmarks.landmark[4].x, 2) > round(hand_landmarks.landmark[3].x, 2) and \
                  round(hand_landmarks.landmark[8].y, 2) < round(hand_landmarks.landmark[5].y, 2) and \
                  round(hand_landmarks.landmark[12].y, 2) < round(hand_landmarks.landmark[9].y, 2) and \
                  round(hand_landmarks.landmark[16].y, 2) < round(hand_landmarks.landmark[13].y, 2) and \
                  round(hand_landmarks.landmark[20].y, 2) < round(hand_landmarks.landmark[17].y, 2):
              cv2.rectangle(image, pt1=(s[1]*10//12,s[0]*2//3), pt2=(s[1], s[0]), color = (0,0,255), thickness = 4, lineType = 8,shift = 0)
              if flag == "search":
                count += 1
              if count > 25:
                cv2.rectangle(image, pt1=(s[1]*10//12,s[0]*2//3), pt2=(s[1], s[0]), color = (0,0,255), thickness = 8, lineType = 8,shift = 0)
                app = "search"
                count = 0
                return "hand", "search", "app"
              flag = "search"
            #music(3)
            elif  round(hand_landmarks.landmark[4].x, 2) > round(hand_landmarks.landmark[3].x, 2) and \
                  round(hand_landmarks.landmark[8].y, 2) < round(hand_landmarks.landmark[5].y, 2) and \
                  round(hand_landmarks.landmark[12].y, 2) < round(hand_landmarks.landmark[9].y, 2) and \
                  round(hand_landmarks.landmark[16].y, 2) < round(hand_landmarks.landmark[13].y, 2) and \
                  round(hand_landmarks.landmark[20].y, 2) > round(hand_landmarks.landmark[19].y, 2):
              cv2.rectangle(image, pt1=(s[1]*10//12,s[0]//3), pt2=(s[1], s[0]*2//3), color = (0,0,255), thickness = 4, lineType = 8,shift = 0)
              if flag == "music":
                count += 1
              if count > 25:
                cv2.rectangle(image, pt1=(s[1]*10//12,s[0]//3), pt2=(s[1], s[0]*2//3), color = (0,0,255), thickness = 8, lineType = 8,shift = 0)
                app = "music"
                count = 0
                return "hand","music", "app"
              flag = "music"
            #movie(2)
            elif  round(hand_landmarks.landmark[4].x, 3) > round(hand_landmarks.landmark[3].x, 3) and \
                  round(hand_landmarks.landmark[8].y, 3) < round(hand_landmarks.landmark[5].y, 3) and \
                  round(hand_landmarks.landmark[12].y, 3) < round(hand_landmarks.landmark[9].y, 3) and \
                  round(hand_landmarks.landmark[16].y, 3) > round(hand_landmarks.landmark[13].y, 3) and \
                  round(hand_landmarks.landmark[20].y, 3) > round(hand_landmarks.landmark[17].y, 3):
              cv2.rectangle(image, pt1=(s[1]*10//12,0), pt2=(s[1], s[0]//3), color = (0,0,255), thickness = 4, lineType = 8,shift = 0)
              if flag == "movie":
                count += 1
              if count > 25:
                cv2.rectangle(image, pt1=(s[1]*10//12,0), pt2=(s[1], s[0]//3), color = (0,0,255), thickness = 8, lineType = 8,shift = 0)
                app = "movie"
                count = 0
                return "hand", "movie", "app"
              flag = "movie"
            #パーのとき(黄)
            elif round(hand_landmarks.landmark[4].x, 2) < round(hand_landmarks.landmark[3].x, 2)and \
                 round(hand_landmarks.landmark[8].y, 2) < round(hand_landmarks.landmark[5].y, 2) and \
                 round(hand_landmarks.landmark[12].y, 2) < round(hand_landmarks.landmark[9].y, 2) and \
                 round(hand_landmarks.landmark[16].y, 2) < round(hand_landmarks.landmark[13].y, 2) and \
                 round(hand_landmarks.landmark[20].y, 2) < round(hand_landmarks.landmark[17].y, 2):
              cv2.rectangle(image, pt1=(s[1]*9//12,0), pt2=(s[1]*10//12, s[0]//7), color = (0,0,255), thickness = 4, lineType = 8,shift = 0)
              if flag == "play":
                count += 1
              if count > 25:
                cv2.rectangle(image, pt1=(s[1]*9//12,0), pt2=(s[1]*10//12, s[0]//7), color = (0,0,255), thickness = 8, lineType = 8,shift = 0)
                if app == "movie":
                  #pyautogui.click(appconst[0], appconst[1])
                  print(driver.find_element_by_class_name('ytp-play-button').get_attribute('title'))
                  if driver.find_element_by_class_name('ytp-play-button').get_attribute('title') == "再生（k）":
                    driver.find_element_by_class_name('ytp-play-button').click()
                elif app == "music":
                  pyautogui.click(appconst[0], appconst[1])
                count = 0
              flag = "play"
            #lockモード(赤)
            elif round(hand_landmarks.landmark[3].x, 2) > round(hand_landmarks.landmark[4].x, 2) and \
                 round(hand_landmarks.landmark[6].x, 1) == round(hand_landmarks.landmark[5].x, 1)  and round(hand_landmarks.landmark[7].y, 2) > round(hand_landmarks.landmark[8].y, 2) and \
                 round(hand_landmarks.landmark[12].y, 2) > round(hand_landmarks.landmark[9].y, 2) and \
                 round(hand_landmarks.landmark[16].y, 2) > round(hand_landmarks.landmark[13].y, 2) and \
                 round(hand_landmarks.landmark[20].y, 2) > round(hand_landmarks.landmark[17].y, 2):
              cv2.rectangle(image, pt1=(s[1]*9//12,s[0]*6//7), pt2=(s[1]*10//12, s[0]), color = (0,0,255), thickness = 4, lineType = 8,shift = 0)
              if flag == "lock":
                count += 1
              if count > 25:
                cv2.rectangle(image, pt1=(s[1]*9//12,s[0]*6//7), pt2=(s[1]*10//12, s[0]), color = (0,0,255), thickness = 8, lineType = 8,shift = 0)
                count = 0
                lockflag = "locked"
              flag = "lock"
            #グーのとき(紫)
            elif round(hand_landmarks.landmark[7].y, 2) > round(hand_landmarks.landmark[6].y, 2) and \
                 round(hand_landmarks.landmark[11].y, 2) > round(hand_landmarks.landmark[10].y, 2) and \
                 round(hand_landmarks.landmark[15].y, 2) > round(hand_landmarks.landmark[14].y, 2) and \
                 round(hand_landmarks.landmark[19].y, 2) > round(hand_landmarks.landmark[18].y, 2):
              cv2.rectangle(image, pt1=(0,0), pt2=(s[1]//12, s[0]//7), color = (0,0,255), thickness = 4, lineType = 8,shift = 0)
              if flag == "stop":
                  count += 1
              if count > 25:
                cv2.rectangle(image, pt1=(0,0), pt2=(s[1]//12, s[0]//7), color = (0,0,255), thickness = 8, lineType = 8,shift = 0)
                if app == "movie":
                  print(driver.find_element_by_class_name('ytp-play-button').get_attribute('title'))
                  if driver.find_element_by_class_name('ytp-play-button').get_attribute('title') == "一時停止（k）":
                    driver.find_element_by_class_name('ytp-play-button').click()
                elif app == "music":
                  pyautogui.click(appconst[0], appconst[1])
                #elif app == "search":
                  #pyautogui.click(appconst[4], appconst[5])
                  #print("gu-")
                count = 0
              flag = "stop"
            #上を指しているとき(赤)
            elif round(hand_landmarks.landmark[5].x, 1) == round(hand_landmarks.landmark[6].x, 1) and round(hand_landmarks.landmark[5].y, 2) > round(hand_landmarks.landmark[6].y, 2) and \
                  round(hand_landmarks.landmark[12].y, 3) > round(hand_landmarks.landmark[9].y, 3) and \
                  round(hand_landmarks.landmark[16].y, 3) > round(hand_landmarks.landmark[13].y, 3) and \
                  round(hand_landmarks.landmark[20].y, 3) > round(hand_landmarks.landmark[17].y, 3):
              cv2.rectangle(image, pt1=(s[1]//12,0), pt2=(s[1]*9//12, s[0]//7), color = (0,0,255), thickness = 4, lineType = 8,shift = 0)
              if flag == "up":
                count += 1
              if count > 25:
                cv2.rectangle(image, pt1=(s[1]//12,0), pt2=(s[1]*9//12, s[0]//7), color = (0,0,255), thickness = 8, lineType = 8,shift = 0)
                if app == "movie" or app == "music":
                  subprocess.run(["amixer","sset","Master", "10%+"])
                elif app == "search":
                  pyautogui.click(1350, 40)
                  pyautogui.press('up')
                  pyautogui.press('up') 
                count = 0
              flag = "up"
            #下を指しているとき(青)
            elif round(hand_landmarks.landmark[5].x, 1) == round(hand_landmarks.landmark[6].x, 1) and round(hand_landmarks.landmark[5].y, 2) <= round(hand_landmarks.landmark[6].y, 2) and \
                 round(hand_landmarks.landmark[12].y, 3) < round(hand_landmarks.landmark[11].y, 3) and \
                 round(hand_landmarks.landmark[16].y, 3) < round(hand_landmarks.landmark[15].y, 3) and \
                 round(hand_landmarks.landmark[20].y, 3) < round(hand_landmarks.landmark[19].y, 3):
              cv2.rectangle(image, pt1=(s[1]//12,s[0]*6//7), pt2=(s[1]*9//12, s[0]), color = (255,0,0), thickness = 4, lineType = 8,shift = 0)
              if flag == "down":
                count += 1
              if count > 25:
                cv2.rectangle(image, pt1=(s[1]//12,s[0]*6//7), pt2=(s[1]*9//12, s[0]), color = (255, 0,0), thickness = 8, lineType = 8,shift = 0)
                if app == "movie" or app == "music":
                  subprocess.run(["amixer","sset","Master", "10%-"])
                elif app == "search":
                  pyautogui.click(1350, 40)
                  pyautogui.press('down') 
                  pyautogui.press('down')               
                count = 0
              flag = "down"
            else:
              flag = "any"
              count = 0
          #ロック中
          elif lockflag == "locked":
            if round(hand_landmarks.landmark[3].x, 2) > round(hand_landmarks.landmark[4].x, 2) and \
               round(hand_landmarks.landmark[6].x, 1) == round(hand_landmarks.landmark[5].x, 1)  and round(hand_landmarks.landmark[7].y, 2) > round(hand_landmarks.landmark[8].y, 2) and \
               round(hand_landmarks.landmark[12].y, 2) > round(hand_landmarks.landmark[9].y, 2) and \
               round(hand_landmarks.landmark[16].y, 2) > round(hand_landmarks.landmark[13].y, 2) and \
               round(hand_landmarks.landmark[20].y, 2) > round(hand_landmarks.landmark[17].y, 2):
              cv2.rectangle(subimage, pt1=(s[1]*9//12,s[0]*6//7), pt2=(s[1]*10//12, s[0]), color = (0,0,255), thickness = 4, lineType = 8,shift = 0)
              if flag == "lock":
                count += 1
              if count > 25:
                cv2.rectangle(subimage, pt1=(s[1]*9//12,s[0]*6//7), pt2=(s[1]*10//12, s[0]), color = (0,0,255), thickness = 8, lineType = 8,shift = 0)
                count = 0
                lockflag = "unlocked"
              flag = "lock"
      if lockflag == "unlocked":
        cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
      elif lockflag == "locked":
        cv2.imshow('MediaPipe Hands', cv2.flip(subimage, 1))
      cv2.moveWindow('MediaPipe Hands', 0, 0)
      if cv2.waitKey(5) & 0xFF == 27:
        break
  cap.release()