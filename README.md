# Lightweight SDN Testbed (LST) 2.0
## Description
Not all emulated testbeds are suitable for security experimentation. Often security testbeds are restricted to their application context or are based on other technologies which have configurability and security application limitations (\textit{e.g.} Mininet). While other proposals allow greater configurability, they do not focus on security applications or are not inserted in the context of SDN networks. To address the identified research gap, the Lightweight SDN Testbed (\prop) is proposed. \prop is a lightweight tool capable of supporting different application contexts both for security and SDN networks programmatically and in real-time through Python. It is possible to monitor the network and collect metrics using Netflow, sFlow, IPFIX, or CICFlowMeter. In addition, pre-built Docker images are available for emulating both benign and malicious network flows.

This tool aims to attend the demands of the most diverse study scenarios in SDN and security networks, through an interface with a set of reduced methods, but which allow high flexibility in the configuration and generation of customized topologies. LST 2.0 is mainly based on containers for generating network nodes and all network configuration and behavior is done programmatically. The tool is organized through a set of well-defined methods belonging to a hierarchy of classes, whose parent class, named Node, has all the attributes and minimal methods to instantiate, delete and configure any container. Thus, users can develop their own classes inheriting the attributes of the Node class and focusing only on the specific settings for the study.

By default, three classes are implemented that are specializations of the Node class. The Host class allows you to create containers that will be common nodes that will consume some service on the network. The Switch class allows you to create virtual switches whose network configuration is specific to forward packets between ports of a single bridge contained in the container and also to connect to a controller on a specific IP and port. If no controller is assigned to the switch, the switch will only perform basic network layer functions and also if no IP is assigned to it, it will be a link layer switch. The Controller class allows you to create containers that can instantiate one or more controllers.

This project provides pre-built Docker images to build a small business environment to emulate benign and malicious flows to assess defense mechanisms. This experiment is a modification of a work developed by Markus Ring et. al. (available at: https://www.hs-coburg.de/cidds), which provided all the scripts to emulate the small business environment. This environment includes several clients and typical servers (e.g. e-mail and Web server). 

## System Requirements
Your machine must be using a Linux distribution. In our experiments, were used a Ubuntu Server version 20.04.2 LTS virtual machine installed on Virtualbox version 6.1.26 configured with 15 GB RAM, 4 CPU cores e 32 GB memory disk space.

## Dependencies
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

If you want to finish the experiment e get back to your original network configuration, press CTRL + C once.

## Docker image build
If it is necessary to make any change on the docker images, check the "docker" folder located on the root directory of this repository. To build any docker image, access the folder containing its "Dockerfile" file and execute:

> docker build --network=host .

To use the newly built image in the experiment, access the "lst2.0/demonstration/cidds.py" file and set "dockerImage" parameter of the "intantiate" method with new docker image name.

## Creating Your Own Experiment
As shown in the section above, the "setup.sh" script expects a JSON file as an argument. This file represents all the machines that will be used in the experiment. You can define the Docker image, the subnet, the IP address, the DNS server, bridge to which the container will be connected. 

In this JSON file, all containers are defined using a dictionary with these fields:

```
"external_${WEB}": {
        "image":"${REPOSITORY}:${WEB}",
        "IP":"192.168.${ESUBNET}.2",
        "bridge":"${EXTERNAL}",
        "depends_on": [],
        "dns":"8.8.8.8"
  }
```

The field "image" represents the repository name and the image name on Dockerhub. The "IP" field is the IP address assigned to the container in the experiment. The "bridge" is the name of the virtual Switch to which the container will be connected. The "depends_on" is a list of docker images names that need to be created before the creation of this container. And the "dns" is the IP of your DNS server.

If you want to make modifications to the experiment and to run the clients and servers correctly, be aware of the following restrictions:

- The "linuxclient" images has an additional field called "client_behaviour", which is the name of the client's behavior script (located in "lst/experiment/client_behaviour"). This file defines all the operations this client can do (e.g. access mail server, realize attacks, access web pages) and you can create yourn own; 
- Make sure that you also create all the needed servers your clients will use. If you define a "linuxclient" behavior that uses a mail service, so you need to create an instance of  "mailserver";
- "linuxclient" images also needs that the "printerserver", "mailserver", "backupserver", "fileserver" to be created first. Thus it needs to be declared on the "depends_on" field;
- If you need the "seafileserver", it must be declared with the IP address that was defined during the building process of this docker image. The default IP is "192.168.50.1";
- Do not repeat IP addresses;
- Do not repeat dictionary names, because they will be used as the name of the container, and they can't be repeated.

You can use environment variables inside the JSON. New environment variables can be defined on "lst/experiment/variables"

## Issues

If any errors occur during the setup and execution o the experiment, check:

- If there exist two definitions of the default gateway, remove one. It can cause problems to configure the Firewall permissions;
- Verify if your computer already has defined subnets that may conflict with the subnets defined in the "lst/experiment/variable" file. It may affect the routing process and potentially break the configuration of a host because of IP address conflicts.
- It is created an interface for each container following the pattern of "veth" + "subnet tag" + "host IP part". For example, the container has the IP 192.168.50.1, then its interface will be named veth50.1. Check if won't have any name conflict with your existing network interfaces to the ones that will be created for the experiment;

## Video

The link of the video for SBRC Salão de Ferramentas is available at https://www.youtube.com/watch?v=ln0Np3dH6kk
