
# ![Logo](apps/execution_node_editor/assets/icons/64x64.png) NodeEditor

A multi purpose node editor for flow-based programming.
![Image](doc/screenshot-image-processing.png)
## Description

The purpose of this node editor is to connect functional building blocks and parameterize them in order to form a graph which can then be executed using the execution subsystem.  

### Execution Subsystem
For running the graph created with the node editor the so called `execution subsystem` written in C++ is used. It is based on the [ExecutionNodes](https://github.com/beyse/ExecutionNodes) flow-based programming library also done by me. (Please note the repository is not publicly available yet)

If you want, you could swap the execution subsystem shipped in the Releases by your own system. It just needs to understand the node editor's output format of the graph.

### Node Type Definition

At the present moment the nodes available in the node editor is limited to only a couple of image processing nodes. You can add your own node types by adding a `JSON File` to a subfolder of
`apps\execution_node_editor\execution_subsystem\node_type_definitions` containing your node attributes.
Here is one example:
```json
{
    "node_type": "GaussianBlurNode",
    "input_ports": [
      {
        "port_name": "image",
        "data_type": "image_t"
      }
    ],
    "output_ports": [
      {
        "port_name": "blurred",
        "data_type": "image_t"
      }
    ],
    "default_settings": 
    {
      "sigma": 1.0
    }
}
```

### Output Formats
The node editor creates two files
* The `Scene` with the file extension `.nes` saves the entire scene containing nodes, edges, node settings, viewport settings and user interface settings. It is designed to be loaded again by the node editor.
* The `Graph` with the file extension `.graph.json` saves only the nodes, edges and node settings. It is designed to be an exchange format for the execution subsystem and running the graph.

## License
This software is licensed under [MIT License](https://opensource.org/licenses/MIT).

## Credits
This node editor is based on `pyqt-node-editor` by [Pavel Křupala](https://gitlab.com/pavel.krupala). Visit the original [repository](https://gitlab.com/pavel.krupala/pyqt-node-editor) on GitLab. 

Contribution from other authors:
* The node settings editor is based on [PyQJsonModel](https://github.com/GrxE/PyQJsonModel) 


## Contribution

If you would like to contribute please read this [Contribution Guide](CONTRIBUTING.md)  
## Reachout

Feel free to contact me if you have any questions: sebastian.beyer@live.com

