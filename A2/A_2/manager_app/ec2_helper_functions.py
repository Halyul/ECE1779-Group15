import boto3
import config


def ec2_get_instance():
    ec2 = boto3.resource('ec2')
    instances = ec2.instances.all()
    return instances


def ec2_create():
    ec2 = boto3.resource('ec2')
    ec2.create_instances(ImageId=config.ami_id, MinCount=1, MaxCount=1,
                         InstanceType='t2.micro', SubnetId=config.subnet_id)


def ec2_destroy(instance_id):
    ec2 = boto3.resource('ec2')
    ec2.instances.filter(InstanceIds=[instance_id]).terminate()


def ec2_destroy_all():
    ec2 = boto3.resource('ec2')
    ec2.instances.terminate()
