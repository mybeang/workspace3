import pythoncom
import wmi


def get_if_list():
    """
    Get the lan card list.

    :return:
        adapter_list: just list of interface name.
        adapter_db: dict. key is name and value is index.
    """
    pythoncom.CoInitialize()
    adapter_list = list()
    adapter_db = dict()
    for adapter in wmi.WMI().Win32_NetworkAdapter():
        if adapter.PhysicalAdapter:
            if 'ROOT' not in adapter.PNPDeviceID:
                adapter_list.append(adapter.Name)
                adapter_db.update({adapter.Name: adapter.Index})
    return adapter_list, adapter_db


def find_if(ifname, db):
    """
    Find the interface in windows by lan card name.

    :param ifname: lan card name
    :param db: data base has mapped name and index about lan card.
    :return: interface object.
    """
    pythoncom.CoInitialize()
    for iface_obj in wmi.WMI().Win32_NetworkAdapterConfiguration():
        if iface_obj.Index == db[ifname]:
            return iface_obj