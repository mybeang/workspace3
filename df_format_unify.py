import re
from pandas import DataFrame
from tabulate import tabulate


def _ch_mac_format(mac):
    # all format to 00:00:00:00:00:00
    if re.findall(r"\d+-\d+-\d+-\d+-\d+-\d+", mac):
        # 00-00-00-00-00-00
        mac = mac.replace("-", ":")
    elif re.findall(r"\d+\.\d+\.\d+", mac):
        # 0000.0000.0000
        _mac = mac.replace(".", "")
        mac = ":".join(["".join(i) for i in zip(_mac[0::2], _mac[1::2])])
    return mac


def _ch_port_format(port):
    # If just pnum, only pnum not with any char.
    # If with linecard, the type of port is capital letter.
    if re.findall(r"^eth\d+$", port):
        # eth01, eth21 ...
        port = port.replace("eth", "")
    elif re.findall(r"\w+\d+\/\d+", port):
        # ge0/1, xe0/1
        port = port.upper()
    return port


def reformed(df):
    """
    Return the format of data in dataframe.

    :param df: Dataframe Object
    :return: Processed Dataframe Object
    """
    df = df.applymap(lambda x: _ch_mac_format(x))  # processing mac format
    df = df.applymap(lambda x: _ch_port_format(x))  # processing port format
    return df


if __name__ == "__main__":
    dfs = list()
    data1 = [
        ('VLAN', 'PORTS', 'MAC'),
        ('10', 'eth1', '00:00:01:00:00:01'),
        ('11', 'eth2', '00:00:01:00:00:02')
    ]
    dfs.append(DataFrame(data1[1:], columns=data1[0]))

    data2 = [
        ('VLAN', 'PORTS', 'MAC'),
        ('10', '1', '00:00:01:00:00:01'),
        ('11', '2', '00:00:01:00:00:02')
    ]
    dfs.append(DataFrame(data2[1:], columns=data2[0]))

    data3 = [
        ('VLAN', 'PORTS', 'MAC'),
        ('10', 'XE0/1', '00-00-01-00-00-01'),
        ('11', 'XE0/2', '00-00-01-00-00-02')
    ]
    dfs.append(DataFrame(data3[1:], columns=data3[0]))

    data4 = [
        ('VLAN', 'PORTS', 'MAC'),
        ('10', 'ge0/1', '0000.0100.0001'),
        ('11', 'ge0/2', '0000.0100.0002')
    ]
    dfs.append(DataFrame(data4[1:], columns=data4[0]))

    data5 = [
        ('VLAN', 'PORTS', 'MAC'),
        ('10', 'portextender1/1', '00:00:01:00:00:01'),
        ('11', 'portextender1/2', '00:00:01:00:00:02')
    ]
    dfs.append(DataFrame(data5[1:], columns=data5[0]))

    print("======================================")
    for _df in dfs:
        header = ('VLAN', 'PORTS', 'MAC')
        print("** origin **")
        print(tabulate(_df, headers=header))
        print("\n** convert **")
        print(tabulate(re_form(_df), headers=header))
        print("======================================")
