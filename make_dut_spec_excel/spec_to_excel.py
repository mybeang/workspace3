import os
import yaml, json
import csv
from pandas import DataFrame
from pathlib2 import Path
from tabulate import tabulate
from collections import Counter


class DutSpec(object):
    def __init__(self):
        self.this_path = Path(__file__).parent
        self.spec_path = self.this_path.joinpath('spec')
        file_list = os.listdir(str(self.spec_path))[:-1]
        data_list = list()

        for file_name in file_list:
            with open(str(self.spec_path.joinpath(file_name)), 'r', encoding='utf-8') as f:
                raw_dict = yaml.load(f)
            device_name = file_name.replace(".yaml", "")
            if device_name == 'default':
                continue
            for k, v in raw_dict['feature'].items():
                main = k
                for s_k, s_v in v.items():
                    if 'type' == s_k:
                        sub = 'self'
                        f_type = v['type']
                    else:
                        sub = s_k
                        f_type = s_v
                    data_list.append((main, sub, f_type, device_name))

        self.header = ['main', 'sub', 'types', 'duts']
        self.df = DataFrame(data_list, columns=self.header)
        self.dict_data = dict()
        mains = [item for item, count in Counter(self.df['main']).items() if count >= 1]
        for main in mains:
            self.dict_data[main] = dict()
            db_of_main = self.df.loc[self.df['main'] == main]
            subs = [item for item, count in Counter(db_of_main['sub']).items() if count >= 1]
            for sub in subs:
                self.dict_data[main][sub] = dict()
                db_of_sub = db_of_main.loc[db_of_main['sub'] == sub]
                f_types = [item for item, count in Counter(db_of_sub['types']).items() if count >= 1]
                for f_type in f_types:
                    duts = list(db_of_sub.loc[db_of_sub['types'] == f_type]['duts'])
                    self.dict_data[main][sub][f_type] = duts

    def show_table(self):
        print(tabulate(self.df, headers=self.header))

    def to_json(self):
        with open(str(self.this_path.joinpath('req_of_ds.json')), 'w') as f:
            json.dump(self.dict_data, f, indent=4)

""" == OUTPUT ==
      main              sub             types                  duts
----  ----------------  --------------  ---------------------  ----------
   0  aaa               self            AaaDasan1              eos
   1  bootloader        self            BootLoaderDasan1       eos
   2  system            self            SystemDasan1           eos
   3  system            os              OsDasan1               eos
   4  system            user            UserDasan1             eos
   5  system            time            TimeDasan1             eos
   6  system            coredump        CoreDumpDasan1         eos
   7  system            config          ConfigDasan1           eos
   8  system            log             LogDasan1              eos
   9  system            service         ServiceDasan1          eos
  10  system            mirror          MirrorDasan1           eos
  11  interface         self            InterfaceDasan1        eos
  12  interface         port            PortDasan1             eos
  13  interface         mgmt            MgmtDasan1             eos
  14  interface         vlan            VlanDasan1             eos
  15  interface         gpon            GponDasan1             eos
  16  bridge            self            BridgeDasan1           eos
  17  vlan              self            VlanDasan1             eos
  18  vlan              port            PortDasan1             eos
  19  vlan              fdb             FdbDasan1              eos
  20  slot              self            SlotDasan3             eos
  21  fdb               self            FdbDasan1              eos
  22  max_host          self            MaxHostDasan1          eos
  23  ip                self            IpDasan1               eos
  24  ip                arp             ArpDasan1              eos
  25  ip                route           RouteDasan1            eos
  26  ip                icmp            IcmpDasan1             eos
  27  ip                multicast       MulticastDasan1        eos
  28  filter            self            FilterDasan1           eos
  29  filter            prefix_list     PrefixListDasan1       eos
  30  filter            access_list     AccessListDasan1       eos
  31  filter            ip_access_list  IpAccessListDasan1     eos
"""