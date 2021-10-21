#! /usr/bin/python3
# _*_ coding: utf-8-unix _*_

from netmiko import ConnectHandler
import ipaddress
import os
import sys
import threading
import queue

def sanity_checks(line_to_check):
    print(f'Cheking line : {line_to_check}')
    if line_to_check == 'reload' or line_to_check == 'conf t':
        print(f'Commande : {line_to_check} interdite!')
        sys.exit()
    print(f'Line : {line_to_check}: OK')

cmd = []

with open('input/commands', 'r') as cmd_file:
    for line in cmd_file:
        line = line.strip()
        sanity_checks(line)
        cmd.append(line)

hosts = []

with open('input/hosts', 'r') as host_file:
    for line in host_file:
        line = (line.strip()).upper()
        hosts.append(line)

q= queue.Queue()

def remote_con(ip):
    print(f'Connecting to {ip}')  
    ssh_connection = ConnectHandler(
        device_type='cisco_ios',
        ip=ip,
        username="admin",
        password="admin",
        secret="cisco",
    )

    ssh_connection.enable()
    print(f'Connection to {item} : OK')
    return(ssh_connection)



def worker():
    while True:
        item = q.get()
        ssh = remote_con(item)
        for each in cmd:
            result = ssh.send_command("show cdp neighbor detail", delay_factor=2)
        print(f'Finished {item}')
        print(result)
        q.task_done()

# Turn-on the worker thread
threading.Thread(target=worker, daemon=True).start()

# Send task
for each in hosts:
    q.put(each)
print('All task requests sent\n', end='')

#block until all task are done
q.join()
print('All work completed')

