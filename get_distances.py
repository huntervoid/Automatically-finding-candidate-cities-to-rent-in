from datetime import datetime
import time

import csv
import pprint

import requests

import googlemaps

from googlemaps import convert

import urllib.parse


# csv_file_path='/Users/huntervoid/programming/Ranking cities in NorCal/cal_cities.csv'
# cal_cities = []
# state=", CA, USA"
# with open(csv_file_path, 'r') as file:
#     csvreader=csv.reader(file)
#     for row in csvreader:
# 	    cal_cities.append(row[1]+state)
# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(cal_cities)

class DistanceMatrixTest():


    def setUp(self):
        csv_file_path='/Users/huntervoid/programming/Ranking cities in NorCal/cal_cities.csv'
        cal_cities = []
        state=", USA"
        with open(csv_file_path, 'r') as file:
            csvreader=csv.reader(file)
            for row in csvreader:
    	        cal_cities.append(row[1]+state)	
        self.key = "AIzaSyAjE6UiHJdgkgDLJ5zDM2upMuX81b15WZI"
        self.client = googlemaps.Client(self.key)
        self.cal_cities = cal_cities
        # print(cal_cities)

        self.attractive_centers = [
			"San Francisco, USA"
			# "Berkeley, USA",
			# "Sacramento, USA"
			# "Napa",
			# "Sonoma",
			# "San Mateo",
			# "Palo Alto"
		]
        # self.attractive_centers = attractive_centers

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

        # if accepts_clientid and self.client_id and self.client_secret:
        #     if self.channel:
        #         params.append(("channel", self.channel))
        #     params.append(("client", self.client_id))

        #     path = "?".join([path, urlencode_params(params)])
        #     sig = sign_hmac(self.client_secret, path)
        #     return path + "&signature=" + sig

        if self.key:
            params.append(("key", self.key))
            return path + "?" + urllib.parse.urlencode(params)

        raise ValueError("Must provide API key for this API. It does not accept "
                         "enterprise credentials.")

    def test_basic_params(self):

        pp = pprint.PrettyPrinter(indent=4)

        origins = self.cal_cities[1:5]
        # pp.pprint(self.attractive_centers)
        destinations = self.attractive_centers
        # pp.pprint(destinations)
        params = self.built_parameters(origins, destinations)
        pp.pprint(params)

        url = self.generate_auth_url("https://maps.googleapis.com/maps/api/distancematrix/json", params)
        pp.pprint(url)

        # matrix = self.client.distance_matrix(self.cal_cities[1:20], self.attractive_centers)


        payload={}
        headers={}
        # # pp.pprint(responses.calls[0].request.url)

        r = requests.request("GET", url, headers=headers, data=payload)

        print(r.text)


foo = DistanceMatrixTest()
foo.setUp()
foo.test_basic_params()
