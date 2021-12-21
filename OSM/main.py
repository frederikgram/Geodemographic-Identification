"""
Search for all municipalties as OSM Relations, take note of the
admin_level as well as the boundary and area tags. These might be the key
to creating a dynamic way of searching for regions on a future platform
"""

import requests
import json


overpass_url = "http://overpass-api.de/api/interpreter"

overpass_query = """
[out:json];
area["ISO3166-1"="DK"];
(
rel["boundary"="administrative"]["admin_level"=7](area);
);
out body;
"""

response = requests.get(overpass_url, 
                        params={'data': overpass_query})
data = response.text
print(data)
