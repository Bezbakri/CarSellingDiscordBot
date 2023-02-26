# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 00:34:28 2023

@author: bezbakri
"""

import csv

raw_file = open("city_zip_lat_long.csv")
freader = csv.reader(raw_file)
row_list = []
_ = next(freader)
for row in freader:
    row_list.append(row)
raw_file.close()

vehicles = open("vehicles.csv")
vehicles_reader = csv.reader(vehicles)
row1 = next(vehicles_reader)
row1.extend(["lat", "long"])
f = open("vehicles_updated.csv", "w", newline='')
fwriter = csv.writer(f)
fwriter.writerow(row1)
while True:
    try:
        row = next(vehicles_reader)
        for row_ in row_list:
            if row_[1] == row[2]:
                row.extend(row_[2:])
                break 
            fwriter.writerow(row)
    except StopIteration:
        print("Iteration End")
        break
    except:
        print("Error")
    
vehicles.close()
f.close()
print("Done")