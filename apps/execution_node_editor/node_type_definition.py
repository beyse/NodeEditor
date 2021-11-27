
import json
import os
import pathlib




class PortDefinition:
    #def __init__(self, port_name : str, data_type : str):
    #    self.port_name = port_name
    #    self.data_type = data_type

    def to_dict(self):
        dict = {}
        dict["port_name"] = self.port_name
        dict["data_type"] = self.data_type
        return dict

    def __init__(self, dict):
        self.port_name = dict["port_name"] 
        self.data_type = dict["data_type"] 

class NodeTypeDefinition:
    #def __init__(self, node_type : str, input_ports , output_ports):
    #    #self.node_name = node_name
    #    self.node_type = node_type
    #    self.input_ports = input_ports
    #    self.output_ports = output_ports

    def to_dict(self):
        dict = {}
        #dict["node_name"] = self.node_name
        dict["node_type"] = self.node_type

        input_port_dicts = []
        for i in self.input_ports :
            input_port_dicts.append(i.to_dict())


        output_port_dicts = []
        for o in self.output_ports :
            output_port_dicts.append(o.to_dict())

        dict["input_ports"] = input_port_dicts
        dict["output_ports"] = output_port_dicts 
        
        dict["default_settings"] = self.default_settings

        return dict

    
    def __init__(self, dict):
        #cls.node_name =  dict["node_name"]
        self.node_type =  dict["node_type"]

        self.input_ports = []
        for i in dict["input_ports"]:
            pd = PortDefinition(i)
            self.input_ports.append(pd)

        self.output_ports = []
        for o in dict["output_ports"]:
            pd = PortDefinition(o)
            self.output_ports.append(pd)

        self.default_settings = dict["default_settings"]

def read_node_type_definitions(directory):

    node_type_definitions = []
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f) and (pathlib.Path(f).suffix == '.json'):
            dict = None
            with open(f) as json_file:
                dict = json.load(json_file)
            ntd = NodeTypeDefinition(dict)
            node_type_definitions.append(ntd)

    return node_type_definitions

def read_node_type_definitions_from_dirs(parent_dir):

    categorized_node_type_definitions = {}

    for filename in os.listdir(parent_dir):
        f = os.path.join(parent_dir, filename)
        if os.path.isdir(f):
            category = filename
            node_type_definitions = read_node_type_definitions(f)
            categorized_node_type_definitions[category] = node_type_definitions
    
    return categorized_node_type_definitions





