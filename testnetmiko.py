from netmiko import ConnectHandler

import ipaddress
import os
import sys
import threading
import queue

def get_cdp_neighbor_details(ip, username, password, secret):

    ssh_connection = ConnectHandler(
        device_type='cisco_ios',
        ip=ip,
        username=username,
        password=password,
        secret=secret,
    )

    ssh_connection.enable()

    result =  ssh_connection.find_prompt() + "\n"

    result += ssh_connection.send_command("show cdp neighbor detail", delay_factor=2)

    ssh_connection.disconnect()

    return result

result = get_cdp_neighbor_details("192.168.0.10", "admin", "admin", "cisco")
print(result)