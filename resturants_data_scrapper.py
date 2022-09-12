import requests as r
from bs4 import BeautifulSoup as bs
import pandas as pd
from path import driver_path
from selenium import webdriver
import time

url = "https://www.zomato.com/jabalpur/restaurants"
user_agent = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}

driver = webdriver.Edge(executable_path= driver_path)

driver.get(url)

time.sleep(2)  # Allow 2 seconds for the web page to (open depends on you)
scroll_pause_time = 3  # You can set your own pause time. dont slow too slow that might not able to load more data
screen_height = driver.execute_script("return window.screen.height;")  # get the screen height of the web
i = 1

while True:
    # scroll one screen height each time
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
    i += 1
    time.sleep(scroll_pause_time)
    # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
    scroll_height = driver.execute_script("return document.body.scrollHeight;")
    # Break the loop when the height we need to scroll to is larger than the total scroll height
    if (screen_height) * i > scroll_height:
        break




webpage = r.get(url, headers= user_agent)
soup = bs(webpage.text, "html.parser")

rest_names=[]
cuisines= []
rating= []
price_per_person = []


