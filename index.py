from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd  
from decouple import config
from count_pages import number_of_pages


ser = Service(config('DRIVER'))
op = webdriver.ChromeOptions()
s = webdriver.Chrome(service=ser, options=op)

for i in number_of_pages:
     s.get(f"https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E1268&index={i}&propertyTypes=&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&keywords=")
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
          
          
     house_class = []
     for a in soup.find_all('div', attrs={'class':'property-information'}):
          for hh in soup.find('span', attrs={'class':'text'}):
               house_class.append(hh)
               
               
               
     pages_scraped = []
     for a in soup.find_all('div', attrs={'class':'select-wrapper pagination-dropdownWrapper'}):
          for hh in soup.find('select', attrs={'class':'select pagination-dropdown'}):
               pages_scraped.append(hh.get_text())

     number_of_pages = [0] #index pages
     len_pages_scraped = len(pages_scraped) - 1
     for i in range(0, len_pages_scraped):
          number_of_pages.append(number_of_pages[-1]+24)
          
          
          
     #load in a dataframe
     df = pd.DataFrame.from_dict({"area":area, "price": prices, "number_bedrooms": number_bedrooms,"property_types":house_class, "agent": agent})
     #df.to_csv("houses.csv",index = False, header=True, encoding='utf-8', sep='\t')



