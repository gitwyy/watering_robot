'''
Copyright (c) [2018] [Kanokkorn]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
# import modules 
#from gps3 import gps3
import serial
import math
import time
import csv
import torch
# setup gps socket
'''#ser = serial.Serial('/dev/ttyUSB0', 9600)
gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()
'''

# prefix parameter for 
distance = 10
earth_radius = 6371e3

in_lat = 10.725450
in_lon = 99.375350

#read csv files
with open('watering_robot/lat_lon.csv', newline='') as f:
    read = csv.reader(f)
    for gps_row in read:
        print(gps_row)
        lat_b = float(gps_row[0]) #unpack list to float
        lon_b = float(gps_row[1]) 
        # main function
        while (distance > 6):            
            lat_A = math.radians(in_lat)
            lat_B = math.radians(lat_b)
            del_lat = math.radians(lat_b-(in_lat))
            del_lon = math.radians(lon_b-(in_lon))
            a = (math.sin(del_lat/2)*math.sin(del_lat/2))+math.cos(lat_A)*math.cos(lat_B)*(math.sin(del_lon/2)*math.sin(del_lon/2))
        
            # check if equal zero
            try:
                c = 2*math.atan2(math.sqrt(a), math.sqrt((1-a)))
            except ValueError as identifier:
                print("No Value")
            distance = earth_radius*c        
            print("distance: ", distance)
            print("MOVE")
            in_lat += 0.0000005
            in_lon += 0.0000005
            time.sleep(0.02)
            #ser.write(str.encode('M'))

        else:
            print("distance: ", distance)
            print("STOP")
            #ser.write(str.encode('S'))
            for xtime in range(20):
                #ser.write(str.encode('N'))
                #ser.write(str.encode('F'))
                print(xtime)
                time.sleep(0.2)
            distance = 10
            in_lat = lat_b
            in_lon = lon_b
    else:
        print('End of lines')



