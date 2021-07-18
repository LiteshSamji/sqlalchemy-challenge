
#import numpy
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Database Setup
## reflect an existing database into a new model
engine = create_engine('sqlite:///Resources/hawaii.sqlite')
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each tables
Measurement = Base.classes.measurement
station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

# Create a Flask app
app = Flask(__name__)

# Flask Routes
@app.route("/")
def home():
    print("Server requested climate app home page...")
    return (
        f"Welcome to the Climate Analysis App!<br/>"
        f"----------------------------------<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        )

@app.route("/api/v1.0/precipitation")
def precipitation():     
    # Calculate the date one year from the last date in data set.
    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)     

    # query to retrieve all the date and precipitation values
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    
    #Dictionary with date as the key and prcp as the value
    precip = {date: prcp for date, prcp in results}
    return jsonify(precip)

if __name__ == "__main__":
    app.run(debug=True)
