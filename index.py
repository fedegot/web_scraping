from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd  
from decouple import config



ser = Service(config('DRIVER'))
op = webdriver.ChromeOptions()
s = webdriver.Chrome(service=ser, options=op)


s.get(config('LINK'))
content = s.page_source
soup = BeautifulSoup(content, features="html.parser")

prices = []
for a in soup.find_all('div', attrs={'class':'propertyCard-priceValue'}):
     prices.append(a.get_text())
     
area = []
for a in soup.find_all("address", attrs={'class':'propertyCard-address property-card-updates'}):
     appendo = a.get_text()
     area.append(appendo)
   
rooms_bed = []                 
for a in soup.find_all("span", attrs={"class":"no-svg-bed-icon bed-icon seperator"}):
     for s in a.select('title'):
          rooms_bed.append(s.get_text())
          
number_bedrooms = []
for x in rooms_bed:
     if "bedrooms" in x:
         number_bedrooms.append(int(x.replace('bedrooms', '')))


first_agent = []
agent = []
for a in soup.find_all('div', attrs={'class':'propertyCard-branchSummary property-card-updates'}):
     m = a.contents[1]
     first_agent.append(m)
     
for x in first_agent:
     mm = x.split()
     mm.remove("by")        
     agent.append(' '.join(mm))
     
#load in a dataframe
df = pd.DataFrame.from_dict({"area":area, "price": prices, "number_bedrooms": number_bedrooms, "agent": agent})
#df.to_csv("houses.csv",index = False, header=True, encoding='utf-8', sep='\t')



