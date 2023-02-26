# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 22:26:36 2023

@author: bezbakri
"""

import csv

#vehicles = open("vehicles.csv")
zip_codes = open("Craigslist-Aware_ZipCodes.csv")
lat_longs = open("us_zip_codes.csv")

#vehicles_reader = csv.reader(vehicles)
zip_codes_reader = csv.reader(zip_codes)
zip_codes_list = []
for row in zip_codes_reader:
    zip_codes_list.append(row)
lat_longs_reader = csv.reader(lat_longs)
lat_longs_list = []
for row in lat_longs_reader:
    lat_longs_list.append(row)


with open("city_zip_lat_long.csv", "w") as f:
    fwriter = csv.writer(f)
    fwriter.writerow(["zip", "city", "lat", "long"])
    for row in zip_codes_list:
        row_to_write = [row[0], row[-1]]
        for row_ in lat_longs_list:
            if row_to_write[0] == row_[0]:
                row_to_write.extend(row_[1:])
        fwriter.writerow(row_to_write)
        
lat_longs.close()
zip_codes.close()