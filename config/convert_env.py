import json
import shutil
import yaml

def convert_json_config(config):
    validator_dict = {}
    faulty_dict = {}
    string = ""

    if 'groups' in config:
        groups = config['groups']
        string += str(groupset_to_node_validatorset(groups))
        validator_dict = groupset_to_node_validatorset(groups)
        del config['groups']

    if 'unary_link' in config:
        unary = config['unary_link']
        string += str(add_unary_validate(unary, validator_dict))
        validator_dict = add_unary_validate(unary, validator_dict)
        del config['unary_link']

    if 'binary_link' in config:
        binary = config['binary_link']
        validator_dict = add_binary_validate(binary, validator_dict)
        del config['binary_link']

    make_env_file(validator_dict)
    make_docker_compose_file(validator_dict) 

def make_env_file(validator_dict):
    for node in validator_dict.keys():
        shutil.copy('default.env', 'q_' + str(node)+'.env')
        with open('q_'+str(node)+'.env', "a") as f:
            v_set = "VALIDATORS=["
            for vnode in validator_dict[node]:
                if(vnode != validator_dict[node][-1]):
                    v_set+=("\"$core"+str(vnode)+"\", ")
                else:
                    v_set+=("\"$core"+str(vnode)+"\"]")
            f.write(v_set)

def make_docker_compose_file(validator_dict):
    port = 11680
    config_dict={}
    config_dict.setdefault("version", "\"3.3\"":)
    config_dict.setdefault("services", dict())
    config_dict.setdefault("volumes", list()) 

    for node in validator_dict.keys():
        config_dict["services"].setdefault("db"+str(node), dict())
        config_dict["services"]["db"+str(node)].setdefault("image", "stellar/stellar-core-state")
        config_dict["services"]["db"+str(node)].setdefault("volumes", ["db"+str(node) + "-data:/var/lib/postgresql/data", "db"+str(node)+"-unixsocket:/postgresql-unix-sockets"])
        config_dict["services"].setdefault("core"+str(node), dict())
        config_dict["services"]["core"+str(node)].setdefault("image", "zzim2x/stellar-core-quorum:9.2.0")
        config_dict["services"]["core"+str(node)].setdefault("env_file", ["q_"+str(node)+".env"])
        config_dict["services"]["core"+str(node)].setdefault("command", "core"+str(node)+" initdb newhist forcescp")
        config_dict["services"]["core"+str(node)].setdefault("volumes", ["./q_inter.cfg.tmpl:/etc/confd/templates/stellar-core.cfg.tmpl", "db"+str(node)+"-unixsocket:/var/run/postgres", "history-data:/opt/stellar-core/history"])
        config_dict["services"]["core"+str(node)].setdefault("environment", dict())
        config_dict["services"]["core"+str(node)]["environment"].setdefault("KNOWN_PEERS", "")
        v_set = "\'["
        for vnode in validator_dict[node]:
            if(vnode != validator_dict[node][-1]):
                v_set+=("\"core"+str(vnode)+"\", ")
            else:
                v_set+=("\"core"+str(vnode)+"\"]\'")
        config_dict["services"]["core"+str(node)]["environment"]["KNOWN_PEERS"]=v_set
        config_dict["services"]["core"+str(node)]["environment"].setdefault("COMMANDS", '[\"ll?level=debug\"]')
        config_dict["services"]["core"+str(node)].setdefault("ports", [str(port+int(node)) + ":11626"])
        config_dict["services"]["core"+str(node)].setdefault("depends_on", ["db"+str(node)])
    with open('docker-compose.yaml', 'w') as f:
        f.write(yaml.dump(config_dict, default_flow_style=False))

def groupset_to_node_validatorset(group_dict):
    node_list = {}
    for group_name in group_dict:
        for from_node in group_dict[group_name]:
            if from_node not in node_list:
                node_list.setdefault(from_node, list())
            for to_node in group_dict[group_name]:
                if (to_node not in node_list[from_node]) and (to_node != from_node):
                    node_list[from_node].append(to_node)

    return node_list


def add_unary_validate(unaryLink_list, validatorList):
    node_list = validatorList
    for nodes in unaryLink_list:
        node_list = add_nodes(nodes[0], nodes[1], node_list)

    return node_list


def add_binary_validate(binaryLink_list, validatorList):
    node_list = validatorList
    for nodes in binaryLink_list:
        node_list = add_nodes(nodes[0], nodes[1], node_list)
        node_list = add_nodes(nodes[1], nodes[0], node_list)

    return node_list


def add_nodes(from_nodes, to_nodes, validatorList):
    node_list = validatorList

    if isinstance(from_nodes, (list, tuple,)):
        for from_node in from_nodes:
            if from_node not in node_list:
                node_list.setdefault(from_node, list())

            if isinstance(to_nodes, (list,)):
                for to_node in to_nodes:
                    if (to_node not in node_list[from_node]) and (to_node != from_node):
                        node_list[from_node].append(to_node)

            else:
                node_list[from_node].append(to_nodes)
    else:
        if from_nodes not in node_list:
            node_list.setdefault('from_nodes', list())

        if isinstance(to_nodes, (list, tuple,)):
            for to_node in to_nodes:
                if to_node not in node_list[from_nodes] and to_node != from_nodes:
                    node_list[from_nodes].append(to_node)

        else:
            node_list[from_nodes].append(to_nodes)

    return node_list

if __name__=='__main__':
    
    with open("config.json") as f:
        convert_json_config(json.load(f))


