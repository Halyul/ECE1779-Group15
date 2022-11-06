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

# Display details about a specific instance.
def ec2_view(id):
    ec2 = boto3.resource('ec2')

    instance = ec2.Instance(id)

    client = boto3.client('cloudwatch')

    metric_name = 'CPUUtilization'

    ##    CPUUtilization, NetworkIn, NetworkOut, NetworkPacketsIn,
    #    NetworkPacketsOut, DiskWriteBytes, DiskReadBytes, DiskWriteOps,
    #    DiskReadOps, CPUCreditBalance, CPUCreditUsage, StatusCheckFailed,
    #    StatusCheckFailed_Instance, StatusCheckFailed_System

    namespace = 'AWS/EC2'
    statistic = 'Average'  # could be Sum,Maximum,Minimum,SampleCount,Average

    cpu = client.get_metric_statistics(
        Period=1 * 60,
        StartTime=datetime.utcnow() - timedelta(seconds=60 * 60),
        EndTime=datetime.utcnow() - timedelta(seconds=0 * 60),
        MetricName=metric_name,
        Namespace=namespace,  # Unit='Percent',
        Statistics=[statistic],
        Dimensions=[{'Name': 'InstanceId', 'Value': id}]
    )

    cpu_stats = []

    for point in cpu['Datapoints']:
        hour = point['Timestamp'].hour
        minute = point['Timestamp'].minute
        time = hour + minute / 60
        cpu_stats.append([time, point['Average']])

    cpu_stats = sorted(cpu_stats, key=itemgetter(0))

    statistic = 'Sum'  # could be Sum,Maximum,Minimum,SampleCount,Average

    network_in = client.get_metric_statistics(
        Period=1 * 60,
        StartTime=datetime.utcnow() - timedelta(seconds=60 * 60),
        EndTime=datetime.utcnow() - timedelta(seconds=0 * 60),
        MetricName='NetworkIn',
        Namespace=namespace,  # Unit='Percent',
        Statistics=[statistic],
        Dimensions=[{'Name': 'InstanceId', 'Value': id}]
    )

    net_in_stats = []

    for point in network_in['Datapoints']:
        hour = point['Timestamp'].hour
        minute = point['Timestamp'].minute
        time = hour + minute / 60
        net_in_stats.append([time, point['Sum']])

    net_in_stats = sorted(net_in_stats, key=itemgetter(0))

    network_out = client.get_metric_statistics(
        Period=5 * 60,
        StartTime=datetime.utcnow() - timedelta(seconds=60 * 60),
        EndTime=datetime.utcnow() - timedelta(seconds=0 * 60),
        MetricName='NetworkOut',
        Namespace=namespace,  # Unit='Percent',
        Statistics=[statistic],
        Dimensions=[{'Name': 'InstanceId', 'Value': id}]
    )

    net_out_stats = []

    for point in network_out['Datapoints']:
        hour = point['Timestamp'].hour
        minute = point['Timestamp'].minute
        time = hour + minute / 60
        net_out_stats.append([time, point['Sum']])
        net_out_stats = sorted(net_out_stats, key=itemgetter(0))
    return (instance, cpu_stats, net_in_stats, net_out_stats)

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
    try:
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
            break
        return instance.public_ip_address
    except Exception as error:
        return "{}".format(error)

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