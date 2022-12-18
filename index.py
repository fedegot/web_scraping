from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from decouple import config
from bs4 import BeautifulSoup
import pandas as pd  
from count_pages import number_of_pages
from sqlalchemy import create_engine


for i in number_of_pages:
     ser = Service(config('DRIVER'))
     op = webdriver.ChromeOptions().add_argument("--headless")
     s = webdriver.Chrome(service=ser, options=op)

     print(f"{i} pagina")
     page = s.get(f"https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E1268&index={i}&propertyTypes=&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&keywords=")
     content = s.page_source
     soup = BeautifulSoup(content, features="html.parser")

     area = []
     for a in soup.find_all("address", attrs={'class':'propertyCard-address property-card-updates'}):
          appendo = a.get_text()
          area.append(appendo)      
           
     prices = []
     for a in soup.find_all('div', attrs={'class':'propertyCard-priceValue'}):
          prices.append(a.get_text())
          
          
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
               
     
     print(len(area))
     print(len(prices))
     print(len(number_bedrooms))
     print(number_bedrooms)
     print(rooms_bed)
     print(len(house_class))
     print(len(agent))
     
     dict_len = {"area": len(area), "prices": len(prices), "number_bedrooms": len(number_bedrooms), "house_class": len(house_class), "agent": len(agent)}
     max_values = max(dict_len.values())
     
     for key in dict_len:
              if dict_len[key] != max_values:
               if key == "number_bedrooms":
                    len_list_fix2(exec(key)) 
               else: len_list_fix(exec(key))       
     
     def len_list_fix(n):
          difference = max_values - dict_len.get(n) 
          n += difference * ["NaN"]
          
     def len_list_fix2(n):
          difference = max_values - dict_len.get("number_bedrooms") 
          for x in range(difference):
               n.append(0000000000)
          #n += [0000] * difference       #issues here
                       

     #load in a dataframe
     df = pd.DataFrame.from_dict({"area": area, "price": prices, "number_bedrooms": number_bedrooms, "property_types": house_class, "agent": agent})
     #df.to_csv("houses.csv",index = False, header=True, encoding='utf-8', sep='\t')
     
     mydb = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user=config('USRNM'),
                               pw=config('PASSSL'),
                               db="mysql"))
     
     
     df.to_sql('cws', con = mydb, if_exists = 'append', chunksize = 1000)


