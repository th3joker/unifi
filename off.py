import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

cloudkey_url = 'https://192.168.0.254:8443' # IP Address and port number your cloudkey uses, think the CK+ uses 443 instead of 8443
username = '<username>' # Username of your CloudKey user account
password = '<password>' # Password for the above
site = 'default' # I just left this as is
port_number = 4 # The port you wish to change
switch_mac = '<MAC Address>' # MAC Address of the Switch you want to change the port profile on
profile_name = 'Disabled'

def login():
    session = requests.Session()
    payload = {'username': username, 'password': password}
    session.post(f'{cloudkey_url}/api/login', json=payload, verify=False)
    return session

def get_profile_id(session, profile_name):
    url = f'{cloudkey_url}/api/s/{site}/rest/portconf'
    try:
        response = session.get(url, verify=False)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving port configurations: {e}")
        return None

    portconfs = response.json()['data']

    for portconf in portconfs:
        if portconf.get('name') == profile_name:
            return portconf['_id']

    print(f"No port configuration found with name: {profile_name}")
    return None

def toggle_port(session, enable=True):
    enable_profile_id = get_profile_id(session, profile_name)
    if enable_profile_id is None:
        return

    url = f'{cloudkey_url}/api/s/{site}/stat/device'
    try:
        response = session.get(url, verify=False)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving devices: {e}")
        return

    devices = response.json()['data']

    switch = None
    for device in devices:
        if isinstance(device, dict) and device.get('mac') == switch_mac:
            switch = device
            break

    if switch is None:
        print(f"No switch found with MAC address: {switch_mac}")
        return

    port_overrides = switch.get('port_overrides', [])

    for port in port_overrides:
        if port['port_idx'] == port_number:
            port['disabled'] = not enable
            port['portconf_id'] = enable_profile_id
            break
    else:
        port_overrides.append({
            'port_idx': port_number,
            'disabled': not enable,
            'portconf_id': enable_profile_id
        })

    payload = {
        'port_overrides': port_overrides,
        'op': 'update-port'
    }
    update_url = f'{cloudkey_url}/api/s/{site}/rest/device/{switch["_id"]}'
    try:
        update_response = session.put(update_url, json=payload, verify=False)
        update_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error updating port: {e}")
        print(f"Error response: {update_response.text}")
        return

    print(f"Port {port_number} has been disabled on switch {switch_mac}")

session = login()
toggle_port(session, enable=False)
