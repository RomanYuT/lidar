"""
Consume LIDAR measurement file and create an image for display.

Adafruit invests time and resources providing this open source code.
Please support Adafruit and open source hardware by purchasing
products from Adafruit!

Written by Dave Astels for Adafruit Industries
Copyright (c) 2019 Adafruit Industries
Licensed under the MIT license.

All text above must be included in any redistribution.
"""

import os
from math import cos, sin, pi, floor
import pygame
from adafruit_rplidar import RPLidar

# Screen width & height
W = 640
H = 480

SCAN_BYTE = b'\x20'
SCAN_TYPE = 129

# Set up pygame and the display
#os.putenv('SDL_FBDEV', '/dev/fb1')
pygame.display.init()
lcd = pygame.display.set_mode((W,H))
pygame.mouse.set_visible(False)
lcd.fill((200,0,0))
pygame.display.update()

# Setup the RPLidar
PORT_NAME1 = '/dev/ttyUSB0'#!!!!!!!!!!!!!!!!!!!!!!!!записать сюда порты
PORT_NAME2 = '/dev/ttyUSB1'
lidar1 = RPLidar(None, PORT_NAME1)
lidar2 = RPLidar(None, PORT_NAME2)

# used to scale data to fit on the screen
max_distance = 0

#pylint: disable=redefined-outer-name,global-statement
def process_data(data1,data2):
    global max_distance
    lcd.fill((0,0,0))
    point = ( int(W / 2) , int(H / 2) )
    
    pygame.draw.circle(lcd,pygame.Color(255, 255, 255),point,10 )
    pygame.draw.circle(lcd,pygame.Color(100, 100, 100),point,100 , 1 )
    pygame.draw.line( lcd,pygame.Color(100, 100, 100) , ( 0, int(H/2)),( W , int(H/2) ) )
    pygame.draw.line( lcd,pygame.Color(100, 100, 100) , ( int(W/2),0),( int(W/2) , H ) )

    for angle in range(360):
        distance1 = data1[angle]
        distance2 = data2[angle]
        if distance1 > 0:                  # ignore initially ungathered data points
            max_distance = max([min([5000, distance1]), max_distance])
            radians = angle * pi / 180.0
            x = distance1 * cos(radians)
            y = distance1 * sin(radians)
            point = ( int(W / 2) + int(x / max_distance * (W/2)), int(H/2) + int(y / max_distance * (H/2) ))
            pygame.draw.circle(lcd,pygame.Color(0, 0, 255),point,2 )

        if distance2 > 0:                  # ignore initially ungathered data points
            max_distance = max([min([5000, distance2]), max_distance])
            radians = angle * pi / 180.0
            x = distance2 * cos(radians)
            y = distance2 * sin(radians)
            point = ( int(W / 2) + int(x / max_distance * (W/2)), int(H/2) + int(y / max_distance * (H/2) ))
            pygame.draw.circle(lcd,pygame.Color(0, 255, 0),point,2 )
    pygame.display.update()


scan_data1 = [0]*360
scan_data2 = [0]*360

def _process_scan(raw):
    '''Processes input raw data and returns measurment data'''
    new_scan = bool(raw[0] & 0b1)
    inversed_new_scan = bool((raw[0] >> 1) & 0b1)
    quality = raw[0] >> 2
    if new_scan == inversed_new_scan:
        raise RPLidarException('New scan flags mismatch')
    check_bit = raw[1] & 0b1
    if check_bit != 1:
        raise RPLidarException('Check bit not equal to 1')
    angle = ((raw[1] >> 1) + (raw[2] << 7)) / 64.
    distance = (raw[3] + (raw[4] << 8)) / 4.
    return new_scan, quality, angle, distance

def lidar_measurments(self, max_buf_meas=500):
       
        lidar.set_pwm(800)
        status, error_code = self.health
        
        cmd = SCAN_BYTE
        self._send_cmd(cmd)
        dsize, is_single, dtype = self._read_descriptor()
        if dsize != 5:
            raise RPLidarException('Wrong info reply length')
        if is_single:
            raise RPLidarException('Not a multiple response mode')
        if dtype != SCAN_TYPE:
            raise RPLidarException('Wrong response data type')
        while True:
            raw = self._read_response(dsize)
            self.log_bytes('debug', 'Received scan response: ', raw)
            if max_buf_meas:
                data_in_buf = self._serial_port.in_waiting
                if data_in_buf > max_buf_meas*dsize:
                    self.log('warning',
                             'Too many measurments in the input buffer: %d/%d. '
                             'Clearing buffer...' %
                             (data_in_buf//dsize, max_buf_meas))
                    self._serial_port.read(data_in_buf//dsize*dsize)
            yield _process_scan(raw)

def lidar_scans(self, max_buf_meas=500, min_len=5):
        
        scan = []
        iterator = lidar_measurments(lidar,max_buf_meas)
        for new_scan, quality, angle, distance in iterator:
            if new_scan:
                if len(scan) > min_len:
                    yield scan
                scan = []
            if quality > 0 and distance > 0:
                scan.append((quality, angle, distance))

try:
   
    
     for scan1,scan2 in zip(lidar1.iter_scans(),lidar2.iter_scans()):
        
        for (_, angle, distance) in scan1:
            scan_data1[min([359, floor(angle)])] = distance
        for (_, angle, distance) in scan2:
            scan_data2[min([359, floor(angle)])] = distance
        process_data(scan_data1,scan_data2)

except KeyboardInterrupt:
    print('Stoping.')
lidar.stop()
lidar.disconnect()
