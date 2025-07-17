import boto3
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize EC2 client
ec2 = boto3.client('ec2')

# 🔒 HARD-CODED VALUES (Edit these)
INSTANCE_ID = 'i-0123456789abcdef0'  # Replace with your EC2 instance ID
NEW_SECURITY_GROUP_IDS = ['sg-0abc1234def567890']  # Replace with your desired SGs

def lambda_handler(event, context):
    try:
        logger.info(f"Starting security group update for instance: {INSTANCE_ID}")

        # Describe the instance to get its network interfaces
        response = ec2.describe_instances(InstanceIds=[INSTANCE_ID])
        interfaces = response['Reservations'][0]['Instances'][0]['NetworkInterfaces']

        for iface in interfaces:
            iface_id = iface['NetworkInterfaceId']
            logger.info(f"Updating network interface {iface_id} with SGs: {NEW_SECURITY_GROUP_IDS}")
            
            # Replace security groups
            ec2.modify_network_interface_attribute(
                NetworkInterfaceId=iface_id,
                Groups=NEW_SECURITY_GROUP_IDS
            )

        logger.info("Security group update completed successfully.")
        return {
            'statusCode': 200,
            'message': f"Security groups for instance {INSTANCE_ID} updated successfully."
        }

    except Exception as e:
        logger.error(f"Error: {e}")
        return {
            'statusCode': 500,
            'error': str(e)
        }
