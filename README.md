# Lightweight SDN Testbed (LST)
## Description
There are many Emulated Testbeds proposed for Software-Defined Networking (SDN). Nonetheless, there are still few studies that focus on security. And some of them are restricted to the context in which it was designed and/or do not always meet requirements such as easy installation and configuration, topology configurability and low cost, harming the reusability of the tool. Aiming to fulfill the identified gap, we propose the Lightweight SDN Testbed (LST), an easy-to-use tool for local executions for SDN and security studies. 

The facility provided by this tool is due to the possibility of configuring the experiment from a single JSON file. You can define the number of machines, the Docker image, the behavior of clients, the IP, and the subnet. Another facility is that the Docker images encapsulate the dependencies and the configuration process. Thus, it reduces the number of dependencies needed to set up the experiment. And the creation of machines is simplified and faster because the configuration must be done only during the creation of the Docker image.

This project provides pre-built Docker images to build a small business environment to emulate benign and malicious flows to assess defense mechanisms. This experiment is a modification of a work developed by Markus Ring et. al. (available at: https://www.hs-coburg.de/cidds), which provided all the scripts to emulate the small business environment. This environment includes several clients and typical servers (e.g. e-mail and Web server). 

## System Requirements
Your machine must be using a Linux distribution. In our experiments, were used a Ubuntu Server version 20.04.2 LTS virtual machine installed on Virtualbox version 6.1.26 configured with 15 GB RAM, 4 CPU cores e 32 GB memory disk space.

## Dependencies
All the dependencies consists of:
- Docker (version 20.10.7)
- Docker Compose (version 1.25.0)
- Pip3 (22.0.3)
- OpenvSwitch (2.13.3)

We provide a Bash script to install all the needed dependencies. To install all dependencies, execute:

> sudo git clone https://github.com/alexandrekaihara/lst

> cd lst/experiment

> sudo chmod +x dependencies.sh && sudo ./dependencies.sh

## Execution
To execute the script to set up the network topology, execute these commands:

> sudo chmod +x setup.sh

> sudo ./setup.sh partial_experiment.json

If you want to finish the experiment e get back to your original network configuration, press CTRL + C once.

## Docker image build
If it is necessary to make any change on the docker images, check the "docker" folder located on the root directory of this repository. To build any docker image, access the folder containing its "Dockerfile" file and execute:

> docker build --network=host --tag mdewinged/lst:NEW_CONTAINER_NAME .

To use the newly built image in the experiment, access the "lst/experiment" folder and change the file named as "variables" and find the respective image and change its value for the "NEW_CONTAINER_NAME" you have attributed. For example, you have built another version of the webserver and named as webserver2. Thus, you need to change the value of WEB=webserver2 in the "variable" file. 

The only image that does not follow the command above is the seafileserver. Due to a particular characteristic of its configuration, the seafileserver must create a network interface to build the image, and its IP address in the experiment is static (default is 192.168.50.1). If you need to change the IP on which the server listens, a rebuild is necessary with the new IP. More detailed instructions are located inside the "lst/docker/seafileserver" folder.

## Creating Own .JSON Experiment
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
