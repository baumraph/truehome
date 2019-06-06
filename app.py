# coding: utf-8
from flask import Flask, render_template, redirect, url_for,request
from flask import make_response
import json
import plotly
import pandas as pd
import numpy as np
import datetime
import dataset
import time


app = Flask(__name__)


def get_sensor_history(table, sensor):
    db = dataset.connect('sqlite:///dataset.db')
    query = db[table].find(
        sensor = sensor,
        timestamp = { 'gt': datetime.datetime.now() - datetime.timedelta(days=1) }
    )

    data = list(map(lambda row: [str(row['timestamp']), row['value']], query))
    x, y = zip(*data)
    x, y = list(x), list(y)

    return { 'x': x, 'y': y, 'type': 'scatter', 'name': sensor }


def get_sensor_value(table, sensor):
    db = dataset.connect('sqlite:///dataset.db')
    query = db[table].find(
        sensor = sensor,
        order_by = ['-id'],
        _limit = 1
    )
    rows = list(query)
    print(rows)
    if len(rows) == 0:
        return None
    return rows[0]['value']


@app.route('/')
def home():
    return render_template(
        'home.html',
        temperature = {
            'living_room': get_sensor_value('temperature', 'living_room'),
            'bathroom': get_sensor_value('temperature', 'bathroom'),
            'balcony': get_sensor_value('temperature', 'balcony')
        },
        humidity = {
            'living_room': get_sensor_value('humidity', 'living_room'),
            'bathroom': get_sensor_value('humidity', 'bathroom'),
            'balcony': get_sensor_value('humidity', 'balcony')
        }
    )


@app.route('/temperature')
def temperature():
    return render_template(
        'temperature.html', 
        temperature = [
            get_sensor_history('temperature', 'living_room'),
            get_sensor_history('temperature', 'bathroom'),
            get_sensor_history('temperature', 'balcony')
        ]
    )


@app.route('/humidity')
def humidity():
    return render_template(
        'humidity.html', 
        humidity = [
            get_sensor_history('humidity', 'living_room'),
            get_sensor_history('humidity', 'bathroom'),
            get_sensor_history('humidity', 'balcony')
        ]
    )


if __name__ == "__main__":
    app.run(debug = True)
