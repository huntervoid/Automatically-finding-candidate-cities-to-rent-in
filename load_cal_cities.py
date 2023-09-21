import csv
import pprint

csv_file_path='/Users/huntervoid/programming/Ranking cities in NorCal/cal_cities.csv'
cal_cities = []
with open(csv_file_path, 'r') as file:
	csvreader=csv.reader(file)
	for row in csvreader:
		cal_cities.append(row[1])
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(cal_cities)