import argparse
import json
import ruamel.yaml
import shutil
import os

parser = argparse.ArgumentParser()
parser.add_argument('config', type=str, help="config json file")
parser.add_argument('name', type=str, help="docker-compose name")

def convert_json_config(config):
    quorum_dict = {}
    horizon_dict = {}
    string = ""

    if 'groups' in config:
        groups = config['groups']
        string += str(groupset_to_node_validatorset(groups))
        quorum_dict = groupset_to_node_validatorset(groups)
        del config['groups']

    if 'unary_link' in config:
        unary = config['unary_link']
        string += str(add_unary_validate(unary, quorum_dict))
        quorum_dict = add_unary_validate(unary, quorum_dict)
        del config['unary_link']

    if 'binary_link' in config:
        binary = config['binary_link']
        quorum_dict = add_binary_validate(binary, quorum_dict)
        del config['binary_link']

    if 'horizon' in config:
        horizon_dict = config['horizon']

    make_env_file(quorum_dict)
    make_docker_compose_file(quorum_dict, horizon_dict)

def make_env_file(quorum_dict):
    for node in quorum_dict.keys():
        shutil.copy('default.env', './'+args.name+'/'+'q_' + str(node)+'.env')
        with open('./'+args.name+'/'+'q_'+str(node)+'.env', "a") as f:
            v_set = "VALIDATORS=["
            for vnode in quorum_dict[node]:
                if(vnode != quorum_dict[node][-1]):
                    v_set+=("\"$core"+str(vnode)+"\", ")
                else:
                    v_set+=("\"$core"+str(vnode)+"\"]")
            f.write(v_set)

def make_docker_compose_file(quorum_dict, horizon_dict):
    dq = ruamel.yaml.scalarstring.DoubleQuotedScalarString
    port = 11680
    h_port = 7999
    config_dict={}
    config_dict.setdefault("version", dq('3.3'))
    config_dict.setdefault("services", dict())
    config_dict.setdefault("volumes", dict())

    for node in quorum_dict.keys():
        config_dict["services"].setdefault("db"+str(node), dict())
        config_dict["services"]["db"+str(node)].setdefault("image", "stellar/stellar-core-state")
        config_dict["services"]["db"+str(node)].setdefault("volumes", [dq("db"+str(node)+"-data:/var/lib/postgresql/data"), dq("db"+str(node)+"-unixsocket:/postgresql-unix-sockets")])
        config_dict["services"].setdefault("core"+str(node), dict())
        config_dict["services"]["core"+str(node)].setdefault("image", "zzim2x/stellar-core-quorum:9.2.0")
        config_dict["services"]["core"+str(node)].setdefault("env_file", [dq("q_"+str(node)+".env")])
        config_dict["services"]["core"+str(node)].setdefault("command", dq("core"+str(node)+" initdb newhist forcescp"))
        config_dict["services"]["core"+str(node)].setdefault("volumes", [dq("./q_inter.cfg.tmpl:/etc/confd/templates/stellar-core.cfg.tmpl"), dq("db"+str(node)+"-unixsocket:/var/run/postgres"), dq("history-data:/opt/stellar-core/history")])
        config_dict["services"]["core"+str(node)].setdefault("environment", dict())
        config_dict["services"]["core"+str(node)]["environment"].setdefault("KNOWN_PEERS", "")
        v_set = "["
        for vnode in quorum_dict[node]:
            if(vnode != quorum_dict[node][-1]):
                v_set+=("\"core"+str(vnode)+"\", ")
            else:
                v_set+=("\"core"+str(vnode)+"\"]")
        config_dict["services"]["core"+str(node)]["environment"]["KNOWN_PEERS"]=v_set
        config_dict["services"]["core"+str(node)]["environment"].setdefault("COMMANDS", '[\"ll?level=debug\"]')
        config_dict["services"]["core"+str(node)].setdefault("ports", [dq(str(port+int(node)) + ":11626")])
        config_dict["services"]["core"+str(node)].setdefault("depends_on", [dq("db"+str(node))])
        config_dict["volumes"].setdefault("db"+str(node)+"-data")
        config_dict["volumes"].setdefault("db"+str(node)+"-unixsocket")

    for horizon in horizon_dict.keys():
        config_dict["services"].setdefault("horizon"+horizon[1], dict())
        config_dict["services"]["horizon"+horizon[1]].setdefault("image", "zzim2x/stellar-horizon:0.12.3")
        config_dict["services"]["horizon"+horizon[1]].setdefault("command", dq("initdb serve"))
        config_dict["services"]["horizon"+horizon[1]].setdefault("env_file", [dq("q_" + str(horizon_dict[horizon]) + ".env")])
        config_dict["services"]["horizon"+horizon[1]].setdefault("ports", [dq(str(h_port + int(horizon[1]))+":8000")])
        config_dict["services"]["horizon"+horizon[1]].setdefault("environment", dict())
        config_dict["services"]["horizon"+horizon[1]]["environment"].setdefault("POSTGRES_UNIX_SOCKET", dq("/var/run/postgres"))
        config_dict["services"]["horizon"+horizon[1]]["environment"].setdefault("POSTGRES_CORE_UNIX_SOCKET", dq("/var/run/postgres-core"))
        config_dict["services"]["horizon"+horizon[1]]["environment"].setdefault("STELLAR_CORE_URL", dq("http://core"+str(horizon_dict[horizon])+":11626"))
        config_dict["services"]["horizon"+horizon[1]]["environment"].setdefault("SERVE_OPTS", dq("--ingest=true"))
        config_dict["services"]["horizon"+horizon[1]].setdefault("volumes", list())
        config_dict["services"]["horizon"+horizon[1]]["volumes"]=[dq("db"+str(horizon_dict[horizon])+"-unixsocket:/var/run/postgres-core"), dq("db"+str(horizon)+"-unixsocket:/var/run/postgres")]
        config_dict["services"]["horizon"+horizon[1]].setdefault("depends_on", [dq("db"+str(horizon_dict[horizon])), dq("db"+str(horizon)), dq("core"+str(horizon_dict[horizon]))])
        config_dict["services"].setdefault("db"+horizon, dict())
        config_dict["services"]["db"+horizon].setdefault("image", "stellar/stellar-core-state")
        config_dict["services"]["db"+horizon].setdefault("volumes", [dq("db"+horizon+"-data:/var/lib/postgresql/data"), dq("db"+horizon+"-unixsocket:/postgresql-unix-sockets")])
        config_dict["volumes"].setdefault("db"+horizon+"-data")
        config_dict["volumes"].setdefault("db"+horizon+"-unixsocket")

    config_dict["volumes"].setdefault("history-data")

    with open('./'+args.name+'/'+'docker-compose.yaml', 'w') as f:
        ruamel.yaml.dump(config_dict, f, Dumper=ruamel.yaml.RoundTripDumper)


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


def add_unary_validate(unaryLink_list, quorum_dict):
    node_list = quorum_dict
    for nodes in unaryLink_list:
        node_list = add_nodes(nodes[0], nodes[1], node_list)

    return node_list


def add_binary_validate(binaryLink_list, quorum_dict):
    node_list = quorum_dict
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
    
    args = parser.parse_args()
    config_file = args.config
    docker_name = args.name
    os.makedirs("./"+docker_name)
    shutil.copy('q_inter.cfg.tmpl', './'+docker_name+'/')

    with open(config_file) as f:
        convert_json_config(json.load(f))


