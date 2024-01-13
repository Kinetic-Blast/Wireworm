import re

def normalize_mac_address(mac_address):
    """
    Normalize the MAC address by removing non-hex characters, converting to uppercase,
    and adding colons between pairs of characters.

    :param mac_address: The MAC address to normalize (string)
    :return: The normalized MAC address
    """
    return ':'.join(re.findall(r'[0-9a-fA-F]{2}', mac_address.upper()))

def find_manufacturer(mac_address, manuf_file_path):
    """
    Find the manufacturer of a given MAC address using the provided manuf_file.

    :param mac_address: The MAC address to look up (string)
    :param manuf_file_path: The path to the file containing MAC address information
    :return: The manufacturer name or 'Not found' if the MAC address is not in the file
    """
    try:
        mac_address = normalize_mac_address(mac_address)

        with open(manuf_file_path, 'r', encoding='utf-8', errors='ignore') as file:
            manuf_data = file.read()

        oui = mac_address[:8]  # Extract the OUI (first 6 characters)

        lines = manuf_data.split('\n')
        for line in lines:
            if line.startswith(oui):
                parts = line.split('\t')
                if len(parts) >= 3:
                    return parts[2].strip()

        return 'Not found'

    except FileNotFoundError:
        return 'File not found'

