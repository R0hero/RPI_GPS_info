# RPI_GPS_info

This script will generate two CSV files with Carrier-to-Noise (CN0) from a specific satellite and the location output from a small Ublox NEO-6M receiver installed on a Rasberry Pi 4 Model b.
The CSV files are to be visually shown in Grafana to see if the CN0 will change over time (it will) and to see if the location is stable.

The serial port will change depending on which pin is used on the Raspberry Pi.

The script can be changed to extract info from different parts of the received data by looking at the spec sheet for the receiver.

Update Nov 16 23:
There has been implemented a custom filesink block for GNU Radio Companion, which will take in a maximum filesize and keep logging 10 files, which in total will add up to the specified maximum filesize. This is to be used together with the file_handling script, which will take an incidence log, if a set condition is met.
