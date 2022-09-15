from bs4 import BeautifulSoup as bs
import pandas as pd
from path import driver_path, check_dir
from selenium import webdriver
import time

check_dir()  # This function is responsible for checking and changing the working directory of the project

homepage_url = "https://www.zomato.com/jabalpur/restaurants"
user_agent = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}

options = webdriver.EdgeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Edge(executable_path=driver_path, options= options)
driver.get(homepage_url)

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

homepage_soup = bs(driver.page_source, "html.parser")

rest_names=[]
cuisines= []
rating= []
price_per_person = []
locality = []
all_rest_page_url = []

name_tags = homepage_soup.find_all("h4")

rest_url = "https://www.zomato.com/"


for rest_name in name_tags[:len(name_tags)-1]:

    rest_names.append(rest_name.text)

    rest_page_tag = rest_name.parent.parent
    all_rest_page_url.append(rest_page_tag["href"])

    rating_tag = rest_name.parent.div.div.div.div.div.div.text
    rating.append(rating_tag)

    price_tag = rest_name.parent.next_sibling.p.next_sibling.text
    price_per_person.append(price_tag)

    cuisine_tag = rest_name.parent.next_sibling.p.text
    cuisines.append(cuisine_tag)


for page_tags in all_rest_page_url:
    page_url = rest_url + page_tags
    driver.get(page_url)
    
    rest_page_soup = bs(driver.page_source, "html.parser")

    h1_tag= rest_page_soup.find_all("h1")
    
    location_tag = h1_tag[1].parent.next_sibling.div.next_sibling.text
    locality.append(location_tag)

driver.close()

restaurants_df = pd.DataFrame({"name": rest_names, "cuisines": cuisines, "rating": rating, "price_per_person": price_per_person, "location": locality})
restaurants_df.to_csv("./Dataset/jabalpur_restaurants.csv")

