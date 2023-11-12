import subprocess
import os
import sys
import time
from colorama import Fore, Style

'''

THIS ONLY FOR EDUCUTIONAL PURPOSES
        CODED BY: AuxGrep

'''
version = 1.0

def args_check():
    if len(sys.argv) < 3:
        sys.exit('USAGE: sudo python3 mac_spoof.py <External_card_interface> <client_mac_address>')

def checkroot():
    if not 'SUDO_UID' in os.environ.keys():
        sys.exit(f'{Fore.RED}Run the script with root{Style.RESET_ALL}')

class Mac_spoof():
    try:
        @staticmethod
        def mac_changer(interface, macADDR):
            non_monitor = os.listdir('/sys/class/net')
            for hacker, network_card in enumerate(non_monitor, start=1):
                print(f'{hacker}.{network_card}')
            print('')
            while True:
                try:
                    card = int(input(f'[>>>] Enter the external network_card interface number 1 to {len(os.listdir("/sys/class/net"))}: '))
                    if card > len(os.listdir('/sys/class/net')) or card == 0:
                        print(f'[xxx] Invalid option!! choose from 1 - {0}'.format(len(os.listdir("/sys/class/net"))))
                        continue
                    else:
                        capture_card = non_monitor[card - 1]
                        with open('card.txt', mode='w') as card_adapter:
                            bk = card_adapter.write(str(capture_card))
                        break
                except KeyboardInterrupt:
                    os.system('clear')
                    sys.exit('Cancelled byeeeee!!!!')

            with open('card.txt', mode='r') as f:
                card_pull = f.read()
            os.system('clear')
            print('[>>>] Deactivating the Network...')
            time.sleep(2)
            subprocess.run(['systemctl', 'stop', 'wpa_supplicant.service'], stderr=subprocess.DEVNULL, \
                        stdout=subprocess.DEVNULL)
            
            print('[>>>] kill Network service')
            time.sleep(2)
            subprocess.run(['airmon-ng', 'check', 'kill'], stderr=subprocess.DEVNULL, \
                        stdout=subprocess.DEVNULL)
            print('[>>>] Enabling the WPA supplicant service')
            time.sleep(1)
            subprocess.run(['systemctl', 'start', 'wpa_supplicant.service'], stderr=subprocess.DEVNULL, \
                        stdout=subprocess.DEVNULL)
            
            print('[>>>] Disabling the {0}'.format(interface))
            time.sleep(2)
            os.system(f'ip link set {card_pull} down')
            print(f'[>>>] Changing the MAc Address to {macADDR}')
            subprocess.run(['macchanger', card_pull, '-b', '-m', macADDR], stderr=subprocess.DEVNULL, \
                        stdout=subprocess.DEVNULL)
            
            print('[>>>] Enabling the interface: {0} up'.format(card_pull))
            time.sleep(2)
            print('[>>>] Starting a Network Manager Service')
            subprocess.run(['systemctl', 'start', 'NetworkManager.service'], stderr=subprocess.DEVNULL, \
                        stdout=subprocess.DEVNULL)
            print('[>>>] DONE')
            return interface, macADDR, card_pull

        @staticmethod
        def check_adapter(interface):
            print('[>>>] Checking the Network card capabilities')
            time.sleep(2)
            try:
                if interface in os.listdir('/sys/class/net'):
                    interface_out = subprocess.check_output(['iwconfig', interface]).decode('utf-8')
                    return 'Mode:Monitor' in interface_out
                else:
                    pass
            except subprocess.CalledProcessError:
                return False
    except KeyboardInterrupt:
        os.system('clear')
        sys.exit('Keyboard Interrupted!! Byeeee!!')

if __name__ == "__main__":
    args_check()
    checkroot()
    interface_name = str(sys.argv[1])
    if Mac_spoof.check_adapter(interface_name):
        print(f'[>>>] Network Adapter Monitor Mode check ...{Fore.GREEN}0k{Style.RESET_ALL}')
        time.sleep(2)
        print(f'[>>>] starting Mac spoofing....{Fore.GREEN}0k{Style.RESET_ALL}')
        time.sleep(2)
        subprocess.run(['airmon-ng', 'stop', interface_name], stderr=subprocess.DEVNULL, \
                       stdout=subprocess.DEVNULL)
        Mac_spoof.mac_changer(interface_name, f"{sys.argv[2]}")

    else:
        print(f'[>>>] Network Adapter Not in Monitor Mode{Fore.MAGENTA} Activating the Network card Now{Style.RESET_ALL}')
        Mac_spoof.mac_changer(interface_name, f"{sys.argv[2]}")
