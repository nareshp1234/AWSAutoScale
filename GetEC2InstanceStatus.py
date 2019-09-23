import boto3
import sys
import json

print('Loading function')


def lambda_handler(event, context):

    print(event["queryStringParameters"]['ASGNAME'])
    autostate = event["queryStringParameters"]['ASGNAME']

    if  autostate:
        print(autostate)
    else:
        print("Enter AutoScaling Group Name")
        return {
            "isBase64Encoded": 'false',
            "statusCode": 200,
            "headers": {'Content-Type': 'application/json'},
            "body": json.dumps(0)
                }

    ec2_client = boto3.client('ec2')
    # print(groups['AutoScalingGroups'])
    asg_client = boto3.client('autoscaling')
    asg = autostate
    print(asg)
    asg_response = asg_client.describe_auto_scaling_groups(AutoScalingGroupNames=[asg])
    # print(asg_response)
    instance_ids = []  # List to hold the instance-ids
    for i in asg_response['AutoScalingGroups']:
        for k in i['Instances']:
            print (k)
            instance_ids.append(k['InstanceId'])
    print("Length : %d" % len(instance_ids))

    return {
            "isBase64Encoded": 'false',
            "statusCode": 200,
            "headers": {'Content-Type': 'application/json'},
            "body": json.dumps(len(instance_ids))
                }