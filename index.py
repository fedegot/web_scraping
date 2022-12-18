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
     page = s.get(f"https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E1164&index={i}&propertyTypes=&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&keywords=")
     content = s.page_source
     soup = BeautifulSoup(content, features="html.parser")

     area = []
     for a in soup.find_all("address", attrs={'class':'propertyCard-address property-card-updates'}):
          appendo = a.text if s else "N/A"
          area.append(appendo)      
           
     prices = []
     for a in soup.find_all('div', attrs={'class':'propertyCard-priceValue'}):
          prices.append(a.text if s else "N/A")
          
          
     rooms_bed = []                 
     for a in soup.find_all("span", attrs={"class":"no-svg-bed-icon bed-icon seperator"}):
          for s in a.select('title'):
                    rooms_bed.append(s.text if s else 00)
               
     number_bedrooms = []
     for x in rooms_bed:
          if "bedrooms" in x:
               number_bedrooms.append(int(x.replace('bedrooms', '')))
          elif "bedroom" in x:
               number_bedrooms.append(int(x.replace("bedroom", "")))
          else:  number_bedrooms.append(int(x))

     first_agent = []
     agent = []
     for a in soup.find_all('div', attrs={'class':'propertyCard-branchSummary property-card-updates'}):
          m = a.contents[1]
          first_agent.append(m)
          
          
     ID_w = []
     for a in soup.find_all('div', attrs={'class':'l-searchResult is-list'}):
          a.find("div")
          ID_w.append(int(a['id'][9:]))
               
          
     for x in first_agent:
          mm = x.split()
          mm.remove("by")        
          agent.append(' '.join(mm))
          
          
     house_class = []
     for a in soup.find_all('div', attrs={'class':'property-information'}):
          for hh in soup.find('span', attrs={'class':'text'}):
               house_class.append(hh)
               
               
     #///////////////MAKE THE LIST TO THE SAME NUMBER - NEED A FIX//////////////////
      
     dict_len = {"area": len(area), "prices": len(prices), "number_bedrooms": len(number_bedrooms), "house_class": len(house_class), "agent": len(agent)}
     max_values = max(dict_len.values())
     
     for key in dict_len:
              if dict_len[key] != max_values and key == "number_bedrooms":
                    difference = max_values - dict_len.get("number_bedrooms") 
                    number_bedrooms += [0000] * difference 
              elif dict_len[key] != max_values: 
                   len_list_fix(exec(key))       
     
     def len_list_fix(n):
          difference = max_values - dict_len.get(n) 
          n += difference * ["NaN"]
          
     def len_list_fix2(n):
          difference = max_values - dict_len.get("number_bedrooms") 
          n += [0000] * difference       #issues here
     
     #///////////////////////////////////////////////////////////////////////////////
     
                   
     #TEST
     print(ID_w)
     print(len(area))
     print(len(prices))
     print(len(number_bedrooms))
     print(number_bedrooms)
     print(rooms_bed)
     print(len(house_class))
     print(len(agent))

     #LOAD IN A DATAFRAME
     df = pd.DataFrame.from_dict({"IDD2": ID_w , "area": area, "price": prices, "number_bedrooms": number_bedrooms, "property_types": house_class, "agent": agent})
     #df.to_csv("houses.csv",index = False, header=True, encoding='utf-8', sep='\t')
     
     
     #CONNECT TO DB
     mydb = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user=config('USRNM'),
                               pw=config('PASSSL'),
                               db="mysql"))
     
     
     df.to_sql('salford2', con = mydb, if_exists = 'append', chunksize = 1000)


