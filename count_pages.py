from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup 
from decouple import config

ser = Service(config('DRIVER'))
op = webdriver.ChromeOptions()
s = webdriver.Chrome(service=ser, options=op)

s.get(config('LINK'))
content = s.page_source
soup = BeautifulSoup(content, features="html.parser")


pages_scraped = []
for a in soup.find_all('div', attrs={'class':'select-wrapper pagination-dropdownWrapper'}):
     for hh in soup.find('select', attrs={'class':'select pagination-dropdown'}):
          pages_scraped.append(hh.get_text())

number_of_pages = [0] #index pages
len_pages_scraped = len(pages_scraped) - 1
for i in range(0, len_pages_scraped):
     number_of_pages.append(number_of_pages[-1]+24)
     
print(number_of_pages)
     
