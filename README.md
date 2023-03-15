# unifi
Disable and enable a switch port and or profile on a schedule

This is just in case anyone else was looking for a solution on how to do this, I searched for a long time and set it up using the Unifi API Browser and Client https://github.com/Art-of-WiFi/UniFi-API-browser and then decided I didn't need the browser running so made a couple of Python scripts instead.

The on.py switches a specified port on or changes it from another port profile. I used Python3 and urllib3 suppresses the HTTPS pop ups. You can run it using /usr/bin/python3 on.py (assuming you name it on_script) or you can put it into cron etc.

The off.py simply disables the specified switch port, useful if you're totally paranoid about Wi-Fi or have kids that change their MAC address to bypass rules that schedule downtime for their MAC Address, you can again put it into cron etc

