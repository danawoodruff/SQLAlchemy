# Dependencies

import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import inspect
from flask import Flask, json, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)

# View all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


# Use Flask to create the routes.
app = Flask(__name__)


# Routes
# Home Page
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

# Route: `/api/v1.0/stations`
# JSON list of stations from the dataset.


@app.route('/api/v1.0/stations')
def stations():
    station_list = session.query(Station.station)\
        .order_by(Station.station).all()
    for row in station_list:
        print(row[0])
    return jsonify(station_list)

# Route: `/api/v1.0/tobs`
# Query the dates and temperature observations of the most active station for the last year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year.


results = session.query(Measurement.date, func.avg(Measurement.prcp)).\
    filter(Measurement.date < "2017-08-24").\
    filter(Measurement.date > "2016-08-23").\
    order_by(Measurement.date).\
    group_by(Measurement.date).\
    all()


@app.route('/api/v1.0/tobs/')
def tobs():

    last_date = session.query(Measurement.date).order_by(
        Measurement.date.desc()).first().date
    oneyear = dt.datetime.strptime(
        last_date, '%Y-%m-%d') - dt.timedelta(days=365)

    temps = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= oneyear).\
        order_by(Measurement.date).all()

    return jsonify(temps)

# Route: `/api/v1.0/precipitation`
# JSON representation of your dictionary.


@app.route("/api/v1.0/precipitation")
def prec():

    last_date = session.query(Measurement.date).order_by(
        Measurement.date.desc()).first().date
    oneyear = dt.datetime.strptime(
        last_date, '%Y-%m-%d') - dt.timedelta(days=365)

    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= oneyear).\
        order_by(Measurement.date).all()

    return jsonify(precipitation)

# Route:  `/api/v1.0/<start>`
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.


@app.route("/api/v1.0/<start>")
def start1(start):

    select = [func.min(Measurement.tobs), func.avg(
        Measurement.tobs), func.max(Measurement.tobs)]

    result_temp = session.query(*select).\
        filter(Measurement.date >= start).all()

    return jsonify(result_temp)

# Route:  `/api/v1.0/<start>/<end>/`
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start-end range.


@app.route("/api/v1.0/<start>/<end>")
def start_end1(start, end):

    select = [func.min(Measurement.tobs), func.avg(
        Measurement.tobs), func.max(Measurement.tobs)]

    result_temp = session.query(*select).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    return jsonify(result_temp)


if __name__ == "__main__":
    app.run(debug=True)
