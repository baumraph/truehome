# coding: utf-8
from flask import Flask, render_template, redirect, url_for,request
from flask import make_response
import json
import plotly
import pandas as pd
import numpy as np
import datetime
import dataset


app = Flask(__name__)


def get_temperature_history(title):
    db = dataset.connect('sqlite:///dataset.db')
    query = db['temperature'].find(
        name = title.lower().replace(' ', '_'), 
        timestamp = { 'gt': datetime.datetime.now() - datetime.timedelta(days=1) }
    )

    x = []
    y = []
    for row in query:
        x.append(str(row['timestamp']))
        y.append(row['temperature'])

    data = {
        'x': x,
        'y': y,
        'type': 'scatter',
        'name': title
    }
    return data


def get_humidity_history(title):
    db = dataset.connect('sqlite:///dataset.db')
    query = db['humidity'].find(
        name = title.lower().replace(' ', '_'), 
        timestamp = { 'gt': datetime.datetime.now() - datetime.timedelta(days=1) }
    )

    x = []
    y = []
    for row in query:
        x.append(str(row['timestamp']))
        y.append(row['humidity'])

    data = {
        'x': x,
        'y': y,
        'type': 'scatter',
        'name': title
    }
    return data


def get_temperature(name):
    db = dataset.connect('sqlite:///dataset.db')
    query = db['temperature'].find(
        name = name,
        order_by = ['id'],
        _limit = 1
    )
    rows = list(query)
    if len(rows) == 0:
        return '?'
    temperature = rows[0]['temperature']
    return '{:4.2f}'.format(temperature)


def get_humidity(name):
    db = dataset.connect('sqlite:///dataset.db')
    query = db['humidity'].find(
        name = name,
        order_by = ['id'],
        _limit = 1
    )
    rows = list(query)
    if len(rows) == 0:
        return '?'
    humidity = rows[0]['humidity']
    return '{:2.0f}'.format(humidity)


@app.route('/')
def home():
    temperature = {
        'living_room': get_temperature('living_room'),
        'bathroom': get_temperature('bathroom'),
        'balcony': get_temperature('balcony')
    }

    humidity = {
        'living_room': get_humidity('living_room'),
        'bathroom': get_humidity('bathroom'),
        'balcony': get_humidity('balcony')
    }

    return render_template(
        'home.html',
        temperature = temperature,
        humidity = humidity
    )


@app.route('/temperature')
def temperature():
    temperature = [
        get_temperature_history('Living Room'),
        get_temperature_history('Bathroom'),
        get_temperature_history('Balcony')
    ]

    return render_template(
        'temperature.html', 
        temperature = temperature
    )


@app.route('/humidity')
def humidity():
    humidity = [
        get_humidity_history('Living Room'),
        get_humidity_history('Bathroom'),
        get_humidity_history('Balcony')
    ]

    return render_template(
        'humidity.html', 
        humidity = humidity
    )


if __name__ == "__main__":
    app.run(debug = True)
