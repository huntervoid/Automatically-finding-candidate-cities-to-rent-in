from datetime import datetime
import time

import csv
import pprint

import math

import locale

import json

import requests

import googlemaps

from googlemaps import convert

import urllib.parse

class DistanceMatrixTest():


    def setUp(self):
        # csv_file_path='/Users/huntervoid/programming/Ranking cities in NorCal/cal_cities.csv'
        # cal_cities = []
        # state=", USA"
        # with open(csv_file_path, 'r') as file:
        #     csvreader=csv.reader(file)
        #     for row in csvreader:
    	#         cal_cities.append(row[1]+state)	
        self.key = "AIzaSyAjE6UiHJdgkgDLJ5zDM2upMuX81b15WZI"
        self.client = googlemaps.Client(self.key)
        # self.cal_cities = cal_cities
        # print(cal_cities)
        self.SF = ["San Francisco, USA"]
        self.attractive_centers = [
			"San Francisco, USA",
			"Berkeley, USA",
			"Sacramento, USA"
			"Napa, USA",
			"Sonoma, USA",
			"San Mateo, USA",
			"Palo Alto, USA",
            "San Jose, USA"
		]
        # self.attractive_centers = attractive_centers
        locale.setlocale(locale.LC_ALL, '')
        # print(self.locale)

    def built_parameters(self, origins, destinations):

        params = {
            "origins": convert.location_list(origins),
            "destinations": convert.location_list(destinations)
        }

        return params


    def generate_auth_url(self, path, params):
        """Returns the path and query string portion of the request URL, first
        adding any necessary parameters.

        :param path: The path portion of the URL.
        :type path: string

        :param params: URL parameters.
        :type params: dict or list of key/value tuples

        :rtype: string

        """
        # Deterministic ordering through sorting by key.
        # Useful for tests, and in the future, any caching.
        extra_params = getattr(self, "_extra_params", None) or {}
        if type(params) is dict:
            params = sorted(dict(extra_params, **params).items())
        else:
            params = sorted(extra_params.items()) + params[:] # Take a copy.

        if self.key:
            params.append(("key", self.key))
            return path + "?" + urllib.parse.urlencode(params)

        raise ValueError("Must provide API key for this API. It does not accept "
                         "enterprise credentials.")

    def test_basic_params(self, origins, destinations):

        pp = pprint.PrettyPrinter(indent=4)

        # origins = self.cal_cities[0:2]
        # pp.pprint(self.attractive_centers)
        # destinations = self.attractive_centers
        # pp.pprint(destinations)
        params = self.built_parameters(origins, destinations)
        # pp.pprint(params)

        url = self.generate_auth_url("https://maps.googleapis.com/maps/api/distancematrix/json", params)
        pp.pprint(url)

        # matrix = self.client.distance_matrix(self.cal_cities[1:20], self.attractive_centers)


        payload={}
        headers={}
        # # pp.pprint(responses.calls[0].request.url)

        r = requests.request("GET", url, headers=headers, data=payload)

        # print(r.text)
        return r

    def filter_results(self, r):
        max_dist_from_SF = 200.0 # km
        SF_neighbors = []
        pp = pprint.PrettyPrinter(indent=4)
        r_dict = json.loads(r.text)
        # pp.pprint(r_dict)
        destinations = r_dict["destination_addresses"]
        origins = r_dict["origin_addresses"]
        # pp.pprint(len(origins))
        # pp.pprint(destinations)
        rows = r_dict["rows"]
        for i in range(len(origins)):
            elements = rows[i]['elements']
            for e in elements:
                s = (e["distance"]['text']).split()
                # distance_from_SF = e["distance"]['text']
                # distance_from_SF = float(s[0])
                distance_from_SF = locale.atof(s[0])
                pp.pprint(distance_from_SF)
                if distance_from_SF <= max_dist_from_SF:
                    SF_neighbors.append(r_dict["origin_addresses"][i])
        # pp.pprint(SF_neighbors)
        return SF_neighbors

pp = pprint.PrettyPrinter(indent=4)
SF = ["San Francisco, USA"]
attractive_centers = [
    "San Francisco, USA",
    "Berkeley, USA",
    "Sacramento, USA"
    "Napa, USA",
    "Sonoma, USA",
    "San Mateo, USA",
    "Palo Alto, USA",
    "San Jose, USA"
]
csv_file_path='/Users/huntervoid/programming/Ranking cities in NorCal/cal_cities.csv'
cal_cities = []
state=", USA"
with open(csv_file_path, 'r') as file:
    csvreader=csv.reader(file)
    for row in csvreader:
        cal_cities.append(row[1]+state) 
# pp.pprint(cal_cities)
foo = DistanceMatrixTest()
foo.setUp()
# results = foo.test_basic_params(cal_cities[25:50], SF)

cities_near_SF = []
f = open("./cities_near_SF.csv", "w")
# cal_cities = cal_cities[0:39]
num_candidate_cities = len(cal_cities)
chunk_size = 15
num_chunks = math.ceil(num_candidate_cities/chunk_size)
leftovers = num_candidate_cities % chunk_size
print(leftovers)
evaluate = []
for c in range(num_chunks):
    if c*chunk_size <= num_candidate_cities-chunk_size-1:
        evaluate = cal_cities[c*chunk_size:(c+1)*chunk_size]
    else:
        evaluate = cal_cities[c*chunk_size:c*chunk_size+leftovers]
    results = foo.test_basic_params(evaluate, SF)
    SF_neighbors = foo.filter_results(results)
    f.write('\n')
    f.write('\n'.join(SF_neighbors))
    pp.pprint(SF_neighbors)
