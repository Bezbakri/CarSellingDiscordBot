# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 23:30:04 2023

@author: bezbakri
"""

import csv

raw_file = open("city_zip_lat_long.csv")
freader = csv.reader(raw_file)
row_list = []
for row in freader:
    if row[0] == '':
        continue
    if len(row[0]) == 4:
        row[0] = "0" + row[0]
    row_list.append(row)
row_list.sort()
raw_file.close()
with open("city_zip_lat_long.csv", "w", newline='') as f:
    fwriter = csv.writer(f)
    fwriter.writerow(["zip", "city", "lat", "long"])
    for row in row_list[:-1]:
        fwriter.writerow(row)
        
print("done")