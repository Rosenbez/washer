import time

import board
import busio

import adafruit_mma8451

i2c = busio.I2C(board.SCL, board.SDA)

# For raspi, may need to change the i2c baudrate in /boot/config.txt
# I needed to add 'dtparam=i2c_arm_baudrate=1000' in the file above
sensor = adafruit_mma8451.MMA8451(i2c)

while True:
    x, y, z = sensor.acceleration
    print('Acceleration: x={0:0.3f}, y={1:0.3f}, z={2:0.3f}, m/s^2'.format(x, y, z))
    time.sleep(.2)

