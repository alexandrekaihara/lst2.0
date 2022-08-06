#!/bin/bash

apt update
RUNLEVEL=1 apt install -y --no-install-recommends openvswitch-switch sudo net-tools iproute2 iputils-ping nano iptables wget unzip libpcap-dev tcpdump sudo default-jdk

# Add java to path
echo -e "export JAVA_HOME=\"/usr/lib/jvm/java-1.11.0-openjdk-amd64\"\nexport PATH=$JAVA_HOME/bin:$PATH" >> /etc/profile
source /etc/profile

until unzip master.zip 
do
    wget https://github.com/iPAS/TCPDUMP_and_CICFlowMeter/archive/refs/heads/master.zip
done
rm master.zip

mkdir /TCPDUMP_and_CICFlowMeter-master/collecteddata


