import os
from math import floor
from adafruit_rplidar import RPLidar
import matplotlib.pyplot as plt
import numpy as np
import PyLidar3
import time # Time module
import two_lidars

for n in two_lidars.dataxy_1pair():
    print(n)
