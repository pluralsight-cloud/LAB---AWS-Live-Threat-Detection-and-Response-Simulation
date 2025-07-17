import json
import boto3

ec2 = boto3.client('ec2')

# Hardcoded security group ID to apply (replace with your SG ID)
NEW_SECURITY_GROUP_ID = "sg-08dde536226f951d7"

def lambda_handler(event, context):
    try:
        print("Received event:", json.dumps(event))

        findings = event.get("detail", {})
        resource = findings.get("resource", {})
        instance_details = resource.get("instanceDetails", {})
        instance_id = instance_details.get("instanceId")

        if not instance_id:
            print("Instance ID not found.")
            return {"statusCode": 400, "body": "No instance ID in event"}

        print(f"Affected instance: {instance_id}")

        # Optional: Describe instance (for logging)
        instance_info = ec2.describe_instances(InstanceIds=[instance_id])
        print(f"Current instance info: {json.dumps(instance_info, default=str)}")

        # Modify the instance's security groups
        ec2.modify_instance_attribute(
            InstanceId=instance_id,
            Groups=[NEW_SECURITY_GROUP_ID]
        )

        print(f"Security group for instance {instance_id} changed to {NEW_SECURITY_GROUP_ID}")

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": f"Security group updated for {instance_id}",
                "newSecurityGroup": NEW_SECURITY_GROUP_ID
            })
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
