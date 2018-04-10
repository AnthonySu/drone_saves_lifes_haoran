from flask import Flask
from flask import request, render_template
from drones_save_lifesII import *
import requests
import os
app = Flask(__name__)
# http://35.185.197.49:5000/?date=2018-03-16&n=200
@app.route('/')
def server_API():
    date = request.args.get('date')
    n = int(request.args.get('n'))
    params = requests.get('https://ce290-hw5-weather-report.appspot.com/', params={'date': date})
    attributes = params.json()
    centroid_x = attributes['centroid_x']
    centroid_y = attributes['centroid_y']
    radius = attributes['radius']
    num_grid = n
    image_path = 'static/path.png'
    shortest_distance = drone_saves_life(centroid_x, centroid_y, radius, num_grid, image_path)
    return render_template('index.html', image_path = image_path, shortest_distance = shortest_distance)
if __name__ == '__main__':
    app.run()