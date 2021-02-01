import statistics


class WasherClient:

    def __init__(self, notifier=None):
        self._accel_buf = {}
        self._readings_per_avg = 10
        self._batt = 0
        self._machine_on = False
        self._std_devs = []
        self._std_dev_limit = 2
        self._on_limit = 0.01
        self._notifier = notifier

    def add_reading(self, accel_data, ts):

        # Add new reading to the accel data dict
        self._accel_buf[ts] = accel_data

        # If we have reached the reading limit, take the std_dev
        if len(self._accel_buf) >= self._readings_per_avg:
            self.calculate_vibration()
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
            if self._machine_on:
                self._transition_to_off()
            self._machine_on = False
            print("Washer is off")
        self._std_devs = []

    def _transition_to_off(self):
        # Notify that the machine has turned off
        if self._notifier:
            self._notifier.laundry_finished()

    def get_mean_std(self, values):
        # return a mean and std dev of a list of values
        return statistics.mean(values), statistics.stdev(values)

    def calculate_vibration(self):
        # Run calculations on the logged accel data

        xvals, yvals, zvals = [], [], []

        for i in self._accel_buf:
            xvals.append(self._accel_buf[i]["x"])
            yvals.append(self._accel_buf[i]["y"])
            zvals.append(self._accel_buf[i]["z"])

        xmean, xdev = self.get_mean_std(xvals)
        self._std_devs.append(xdev)
        print(f"x mean: {xmean}, x stdev: {xdev:.7f}")
