import socket
import datetime
import yaml
import csv

from washer_client import WasherClient
from notifier import EmailNotifier


def write_data(data_dict):
    with open("accel_logs.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for t in data_dict:
            writer.writerow(
                [str(t), data_dict[t]["x"], data_dict[t]["y"], data_dict[t]["z"]]
            )
    print("data written")


class udp_connection:
    def __init__(self, udp_ip, udp_port):
        self._udp_ip = udp_ip
        self._udp_port = udp_port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind(("", self._udp_port))

    def read_json_data(self) -> dict:
        # Read json/yaml from the given socket, return a dict
        data, addr = self._sock.recvfrom(1024)
        accel_data = yaml.safe_load(data)
        print('recieved message:', data.decode('utf-8'))
        # print(datetime.datetime.now())
        # print('from:', addr)
        return accel_data


if __name__ == "__main__":
    UDP_IP = "192.168.7.54"
    UDP_PORT = 5005
    test_email = "xxxxxxxxxxxxxxxxxxxxx"

    washer_udp = udp_connection(UDP_IP, UDP_PORT)
    test_notifier = EmailNotifier(test_email)
    washer = WasherClient(test_notifier)
    print("Starting UPD Socket")
    while True:
        accel_data = washer_udp.read_json_data()
        ts = datetime.datetime.now()
        washer.add_reading(accel_data, ts)
