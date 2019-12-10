
from flask import Flask, render_template, request
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map, icons
import json
import pandas as pd
import requests
import geopandas as gpd
app = Flask(__name__)

markers = [{
  "coords":{'lat': 38.694862, 'lng': -122.772130},
  'iconImage':'http://maps.google.com/mapfiles/ms/icons/firedept.png',
 'content':'<h3>Kincade Fire</h3> <p>74% contained as of 11/02. For fire status updates visit <a href=\\"https:\/\/www.fire.ca.gov/incidents/2019/10/23/kincade-fire/\\" target=\\"_blank\\">Cal-fire website</a>.</p>'
},
{
'coords':{'lat':38.434535, 'lng':-122.701085},
'iconImage':'http://maps.google.com/mapfiles/ms/icons/homegardenbusiness.png',
'content':'<h3>Santa Rosa Veterans Memorial Building (evacuation center)</h3> <p>If you are trying to locate your large animal contact Animal Services at <a href=\\"tel:17075657100\\">(707) 565-7100</a>.</p>'
},
{
'coords':{'lat':38.610939, 'lng':-122.868083},
'iconImage':'http://maps.google.com/mapfiles/ms/icons/homegardenbusiness.png',
'content':'<h3>St. Paul’s Church Healdsburg CA(warming center)</h3>'
}
]


# reading the road_closures csv
road = pd.read_csv('road_closures.csv')

#getting only the closed roads related to fire
road = road[road['status'].str.contains('Fire')]

#loops over the each closed road
# gets and formates the
road_geo = []
for i in road.road:

    i = i.replace(' ', '%20')
    url = f'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={i}&inputtype=textquery&fields=geometry&key={YOUR_API_KEY}'

    res = requests.get(url)
    go = res.json()
    mo =go['candidates'][0]['geometry']['location']
    road_geo.append({"coords":mo, "iconImage" : 'http://maps.google.com/mapfiles/kml/shapes/caution.png'})




fire_map = gpd.read_file('MODIS_C6_USA_contiguous_and_Hawaii_24h/')
fire_map_loc = []
for i,k in zip(fire_map['LATITUDE'],fire_map['LONGITUDE']):
    fire_map_loc.append({"coords" : {'lat' : i,'lng' : k }, 'iconImage' : 'http://maps.google.com/mapfiles/ms/icons/firedept.png'})


@app.route('/')
def hello_world():
    return render_template('dir.html', markers=json.dumps(markers), road_geo=json.dumps(road_geo), fire_map_loc=json.dumps(fire_map_loc))

if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)


url = f'https://maps.googleapis.com/maps/api/geocode/json?address=Walmart+Falls+Church&key={YOUR_API_KEY}'
