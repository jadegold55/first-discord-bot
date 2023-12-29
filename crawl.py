import random
from bs4 import BeautifulSoup
import pandas as pd
import requests
import urllib.request
from string import digits
import re

quotes = []
URL = "https://sarahscoop.com/155-best-funny-spongebob-quotes/"
webpage = requests.get(URL)
soup = BeautifulSoup(webpage.text, "html.parser")
quoteText = soup.find_all("h2", attrs={"class": "wp-block-heading"})
for i in quoteText:
    quotes.append(str(i.text.strip()))
hi = quotes.pop()
quote = []

p = re.compile('[0-9.]')
for x in quotes:
    m = p.sub('', x)
    quote.append(m)
print(quote)
