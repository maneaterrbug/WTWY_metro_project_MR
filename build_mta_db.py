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

def get_week_num_list(min_date, max_month):
    mon_len_dict = {1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
    year = 21
    month = int(str(min_date)[2:4])
    date = int(str(min_date)[4:6])
    out_list = []


    while month <= max_month:
        if month != 1:
            if date > mon_len_dict[month-1]:
                date -= mon_len_dict[month-1]

        while date <= mon_len_dict[month]:
            date_val = int(str(year) + (str(month) if len(str(month)) == 2 else '0'+str(month)) + (str(date) if len(str(date)) == 2 else '0'+str(date)))
            out_list.append(date_val)
            date+=7

        month += 1
    return out_list


    
week_nums = get_week_num_list(210102,8)


turnstiles_df = get_data(week_nums) #use our function to get a df with all of our data
print(turnstiles_df)
turnstiles_df.to_csv('mta_data_all.csv', header = False, index = False)


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
