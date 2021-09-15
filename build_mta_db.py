import pandas as pd 
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

def get_data(week_nums):
    url = "http://web.mta.info/developers/data/nyct/turnstile/turnstile_{}.txt" #url with formatting to fill in the number of the particular week
    dfs = []
    for week_num in week_nums: #for each week
        file_url = url.format(week_num) #format the url so it grabs that week
        dfs.append(pd.read_csv(file_url)) #append to our empty list
    return pd.concat(dfs) #combine files for each week
        

##need to make a loop here to generate integer values for each date desired...likely out to a year back, 
## I think the csv isnt getting overwritten when we write the file with new records
week_nums = [210206,210213,210220,210227,210306,210313,210320,210327,210403,210410,210417,210424,210501,210508,210515,210522,210529]
turnstiles_df = get_data(week_nums) #use our function to get a df with all of our data

turnstiles_df.to_csv('mta_data_all.csv', header = False, index = False)

print(turnstiles_df)

#### https://www.reddit.com/r/datasets/comments/hixfeo/how_to_obtain_median_income_data_for_zip_codes/ .... need to get a list of the zipcodes per borough in nyc 
#### then join with census data, shouldnt be an issue


## need to add code here to create db or drop table and re-add table if it exists

engine = create_engine('sqlite:///mta.db')

if not database_exists(engine.url):
    create_database(engine.url)
    with engine.connect() as connection:
        connection.execute("CREATE TABLE mta_data (CA TEXT,UNIT TEXT,SCP TEXT,STATION TEXT,LINENAME TEXT,DIVISION TEXT,DATE TEXT,TIME TEXT,DESC TEXT,ENTRIES INTEGER,EXITS INTEGER,PRIMARY KEY (CA,UNIT,SCP,STATION,LINENAME,DIVISION,DATE,TIME,DESC,ENTRIES,EXITS));")
else:
    with engine.connect() as connection:
        connection.execute("DROP TABLE mta_data;")
        connection.execute("CREATE TABLE mta_data (CA TEXT,UNIT TEXT,SCP TEXT,STATION TEXT,LINENAME TEXT,DIVISION TEXT,DATE TEXT,TIME TEXT,DESC TEXT,ENTRIES INTEGER,EXITS INTEGER,PRIMARY KEY (CA,UNIT,SCP,STATION,LINENAME,DIVISION,DATE,TIME,DESC,ENTRIES,EXITS));")


## need to fix this part here
# with engine.connect() as connection:
#     connection.execute(".mode csv")
#     connection.execute(".import mta_data_all.csv mta_data")
