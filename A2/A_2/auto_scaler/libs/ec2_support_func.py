import boto3
from datetime import datetime, timedelta
from operator import itemgetter
import logging

import sys
sys.path.append("../..") 
import auto_scaler.config as config

# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html

# Display an HTML list of all ec2 instances
def ec2_list(status):
    # create connection to ec2
    ec2 = boto3.resource('ec2')

    if status == "" or status == "all":
        instances = ec2.instances.all()
    else:  # status := pending | running | shutting-down | terminated | stopping | stopped
        ########### your code starts here  ################
        instances = ec2.instances.filter(
            Filters=[
                {
                    'Name': 'instance-state-name',
                    'Values': [status]
                }
            ]
        )
        ########### your code ends here    ################
    return instances

# Start a new EC2 instance
def ec2_create():
    ec2 = boto3.resource('ec2')
    instance = ec2.create_instances(ImageId=config.ami_id, MinCount=1, MaxCount=1,
                          InstanceType='t2.micro', SubnetId=config.subnet_id, 
                          SecurityGroupIds=[config.security_group_id], KeyName=config.ssh_key_name)

    return instance[0]

# Terminate a EC2 instance
def ec2_destroy(id):
    # create connection to ec2
    ec2 = boto3.resource('ec2')
    ec2.instances.filter(InstanceIds=[id]).terminate()
    return

# get the ipv4 address from the ec2 instance id
def ec2_get_instance_ip(id):
    # create connection to ec2
    ec2 = boto3.resource('ec2')
    instances = ec2.instances.filter(
            Filters=[
                {
                    'Name': 'instance-id',
                    'Values': [id]
                }
            ])
    for item in instances:
        instance = item
        return instance.public_ip_address
    return "ec2 with id {} not found!".format(id)

# get id from ipv4 address
def ec2_get_instance_id(ip):
    # create connection to ec2
    ec2 = boto3.resource('ec2')
    instances = ec2.instances.filter(
            Filters=[
                {
                    'Name': 'ip-address',
                    'Values': [ip]
                }
            ])
    for item in instances:
        instance = item
        return instance.id
    return "ec2 with ip {} not found!".format(ip)

def ec2_get_cache_ec2_object_list():
    ec2 = boto3.resource('ec2')
    instances = ec2.instances.filter(
            Filters=[
                {
                    'Name': 'network-interface.subnet-id',
                    'Values': [config.subnet_id]
                }
            ])
    cache_ec2_object_list = []
    for item in instances:
        cache_ec2_object_list.append(item)
    return cache_ec2_object_list