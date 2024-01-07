import requests

def get_vendor_info(mac_address):
    url = f"https://api.macvendors.com/{mac_address}"

    try:
        response = requests.get(url)
        return response.text.strip()
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None