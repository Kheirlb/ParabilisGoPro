from wifi import Cell, Scheme
##savedCell = list(Cell.all('wlan0'))[0]
##print(savedCell.ssid)
##print(savedCell.quality)
##print(savedCell.encrypted)
##print(savedCell.encryption_type)
#ssids = [cell.ssid for cell in Cell.all('wlan0')]
#print(ssids)

class WifiItem():
    def __init__(self):
        self.ssid = ''
    
    def setValues(self, ssid, pw):
        self.ssid = ssid
        self.passkey = pw
        self.encrypted = True
        self.encryption_type = 'wpa2'

wifi1 = WifiItem()
wifi1.setValues('Parabilis', 'wehavecookies')
print(wifi1.ssid)
print(wifi1.passkey)
scheme = Scheme.for_cell('wlan0', wifi1.ssid, wifi1, passkey=wifi1.passkey)
scheme.activate()