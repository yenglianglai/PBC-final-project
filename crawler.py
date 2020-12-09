from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import time
import tkinter as tk
import urllib.parse
import urllib.request
from PIL import Image, ImageTk
import io


input_topic = input()

options = Options()
options.add_argument("--disable-notifications")

chrome = webdriver.Chrome("C:/Users/perfu/Desktop/商程設/期末專案/chromedriver.exe", chrome_options=options)

chrome.get("https://lookbook.nu/")

wait = WebDriverWait(chrome, 20)

search = chrome.find_element_by_name('q')
search.send_keys(input_topic)
search.submit()

pos = 0  
m = 0 # 圖片編號 
for i in range(2):  
    pos += i*500 # 每次下滾500  
    js = "document.documentElement.scrollTop=%d" % pos  
    chrome.execute_script(js)  
    time.sleep(1)

soup = BeautifulSoup(chrome.page_source, 'lxml')
imgs = soup.find_all('img', {'class': 'thumbimage'})
srcs = []
for img in imgs:
    if img != 'None': 
        srcs.append(img.get('src'))

chrome.close()

mainWindow = tk.Tk()
mainWindow.title("What to wear")
mainWindow.geometry("1000x1240")
mainWindow.minsize(width=1000, height=1240)


sbar = tk.Scrollbar(mainWindow)
sbar.pack(side = tk.RIGHT, fill = tk.Y)

canvas = tk.Canvas(mainWindow, bg = 'white', yscrollcommand=sbar.set)
canvas.pack(fill = 'both', expand=True)
sbar.config(command=canvas.yview)
images = []
for i in range(len(srcs)):
    picture_url = "http:" + srcs[i]
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = urllib.request.Request(url=picture_url, headers=headers)
    raw_data = urllib.request.urlopen(req).read()
    im = Image.open(io.BytesIO(raw_data))
    img = ImageTk.PhotoImage(im)
    image1 = canvas.create_image(50,150*i, anchor = tk.NW, image=img)
    images.append(img)
mainWindow.mainloop()

print(images)
