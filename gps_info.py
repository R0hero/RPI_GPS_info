import serial
import numpy as np
import os
import csv
from influxdb import InfluxDBClient

def get_cn0(received_data):
    GSV_string = received_data.split(',')
    sv_id = GSV_string[4]
    cn0 = GSV_string[7]
    if cn0 == '':
        cn0 = -1
    try:
        cn0 = int(cn0)
    except ValueError:
        if not cn0[:2] == '*4':
            cn0 = int(cn0[:2])
        else:
            cn0 = -1
    return sv_id, cn0

def get_ll(received_data):
    GGA_string = received_data.split(',')
    utc_time = GGA_string[1]
    lat = GGA_string[2]
    lon = GGA_string[4]
    
    if not lat == '':
        lat = convert_to_deg(float(lat))
    else:
        lat = float(-1)
        
    if not lon == '':
        lon = convert_to_deg(float(lon))
    else:
        lon = float(-1)
    return lat, lon, utc_time

def convert_to_deg(raw_val):
    decimal_val = raw_val/100
    deg = int(decimal_val)
    mm_mmmm = (decimal_val - int(decimal_val))/0.6
    corr_val = deg + mm_mmmm
    return corr_val

def get_no_sv(received_data):
    GGA_string = received_data.split(',')
    no_sv = GGA_string[7]
    
    return no_sv

def append_to_csv(filepath,data):
    with open(filepath, mode='a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(data)

def write_to_influxdb(measurement_name,data):
    json_body = [
        {
            "measurement": measurement_name,
            "fields": data,
        }
    ]
    CLIENT.write_points(json_body)

def main():
    
    i = 0
    while True:
        received_data = (str)(SERIAL.readline())
        
        # get CN0 values for specific sv
        if NMEA_SEARCH_STRING_GSV in received_data and CN0_BOOL:
            lat, lon, time = get_ll(received_data)
            sv_id, cn0 = get_cn0(received_data)
            print(f'SATELLITE {sv_id} HAS A CN0 of {cn0}')
            append_to_csv(DATA_PATH_CN0,[time, sv_id, cn0])
            print(time)
            write_to_influxdb('CN0_OUTPUT',{'gps_time': time, 'sv_id': sv_id, 'cn0': cn0})
        
        # get location and time
        if NMEA_SEARCH_STRING_GGA in received_data and POS_BOOL:
            lat, lon, time = get_ll(received_data)
            print(time)
            no_sv = get_no_sv(received_data)
            print(f'UTC TIME: {time}\nLAT: {lat} AND LON: {lon}')
            print(f'NO. OF SATELLITES USED FOR POS FIX: {no_sv}')
            append_to_csv(DATA_PATH_LOC,[time, no_sv, lat, lon])
            write_to_influxdb('LOC_OUTPUT',{'gps_time': time, 'lat': lat, 'lon': lon, 'no_sv': no_sv})

        # failsafe if my keyboard stops working :)
        i += 1
        if i == 1000000:
            break

        
if __name__ == '__main__':
    
    SERIAL = serial.Serial ("/dev/ttyS0")
    
    NMEA_SEARCH_STRING_GSV = '$GPGSV'
    NMEA_SEARCH_STRING_GGA = '$GPGGA'
    
    CN0_BOOL = True
    POS_BOOL = True

    DATA_PATH_CN0 = f'DATA{os.sep}CN0_OUTPUT.CSV'
    DATA_PATH_LOC = f'DATA{os.sep}LOC_OUTPUT.CSV'
    

    # InfluxDB stuff
    INFLUXDB_HOST = 'localhost'  # Update with your InfluxDB host
    INFLUXDB_PORT = 8086         # Update with your InfluxDB port
    INFLUX_DB = 'RPI_OUTPUT'  # Replace with your database name
    CLIENT = InfluxDBClient(host=INFLUXDB_HOST, port=INFLUXDB_PORT)
    CLIENT.switch_database(INFLUX_DB)


    main()