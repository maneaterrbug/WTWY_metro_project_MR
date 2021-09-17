<h1>Strategizing bla bla<h1>
Matt Ryan

<h3>Abstract<h3>

In this project, we are tasked with helping the non-profit organization, WomanTechWomanYes (WTWY), both maximize attendance to their annual summer fundraising gala and spread awareness of their cause by using data analytics methods to ***optimize their resources WTWY plans to post street teams at the entrances to subway stations ***. In order to aid WTWY in strategically scheduling their street teams to maximize engagement, we turned to New York City subway ridership [records](http://web.mta.info/developers/turnstile.html) and US census data to provide insight into both the most heavily trafficked stations, as well as the stations in areas with residents most likely/able to donate. 


<h3>Design<h3>



<h3>Data<h3>

The base dataset used here is comprised of 1 year's worth of NYC MTA turnstile audit [records](http://web.mta.info/developers/turnstile.html), with the first and last turnstile audits records included on 01/04/2020 and 12/26/2020, respectively. Of interest, each turnstile audit record includes the turnstile's station and linename, the date and time the record was collected ***(the second of which generally falling into 1 of 6 uniform windows throughout the day)***, and running sums of entries and exits. We were able to use these fields to group our turnstiles into more granular sets ***to provide more insight***, and ultimately used one of these slices to determine 5 stations on which we performed further exploration and analysis.

<h3>Tools<h3>

* SQLAlchemy for loading and unloading of data
* Numpy and Pandas for manipulation of data
* SQLite for higher level data exploration
* Matplotlib for data plotting/visualization

<h3>Communication<h3>