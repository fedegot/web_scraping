from index import df
from sqlalchemy import create_engine
from decouple import config

mydb = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user=config('USRNM'),
                               pw=config('PASSSL'),
                               db="mysql"))

df.to_sql('cacca', con = mydb, if_exists = 'append', chunksize = 1000)
