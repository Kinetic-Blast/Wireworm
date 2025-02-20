import pywifi
import time
import MacAdress
from pywifi import const
from rich.console import Console
from rich.table import Table
from rich.live import Live

MacFile = "manufacturers.txt"  # Path to the MAC address vendor file

def dbm_to_percentage(dbm):
    """Convert dBm signal strength to a percentage."""
    return max(0, min(100, 2 * (dbm + 100)))

def get_wifi_info():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()
    time.sleep(1)  # Allow scan results to populate
    scan_results = iface.scan_results()

    # Security mapping
    security_names = {
        0: 'None', 1: 'WEP', 2: 'WPA', 3: 'WPA-PSK',
        4: 'WPA2', 5: 'WPA2-PSK', 6: 'WPA3'
    }

    # Filter out duplicate SSIDs
    unique_networks = {}
    for result in scan_results:
        ssid = result.ssid if result.ssid else "Hidden Network"
        security_type = security_names.get(result.akm[0] if result.akm else 0, 'Unknown')

        bssid = result.bssid.rstrip(':')  # Ensure proper formatting
        vendor_info = MacAdress.find_manufacturer(bssid, MacFile)  # Lookup vendor info

        if ssid not in unique_networks or result.signal > unique_networks[ssid]['signal']:
            unique_networks[ssid] = {
                'signal': result.signal,
                'signal_percentage': dbm_to_percentage(result.signal),
                'bssid': bssid,
                'security': security_type,
                'vendor': vendor_info if vendor_info else "Unknown"
            }

    # Sort networks by strongest signal (highest dBm)
    sorted_networks = dict(sorted(unique_networks.items(), key=lambda x: x[1]['signal'], reverse=True))
    return sorted_networks

def create_table(networks):
    """Generate a table for displaying Wi-Fi scan results."""
    table = Table(title="Real-Time Wi-Fi Scanner (Sorted by Signal Strength)", show_header=True, header_style="bold cyan")
    table.add_column("SSID", style="bold")
    table.add_column("Signal (dBm)", justify="right")
    table.add_column("Signal %", justify="right")
    table.add_column("BSSID", justify="right")
    table.add_column("Security", justify="right")
    table.add_column("Vendor", justify="right")

    for ssid, data in networks.items():
        table.add_row(
            ssid,
            f"{data['signal']} dBm",
            f"{data['signal_percentage']}%",
            data['bssid'],
            data['security'],
            data['vendor']
        )
    return table

def live_scan():
    """Continuously update Wi-Fi scan results in real-time."""
    console = Console()
    with Live(console=console, auto_refresh=True) as live:
        while True:
            networks = get_wifi_info()
            live.update(create_table(networks))
            time.sleep(3)  # Refresh interval

if __name__ == "__main__":
    live_scan()
