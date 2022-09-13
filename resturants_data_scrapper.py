import requests as r
from bs4 import BeautifulSoup as bs
import pandas as pd
from path import driver_path, check_dir
from pathlib import Path
from selenium import webdriver
import time
import os 

check_dir()  # This function is responsible for checking and changing the working directory of the project

if not os.path.exists("./Dataset"): #creates a directory for downloaded data if it does'nt exists
    Path("./Dataset").mkdir(parents=True, exist_ok=True)

url = "https://www.zomato.com/jabalpur/restaurants"
user_agent = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}

options = webdriver.EdgeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Edge(executable_path=driver_path, options= options)
driver.get(url)

time.sleep(1)  # Suspends the webpage for 1 seconds
scroll_pause_time = 2  # Time interval between two consecutive scrolls
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

soup = bs(driver.page_source, "html.parser")

rest_names=[]
cuisines= []
rating= []
price_per_person = []

name_tags = soup.find_all("h4")

for rest_name in name_tags[:len(name_tags)-1]:

    rest_names.append(rest_name.text)

    rating_tag = rest_name.parent.div.div.div.div.div.div.text
    rating.append(rating_tag)

    price_tag = rest_name.parent.next_sibling.p.next_sibling.text
    price_per_person.append(price_tag)

    cuisine_tag = rest_name.parent.next_sibling.p.text
    cuisines.append(cuisine_tag)

restaurants_df = pd.DataFrame({"name": rest_names, "cuisines": cuisines, "rating": rating, "price_per_person": price_per_person})

restaurants_df.to_csv("./Dataset/jabalpur_restaurants.csv")