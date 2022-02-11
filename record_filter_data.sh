#!/bin/bash

./jarvis build jetson/imu_channel
./jarvis build jetson/gps
./jarvis build jetson/filter
./jarvis build lcm_tools/echo
trap 'kill %1; kill %2; kill %3; kill %4; kill %5' SIGINT
./jarvis exec jetson/imu_channel &
./jarvis exec jetson/gps &
./jarvis exec jetson/filter &
./jarvis exec lcm_tools/echo IMUData /imu_data > "data/imu_data$1.txt" &
./jarvis exec lcm_tools/echo GPS /gps > "data/gps_data$1.txt" &
./jarvis exec lcm_tools/echo Odometry /odometry > "data/odom_data$1.txt"
