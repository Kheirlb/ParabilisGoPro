import sh
import time
from goprocam import GoProCamera, constants

sh.rfkill('unblock', '0') #starts wifi if off

print(sh.wpa_cli("-i", "wlan0", "list_networks")) #lists all networks

#choose cameras from networks listed
input1 = input('Choose first camera using the network id (Ex: 1): ')
input2 = input('Choose second camera using the network id (Ex: 2): ')

recordCmd = input('Would you like to start recording for all selected cameras once connected? (y/n): ')

sh.wpa_cli("-i", "wlan0", "select_network", input1)
print(sh.wpa_cli("-i", "wlan0", "list_networks"))

time.sleep(2)

while sh.hostname('-I') == '\n':
    print('Waiting for connection...')
    print(sh.hostname('-I'))
    time.sleep(1)   

print(sh.hostname('-I'))
gp1 = GoProCamera.GoPro()
gp1.overview()

if recordCmd =='y':
    gp1.shutter(constants.start)

if gp1.IsRecording() == 1:
    print('First camera IsRecording confirmation: YES, RECORDING NOW')

endRecording = input('Press [Enter] to End Recording: ')
gp1.shutter(constants.stop)



    


