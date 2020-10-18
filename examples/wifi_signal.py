#!/usr/bin/env python

import time
import blinkt
import subprocess

# send a command to the shell and return the result
def cmd(cmd):
    return subprocess.Popen(
        cmd, shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    ).stdout.read().decode()

# parsing iwconfig output which looks something like
# wlan0     IEEE 802.11  ESSID:"tm2tb-dix"
#           Mode:Managed  Frequency:5.24 GHz  Access Point: 38:94:ED:CE:87:E4
#           Bit Rate=24 Mb/s   Tx-Power=31 dB
#           Retry short limit:7   RTS thr:off   Fragment thr:off
#           Power Management:on
#           Link Quality=38/70  Signal level=-72 dBm
#           Rx invalid nwid:0  Rx invalid crypt:0  Rx invalid frag:0
#           Tx excessive retries:394  Invalid misc:0   Missed beacon:0
def get_signal_from_iwconfig_output(output):
    for line in response.splitlines():
        if line.split()[0] == 'Link':
            # this is ugly as shit, but gets the numerator
            return int(line.split()[1].split('=')[1].split('/')[0])

def get_max_signal_from_iwconfig_output(output):
    for line in response.splitlines():
        if line.split()[0] == 'Link':
            # this is ugly as shit, but gets the numerator
            return int(line.split()[1].split('=')[1].split('/')[1])


blinkt.set_clear_on_exit()
num_pixels = blinkt.NUM_PIXELS
strength = 0
max_strength = 70
min_strength = 30

while True:
    response = cmd('iwconfig wlan0')
    strength = get_signal_from_iwconfig_output(response)
    if strength < min_strength:
        strength = min_strength
    max_strength = get_max_signal_from_iwconfig_output(response)
    print strength
    pixels_to_set = (strength - min_strength) * num_pixels // (max_strength - min_strength)
    pixels_to_set += 1 # always have one LED lit
    if pixels_to_set > num_pixels:
        pixels_to_set = num_pixels
    for i in range(0, pixels_to_set):
        blinkt.set_pixel(i, 128, 0, 0)
    strength += 1
    strength %= max_strength
    blinkt.show()
    time.sleep(0.1)
    blinkt.clear()
