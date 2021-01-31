import socket
import datetime
import statistics
import yaml
import csv


def write_data(data_dict):
    with open("accel_logs.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for t in data_dict:
            writer.writerow(
                [str(t), data_dict[t]["x"], data_dict[t]["y"], data_dict[t]["z"]]
            )
    print("data written")


class washer_client:
    def __init__(self):
        self._accel_buf = {}
        self._readings_per_avg = 10
        self._batt = 0
        self._machine_on = False
        self._std_devs = []
        self._std_dev_limit = 2
        self._on_limit = 0.01

    def add_reading(self, accel_data, ts):

        # Add new reading to the accel data dict
        self._accel_buf[ts] = accel_data

        # If we have reached the reading limit, take the std_dev
        if len(self._accel_buf) >= self._readings_per_avg:
            # write_data(accel_buf)
            self.accel_calculate()
            print(f"Battery: {accel_data['batt']:.3f}V")
            self._batt = accel_data["batt"]
            self._accel_buf = {}
            self._buf_count = 0

        if len(self._std_devs) >= self._std_dev_limit:
            self.set_machine_state()

        return

    def set_machine_state(self):
        sensor_mean_std_dev = statistics.mean(self._std_devs)
        print("setting machine state")
        print(f"mean std dev {sensor_mean_std_dev:.6f}")
        if sensor_mean_std_dev >= self._on_limit:
            self._machine_on = True
            print("Washer is on")
        else:
            self._machine_on = False
            print("Washer is off")
        self._std_devs = []

    def get_mean_std(self, values):
        # return a mean and std dev of a list of values
        return statistics.mean(values), statistics.stdev(values)

    def accel_calculate(self):
        # Run calculations on the logged accel data

        xvals, yvals, zvals = [], [], []

        for i in self._accel_buf:
            xvals.append(self._accel_buf[i]["x"])
            yvals.append(self._accel_buf[i]["y"])
            zvals.append(self._accel_buf[i]["z"])

        xmean, xdev = self.get_mean_std(xvals)
        self._std_devs.append(xdev)
        print(f"x mean: {xmean}, x stdev: {xdev:.7f}")


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
        # print('recieved message:', data.decode('utf-8'))
        # print(datetime.datetime.now())
        # print('from:', addr)
        return accel_data


if __name__ == "__main__":
    UDP_IP = "192.168.7.54"
    UDP_PORT = 5005

    washer_udp = udp_connection(UDP_IP, UDP_PORT)
    washer = washer_client()
    print("Starting UPD Socket")
    while True:
        accel_data = washer_udp.read_json_data()
        ts = datetime.datetime.now()
        washer.add_reading(accel_data, ts)
