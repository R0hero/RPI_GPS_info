import csv
import os
import random
import numpy as np

def append_to_csv(filepath,data):
    with open(filepath, mode='a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(data)


def main():
    i = 0

    sv_id = np.ones(5)
    while True:

        if i % 2 == 0:
            for j in range(5):
                if i == 0:
                    sv_id[j] = random.randrange(0,32)
                cn0 = random.randrange(0,60)
                append_to_csv(DATA_PATH_CN0,[sv_id[j], cn0])
        else:
            if i == 1:
                time = random.randrange(200)
                no_sv = random.randrange(0,32)
                lat = random.randrange(23232,123233)
                lon = random.randrange(1222,512351)
            time += 1
            append_to_csv(DATA_PATH_LOC,[time, no_sv, lat, lon])

        if i == 100:
            break
        i += 1

if __name__ == '__main__':

    DATA_PATH_CN0 = 'DATA' + os.sep + 'CN0_OUTPUT.CSV'
    DATA_PATH_LOC = 'DATA' + os.sep + 'LOC_OUTPUT.CSV'
    main()