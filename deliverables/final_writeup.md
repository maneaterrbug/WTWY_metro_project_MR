# Strategizing bla bla
Matt Ryan

## Abstract

In this project, we are tasked with helping the non-profit organization, WomanTechWomanYes (WTWY), to both maximize attendance to their annual summer fundraising gala and spread awareness of their cause by using data analytics methods to optimize the deployment of their street teams. In order to aid WTWY in strategically scheduling their street teams to maximize engagement, we turned to New York City subway ridership [records](http://web.mta.info/developers/turnstile.html) and US census data to provide insight into both the most heavily trafficked stations, as well as the stations in areas with residents most likely/able to donate. 


## Design
With women only making up 27% of STEM workers despite accounting for nearly half the US workforce and only earning 85% their male counterparts according to 2019 Census Bureau estimates, the mission of WTWY is an important one. As such, WTWY being able to achieve high public engagement with their subway street teams using a data-driven approach is critical. Using the MTA data available to us, it is possible to take a more granular approach to our understanding of NYC metro-ridership, identifying key insights into high-traffic stations, times of day, and overall trends.


## Data

The base dataset used here is comprised of 1 year's worth of NYC MTA turnstile audit [records](http://web.mta.info/developers/turnstile.html), with the first and last turnstile audits records included on 01/04/2020 and 12/26/2020, respectively. Of interest, each turnstile audit record includes the turnstile's station and linename, the date and time the record was collected ***(the second of which generally falling into 1 of 6 uniform windows throughout the day)***, and running sums of entries and exits. We were able to use these fields to group our turnstiles into more granular sets ***to provide more insight***, and ultimately used one of these slices to determine 5 stations on which we performed further exploration and analysis.

## Algorithms

*Discuss the methods used to clean and organize the data, and some of the tough decisions made*

## Tools

* SQLAlchemy for exploration and loading of data
* Numpy and Pandas for manipulation of data
* SQLite for higher level data exploration
* Matplotlib for data plotting/visualization

## Communication

![](figs/tot_sum_by_stat.png)
![](figs/hourly_by_stn.png)
![](figs/fig_subplot.png)
