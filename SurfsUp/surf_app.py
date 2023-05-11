# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.sql import exists
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
app = Flask(__name__)

#################################################
# Flask Setup
#################################################


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start (enter as YYYY-MM-DD)<br/>"
        f"/api/v1.0/start/end (enter as YYYY-MM-DD/YYYY-MM-DD)"

    )
# create the precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # create session link from Python to the DB
    session = Session(engine)

    # calculate the date 1 year ago from the last data point in the database
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = dt.datetime.strptime(last_date[0], '%Y-%m-%d')
    year_ago = last_date - dt.timedelta(days=365)

    # query the last 12 months of precipitation data
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= year_ago).all()
    
    precipitation_results = list(np.ravel(results))

    return jsonify(precipitation_results)

# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations") 
def stations():
    # Create session (link) from Python to the DB
    session = Session(engine)

    # Query Stations
    results = session.query(Station.name).all()

    # Convert list of tuples into normal list
    station_details = list(np.ravel(results))

    return jsonify(station_details)

# create the tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    # create session link from Python to the DB
    session = Session(engine)

    # calculate the date 1 year ago from the last data point in the database
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = dt.datetime.strptime(last_date[0], '%Y-%m-%d')
    year_ago = last_date - dt.timedelta(days=365)

    # query the temperature observations of the most active station for the previous year of data
    station_temps = session.query(Measurement.date, Measurement.tobs).\
        filter
@app.route("/api/v1.0/<start>")
def temp_start(start):
    # Create session from Python to the DB
    session = Session(engine)

    # Query the min, avg, and max temps for all dates greater than or equal to the start date
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    temps = session.query(*sel).\
        filter(Measurement.date >= start).\
        order_by(Measurement.date).all()

    # Close the session
    session.close()

    # Convert the query results to a list
    temp_list = []
    for min_temp, avg_temp, max_temp in temps:
        temp_dict = {}
        temp_dict["Minimum Temperature"] = min_temp
        temp_dict["Average Temperature"] = avg_temp
        temp_dict["Maximum Temperature"] = max_temp
        temp_list.append(temp_dict)

    # Return the JSON of the list
    return jsonify(temp_list)


@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start, end):
    # Create session from Python to the DB
    session = Session(engine)

    # Query the min, avg, and max temps for dates between the start and end dates 
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    temps = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).\
        order_by(Measurement.date).all()

    # Close the session
    session.close()

    # Convert the query results to a list
    temp_list = []
    for min_temp, avg_temp, max_temp in temps:
        temp_dict = {}
        temp_dict["Minimum Temperature"] = min_temp
        temp_dict["Average Temperature"] = avg_temp
        temp_dict["Maximum Temperature"] = max_temp
        temp_list.append(temp_dict)

    # Return the JSON  of the list
    return jsonify(temp_list)


