import os
import subprocess
import sys


channel = sys.argv[1]
bandwidth = sys.argv[2]
n_packets = sys.argv[3]
n_streams = "1"
if len(sys.argv) >= 5:
    n_streams = sys.argv[4]


b64_params = subprocess.check_output(["mcp", "-C", "1", "-N", n_streams, "-c", f'{channel}/{bandwidth}']).decode("utf-8")
os.system("ifconfig wlan0 up")
os.system(f'nexutil -Iwlan0 -s500 -b -l34 -v{b64_params}')

os.system("iw dev wlan0 interface add mon0 type monitor")

os.system("ip link set mon0 up")