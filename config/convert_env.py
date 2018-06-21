import json

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

    if 'nodes' in config:
        nodes = config['nodes']
        config['faulties'] = dict()
        for node in nodes:
            if 'threshold' in nodes[node]:
                validator_dict[node]['quorum']['threshold'] = nodes[node]['threshold']

            if 'faulty_kind' in nodes[node]:
                case_dict = {}
                faulty_dict[node] = []
                case_dict.setdefault('case', dict())['kind'] = nodes[node]['faulty_kind']
                faulty_dict[node].append(case_dict)

                if 'faulty_percent' in nodes[node]:
                    for node_case in faulty_dict[node]:
                        node_case['case']['frequency'] = nodes[node]['faulty_percent']

                    if isinstance(nodes[node]['faulty_percent'], dict):
                        for node_case in faulty_dict[node]:
                            node_case['case']['frequency']['per_consensus'] = nodes[node]['faulty_percent']['per_consensus']

                if 'duration' in nodes[node]:
                    for node_case in faulty_dict[node]:
                        node_case['case']['duration'] = nodes[node]['duration']

                if 'target_nodes' in nodes[node]:
                    for node_case in faulty_dict[node]:
                        node_case['case']['target_nodes'] = nodes[node]['target_nodes']

        del config['nodes']

    with open("q_inter.env", "w") as q:
        q.write(str(validator_dict))
        q.write(str(faulty_dict))
        q.write("/n")
        q.write(string)
    config['nodes'] = validator_dict
    config['faulties'] = faulty_dict


    return config 

def groupset_to_node_validatorset(group_dict):
    node_list = {}
    for group_name in group_dict:
        for from_node in group_dict[group_name]:
            if from_node not in node_list:
                node_list.setdefault(from_node, dict()).setdefault('quorum', dict()).setdefault('validators', list())
            for to_node in group_dict[group_name]:
                if (to_node not in node_list[from_node]) and (to_node != from_node):
                    node_list[from_node]['quorum']['validators'].append(to_node)

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
                node_list.setdefault(from_node, dict()).setdefault('quorum', dict()).setdefault('validators', list())

            if isinstance(to_nodes, (list,)):
                for to_node in to_nodes:
                    if (to_node not in node_list[from_node]) and (to_node != from_node):
                        node_list[from_node]['quorum']['validators'].append(to_node)

            else:
                node_list[from_node].append(to_nodes)
    else:
        if from_nodes not in node_list:
            node_list.setdefault('from_nodes', dict()).setdefault('quorum', dict()).setdefault('validators', list())

        if isinstance(to_nodes, (list, tuple,)):
            for to_node in to_nodes:
                if to_node not in node_list[from_nodes] and to_node != from_nodes:
                    node_list[from_nodes]['quorum']['validators'].append(to_node)

        else:
            node_list[from_nodes]['quorum']['validators'].append(to_nodes)

    return node_list

if __name__=='__main__':
    
    with open("config.json") as f:
        temp_design=convert_json_config(json.load(f))
    print(temp_design)


