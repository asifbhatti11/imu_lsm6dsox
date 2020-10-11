#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Imu
import time
import board
import busio
from adafruit_lsm6ds import LSM6DSOX

i2c = busio.I2C(board.SCL, board.SDA)
sensor = LSM6DSOX(i2c)

calibration=(0,0,0)
# go to https://learn.adafruit.com/adafruit-sensorlab-magnetometer-calibration 
# and perform calibration, replace (0,0,0) with it.

def imu():
    pub = rospy.Publisher('imu', Imu, queue_size=1)
    rospy.init_node('imu', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        imu_msg = Imu()
        imu_msg.header.stamp = rospy.Time.now()
        imu_msg.header.frame_id = "lsm6dsox"
        imu_msg.linear_acceleration.x=sensor.acceleration[0]
        imu_msg.linear_acceleration.y=sensor.acceleration[1]
        imu_msg.linear_acceleration.z=sensor.acceleration[2]
        imu_msg.angular_velocity.x=sensor.gyro[0]-calibration[0]
        imu_msg.angular_velocity.y=sensor.gyro[1]-calibration[1]
        imu_msg.angular_velocity.z=sensor.gyro[2]-calibration[2]
        pub.publish(imu_msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        imu()
    except rospy.ROSInterruptException:
        pass

