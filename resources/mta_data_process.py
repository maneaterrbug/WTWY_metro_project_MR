from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


## Creates the sqlalchemy engine and uses a SQL query to store the data in a dataframe
### Please see exploration_queries.sql file in this repo for SQL queries used for general high level data exploration
engine = create_engine('sqlite:///mta.db')
turnstiles_df = pd.read_sql('SELECT * FROM mta_data;', engine)



turnstiles_df['DATE'] = turnstiles_df['DATE'].astype('datetime64[ns]')
turnstiles_df['STATION_LINE'] = turnstiles_df.STATION + ", " + turnstiles_df.LINENAME

## Creates a new df grouped by turnstile (ie the first 4 columns) and adds DAILY_TOT and DAILY_TOT_ABS columns
turnstiles_daily = (turnstiles_df
                        .groupby(["CA", "UNIT", "SCP", "STATION_LINE", "DATE"],as_index=False)
                        .ENTRIES.first())
turnstiles_daily['DAILY_TOT'] = turnstiles_daily.groupby(["CA", "UNIT", "SCP", "STATION_LINE"]).ENTRIES.diff()
turnstiles_daily['DAILY_TOT_ABS'] = np.absolute(turnstiles_daily.DAILY_TOT)


## Creates df turnstiles_hourly, which functions similarly to daily but does not group entries by day
turnstiles_hourly = turnstiles_df.copy()
turnstiles_hourly = turnstiles_hourly[turnstiles_hourly.TIME.isin(['00:00:00','04:00:00','08:00:00','12:00:00','16:00:00','20:00:00','24:00:00'])]
turnstiles_hourly['HOURLY_AMT'] = turnstiles_hourly.groupby(["CA", "UNIT", "SCP", "STATION_LINE"]).ENTRIES.diff()
turnstiles_hourly['HOURLY_AMT_ABS'] = np.absolute(turnstiles_hourly.HOURLY_AMT)


## Applies data cleaning masks
mask = (turnstiles_daily.DAILY_TOT_ABS < 10000)
maskh = (turnstiles_hourly.HOURLY_AMT_ABS < 2000)
turnstiles_daily_cleaned = turnstiles_daily[mask]
turnstiles_hourly_cleaned = turnstiles_hourly[maskh]
mask_shift = (turnstiles_daily.SCP.shift(1) != turnstiles_daily.SCP)
turnstiles_daily.loc[mask_shift,'DAILY_TOT'] = np.nan



## Organizes entries by station and creates a sum per station
station_daily = (turnstiles_daily_cleaned
                        .groupby(['STATION_LINE','DATE'])[['DAILY_TOT_ABS']]
                        .sum()
                        .reset_index())
station_daily_sum = (station_daily
                        .groupby('STATION_LINE')
                        .DAILY_TOT_ABS.sum()
                        .reset_index()
                        .sort_values('DAILY_TOT_ABS',ascending = False).head(15))
station_daily_sum['STATION'] = station_daily_sum.STATION_LINE.apply(lambda x: x[:x.find(',')])


#hourly mean for station
top_list = station_daily_sum.STATION_LINE.head(5).to_list()
station_hourly = turnstiles_hourly_cleaned.groupby(['STATION_LINE','TIME'])[['HOURLY_AMT_ABS']].mean().reset_index()
station_hourly_top = station_hourly[station_hourly.STATION_LINE.isin(top_list)].reset_index()


## Creates a df with daily_tot value grouped by each station, then applies masks/operations to see
## only the top 5 stations and a dow sum by station (could clean up mask so it is not hard-coded, honestly just sort here and then run an iloc)
daily_by_station = turnstiles_daily_cleaned.groupby(['STATION_LINE','DATE']).DAILY_TOT_ABS.sum().reset_index()


top_station_mask = daily_by_station['STATION_LINE'].isin(top_list)

daily_by_station_top = daily_by_station[top_station_mask].reset_index()
daily_by_station_top['DAY_OF_WEEK_NUM'] = pd.to_datetime(daily_by_station_top['DATE']).dt.dayofweek

daily_by_station_dow_mean = (daily_by_station_top
                                .groupby(['STATION_LINE','DAY_OF_WEEK_NUM'])
                                .DAILY_TOT_ABS
                                .mean()
                                .reset_index())


##############
## Plotting ##
##############

#Bar
color_lst = ['tab:blue','tab:orange','tab:green','tab:red','tab:purple','grey','grey','grey','grey','grey','grey','grey','grey','grey','grey']
plt.figure(figsize=(7,4))
plt.bar(station_daily_sum.STATION_LINE, station_daily_sum.DAILY_TOT_ABS, tick_label = station_daily_sum.STATION, color = color_lst)
plt.ylabel('# of Entries')
plt.xlabel('Station')
plt.xticks(size = 7, rotation = 45)
plt.title('Total Sum of Entries by Station (01/02/2021-08-28-2021)')

plt.savefig('figs/tot_sum_by_stat.png', bbox_inches = 'tight')


#Line for entire time frame
plt.figure(figsize=(15,8))
plt.grid()  
for i, group in daily_by_station_top.groupby('STATION_LINE'):
    plt.plot(group['DATE'], group['DAILY_TOT_ABS'], label = i)

plt.legend(shadow = True, loc = 0, fontsize = 'small')
plt.ylabel('# of Entries')
plt.xlabel('Date')
plt.xticks(rotation=45)
plt.title('Total Daily Entries by Station (01/02/2021-08-28-2021)')

plt.savefig('figs/daily_entries_by_station.png', bbox_inches = 'tight')

#Line for week
plt.figure(figsize=(15,8))
plt.grid() 
for i, group in daily_by_station_dow_mean.groupby('STATION_LINE'):
    plt.plot(group['DAY_OF_WEEK_NUM'], group['DAILY_TOT_ABS'], label = i)
    
plt.legend(shadow = True, loc = 0, fontsize = 'small')

plt.ylabel('# of Entries')
plt.xlabel('Day of Week')
plt.xticks(np.arange(7),['Sn','Mo','Tu','We','Th','Fr','St'])
plt.title('Sum of Entries by Station by Day (01/02/2021-08-28-2021)')

plt.savefig('figs/daily_entries_sum_week.png', bbox_inches = 'tight')

#Prev 2 figs subplotted
plt.figure(figsize=(15,15))
fig, (ax1,ax2) = plt.subplots(2, figsize = (15,15))
ax2.grid() 
for i, group in daily_by_station_dow_mean.groupby('STATION_LINE'):
    ax2.plot(group['DAY_OF_WEEK_NUM'], group['DAILY_TOT_ABS'], label = i)
    
ax2.legend(shadow = True, loc = 0, fontsize = 'x-small')
ax2.set(xlabel = 'Day of Week', ylabel = '# of Entries')
ax2.set_xticklabels(['','Sn','Mo','Tu','We','Th','Fr','St'])

ax1.grid()
for i, group in daily_by_station_top.groupby('STATION_LINE'):
    ax1.plot(group['DATE'], group['DAILY_TOT_ABS'], label = i)

ax1.legend(shadow = True, loc = 0, fontsize = 'x-small')
ax1.set(xlabel = 'Month', ylabel = '# of Entries')

plt.savefig('figs/fig_subplot.png', bbox_inches = 'tight')

# Each stations mean entries by time of day
fig, axs = plt.subplots(1,5, figsize=(20,5), sharey = 'row')
fig.suptitle('Mean Entries per Time of Day per Station', size = 20)
idx = 0
for i, group in station_hourly_top.groupby('STATION_LINE'):
    axs[idx].bar(group['TIME'],group['HOURLY_AMT_ABS'], label = i, color = color_lst[idx])
    axs[idx].set_title(i)
    axs[idx].tick_params('x',labelrotation = 45)
    idx+=1

plt.savefig('figs/hourly_by_stn.png', bbox_inches = 'tight')





