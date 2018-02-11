# -*- coding: utf-8 -*-

"""
Script to drive a edison car using a webserver hosted on the vehicle.

"""
from datetime import datetime
import edisoncar as ec

V = ec.vehicle.Vehicle()

cam = ec.parts.Webcam()
V.add(cam, outputs = [ 'cam/image_array' ], threaded = True)

rcin_controller = ec.parts.TeensyRCin()
V.add(rcin_controller, outputs = [ 'rcin/angle', 'rcin/throttle' ], threaded = True)

speed_controller = ec.parts.AStarSpeed()
V.add(speed_controller, outputs = [ 'odo/speed' ], threaded = True)

ctr = ec.parts.LocalWebController()
V.add(ctr,
      inputs = [ 'cam/image_array', 'rcin/angle', 'rcin/throttle' ],
      outputs = [ 'user/angle', 'user/throttle', 'user/mode', 'user/recording' ],
      threaded = True)

steering_controller = ec.parts.Teensy('S')
steering = ec.parts.PWMSteering(controller = steering_controller,
                                left_pulse = 496, right_pulse = 242)

throttle_controller = ec.parts.Teensy('T')
throttle = ec.parts.PWMThrottle(controller = throttle_controller,
                                max_pulse = 496, zero_pulse = 369, min_pulse = 242)

V.add(steering, inputs = [ 'user/angle', 'user/mode' ])
V.add(throttle, inputs = [ 'user/throttle', 'user/mode' ])

#add tub to save data
path = '~/myedison/sessions/' + datetime.now().strftime('%Y_%m_%d__%H_%M_%S')
inputs = [ 'user/angle', 'user/throttle', 'cam/image_array', 'user/mode', 'odo/speed', 'user/recording' ]
types = [ 'float', 'float', 'image_array', 'str', 'float', 'boolean' ]
tub = ec.parts.OriginalWriter(path, inputs = inputs, types = types)
V.add(tub, inputs = inputs)

#run the vehicle for 20 seconds
V.start(rate_hz = 20) # , max_loop_count = 1000)

#you can now go to localhost:8887 to move a square around the image
