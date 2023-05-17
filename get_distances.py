from datetime import datetime
import time

import csv
import pprint
import re

import math
import os

import locale

import json

import requests

import googlemaps

from googlemaps import convert

import urllib.parse

class DistanceMatrixTest():


    def setUp(self):
        self.key = "AIzaSyAjE6UiHJdgkgDLJ5zDM2upMuX81b15WZI"
        self.client = googlemaps.Client(self.key)
        # self.cal_cities = cal_cities
        # print(cal_cities)
        self.SF = ["San Francisco, USA"]
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
        # pp.pprint(destinations)
        params = self.built_parameters(origins, destinations)
        # pp.pprint(params)

        url = self.generate_auth_url("https://maps.googleapis.com/maps/api/distancematrix/json", params)
        # pp.pprint(url)

        payload={}
        headers={}
        # # pp.pprint(responses.calls[0].request.url)

        r = requests.request("GET", url, headers=headers, data=payload)

        # print(r.text)
        return r

    def filter_results(self, r):
        max_dist_from_center = 32 # km
        city_neighbors = []
        pp = pprint.PrettyPrinter(indent=4)
        r_dict = json.loads(r.text)
        # pp.pprint(r_dict)
        destinations = r_dict["destination_addresses"]
        origins = r_dict["origin_addresses"]
        # pp.pprint(origins)
        # pp.pprint(len(origins))
        # pp.pprint(destinations)
        rows = r_dict["rows"]
        for i in range(len(origins)):
            elements = rows[i]['elements']
            for e in elements:
                try:
                    s = (e["distance"]['text']).split()
                except:
                    continue
                # distance_from_SF = e["distance"]['text']
                # distance_from_SF = float(s[0])
                distance_from_center = locale.atof(s[0])
                # pp.pprint(distance_from_SF)
                if distance_from_center <= max_dist_from_center:
                    city_neighbors.append(r_dict["origin_addresses"][i])
        # pp.pprint(city_neighbors)
        return city_neighbors

    def compute_distance_matrix(self, origins, destinations):
        results = foo.test_basic_params(origins, destinations)
        pp = pprint.PrettyPrinter(indent=4)
        r_dict = json.loads(results.text)
        destinations = r_dict["destination_addresses"]
        origins = r_dict["origin_addresses"]
        rows = r_dict["rows"]
        distances = [["City"]]
        for d in destinations:
            d_city = re.sub("CA|USA|,", "", d)
            d_city = re.sub(" ","_", d_city)
            d_city = re.sub("__","", d_city)
            distances[0].append(d_city)
        # distance = []
        # distance = ["City"]
        # distance.extend(destinations)
        for i in range(len(origins)):
            elements = rows[i]['elements']
            distance = []
            # o = origins[i].split()
            # distance.append(origins[i])
            # distance.append(o)
            o_city = re.sub("CA|USA|,", "", origins[i])
            # print(o_city)
            o_city = re.sub(" ","_", o_city)
            o_city = re.sub("__","", o_city)
            # print(o_city)
            distance = [o_city]
            for e in elements:
                try:
                    # pp.pprint(e)
                    d = (e["distance"]['text']).split()
                    # pp.pprint(d)
                    distance.append(str(locale.atof(d[0])))

                except Exception as exception:
                    # pp.pprint(d)
                    print(exception)
                    continue
                    # distance.extend by -1
            distances.append(distance)
        filename = "./distance_matrix.csv"
        # f = open(filename, "w")
        with open(filename, 'w') as f:
            for distance in distances:
                pp.pprint(' '.join(distance))
                d_str = ' '.join(distance)
                # pp.pprint(d_str)
                f.write(f"{d_str}\n")
                # pp.pprint(distances, stream=f)
                # file_pp = pprint.PrettyPrinter(stream = f)
                # file_pp.pprint(d_str)
                # f.write(pp.pprint.pformat(distances))

        return distances
                # distance_from_SF = e["distance"]['text']
                # distance_from_SF = float(s[0])

    def find_neighbors(self, center_city, destinations):
        pp = pprint.PrettyPrinter(indent=4)
        cities_near_center = []
        center_name = '_'.join(center_city.split())
        center_name = center_name.replace(',', '')
        print(center_name)
        filename = "./cities_near_" + center_name + ".csv"
        # Check if file exists


        f = open(filename, "w")
        num_candidate_cities = len(destinations)
        chunk_size = 15
        num_chunks = math.ceil(num_candidate_cities/chunk_size)
        leftovers = num_candidate_cities % chunk_size
        print(leftovers)
        evaluate = []
        all_city_neighbors = []
        for c in range(num_chunks):
            if c*chunk_size <= num_candidate_cities-chunk_size-1:
                evaluate = destinations[c*chunk_size:(c+1)*chunk_size]
            else:
                evaluate = destinations[c*chunk_size:c*chunk_size+leftovers]
            results = foo.test_basic_params(evaluate, center_city)
            # pp.pprint(results)
            city_neighbors = foo.filter_results(results)
            if len(city_neighbors) > 0:
                # pp.pprint(city_neighbors)
                write_string = '\n'.join(city_neighbors)
                print(write_string, file=f)
                all_city_neighbors.extend(city_neighbors)
        f.close()
        return all_city_neighbors


pp = pprint.PrettyPrinter(indent=4)
SF = ["San Francisco, USA"]
attractive_centers = [
    # "San Francisco, USA",
    "Half Moon Bay, USA",
    # "San Jose, USA",
    # "Fremont, USA",
    "Palo Alto",
    # "Berkeley, USA",
    # "Sacramento, USA",
    "San Mateo, USA",
    # "Oakland, USA"
]
csv_file_path='/Users/huntervoid/programming/Ranking cities in NorCal/cal_cities.csv'
cal_cities = []
state=", CA, USA"
with open(csv_file_path, 'r') as file:
    csvreader=csv.reader(file)
    for row in csvreader:
        # pp.pprint(row)
        cal_cities.append(row[1]+state) 
# pp.pprint(cal_cities)
foo = DistanceMatrixTest()
foo.setUp()
all_city_neighbors = []
all_attractive_centers_neighbors = []

dist_mat = foo.compute_distance_matrix(cal_cities[0:10], attractive_centers)
# pp.pprint(dist_mat)


# for center in attractive_centers:
#     all_city_neighbors = foo.find_neighbors(center, cal_cities[0:100])
#     pp.pprint(all_city_neighbors)
#     all_attractive_centers_neighbors.append(all_city_neighbors)

# intersection = []
# for i in range(len(all_attractive_centers_neighbors)):
#     if i > 0:
#         intersection = list(set(intersection) & set(all_attractive_centers_neighbors[i]))
#     else:
#         intersection = all_attractive_centers_neighbors[i]
#     pp.pprint(intersection)

# pp.pprint(intersection)
# filename = "./intersection.csv"
# f = open(filename, "w")
# f.write('\n'.join(intersection))