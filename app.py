from flask import Flask, jsonify

import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.pool import StaticPool

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    return (
      f"Hawaii Climate App<br/>"
      f"Available Routes:<br/>"
      f"/api/v1.0/precipitation<br/>"
      f"/api/v1.0/stations<br/>"
      f"/api/v1.0/tobs<br/>"
      f"/api/v1.0/start<br/>"
      f"/api/v1.0/start/end"
      )

@app.route("/api/v1.0/precipitation")
def precipitation():
  one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
  prcp_data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= one_year_ago).\
      order_by(Measurement.date).all()
  prcp_data_list = dict(prcp_data)
  return jsonify(prcp_data_list)

@app.route("/api/v1.0/stations")
def stations():
      stations_all = session.query(Station.station, Station.name).all()
      station_list = list(stations_all)
      return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
      one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
      tobs_data = session.query(Measurement.date, Measurement.tobs).\
          filter(Measurement.date >= one_year_ago).\
          order_by(Measurement.date).all()
      tobs_data_list = list(tobs_data)
      return jsonify(tobs_data_list)

@app.route("/api/v1.0/start")
def start_day():
      start_date = dt.date(2017,1,1)
      start_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
          group_by(Measurement.date).all()
      start_day_list = list(start_day)
      return jsonify (start_day_list)

@app.route("/api/v1.0/start/end")
def start_end_day():
      start_date = dt.date(2017,1,1)
      end_date = dt.date(2017,1,4)
      start_end_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).\
        group_by(Measurement.date).all()
      start_end_day_list = list(start_end_day)
      return jsonify (start_end_day_list)

if __name__=='__main__':
  app.run(debug=True)