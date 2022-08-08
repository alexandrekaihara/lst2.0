# Lightweight SDN Testbed (LST) 2.0
## Description
Not all emulated testbeds are suitable for security experimentation. Often security testbeds are restricted to their application context or are based on other technologies which have configurability and security application limitations (\textit{e.g.} Mininet). While other proposals allow greater configurability, they do not focus on security applications or are not inserted in the context of SDN networks. To address the identified research gap, the Lightweight SDN Testbed (\prop) is proposed. \prop is a lightweight tool capable of supporting different application contexts both for security and SDN networks programmatically and in real-time through Python. It is possible to monitor the network and collect metrics using Netflow, sFlow, IPFIX, or CICFlowMeter. In addition, pre-built Docker images are available for emulating both benign and malicious network flows.

This tool aims to attend the demands of the most diverse study scenarios in SDN and security networks, through an interface with a set of reduced methods, but which allow high flexibility in the configuration and generation of customized topologies. LST 2.0 is mainly based on containers for generating network nodes and all network configuration and behavior is done programmatically. The tool is organized through a set of well-defined methods belonging to a hierarchy of classes, whose parent class, named Node, has all the attributes and minimal methods to instantiate, delete and configure any container. Thus, users can develop their own classes inheriting the attributes of the Node class and focusing only on the specific settings for the study.

By default, three classes are implemented that are specializations of the Node class. The Host class allows you to create containers that will be common nodes that will consume some service on the network. The Switch class allows you to create virtual switches whose network configuration is specific to forward packets between ports of a single bridge contained in the container and also to connect to a controller on a specific IP and port. If no controller is assigned to the switch, the switch will only perform basic network layer functions and also if no IP is assigned to it, it will be a link layer switch. The Controller class allows you to create containers that can instantiate one or more controllers.

This project provides pre-built Docker images to build a small business environment to emulate benign and malicious flows to assess defense mechanisms. This experiment is a modification of a work developed by Markus Ring et. al. (available at: https://www.hs-coburg.de/cidds), which provided all the scripts to emulate the small business environment. This environment includes several clients and typical servers (e.g. e-mail and Web server). 

## System Requirements
Your machine must be using a Linux distribution. In our experiments, were used a Ubuntu Server version 20.04.2 LTS virtual machine installed on Virtualbox version 6.1.26 configured with 15 GB RAM, 4 CPU cores e 32 GB memory disk space.

## Installation
All the dependencies consists of:
- Docker (version 20.10.7)
- Python (version 3.8.10)

We provide a Bash script to install all the needed dependencies. To install all dependencies, execute:

> sudo git clone https://github.com/alexandrekaihara/lst2.0

> cd lst2.0/src

> sudo chmod +x dependencies.sh && sudo ./dependencies.sh

## Execution
To execute the script to set up the network topology, execute these commands:

> cd lst2.0/demonstration

> python3 cidds.py

If you want to finish the experiment, press CTRL + C once.

## Docker image build
If it is necessary to make any change on the docker images, check the "docker" folder located on the root directory of this repository. To build any docker image, access the folder containing its "Dockerfile" file and execute:

> docker build --network=host --tag=NEWNAME .

To use the newly built image in the experiment, access the "lst2.0/demonstration/cidds.py" file and set "dockerImage" parameter of the "intantiate" method with NEWNAME.

## Creating Your Own Experiment
As shown in the section above, the "cidds.py" is an example of how to create a topology with LST 2.0. The following subsections will explain how to execute the basic configurations to instantiate e linear SDN topology with two nodes.

It is important to mention that all the configuration methods must be used after creating the container using the "instantiate" method.

### Create network node
To create a network node it is necessary to create an instance of [Switch](lst2.0/src/Switch.py), [Host](lst2.0/src/Host) or [Controller](lst2.0/src/Controller), passing the name of the node as a parameter.

> cd lst2.0/src
> python3

Then execute the following commands:

```
from host import Host
from switch import Switch
from controller import Controller

h1 = Host('h1')
h2 = Host('h2')
s1 = Switch('s1')
c1 = Controller('c1')
```

PS: You are responsible for keeping the instance of each node class in order to delete them at the end

Then is necessary to instantiate the controller using the instance of the class.

```
h1.instantiate()
h2.instantiate()
s1.instantiate()
c1.instantiate()
```

### Connect nodes
After instantiating nodes, you can connect them by using the "connect" method passing the instance of another node.

```
h1.connect(s1)
h2.connect(s1)
s1.connect(c1)
```

### Setting IP into nodes
To set the IP into the nodes you must pass the IP address, its network mask and the reference to the node that it is connected to. The network mask is an integer that represents the network mask, for example, the network mask '255.255.255.0' correspond to 24.

```
h1.setIp('10.0.0.1', 24, s1)
h2.setIp('10.0.0.2', 24, s1)
s1.setIp('10.0.0.3', 24)
c1.setIp('10.0.0.4', 24, s1)
```

### Set up the controller
By default, the Controller instance creates a Docker container with the Ryu controller installer inside of it. To instantiate the controller and connect it to a switch you must execute:

```
c1.initController('10.0.0.4', 9001)
s1.setController('10.0.0.4', 9001)
```

Verify if the controller and the switch can communicate successfully with each other.

### Enable connection to Internet
To enable connection to Internet, the tool must create an interface from the container to the host. The IP parameter of "connectToInternet" can be any address that does not conflict with another already existing subnet on host and this address will be the default gateway for all the other nodes.

```
s1.connectToInternet('10.0.0.5', 24)
```

### Set Default Gateway
To enable all the other nodes to have access to the Internet, it must be defined the default gateway inside each container to the configured address in the previous section.

```
h1.setDefaultGateway('10.0.0.5', s1)
h2.setDefaultGateway('10.0.0.5', s1)
c1.setDefaultGateway('10.0.0.5', s1)
```

### Deleting Nodes
To delete the nodes execute the following commands:

```
h1.delete()
h2.delete()
s1.delete()
c1.delete()
```
