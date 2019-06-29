import numpy as np
import pandas as pd
import datetime as dt
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)


Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


app = Flask(__name__)

@app.route("/")
def welcome():
    "Listing all available routes."
    return(
        f"/api/v1.0/precipitation <br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/start/<start><br>"
        f"/api/v1.0/start-end/start/<start>/end/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    prcp_data = session.query(Measurement.date, Measurement.prcp).all()
    # prcp_results = list(np.ravel(prcp_query)
    return  jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def stations():
    station = session.query(Station.id, Station.station, Station.name,\
    Station.latitude, Station.longitude).all()

    return jsonify(station)

@app.route("/api/v1.0/tobs")
def temperature():
    date_query = session.query(Measurement.date)
    prcp_recent_record = date_query.order_by(Measurement.date.desc()).first()
    
    prcp_last_record = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    prcp_query = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > prcp_last_record).\
    order_by(Measurement.date).all()
    return jsonify(prcp_query)

@app.route("/api/v1.0/start/<start>")
def start(start):
    start_date = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= start).all()
    return jsonify(start_date)

@app.route("/api/v1.0/start-end/start/<start>/end/<end>")
def start_end(start, end):
    start_end = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(start_end)

if __name__ == '__main__':
    app.run(debug=True)