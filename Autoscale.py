import boto3
import botocore
import pymsteams
import sys

print('Loading function')


def lambda_handler(event, context):

    print(event["queryStringParameters"]['STATE'])
    autostate = event["queryStringParameters"]['STATE']
    if autostate:
        if autostate == "DOWN":
            propfilename = "L0.properties"
            print(propfilename)
        elif autostate == "UP":
            propfilename = "L1.properties"
            print(propfilename)
        else:
            propfilename = "L0.properties"
            print("Happy Path")
    else:
        print("Enter Arguments to proceed Ex : UP, DOWN ")
        sys.exit()
    myTeamsMessage = pymsteams.connectorcard(
        "<webhookurl>")
    # Let's use Amazon S3
    s3 = boto3.resource('s3')
    # autoscale
    client = boto3.client('autoscaling')
    try:
        s3.Object('scale-teams-integration', propfilename).load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            print("The object does not exist.")
        raise
    else:
        # The object does exist.
        print("object does exist")
        obj = s3.Object('scale-teams-integration', propfilename)
        for line in obj.get()['Body']._raw_stream:
            if("#" in line.decode('utf-8')):
                # Comments we skip it....
                print("line with #")
            else:
                currentline = line.decode('utf-8')
                autoscale = currentline.split('=')
                print(autoscale)
                autoscalename = autoscale[0]
                print("Autoscale group name : ", autoscalename)
                minmaxdesired = autoscale[1]
                print("min max desired : ", minmaxdesired)
                values = minmaxdesired.split(',')
                min = values[0]
                print("min : ", min)
                max = values[1]
                print("max : ", max)
                desired = values[2]
                print("desired : ", desired)

                changedvalue = {min, max, desired}
                s = ', '

                response = client.update_auto_scaling_group(
                    AutoScalingGroupName=autoscalename,
                    MaxSize=int(max),
                    MinSize=int(min),
                    DesiredCapacity=int(desired),
                )
                # create the section
                myMessageSection = pymsteams.cardsection()

                # Section Title
                myMessageSection.title("AutoScalingGroup Status")

                # Activity Elements
                myMessageSection.activityTitle(autoscalename)
                myMessageSection.activitySubtitle(s.join(changedvalue))
                myMessageSection.activityImage(
                    "https://s3.amazonaws.com/<bucketname>/Autoscale.png")
                myMessageSection.activityText("This is my activity Text")

                # Facts are key value pairs displayed in a list.
                #myMessageSection.addFact(autoscalename, s.join(changedvalue))

                # Section Text
                #myMessageSection.text("Autoscale Section")

                # Add your section to the connector card object before sending
                myTeamsMessage.addSection(myMessageSection)
                myTeamsMessage.text("Naresh Purushotham")
                myTeamsMessage.printme()
                # send the message.
                myTeamsMessage.send()
