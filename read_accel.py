import socket
import datetime
import yaml
import csv


def write_data(data_dict):
    with open('accel_logs.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for t in data_dict:
            writer.writerow([str(t), data_dict[t]['x'],
                            data_dict[t]['y'],
                            data_dict[t]['z']])
    print('data written')


UDP_IP= '192.168.7.54'
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print('Starting UPD Socket')
accel_buf ={}
buf_lim = 30
buf_count = 0

while True:
    data, addr = sock.recvfrom(1024)
    ts = datetime.datetime.now()
    accel_data = yaml.load(data)
    print('recieved message:', data.decode('utf-8'))
    print(datetime.datetime.now())
    print('from:', addr)
    
    accel_buf[ts] = accel_data
    buf_count += 1
    
    if buf_count >= buf_lim:
        write_data(accel_buf)
        accel_buf = {}
        buf_count = 0

