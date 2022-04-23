#!/usr/bin/python
import serial
import time
import struct
import signal
import sys
import numpy as np

imu_dataset = []
port = serial.Serial('/dev/ttyACM1', 921600, timeout=1)
port.flush()

try:
    while True:
        data=port.read_until(''.join(['abc\n']).encode('utf-8'))[:-4]
        if(len(data)==8):
            packed_data = struct.unpack('2i',data)
            camera_ts, encoder = packed_data
            print(encoder)
            imu_dataset.append([time.time_ns()/1000000.0,camera_ts, encoder])
        else:
            print("Failed to receive")
            print(len(data))

        time.sleep(1/250)

except KeyboardInterrupt:
    imu_dataset = np.vstack(imu_dataset)
    print('saving the dataset')
    np.savetxt("data_tmp_dir/enc_dataset.csv", imu_dataset, delimiter=",")
    port.flush()
    port.close()
