# import dependencies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt

# Database Setup
engine = create_engine('sqlite:///Resources/hawaii.sqlite')

# reflect existing database into new model
Base = automap_base()
# reflect tables
Base.prepare(engine, reflect = True)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route('/')
def home():
    '''List all available api routes.'''
    return(
        f'Available Routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/start<br/>'
        f'/api/v1.0/start/end'
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    '''Return a list where date is the key and value is prcp'''

    print('Received precipitation api call')

    # Create session
    session = Session(engine)

    # Precipitation data for last 12 months of data. Find last date in database
    last_date_query = session.query(func.max(func.strftime('%Y-%m-%d', Measurement.date))).all()
    max_date_str = last_date_query[0][0]
    max_date = dt.datetime.strptime(max_date_str, '%Y-%m-%d')

    # Get a date 365 days prior to max date
    begin_date = max_date - dt.timedelta(365)

    # Find precipitation data
    precip_data = session.query(func.strftime("%Y-%m-%d", Measurement.date), Measurement.prcp).\
    filter(func.strftime("%Y-%m-%d", Measurement.date) >= begin_date).all()

    # Close session
    session.close()

    # Dictionary with date as key and prcp as value
    dates_dict = {}
    for date in precip_data:
        dates_dict[date[0]] = date[1]

    return jsonify(dates_dict)

@app.route('/api/v1.0/stations')
def stations():
    '''return a list of stations'''

    print('Received station api call.')

    # Create session
    session = Session(engine)

    # Query stations table
    stations_info = session.query(Station).all()

    # Close session
    session.close()

    # create a list of dicts
    stations_list = []
    for station in stations_info:
        station_dict = {}
        station_dict["id"] = station.id
        station_dict["Station"] = station.station
        station_dict["Name"] = station.name
        station_dict["Latitude"] = station.latitude
        station_dict["Longitude"] = station.longitude
        station_dict["Elevation"] = station.elevation
        stations_list.append(station_dict)

    return jsonify(stations_list)

@app.route('/api/v1.0/tobs')
def tobs():
    '''Return list of temperature observations for previous year'''

    print('Received tobs api call.')

    # Create session
    session = Session(engine)

    # Temperature data for last 12 months.
    last_date_query = session.query(func.max(func.strftime('%Y-%m-%d', Measurement.date))).all()
    max_date_str = last_date_query[0][0]
    max_date = dt.datetime.strptime(max_date_str, '%Y-%m-%d')

    # Get a date 365 days prior to max date
    begin_date = max_date - dt.timedelta(365)

    #get temperature measurements for last year
    results = session.query(Measurement).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) >= begin_date).all()

    # Close session
    session.close()

    #create list of dictionaries (one for each observation)
    tobs_list = []
    for result in results:
        tobs_dict = {}
        tobs_dict["date"] = result.date
        tobs_dict["station"] = result.station
        tobs_dict["tobs"] = result.tobs
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

@app.route('/api/v1.0/<start>')
def start(start):
    '''Return a list of min, avg, and max temps from start until the end of the data set.'''

    print('Received start date api call.')

    # Create session
    session = Session(engine)

    # This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' and return the minimum, average, and maximum temperatures for that range of dates
    def calc_temps(start_date):
        '''TMIN, TAVG, and TMAX for a list of dates.
    
        Args:
            start_date (string): A date string in the format %Y-%m-%d
            end_date (string): A date string in the format %Y-%m-%d
        
        Returns:
            TMIN, TAVE, and TMAX
        '''
    
        return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).all()
    
    # Find the first date in the database
    first_date_query = session.query(func.min(func.strftime('%Y-%m-%d', Measurement.date))).all()
    min_date = first_date_query[0][0]

    # get temps
    temps = calc_temps(min_date)

    # Close session
    session.close()

    #create list
    temp_list = []
    date_dict = {'start_date': min_date}
    temp_list.append(date_dict)
    temp_list.append({'Observation': 'TMIN', 'Temperature': temps[0][0]})
    temp_list.append({'Observation': 'TAVG', 'Temperature': temps[0][1]})
    temp_list.append({'Observation': 'TMAX', 'Temperature': temps[0][2]})

    return jsonify(temp_list)

@app.route('/api/v1.0/<start>/<end>')
def start_end(start, end):
    '''Return a list of min, avg, and max temps from start until the end of the data set.'''

    print('Received start/end date api call.')

    # Create session
    session = Session(engine)

    # This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' and return the minimum, average, and maximum temperatures for that range of dates
    def calc_temps(start_date, end_date):
        '''TMIN, TAVG, and TMAX for a list of dates.
    
        Args:
            start_date (string): A date string in the format %Y-%m-%d
            end_date (string): A date string in the format %Y-%m-%d
        
        Returns:
            TMIN, TAVE, and TMAX
        '''
    
        return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    
    # Find the first date in the database
    first_date_query = session.query(func.min(func.strftime('%Y-%m-%d', Measurement.date))).all()
    min_date = first_date_query[0][0]

    # Find the last date in the database
    last_date_query = session.query(func.max(func.strftime('%Y-%m-%d', Measurement.date))).all()
    max_date = last_date_query[0][0]

    # get temps
    temps = calc_temps(min_date, max_date)

    # Close session
    session.close()

    #create list
    temp_list = []
    date_dict = {'start_date': min_date, 'end_date':max_date}
    temp_list.append(date_dict)
    temp_list.append({'Observation': 'TMIN', 'Temperature': temps[0][0]})
    temp_list.append({'Observation': 'TAVG', 'Temperature': temps[0][1]})
    temp_list.append({'Observation': 'TMAX', 'Temperature': temps[0][2]})

    return jsonify(temp_list)

#code to actually run
if __name__ == "__main__":
    app.run(debug = True)