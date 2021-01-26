# Dependencies

import datetime as dt

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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
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
    print (f"Hawaii Weather Stations:")   
    for row in station_list:
        print (row[0])
    return jsonify(station_list)

if __name__ == "__main__":
    app.run(debug=True)