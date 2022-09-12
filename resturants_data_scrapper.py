import requests as r
from bs4 import BeautifulSoup as bs
import pandas as pd

url = "https://www.zomato.com/jabalpur/restaurants"

webpage = r.get(url)
soup = bs(webpage.content, "html.parser")
print(soup)
