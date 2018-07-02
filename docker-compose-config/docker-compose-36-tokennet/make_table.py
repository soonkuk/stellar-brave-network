from texttable import Texttable
leader_dict={}
with open('leaders01', 'r') as f:
    for line in f.readlines():
        leader = line.split()[5][4:]
        if str(leader) not in leader_dict.keys():
            leader_dict.setdefault("core"+str(leader), 1)
        leader_dict["core"+str(leader)]+=1
        print(leader_dict)

t = Texttable()
for key in leader_dict.keys():
    t.add_row([key, str(leader_dict[key])])
print (t.draw())
