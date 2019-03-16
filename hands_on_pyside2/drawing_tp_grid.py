from pandas import DataFrame
from tabulate import tabulate


def print_topology(last_port):
    ports = list(range(1, last_port+1))
    ports.pop(1)
    ports.append(2)
    ports = ["p{}".format(i) for i in ports]
    ports.insert(0, 'Lan1')
    ports.append('Lan2')
    tps_tuple_list = list(zip(ports[0::2], ports[1::2]))
    tps = ["{} <-> {}".format(*tp) for tp in tps_tuple_list]
    data = {"Topology":tps}
    tp_data = DataFrame(data)
    print(tabulate(tp_data, headers='keys', tablefmt='grid'))

def vlan_setting(last_port):
    vlan_num = int(last_port / 2)
    vlans = [i + 10 for i in range(vlan_num)]
    ports = list(range(1, last_port+1))
    ports.pop(1)
    ports.append(2)
    ports = ["p{}".format(i) for i in ports]
    mem_list = list(zip(ports[0::2], ports[1::2]))
    data = {"vlan_id": vlans, "membership": mem_list}
    tp_data = DataFrame(data)
    print(tabulate(tp_data, headers='keys', tablefmt='grid'))


if __name__=="__main__":
    last_ports = [6, 8, 10, 24, 26, 44, 48]
    for last_port in last_ports:
        if not (last_port % 2 == 0):
            raise ValueError("last port should be odd")
        print("Use port num: %d" % last_port)
        print_topology(last_port)
        vlan_setting(last_port)
        print("")