from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


## Creates the sqlalchemy engine and uses a SQL query to store the data in a dataframe
engine = create_engine('sqlite:///mta.db')
turnstiles_df = pd.read_sql('SELECT * FROM mta_data;', engine)

## Creates a new df grouped by turnstile (ie the first 4 columns) and adds DAILY_TOT and DAILY_TOT_ABS columns
turnstiles_daily = (turnstiles_df
                        .groupby(["CA", "UNIT", "SCP", "STATION", "DATE"],as_index=False)
                        .ENTRIES.first())
turnstiles_daily['DAILY_TOT'] = turnstiles_daily.groupby(["CA", "UNIT", "SCP", "STATION"]).ENTRIES.diff()
turnstiles_daily['DAILY_TOT_ABS'] = np.absolute(turnstiles_daily.DAILY_TOT)



## Applies max value mask
mask = (turnstiles_daily.DAILY_TOT_ABS < 10000)
turnstiles_daily_cleaned = turnstiles_daily[mask]


## Organizes entries by station and creates a sum per station
station_daily = (turnstiles_daily_cleaned
                        .groupby(['STATION','DATE'])[['DAILY_TOT_ABS']]
                        .sum()
                        .reset_index())
station_daily_sum = (station_daily
                        .groupby('STATION')
                        .DAILY_TOT_ABS.sum()
                        .reset_index()
                        .sort_values('DAILY_TOT_ABS',ascending = False).head(15))

station_daily_sum.head(5)

## Creates a df with daily_tot value grouped by each station, then applies masks/operations to see
## only the top 5 stations and a dow sum by station (could clean up mask so it is not hard-coded)
daily_by_station = turnstiles_daily_cleaned.groupby(['STATION','DATE']).DAILY_TOT_ABS.sum().reset_index()
station_mask = ((daily_by_station['STATION'] == '34 ST-PENN STA') | 
                (daily_by_station['STATION'] == '34 ST-HERALD SQ') | 
                (daily_by_station['STATION'] == '86 ST') |
                (daily_by_station['STATION'] == '125 ST') | 
                (daily_by_station['STATION'] == 'GRD CNTRL-42 ST'))

daily_by_station_top = daily_by_station[station_mask].reset_index()
daily_by_station_top['DAY_OF_WEEK_NUM'] = pd.to_datetime(daily_by_station_top['DATE']).dt.dayofweek

daily_by_station_dow_sum = (daily_by_station_top
                                .groupby(['STATION','DAY_OF_WEEK_NUM'])
                                .DAILY_TOT_ABS
                                .sum()
                                .reset_index())


#######
## Plotting 
#######

#Bar
plt.figure(figsize=(10,5)) 
plt.bar(station_daily_sum.STATION, station_daily_sum.DAILY_TOT_ABS)
plt.ylabel('# of Entries')
plt.xlabel('Station')
plt.xticks(rotation=45)
plt.title('Total Sum of Entries by Station (02-06-2021-05-29-2021)')

plt.savefig('figs/tot_sum_by_stat.png', bbox_inches = 'tight')


#Line for entire time frame
plt.figure(figsize=(15,8)) 
for i, group in daily_by_station_top.groupby('STATION'):
    plt.plot(group['DATE'], group['DAILY_TOT_ABS'], label = i)

plt.legend(shadow = True, loc = 0, fontsize = 'small')
plt.ylabel('# of Entries')
plt.xlabel('Date')
plt.xticks(rotation=45)
plt.title('Total Daily Entries by Station (02-06-2021-05-29-2021)')

plt.savefig('figs/daily_entries_by_station.png', bbox_inches = 'tight')

#Line for week
plt.figure(figsize=(15,8)) 
for i, group in daily_by_station_dow_sum.groupby('STATION'):
    plt.plot(group['DAY_OF_WEEK_NUM'], group['DAILY_TOT_ABS'], label = i)
    
plt.legend(shadow = True, loc = 0, fontsize = 'small')

plt.ylabel('# of Entries')
plt.xlabel('Day of Week')
plt.xticks(np.arange(7),['Sn','Mo','Tu','We','Th','Fr','St'])
plt.title('Sum of Entries by Station by Day (02-06-2021-05-29-2021)')

plt.savefig('figs/daily_entries_sum_week.png', bbox_inches = 'tight')







####There are large jumps of entries when the year shifts and for some (use existing code in mta pair 2 to clean this up)

station_daily = turnstiles_daily.groupby(['STATION','DATE'])[['DAILY_TOT']].sum().reset_index()

print(station_daily.groupby('STATION').DAILY_TOT.sum().reset_index().sort_values('DAILY_TOT',ascending = False))

station_daily_sum = station_daily.groupby('STATION').DAILY_TOT.sum().reset_index().sort_values('DAILY_TOT',ascending = False)

print(plt.bar(station_daily_sum.STATION, station_daily_sum.DAILY_TOT))





## https://new.mta.info/agency/new-york-city-transit/subway-bus-ridership-2020
##cleaning up diffs around changing scp borders
# mask = (turnstiles_daily.SCP.shift(1) != turnstiles_daily.SCP)
# turnstiles_daily['DAILY_TOT'][mask] = np.nan
