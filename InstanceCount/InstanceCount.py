import boto3
import sys

print('Loading function')


def lambda_handler(event, context):

    print(event["queryStringParameters"]['STATE'])
    autostate = event["queryStringParameters"]['STATE']

    if not autostate:
        print(autostate)
    else:
        print("Enter AutoScaling Group Name")
        sys.exit()

    ec2_client = boto3.client('ec2')
    # print(groups['AutoScalingGroups'])
    asg_client = boto3.client('autoscaling')
    asg = "gsd-panda-rq-app-ASGRP-N1SHV5N9YAGW"
    print (asg)
    asg_response = asg_client.describe_auto_scaling_groups(AutoScalingGroupNames=[asg])
    # print(asg_response)
    instance_ids = []  # List to hold the instance-ids
    for i in asg_response['AutoScalingGroups']:
        for k in i['Instances']:
            print (k)
            instance_ids.append(k['InstanceId'])
    print("Length : %d" % len(instance_ids))

