from datetime import datetime
import time

import csv
import pprint
import re

import math
import os

import copy

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

    # def filter_results(self, r):
    #     max_dist_from_center = 32 # km
    #     city_neighbors = []
    #     pp = pprint.PrettyPrinter(indent=4)
    #     r_dict = json.loads(r.text)
    #     # pp.pprint(r_dict)
    #     destinations = r_dict["destination_addresses"]
    #     origins = r_dict["origin_addresses"]
    #     # pp.pprint(origins)
    #     # pp.pprint(len(origins))
    #     # pp.pprint(destinations)
    #     rows = r_dict["rows"]
    #     for i in range(len(origins)):
    #         elements = rows[i]['elements']
    #         for e in elements:
    #             try:
    #                 s = (e["distance"]['text']).split()
    #             except:
    #                 continue
    #             # distance_from_SF = e["distance"]['text']
    #             # distance_from_SF = float(s[0])
    #             distance_from_center = locale.atof(s[0])
    #             # pp.pprint(distance_from_SF)
    #             if distance_from_center <= max_dist_from_center:
    #                 city_neighbors.append(r_dict["origin_addresses"][i])
    #     # pp.pprint(city_neighbors)
    #     return city_neighbors

    # def filter_results(self, distances):
    #     max_dist_from_center = 150.0 # km
    #     min_hits_num = 3
    #     city_neighbors = []
    #     pp = pprint.PrettyPrinter(indent=4)
    #     distances_bak = copy.deepcopy(distances)
    #     # pp.pprint(distances_bak)
    #     distances = distances[1:]
    #     # pp.pprint(distances_bak)
    #     for origin in range(len(distances)):
    #         # if origin == 0:
    #         #     continue
    #         num_hits = 0
    #         for destination in range(len(distances[0])-1):
    #             destination += 1
    #             if float(distances[origin][destination]) <= float(max_dist_from_center):
    #                 # pp.pprint(float(distances[origin][destination]))
    #                 num_hits += 1
    #         if num_hits < min_hits_num:
    #             distances_bak[origin] = []
    #     return distances_bak


    def filter_results(self, distances):
        max_dist_from_center = 150.0 # km
        min_hits_num = 3
        city_neighbors = []
        pp = pprint.PrettyPrinter(indent=4)
        distances_filtered = []
        distances = distances[1:]
        for origin in range(len(distances)):
            # if origin == 0:
            #     continue
            num_hits = 0
            for destination in range(len(distances[0])-1):
                destination += 1
                if float(distances[origin][destination]) <= float(max_dist_from_center):
                    # pp.pprint(float(distances[origin][destination]))
                    num_hits += 1
            if num_hits >= min_hits_num:
                distances_filtered.append(distances[origin])
        return distances_filtered    


    def chunk_origins(self, origins):
        num_candidate_cities = len(origins)
        chunk_size = 10
        num_chunks = math.ceil(num_candidate_cities/chunk_size)
        leftovers = num_candidate_cities % chunk_size
        # print(leftovers)
        chunked_origins = []
        # all_city_neighbors = []
        for c in range(num_chunks):
            if c*chunk_size <= num_candidate_cities-chunk_size-1:
                chunked_origins.append(origins[c*chunk_size:(c+1)*chunk_size])
            else:
                chunked_origins.append(origins[c*chunk_size:c*chunk_size+leftovers])
        return chunked_origins

    def compute_distance_matrix(self, all_origins, destinations):
        pp = pprint.PrettyPrinter(indent=4)
        chunked_origins = self.chunk_origins(all_origins)
        # pp.pprint(chunked_origins)
        filename = "./distance_matrix.csv"
        distances = [[]]
        for origins in chunked_origins:
            # pp.pprint(origins)
            # pp.pprint(destinations)
            results = foo.test_basic_params(origins, destinations)
            # pp = pprint.PrettyPrinter(indent=4)
            r_dict = json.loads(results.text)
            # pp.pprint(r_dict)
            destinations = r_dict["destination_addresses"]
            origins = r_dict["origin_addresses"]
            rows = r_dict["rows"]
            # distances = [[]]
            if os.path.isfile(filename) == False:
                distances[0] = ["City"]
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
                # pp.pprint(distances)
                distances.append(distance)
                # pp.pprint(distances)
            # filename = "./distance_matrix.csv"
            # f = open(filename, "w")
            if os.path.isfile(filename) == False:
                with open(filename, 'w') as f:
                    for distance in distances:
                        # pp.pprint(' '.join(distance))
                        d_str = ' '.join(distance)
                        # pp.pprint(d_str)
                        f.write(f"{d_str}\n")
                    f.close()
            else:
                with open(filename, 'a') as f:
                    for distance in distances:
                        # pp.pprint(' '.join(distance))
                        d_str = ' '.join(distance)
                        # pp.pprint(d_str)
                        f.write(f"{d_str}\n")
                    f.close()

        return distances

    def find_neighbors(self, center_city, destinations):
        pp = pprint.PrettyPrinter(indent=4)

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
    "San Francisco, USA",
    "Half Moon Bay, USA",
    "San Jose, USA",
    "Fremont, USA",
    "Palo Alto",
    "Berkeley, USA",
    # "Sacramento, USA",
    "San Mateo, USA",
    "Oakland, USA"
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

dist_mat = foo.compute_distance_matrix(cal_cities[0:15], attractive_centers)
# pp.pprint(dist_mat)
filtered_cities = foo.filter_results(dist_mat)
pp.pprint(filtered_cities)


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