import boto3

from manager_app import config


def ec2_create():
    ec2 = boto3.resource('ec2')
    instance = ec2.create_instances(ImageId=config.ami_id, MinCount=1, MaxCount=1,
                                    InstanceType='t2.micro', SubnetId=config.subnet_id)
    return instance[0]


def ec2_destroy(instance_id):
    ec2 = boto3.resource('ec2')
    ec2.instances.filter(InstanceIds=[instance_id]).terminate()


def ec2_get_instance_ip(instance_id):
    ec2 = boto3.resource('ec2')
    instances = ec2.instances.filter(
        Filters=[
            {
                'Name': 'instance-id',
                'Values': [instance_id]
            }
        ])
    instance = list(instances.all())[0]
    return instance.public_ip_address
