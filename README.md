# sqlalchemy-challenge
## Instructions
### Step 1 - Climate Analysis and Exploration
### To begin, use Python and SQLAlchemy to do basic climate analysis and data exploration of your climate database. All of the following analysis should be completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.
#### - Use the provided starter notebook and hawaii.sqlite files to complete your climate analysis and data exploration.
#### - Choose a start date and end date for your trip. Make sure that your vacation range is approximately 3-15 days total.
#### - Use SQLAlchemy create_engine to connect to your sqlite database.
#### - Use SQLAlchemy automap_base() to reflect your tables into classes and save a reference to those classes called Station and Measurement.

### Precipitation Analysis
#### - Design a query to retrieve the last 12 months of precipitation data.
#### - Select only the date and prcp values.
#### - Load the query results into a Pandas DataFrame and set the index to the date column.
#### - Sort the DataFrame values by date.
#### - Plot the results using the DataFrame plot method.
#### - Use Pandas to print the summary statistics for the precipitation data.

![precip_image](images/precip.PNG)

### Station Analysis
#### - Design a query to calculate the total number of stations.
#### - Design a query to find the most active stations.
##### * List the stations and observation counts in descending order.
##### * Which station has the highest number of observations?
##### * Design a query to retrieve the last 12 months of temperature observation data (TOBS).
#### - Filter by the station with the highest number of observations.
#### - Plot the results as a histogram with bins=12.

![stations_image](images/temphist.PNG)

### Temperature Analysis II
#### - The starter notebook contains a function called calc_temps that will accept a start date and end date in the format %Y-%m-%d. The function will return the minimum, average, and maximum temperatures for that range of dates.
#### - Use the calc_temps function to calculate the min, avg, and max temperatures for your trip using the matching dates from the previous year (i.e., use "2017-01-01" if your trip start date was "2018-01-01").
#### - Plot the min, avg, and max temperature from your previous query as a bar chart.
##### * Use the average temperature as the bar height.
##### * Use the peak-to-peak (TMAX-TMIN) value as the y error bar (YERR).

![temp_image](images/tempbar.PNG)

### Daily Rainfall Average
#### - Calculate the rainfall per weather station using the previous year's matching dates.
#### - Calculate the daily normals. Normals are the averages for the min, avg, and max temperatures.
#### - You are provided with a function called daily_normals that will calculate the daily normals for a specific date. This date string will be in the format %m-%d. Be sure to use all historic TOBS that match that date string.
#### - Create a list of dates for your trip in the format %m-%d. Use the daily_normals function to calculate the normals for each date string and append the results to a list.
#### - Load the list of daily normals into a Pandas DataFrame and set the index equal to the date.
#### - Use Pandas to plot an area plot (stacked=False) for the daily normals.

![rainfall_image](images/dailynormarea.PNG)
