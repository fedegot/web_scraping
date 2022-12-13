from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd  
import bleach

ser = Service("C:/Users/got_a/OneDrive/Documents/chromedriver.exe")
op = webdriver.ChromeOptions()
s = webdriver.Chrome(service=ser, options=op)

area = []
prices = []
rooms = []
# agent = []

s.get("https://www.rightmove.co.uk/property-for-sale/find.html?searchType=SALE&locationIdentifier=REGION%5E1268&insId=1&radius=0.0&minPrice=&maxPrice=&minBedrooms=&maxBedrooms=&displayPropertyType=&maxDaysSinceAdded=&_includeSSTC=on&sortByPriceDescending=&primaryDisplayPropertyType=&secondaryDisplayPropertyType=&oldDisplayPropertyType=&oldPrimaryDisplayPropertyType=&newHome=&auction=false")
content = s.page_source
soup = BeautifulSoup(content, features="html.parser")

for a in soup.find_all('div', attrs={'class':'propertyCard-wrapper'}):
     area = a.find('address', attrs={'class':'propertyCard-address property-card-updates'})
     prices = a.find('div', attrs={'class':'propertyCard-priceValue'})

     area.append(area.text)
     prices.append(prices.text)
          
for j in soup.find_all("span", attrs={"class":"no-svg-bed-icon bed-icon seperator"}):
     for s in j.select('title'):
        rooms.append(s.extract())
    


print(rooms)
    
    
    
# df = pd.DataFrame({"Area":area}, index=[1])
# df.to_csv("houses.csv",  encoding="utf-8")
    



