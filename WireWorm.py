import pywifi
import MacAdress
import time
from pywifi import const

print("""
    ██     ██ ██ ██████  ███████      
    ██     ██ ██ ██   ██ ██           
    ██  █  ██ ██ ██████  █████        
    ██ ███ ██ ██ ██   ██ ██           
     ███ ███  ██ ██   ██ ███████      
                                      
                                      
██     ██  ██████  ██████  ███    ███ 
██     ██ ██    ██ ██   ██ ████  ████ 
██  █  ██ ██    ██ ██████  ██ ████ ██ 
██ ███ ██ ██    ██ ██   ██ ██  ██  ██ 
 ███ ███   ██████  ██   ██ ██      ██ 
                                      
                                      """)





def get_wifi_info():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()

    scan_results = iface.scan_results()

    # Filter out duplicate SSIDs
    unique_networks = {}
    for result in scan_results:
        ssid = result.ssid
        if ssid not in unique_networks or result.signal > unique_networks[ssid]['signal']:
            # Remove the trailing colon from the BSSID
            bssid = result.bssid.rstrip(':')
            unique_networks[ssid] = {
                'signal': result.signal,
                'bssid': bssid,
                'security': result.akm[0],}

    

    # Print the information
    for i, (ssid, data) in enumerate(unique_networks.items(), start=1):

        vendor_info=MacAdress.get_vendor_info(data['bssid'])

        security_names = {0: 'None',1: 'WEP',2: 'WPA',3: 'WPA-PSK',4: 'WPA2',5: 'WPA2-PSK',6: 'WPA3',}
        security_name = security_names.get(data['security'], 'Unknown')
        


        print(f"Network {i}:")
        print(f"  Wi-Fi SSID: {ssid}")
        print(f"  Signal Strength: {data['signal']:.2f} dBm")
        print(f"  BSSID: {data['bssid']}")
        print(f"  Wireless Security: {security_name}")

        print("  --- Additional Information --- \n")

        if vendor_info:print(f"Vendor Information for {data['bssid']} | {vendor_info}")
        else:print("Failed to retrieve vendor information.")


        print("\n")
        time.sleep(2)

if __name__ == "__main__":
    get_wifi_info()









