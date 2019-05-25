import sh
print(sh.wpa_cli("-i", "wlan0", "list_networks"))

search1 = "SmashCam01"
networkNum = sh.cut(sh.grep(sh.wpa_cli("-i", "wlan0", "list_networks"), search1), "-f", "1")
sh.wpa_cli("-i", "wlan0", "select_network", networkNum)
print(sh.wpa_cli("-i", "wlan0", "list_networks"))
    


