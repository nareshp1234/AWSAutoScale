import boto3
import json

print('Loading function')


def lambda_handler(event, context):    
    print(event["queryStringParameters"]['ASGNAME'])
    autostate = event["queryStringParameters"]['ASGNAME']

    if autostate:
        print(autostate)
    else:
        print("Enter AutoScaling Group Name")
        return {
            "isBase64Encoded": 'false',
            "statusCode": 200,
            "headers": {'Content-Type': 'application/json'},
            "body": json.dumps(0)
            }

    # autoscale
    client = boto3.client('autoscaling')
    autoscalename = autostate
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
    return {
            "isBase64Encoded": 'false',
            "statusCode": 200,
            "headers": {'Content-Type': 'application/json'},
            "body": json.dumps(output)
                }        
