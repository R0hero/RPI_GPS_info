import serial
import sys
import numpy as np
import os
import csv

def get_cn0(received_data):
    GSV_string = received_data.split(',')
    sv_id = GSV_string[4]
    cn0 = GSV_string[7]
    if cn0 == '':
        cn0 = np.nan
    return sv_id, cn0

def get_ll(received_data):
    GGA_string = received_data.split(',')
    utc_time = GGA_string[1]
    lat = GGA_string[2]
    lon = GGA_string[4]
    
    if not lat == '':
        lat = convert_to_deg(float(lat))
    else:
        lat = np.nan
        
    if not lon == '':
        lon = convert_to_deg(float(lon))
    else:
        lon = np.nan
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

def main():
    
    i = 0
    while True:
        received_data = (str)(SERIAL.readline())
        
        # get CN0 values for specific sv
        if NMEA_SEARCH_STRING_GSV in received_data and CN0_BOOL:
            sv_id, cn0 = get_cn0(received_data)
            print(f'SATELLITE {sv_id} HAS A CN0 of {cn0}')
            append_to_csv(DATA_PATH_CN0,[sv_id, cn0])
        
        # get location and time
        if NMEA_SEARCH_STRING_GGA in received_data and POS_BOOL:
            lat, lon, time = get_ll(received_data)
            no_sv = get_no_sv(received_data)
            print(f'UTC TIME: {time}\nLAT: {lat:.4f} AND LON: {lon:.4f}')
            print(f'NO. OF SATELLITES USED FOR POS FIX: {no_sv}')
            append_to_csv(DATA_PATH_LOC,[time, no_sv, lat, lon])
        
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
    
    main()