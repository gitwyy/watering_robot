import gps3
import serial
import math
import time
import csv

# setup
ser = serial.Serial('/dev/ttyUSB0', 9600)
gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()
earth_radius = 6371e3
x = 0

#read csv files
with open('watering_robot/lat_lon.csv', newline='') as f:
    read = csv.reader(f)
    for gps_row in read:
        print(gps_row)
        lat_b = float(gps_row[0])
        lon_b = float(gps_row[1])
        time.sleep(0.2)
        
        #read GPS from socket
        for new_data in gps_socket:
            if new_data:
                data_stream.unpack(new_data)
                print('Altitude = ', data_stream.TPV['lat'], 'Latitude = ', data_stream.TPV['lon'])
                if (data_stream.TPV['lat'] == 'n/a') or (data_stream.TPV['lon'] != 'n/a'):
                    pass
                if (data_stream.TPV['lat'] != '10.0') or (data_stream.TPV['lon'] != '10.0'):
                    try:
                        in_lat = float(data_stream.TPV['lat'])
                    except ValueError:
                        print("lat N/A value")
                        in_lat = (10.712709)
                    try:
                        in_lon = float(data_stream.TPV['lon'])
                    except ValueError:
                        print("lon N/A value")
                        in_lon = (99.378788)
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
                
                # main function
                if (distance > 3):
                    print("distance: ", distance)
                    print("MOVE")
                    ser.write(str.encode('M'))

                elif (distance < 3 and distance != 0):
                    print("distance: ", distance)
                    print("STOP")
                    ser.write(str.encode('S'))
                    time.sleep(20)
                    pass

                elif (distance == 0):
                    print("No value")
                    print("Reset to new value")
