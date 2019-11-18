from textfsm import TextFSM
from pandas import DataFrame
from io import StringIO
from tabulate import tabulate


template = """####
Value Filldown PROTOCOL (\w)
Value Filldown CANDIDATE (\s|\*)
Value Filldown CODE (\w{0,2})
Value Required,Filldown NETWORK (\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})
Value Filldown MASK (\d{1,2})
Value DISTANCE (\d+)
Value METRIC (\d+)
Value NEXTHOP_IP (\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})
Value NEXTHOP_IF ([A-Z][\w\-\.:/]+)
Value UPTIME (\d[\w:\.]+)

Start
  ^Gateway.* -> Routes

Routes
  # For "is (variably )subnetted" line, capture mask, clear all values.
  ^\s+\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}\/${MASK}\sis -> Clear
  #
  # Match directly connected route with explicit mask
  ^${PROTOCOL}${CANDIDATE}${CODE}(\s+)?${NETWORK}\/${MASK}\sis\sdirectly\sconnected,\s${NEXTHOP_IF} -> Record
  #
  # Match directly connected route (mask is inherited from "is subnetted")
  ^${PROTOCOL}${CANDIDATE}${CODE}(\s+)?${NETWORK}\sis\sdirectly\sconnected,\s${NEXTHOP_IF} -> Record
  #
  # Match regular routes, with mask, where all data in same line
  ^${PROTOCOL}${CANDIDATE}${CODE}(\s+)?${NETWORK}\/${MASK}\s\[${DISTANCE}/${METRIC}\]\svia\s${NEXTHOP_IP}(,\s${UPTIME})?(,\s${NEXTHOP_IF})? -> Record
  #
  # Match regular route, all one line, where mask is learned from "is subnetted" line
  ^${PROTOCOL}${CANDIDATE}${CODE}(\s+)?${NETWORK}\s\[${DISTANCE}\/${METRIC}\]\svia\s${NEXTHOP_IP}(,\s${UPTIME})?(,\s${NEXTHOP_IF})? -> Record
  #
  # Match route with no via statement (Null via protocol)
  ^${PROTOCOL}${CANDIDATE}${CODE}(\s+)?${NETWORK}\/${MASK}\s\[${DISTANCE}/${METRIC}\],\s${UPTIME},\s${NEXTHOP_IF} -> Record
  #
  # Match "is a summary" routes (often Null0)
  ^${PROTOCOL}${CANDIDATE}${CODE}(\s+)?${NETWORK}\/${MASK}\sis\sa\ssummary,\s${UPTIME},\s${NEXTHOP_IF} -> Record
  #
  # Match regular routes where the network/mask is on the line above the rest of the route
  ^${PROTOCOL}${CANDIDATE}${CODE}(\s+)?${NETWORK}\/${MASK} -> Next
  #
  # Match regular routes where the network only (mask from subnetted line) is on the line above the rest of the route
  ^${PROTOCOL}${CANDIDATE}${CODE}(\s+)?${NETWORK} -> Next
  #
  # Match the rest of the route information on line below network (and possibly mask)
  ^\s+\[${DISTANCE}\/${METRIC}\]\svia\s${NEXTHOP_IP}(,\s${UPTIME})?(,\s${NEXTHOP_IF})? -> Record
  #
  # Match load-balanced routes
  ^\s+\[${DISTANCE}\/${METRIC}\]\svia\s${NEXTHOP_IP} -> Record
  #
  # Clear all variables on empty lines
  ^\s* -> Clearall

EOF"""
res = ["""IOSXE-01# show ip route
Codes: C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       o - ODR, P - periodic downloaded static route

Gateway of last resort is 194.0.0.2 to network 0.0.0.0

     1.0.0.0/32 is subnetted, 1 subnets
S       1.1.1.1 [1/0] via 212.0.0.1
                [1/0] via 192.168.0.1
     2.0.0.0/24 is subnetted, 1 subnets
S       2.2.2.0 is directly connected, FastEthernet0/0.100
     4.0.0.0/16 is subnetted, 1 subnets
O E2    4.4.0.0 [110/20] via 194.0.0.2, 1d18h, FastEthernet0/0.100
     5.0.0.0/24 is subnetted, 1 subnets
D EX    5.5.5.0 [170/2297856] via 10.0.1.2, 00:12:01, Serial0/0"""]

for r in res:
    print("=" * 80)
    print(r)
    print("*" * 80)
    parser = TextFSM(StringIO(template))
    hdrs, vals = parser.header, parser.ParseText(r)
    df = DataFrame(vals, columns=hdrs)
    print(tabulate(df, headers=hdrs))
print("=" * 80)

import pdb
pdb.set_trace()
