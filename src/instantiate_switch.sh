#!/bin/bash 

docker run -d --network=none --privileged --name=$1 mdewinged/cidds:openvswitch