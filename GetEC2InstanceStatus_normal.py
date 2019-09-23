import boto3
import sys
import json

print('Loading function')

autostate = str(sys.argv[1:])

if len(sys.argv)>1:
    print(autostate)
else:
    print("Enter AutoScaling Group Name")
    sys.exit()    
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
