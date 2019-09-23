import boto3
import json
import sys

print('Loading function')


print(sys.argv[1])
autostate = str(sys.argv[1])

if len(sys.argv)>1:
    print(autostate)
else:
    print("Enter AutoScaling Group Name")
    sys.exit()

# autoscale
client = boto3.client('autoscaling')
autoscalename = autostate
print(autoscalename)
max = 0
min = 0
desired = 0
response = client.update_auto_scaling_group(
             AutoScalingGroupName=autoscalename,
             MaxSize=int(max),
             MinSize=int(min),
             DesiredCapacity=int(desired),
         )
output = json.dumps(response)
print(output)        
