import os

#"[fe80::5184:6da9:7e6b:bc24%15]" #
rpi_address = "[fe80::5184:6da9:7e6b:bc24%15]" #input("raspberrypi address (include square brackets if IPv6)? ")

channel = input('channel? ')
bandwidth = input('bandwidth(MHz)? ')
n_packets = input('number of packets? ')
n_streams = "1"

# setup wifi interface monitor on rpi
os.system(f'ssh pi@{rpi_address} sudo python setup_monitor.py {channel} {bandwidth} {n_packets} {n_streams}')



if os.name == 'nt': # for windows cuz windows is so special crying emoji
    path = '\\'.join(__file__.split('\\')[:-1]) + '\\'
    file_path = f'data\\{channel}_{bandwidth}\\'
    
    print("current directory: " + path)
    
    if not os.path.isdir(path + file_path):
        os.system(f"mkdir " + (path + file_path))    # for windows               

else:  # for others (macos / linux)
    path = '/'.join(__file__.split('/')[:-1]) + '/'
    file_path = f'data/{channel}_{bandwidth}/'
    
    print("current directory: " + path)

    # create required directories if they do not exist yet
    if not os.path.isdir(path + file_path):
        os.system(f"mkdir -p " + path + file_path)  





# do the same in the rpi
os.system(f"ssh pi@{rpi_address} sudo mkdir -p ~/{file_path[:-1]}")

print()

# scan current directory for past data
print(path + file_path)
obj = os.scandir(path + file_path)

acts = {}
act = ""

for filename in obj:
    file_info = filename.name[:-5].rsplit('-', 1)
    if not file_info[0] in acts.keys():
        acts[file_info[0]] = 0
    else:
        acts[file_info[0]] = max(int(file_info[1]), acts[file_info[0]])


if not len(acts.keys()) == 0:
    print("previous actions in this directory:")
    max_filename_length = max([len(key) for key in acts.keys()])
    for item in acts.items():
        print(item[0].expandtabs(max_filename_length) + f'\t [{item[1]+1} time{"" if item[1]==0 else "s"}]')
else:
    print("empty directory")



# data collection
new_act = input('\nactivity (q to quit)? ')
while not new_act=='q':
    act = act if new_act=="" else new_act
    
    if act not in acts.keys():
        acts[act] = 0
    else:  
        acts[act] += 1

    new_filename = act + '-' + str(acts[act])
    
    # run the data collection
    os.system(f'ssh pi@{rpi_address} '+ f'sudo tcpdump -i wlan0 dst port 5500 -vv -w data/{channel}_{bandwidth}/{new_filename}.pcap -c {n_packets}')

    # copy the data to directory on host computer
    os.system(f"scp -6 pi@{rpi_address}:~/data/{channel}_{bandwidth}/{new_filename}.pcap {path}{file_path}")
    
    new_act = input('\nactivity (q to quit)? ')



















