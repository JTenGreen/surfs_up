# Import dependencies
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Set up database
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect database into classes
Base = automap_base()
Base.prepare(engine, reflect=True)

# Add references
Measurement = Base.classes.measurement
Station = Base.classes.station

# Add session link from python to database
session = Session(engine)

# Define app for flask
app = Flask(__name__)

# Define root of routes
@app.route("/")

# Add routing information for each other routes.
# Create function welcome() with a return statement
# Add the precipitation, stations, tobs, and temp routes that we'll need for this module into our return statement. 
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# Precipitation Route
# New routes should ALWAYS be to the LEFT
@app.route("/api/v1.0/precipitation")

def precipitation():
    # Code that gets data from a year ago using timedelta
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    #Jsonify the dictionary a.k.a. structured text files with attribute-value pairs.
    return jsonify(precip)


# Stations Route
@app.route("/api/v1.0/stations")  

def stations():
    results = session.query(Station.station).all()
    #Unravel results into a one dimensional array with the function np.ravel(), using results as parameter
    #Then convert unreaveled results into a list, using the list() function, then Jsonify
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# Monthly Temperature route
@app.route("/api/v1.0/tobs")
def temp_monthly():
    #Using timedelta calculate previous dates data
    prev_year = dt.date(2017, 8 , 23) - dt.timedelta(days=365)
    #Query primary station for all temp observations from prev year
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)


# Statistics Route
# We need to povide both starting and ending date
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    # Use if-not statement to query database using the list we just made, unravel the results into one-dimensional array 
    # and convert to list
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

if __name__ == '__main__':
    app.run()
