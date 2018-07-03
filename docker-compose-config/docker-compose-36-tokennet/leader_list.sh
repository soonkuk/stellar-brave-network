import argparse
import collections
from texttable import Texttable

parser = argparse.ArgumentParser()
parser.add_argument('node', type=str, help='node name')
args = parser.parse_args()
node = args.node
leader_dict={}
with open('node'+str(node)+'_leader_list', 'r') as f:
    for line in f.readlines():
        leader = line.split()[5][4:]
        if int(leader) < 10:
            leader = "0"+str(leader)
        if str(leader) not in leader_dict.keys():
            leader_dict.setdefault("core"+str(leader), 1)
        leader_dict["core"+str(leader)]+=1

ol = collections.OrderedDict(sorted(leader_dict.items()))
t = Texttable()
for k, v in ol.items():
    t.add_row([k, str(v)])
print (t.draw())
