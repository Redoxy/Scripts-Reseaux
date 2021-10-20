#! /usr/bin/python3
# _*_ coding: utf-8-unix _*_

#from netmiko import ConnectHandler
import ipaddress
import os
import threading
import queue

cmd = []

with open('input/commands', 'r') as cmd_file:
    for line in cmd_file:
        cmd.append(line)

hosts = []

with open('input/hosts', 'r') as host_file:
    for line in host_file:
        line = line.upper()
        hosts.append(line)

q= queue.Queue()

def worker():
    while True:
        item = q.get()
        print(f'Working on {item}')
        for each in cmd:
            print(f'Command :{each} sent to device : {item}')
        print(f'Finished {item}')
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

