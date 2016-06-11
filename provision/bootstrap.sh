#!/bin/sh

# Get Build dependencies and Ansible on the box

yes '' | apt-get install software-properties-common
yes '' | apt-add-repository ppa:ansible/ansible
yes '' | apt-get update
yes '' | apt-get install git build-essential ansible
