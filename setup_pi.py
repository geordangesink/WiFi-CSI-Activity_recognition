## setup raspberry pi (rpi)
## this code requires:
## - the rpi to have SSH enabled, as well as a working SSH connection between this computer and the rpi (SSH key pairs installed)
## - the rpi to have access to the internet (WLAN or Ethernet)
## 
## this code:
## - installs the nexmon_csi repository from github (https://github.com/nexmonster/nexmon_csi_bin) using the nexmonster one-line install 
## - copies the necessary python scripts to the root of pi user on the rpi
## - 

import os

rpi_address = input("RaspberryPi IPv6 address? ")

# one-line install from nexmonster github (note that installing nexmon disables wifi on the rpi)
os.system(f'ssh pi@[{rpi_address}] curl -fsSL https://raw.githubusercontent.com/nexmonster/nexmon_csi_bin/main/install.sh | sudo bash')

# make sure wifi chip wlan0 is active
os.system(f'ssh pi@[{rpi_address}] ifconfig wlan0 up')

# add a listener/monitor called mon0 on the wifi chip wlan0
os.system(f'ssh pi@[{rpi_address}] iw dev wlan0 interface add mon0 type monitor')

# copy script to the root of the rpi
os.system(f'scp ./setup_monitor.py pi@[{rpi_address}]:~')