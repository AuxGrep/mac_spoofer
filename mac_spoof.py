import subprocess
import logging
import sys
import time
import os
import platform
from colorama import Fore, Style
import argparse

logs = logging.basicConfig(level=logging.DEBUG, filemode='a', filename='mac_spoof.log', format='[%(asctime)s] - %(levelname)s %(message)s')

version = 2.0

def args_parse():
    parser = argparse.ArgumentParser(description='Spoof MAC address on a network interface')
    parser.add_argument('-i', '--interface', help='Network interface to spoof MAC address on', required=True)
    parser.add_argument('-m', '--mac', help='MAC Spoofer Program', required=True)
    return parser.parse_args()

def checkroot():
    if not 'SUDO_UID' in os.environ.keys():
        sys.exit(f'{Fore.RED}Run the script with root{Style.RESET_ALL}')

def interface_check(interface):
    try:
        if interface in os.listdir('/sys/class/net'):
            return interface
        else:
            logging.error(f'This interface:{interface} is Invalid')
            sys.exit(f'\nInvalid Interface: {interface}')

    except Exception as e:
        exit(logging.error(e))

def os_check(support=['Linux', 'Unix']):
    if platform.system() not in support:
        logging.error('Unsupported OS detected')
        exit('This program runs on Linux only')

def mac(interface, bssid):
    try:
        logging.info(f'Disabling the WPA service on {interface}')
        print('[Console] ===> Disabling WPA service')
        subprocess.run(['systemctl', 'stop', 'wpa_supplicant.service'], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        time.sleep(2)

        logging.info(f'Killing the Network and Libs for WPA service')
        print('[Console] ===> Killing the Network and Libs for WPA service')
        subprocess.run(['airmon-ng', 'check', 'kill'], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        time.sleep(2)

        logging.info(f'Starting the Network and Libs for WPA service')
        print('[Console] ===> Starting the Network and Libs for WPA service')
        subprocess.run(['systemctl', 'start', 'wpa_supplicant.service'], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        time.sleep(2)

        logging.warning(f'Bringing the Interface Down')
        print('[Console] ===> Bringing the Interface Down')
        os.system(f'ip link set {interface} down')
        time.sleep(2)

        logging.info(f'Changing the MAC Address on Interface {interface} to {bssid}')
        print(f'[Console] ===> Changing the MAC Address on Interface {interface} to {bssid}')
        subprocess.run(['macchanger', interface, '-b', '-m', bssid], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        time.sleep(2)

        print(f'[Console] ===> Enabling the interface: {interface} up')
        logging.info(f'Enabling the interface: {interface} up')
        os.system(f'ip link set {interface} up')

        print('[Console] ===> Starting a Network Manager Service')
        logging.info('Starting a Network Manager Service')
        subprocess.run(['systemctl', 'start', 'NetworkManager.service'], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        time.sleep(3)

        print('[Console] ===> Done')
    except OSError as e:
        logging.error(e)

def print_banner():
    banner = r"""
{0}__  __    _    ____   ____  ____   ___   ___  _____ _____ ____  
|  \/  |  / \  / ___| / ___||  _ \ / _ \ / _ \|  ___| ____|  _ \ 
| |\/| | / _ \| |     \___ \| |_) | | | | | | | |_  |  _| | |_) |
| |  | |/ ___ \ |___   ___) |  __/| |_| | |_| |  _| | |___|  _ <  COder: AuxGrep
|_|  |_/_/   \_\____| |____/|_|    \___/ \___/|_|   |_____|_| \_\
                                                                 {1}""".format(Fore.CYAN, Style.RESET_ALL)
    print(banner)

if __name__ == "__main__":
    print_banner()
    print('Program Started .....')
    time.sleep(3)
    args = args_parse()
    checkroot()
    interface_check(interface=args.interface)
    os_check()
    mac(interface=args.interface, bssid=args.mac)
