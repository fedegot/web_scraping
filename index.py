from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd  
from decouple import config

#ser = Service("C:/Users/got_a/OneDrive/Documents/chromedriver.exe")
ser = Service("/home/fedegot/Downloads/chromedriver")
op = webdriver.ChromeOptions()
s = webdriver.Chrome(service=ser, options=op)

area = []
prices = []
rooms = []
first_agent = []
agent = []

s.get(config('LINK'))
content = s.page_source
soup = BeautifulSoup(content, features="html.parser")

for a in soup.find_all('div', attrs={'class':'propertyCard-priceValue'}):
     prices.append(a.get_text())

for a in soup.find_all("address", attrs={'class':'propertyCard-address property-card-updates'}):
     appendo = a.get_text()
     area.append(appendo)
                    
for j in soup.find_all("span", attrs={"class":"no-svg-bed-icon bed-icon seperator"}):
     for s in j.select('title'):
        rooms.append(s.get_text())
    

for a in soup.find_all('div', attrs={'class':'propertyCard-branchSummary property-card-updates'}):
     m = a.contents[1]
     first_agent.append(m)
     
for x in first_agent:
     mm = x.split()
     mm.remove("by")        
     agent.append(' '.join(mm))
     
      

print(len(rooms))
print(len(prices))
print(len(area))
print(len(agent))


df = pd.DataFrame.from_dict({"Area":area, "Price": prices, "Rooms": rooms, "Agent": agent})
df.to_csv("houses.csv",index = False, header=True, encoding='utf-8', sep='\t')


