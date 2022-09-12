import requests as r
from bs4 import BeautifulSoup as bs
import pandas as pd
from path import driver_path
from selenium import webdriver
import time

url = "https://www.zomato.com/jabalpur/restaurants"
user_agent = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}

driver = webdriver.Edge(executable_path=driver_path)
driver.get(url)

time.sleep(2)  # Suspends the webpage for 2 seconds
scroll_pause_time = 3  # Time interval between two consecutive scrolls
screen_height = driver.execute_script("return window.screen.height;")  # extract the screen height of the webpage
i = 1

while True:
    # scroll a height of one screen at a time
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
    i += 1
    time.sleep(scroll_pause_time)
    # update scroll height after each scroll
    scroll_height = driver.execute_script("return document.body.scrollHeight;")
    # Break the loop when the height to scroll to is larger than the total scroll height
    if (screen_height) * i > scroll_height:
        break

webpage = r.get(url, headers= user_agent)
soup = bs(webpage.text, "html.parser")

rest_names=[]
cuisines= []
rating= []
price_per_person = []


