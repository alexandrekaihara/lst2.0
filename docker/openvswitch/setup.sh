#!/bin/bash

#
# Copyright (C) 2022 Alexandre Mitsuru Kaihara
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


# Add java to path
echo -e "export JAVA_HOME=\"/usr/lib/jvm/java-1.11.0-openjdk-amd64\"\nexport PATH=$JAVA_HOME/bin:$PATH" >> /etc/profile
source /etc/profile

until unzip master.zip 
do
    wget https://github.com/iPAS/TCPDUMP_and_CICFlowMeter/archive/refs/heads/master.zip
done
rm master.zip

mv CICFlowMeter /TCPDUMP_and_CICFlowMeter-master/CICFlowMeters/CICFlowMeter-4.0/bin/CICFlowMeter

cd /TCPDUMP_and_CICFlowMeter-master

mkdir collecteddata

sed -i "s/trap/#trap/g" capture_interface_pcap.sh
sed -i "s/trap/#trap/g" convert_pcap_csv.sh
sed -i "s/sudo tcpdump/sudo tcpdump -Z root/g" capture_interface_pcap.sh

