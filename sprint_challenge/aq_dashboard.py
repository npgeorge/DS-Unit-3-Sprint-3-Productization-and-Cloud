"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

import openaq
import requests

# flask app variable
APP = Flask(__name__)

# setting openAQ as our API object
api = openaq.OpenAQ()

# setting up the call to the OpenAQ api
status, body = api.measurements(city='Los Angeles', parameter='pm25')

# could also call str() on body if we don't want in json, looks better in json though
dict_in_json = body

#
#
#
# SQL Database
#
#
#

# SQL config to database
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)

# creating columns for the Record database
class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return f'<<<< Time {self.datetime} & Value {self.value} of pm25 measurement>>>>'

#
#
#
#ROUTES
#
#
#

# original working route, kept as a check
@APP.route('/og')
def og():
    """calling 100 measurements from Los Angeles Chile"""
    return dict_in_json

# creating a list of utc_datetime and values
utc_val_list = []
for x in body['results']:
    datetime = x['date']['utc']
    value = x['value']
    utc_val_list.append([datetime, value])

# routing list of datetimes and values to homepage
@APP.route('/')
def root():
    """list of (utc_datetime, value) tuples"""
    # calling str() to return as a string
    return str(utc_val_list)

#
#
#
#POPULATING DATA FRAME
#
#
#

def update(body):
    # instantiate empty list
    utc_val_list = []
    # for given x param in body['results'], assign datetime and value variables
    for x in body['results']:
        # assigning utc datetime variable
        datetime = x['date']['utc']
        # assigning value variable
        value = x['value']
        # append these assigned variables to a list
        utc_val_list.append([datetime, value])
        # update the Record data frame with entire list
        DB.session.add(Record(datetime=datetime, value=value))

# getting data and placing into the Record data frame
@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()

    # added update function here
    update(body)

    DB.session.commit()
    return 'Data refreshed!'

#
#
#
#PART FOUR, MADE NEW ROUTE FOR EASIER NAVIGATING
#
#
#

filter_vals = Record.query.filter(Record.value >= 10).all()

@APP.route('/partfour')
def partfour():
    """list of (utc_datetime, value) tuples greater than or equal to 10"""
    # calling str() to return as a string
    return str(filter_vals)

#
#
#
# ADDITIONAL REQUESTS
#
#
#

# setting up the call to the OpenAQ api
status, resp = api.countries()
# >>> resp['results']

# could also call str() on body if we don't want in json, looks better in json though
dict_of_resp = resp['results']

# original working route, kept as a check
@APP.route('/countries')
def countries():
    """returning full list of countries"""
    return jsonify(dict_of_resp)