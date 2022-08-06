#!/usr/bin/env python
import signal
import sys
import subprocess
from host import Host
from switch import Switch
from controller import Controller
from configparser import ConfigParser
from node import Node
from globalvariables import *


nodes = {}


def create_seafile() -> Node:
    node = create_node('seafile', seafileserver, nodes['brex'], external_subnet, 1, setFiles=False)
    subprocess.run(f'docker cp seafile:/home/seafolder seafolder', shell=True)
    out = subprocess.run("cat seafolder", shell=True, capture_output=True)
    parser = ConfigParser()
    parser.read('serverconfig.ini')
    parser.set("50", "seafolder",  out.stdout.decode('utf8'))
    parser.set("200", "seafolder", out.stdout.decode('utf8'))
    parser.set("210", "seafolder", out.stdout.decode('utf8'))
    parser.set("220", "seafolder", out.stdout.decode('utf8'))
    with open('serverconfig.ini', 'w') as configfile:
        parser.write(configfile)
    return node


def create_linuxclient(name: str, image: str, bridge: Node, subnet: str, address: int, behaviour: str) -> Node:
    node = create_node(name, image, bridge, subnet, address)
    subprocess.run(f"docker cp automation {name}:/home/debian/automation", shell=True)
    subprocess.run(f"docker cp printersip/{subnet.split('.')[2]} {name}:/home/debian/automation/packages/system/printerip", shell=True)
    subprocess.run(f"docker cp sshiplist.ini {name}:/home/debian/automation/packages/system/sshiplist.ini", shell=True)
    subprocess.run(f"docker cp client_behaviour/{behaviour}.ini {name}:/home/debian/automation/packages/system/config.ini", shell=True)
    subprocess.run(f"docker cp serverconfig.ini {name}:/home/debian/automation/packages/system/serverconfig.ini", shell=True)
    if behaviour == 'external_attacker':
        subprocess.run(f"docker cp attack/external_ipListPort80.txt {name}:/home/debian/automation/packages/attacking/ipListPort80.txt", shell=True)
        subprocess.run(f"docker cp attack/external_ipList.txt {name}:/home/debian/automation/packages/attacking/ipList.txt", shell=True)
        subprocess.run(f"docker cp attack/external_iprange.txt {name}:/home/debian/automation/packages/attacking/iprange.txt", shell=True)
    elif behaviour == 'attacker':
        subprocess.run(f"docker cp attack/internal_ipListPort80.txt {name}:/home/debian/automation/packages/attacking/ipListPort80.txt", shell=True)
        subprocess.run(f"docker cp attack/internal_ipList.txt {name}:/home/debian/automation/packages/attacking/ipList.txt", shell=True)
        subprocess.run(f"docker cp attack/internal_iprange.txt {name}:/home/debian/automation/packages/attacking/iprange.txt", shell=True)
    return node


def create_node(name: str, image: str, bridge: Node, subnet: str, address: int, setFiles=True) -> Node:
    node = Host(name)
    node.instantiate(image)
    node.connect(bridge)
    node.setIp(subnet+str(address), 24, bridge)
    node.setDns(['8.8.8.8', '8.8.4.4'])
    # Define default gateway of nodes
    if bridge == nodes['brint']: node.setDefaultGateway(int_gateway, bridge)
    if bridge == nodes['brex']:  node.setDefaultGateway(ex_gateway , bridge)
    # Add routes to enable nodes within internal subnet communicate with server subnet
    if subnet != server_subnet: node.addRoute(server_subnet+'0', 24, bridge)
    if subnet != management_subnet: node.addRoute(management_subnet+'0', 24, bridge)
    if subnet != office_subnet: node.addRoute(office_subnet+'0', 24, bridge)
    if subnet != developer_subnet: node.addRoute(developer_subnet+'0', 24, bridge)
    if subnet != external_subnet: node.addRoute(external_subnet+'0', 24, bridge)
    if setFiles:
        subprocess.run(f"docker cp serverconfig.ini {name}:/home/debian/serverconfig.ini", shell=True)
        subprocess.run(f"docker cp backup.py {name}:/home/debian/backup.py", shell=True)
    return node


def unmakeChanges(nodes):
    [node.delete() for _,node in nodes.items()]


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    unmakeChanges(nodes)
    sys.exit(0)


#try:
# Set up Switches
nodes['brint'] = Switch("brint")
nodes['brint'].instantiate()
nodes['brint'].setIp(brint_ip, 24)
nodes['brint'].connectToInternet(int_gateway, 24)

nodes['brex'] = Switch("brex")
nodes['brex'].instantiate()
nodes['brex'].setIp(brex_ip, 24)
nodes['brex'].connectToInternet(ex_gateway, 24)
nodes['brex'].connect(nodes['brint'])

subprocess.run(f"ip route add 192.168.200.0/24 dev veth-host-brint", shell=True)
subprocess.run(f"ip route add 192.168.210.0/24 dev veth-host-brint", shell=True)
subprocess.run(f"ip route add 192.168.220.0/24 dev veth-host-brint", shell=True)


# Create Seafile Server
nodes['seafile'] = create_seafile()


# Set up controllers
nodes['c1'] = Controller("c1")
nodes['c1'].instantiate()
nodes['c1'].connect(nodes['brint'])
nodes['c1'].setIp(c1_ip, 24, nodes['brint'])
nodes['c1'].initController(c1_ip, c1port)
nodes['brint'].setController(c1_ip, c1port)

nodes['c2'] = Controller("c2")
nodes['c2'].instantiate()
nodes['c2'].connect(nodes['brex'])
nodes['c2'].setIp(c2_ip, 24, nodes['brex'])
nodes['c2'].initController(c2_ip, c2port)
nodes['brex'].setController(c2_ip, c2port)


# Set Server Subnet
nodes['mail']   = create_node('mail',   mailserver,   nodes['brint'], server_subnet, 1)
nodes['file']   = create_node('file',   fileserver,   nodes['brint'], server_subnet, 2)
nodes['web']    = create_node('web',    webserver,    nodes['brint'], server_subnet, 3)
nodes['backup'] = create_node('backup', backupserver, nodes['brint'], server_subnet, 4)


# Set Management Subnet
nodes['mprinter'] = create_node('mprinter', printerserver, nodes['brint'], management_subnet, 1)
nodes['m1'] = create_linuxclient('m1', linuxclient, nodes['brint'], management_subnet, 2, 'management')
nodes['m2'] = create_linuxclient('m2', linuxclient, nodes['brint'], management_subnet, 3, 'management')
nodes['m3'] = create_linuxclient('m3', linuxclient, nodes['brint'], management_subnet, 4, 'management')
nodes['m4'] = create_linuxclient('m4', linuxclient, nodes['brint'], management_subnet, 5, 'management')
    

# Set Office Subnet
nodes['oprinter'] = create_node('oprinter', printerserver, nodes['brint'], office_subnet, 1)
nodes['o1'] = create_linuxclient('o1', linuxclient, nodes['brint'], office_subnet, 2, 'office')
nodes['o2'] = create_linuxclient('o2', linuxclient, nodes['brint'], office_subnet, 3, 'office')


# Set Developer Subnet
nodes['dprinter'] = create_node('dprinter', printerserver, nodes['brint'], developer_subnet, 1)
nodes['d1' ] = create_linuxclient('d1',   linuxclient, nodes['brint'], developer_subnet, 2,  'administrator')
nodes['d2' ] = create_linuxclient('d2',   linuxclient, nodes['brint'], developer_subnet, 3,  'administrator')
nodes['d3' ] = create_linuxclient('d3',   linuxclient, nodes['brint'], developer_subnet, 4,  'developer')
nodes['d4' ] = create_linuxclient('d4',   linuxclient, nodes['brint'], developer_subnet, 5,  'developer')
nodes['d5' ] = create_linuxclient('d5',   linuxclient, nodes['brint'], developer_subnet, 6,  'developer')
nodes['d6' ] = create_linuxclient('d6',   linuxclient, nodes['brint'], developer_subnet, 7,  'developer')
nodes['d7' ] = create_linuxclient('d7',   linuxclient, nodes['brint'], developer_subnet, 8,  'developer')
nodes['d8' ] = create_linuxclient('d8',   linuxclient, nodes['brint'], developer_subnet, 9,  'developer')
nodes['d9' ] = create_linuxclient('d9',   linuxclient, nodes['brint'], developer_subnet, 10, 'developer')
nodes['d10'] = create_linuxclient('d10', linuxclient, nodes['brint'], developer_subnet, 11, 'developer')
nodes['d11'] = create_linuxclient('d11', linuxclient, nodes['brint'], developer_subnet, 12, 'developer')
nodes['d12'] = create_linuxclient('d12', linuxclient, nodes['brint'], developer_subnet, 13, 'attacker')
nodes['d13'] = create_linuxclient('d13', linuxclient, nodes['brint'], developer_subnet, 14, 'attacker')


# Set External Subnet
nodes['eweb'] =  create_node('eweb', repository+'webserver',  nodes['brex'], external_subnet, 2)
nodes['e1'] = create_linuxclient('e1', linuxclient, nodes['brex'], external_subnet, 3, 'external_attacker')
nodes['e2'] = create_linuxclient('e2', linuxclient, nodes['brex'], external_subnet, 4, 'external_attacker')

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to destroy experiment')
signal.pause()
except Exception as e:
    print(str(e))
    unmakeChanges(nodes)


