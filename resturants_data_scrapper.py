import requests as r
from bs4 import BeautifulSoup as bs
import pandas as pd
from path import driver_path
from selenium import webdriver
import time

url = "https://www.zomato.com/jabalpur/restaurants"
user_agent = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}

webpage = r.get(url, headers= user_agent)
soup = bs(webpage.text, "html.parser")

rest_names=[]
cuisines= []
rating= []
price_per_person = []


