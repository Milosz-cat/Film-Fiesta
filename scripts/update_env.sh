#!/bin/bash

: '
This script updates the .env file FOR LINUX with the IP addresses obtained from the hostname -I command.
It ensures that the ALLOWED_HOSTS value contains the static IP addresses 127.0.0.1 and 0.0.0.0, 
as well as the IP addresses returned by the command.
If the .env file does not exist, it copies from .env.sample.

The purpose of this procedure is to ensure that by starting the application in the terminal 
(e.g. linux sever VM) you will be able to run it on a browser on a device located in a given network
 (browser on a phone)
'

# Get all IP addresses using the hostname -I command
IP_ADDRESSES=$(hostname -I)

# Construct the value for ALLOWED_HOSTS
ALLOWED_HOSTS_VALUE="ALLOWED_HOSTS=127.0.0.1 0.0.0.0 $IP_ADDRESSES"

# Path to the .env file in the parent directory
ENV_PATH="./.env"
ENV_SAMPLE_PATH="./.env.sample"

# Check if the .env file exists
if [ ! -f $ENV_PATH ]; then
    # If it doesn't exist, copy .env.sample to .env in the parent directory
    cp $ENV_SAMPLE_PATH $ENV_PATH
fi

# Check if ALLOWED_HOSTS exists in the .env file
if grep -q "ALLOWED_HOSTS" $ENV_PATH; then
    # If it exists, update the value
    sed -i "s/ALLOWED_HOSTS=.*/$ALLOWED_HOSTS_VALUE/" $ENV_PATH
fi