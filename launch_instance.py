import boto3

def launch_ec2_instance(instance_name, instance_type, key_pair_name, image_id, security_group_id, instance_count):
    ec2 = boto3.resource("ec2")

    instance = ec2.create_instances(
        ImageId=image_id,
        InstanceType=instance_type,
        KeyName=key_pair_name,
        SecurityGroupIds=[security_group_id],
        MinCount=1,
        MaxCount=instance_count,
        TagSpecifications=[{
            'ResourceType': "instance",
            'Tags': [{'Key': 'Name','Value':instance_name}]
        }]
    )
    print(instance.instance_id)
    return instance
