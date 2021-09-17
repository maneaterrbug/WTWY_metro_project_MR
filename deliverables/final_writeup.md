# Using Data Analytics to Inform and Improve WTWY Fundraising and Outreach Efforts
Matt Ryan

## Abstract

In this project, we are tasked with helping the non-profit organization, WomanTechWomanYes (WTWY), to both maximize attendance to their annual summer fundraising gala and spread awareness of their cause by using data analytics methods to optimize the deployment of their subway street teams. To answer this question, we turned to New York City subway ridership [records](http://web.mta.info/developers/turnstile.html) to provide insight into the levels and trends of subway station traffic, as well as make actionable recommendations recommendations for street team deployment strategies. 


## Design
With women only making up 27% of STEM workers despite accounting for nearly half the US workforce and only earning 85% their male counterparts (according to 2019 [Census Bureau estimates](https://www.census.gov/library/stories/2021/01/women-making-gains-in-stem-occupations-but-still-underrepresented.html)), the mission of WTWY is an important one. As such, WTWY being able to achieve high public engagement with their subway street teams using a data-driven approach can be critical. Using the MTA data available to us, it is possible to take a more granular approach to our understanding of NYC metro-ridership, identifying key insights into high-traffic stations, times of day, and overall trends in metro traffic in the months leading up to the gala.


## Data

The base dataset used here is comprised of the 2021 NYC MTA turnstile audit [records](http://web.mta.info/developers/turnstile.html), with the first and last turnstile audits record files beginning on dates 01/02/2021 and 08/28/2021, respectively. Of particular interest to us, each turnstile audit record includes the turnstile's associated station and line, the date and time the record was collected (with the time field generally falling into 1 of 6 uniform intervals throughout the day), and running counts of entries and exits. We were able to use these fields to group our turnstiles into more granular sets, and ultimately used one of these slices to determine **5 high volume stations of interest** on which we performed further exploration and analysis.

## Algorithms

***Exploratory Data Analysis***
* **Gathering data and setting up database**
	* A python [script](https://github.com/maneaterrbug/WTWY_metro_project_MR/blob/master/build_mta_db.py) was written and used in conjunction with SQLite3 to build a local database by dynamically cycling through all relevant .csv files found on the MTA website dependent within the desired timeframe and importing into a table in the local database
* **Initial Cleaning**
	* Cleaning of field datatypes (ie DATE field from 'string' to 'datetime')
	* Concatenation of STATION and LINE_NUM fields to correct for duplicate station issue
* **Processing and manipulating our data** - all cleaning and aggregation methods discussed here can be found in this python [script](https://github.com/maneaterrbug/WTWY_metro_project_MR/blob/master/mta_data_process.py)
	* By sorting the data into two initial dataframes, one grouped by day and one by time of record, the total amount of passengers that entered per turnstile over the course of the desired timeframe was able to be calculated using a pandas.DataFrame.diff() call. 
	* Using the daily dataframe, we were able to aggregate by unique station over our new entries value to determine the stations with the heaviest foot-traffic
	* From this list of high-volume stations, we identified the top 5 most-visited stations and applied them as a mask on our original date and time dataframes
	* Finally, aggregating functions such as .mean() and .sum() were applied to our newly organized dataframes to identify the most and least heavily trafficked days of the week and times of the day for each of our 5 stations
* **Final Cleaning**
	* During the course of the data processing and aggregation we discovered many abherrant records with potential to throw off any insights we might make
	* The newly calculated .diff() entries fields brought to light several new discrepancies with our data including:
		* reverse counting turnstiles leading to negative totals
		* long stretches of time during which data was not collected leading to extremely high .diff() values
		* turnstile counts being reset to 0 leading to negative values orders of magnitude larger than we might expect
		* large jumps up or down in cumulative entries count between 2 unique turnstiles' records in the dataset, leading to .diff() values orders of magnitude larger than we might expect
	* Which were accounted for by:
		* instead using the absoulute value of our .diff() entries using np.absolute()
		* filtering out absolute values that our unrealistically large (ie > 10,000 per day or > 2,000 for a 4 hour time-frame)
		* manually redefining our turnstiles switch-over .diff() values to null


## Tools

* SQLAlchemy for exploration and loading of data
* Numpy and Pandas for manipulation of data
* SQLite for higher level data exploration
* Matplotlib for data plotting/visualization

## Communication

Shown here is a representation of the 15 stations with the highest volume of turnstile entries, with top 5 most trafficked stations highlighted in color:
![](../figs/tot_sum_by_stat.png)

We take a deeper look into these stations trends over the course of entire time-frame:
![](../figs/daily_entries_by_station.png)

This is a lot of data and can seem unwieldy to try to work with. As such, we decided to look into station averages over the course of a day and over the course of a week: 
![](../figs/daily_entries_sum_week.png)
![](../figs/hourly_by_stn.png)
