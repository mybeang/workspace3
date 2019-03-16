import netifaces as ni
from pprint import pformat
from scapy.all import get_windows_if_list


iface_lists = [i['name'] for i in get_windows_if_list()]
#print(pformat(iface_lists))

test_host_name = 'Intel(R) Ethernet Connection I217-LM'

def find_guid_from_host_name(host_name):
    for devinfo in get_windows_if_list():
        if devinfo['name'] == host_name:
            return devinfo['guid']

my_guid = find_guid_from_host_name(test_host_name)

ip, netmask, broadcast = ni.ifaddresses(my_guid)[2][0].values()

print("HostName: {}".format(test_host_name))
print("GUID: {}".format(my_guid))
print("IP = {}".format(ip))
print("netmask = {}".format(netmask))