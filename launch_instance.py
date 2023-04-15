import boto3
import time
import subprocess
def launch_ec2_instance(instance_name, instance_type, key_pair_name, image_id, security_group_id, instance_count,
                        add_docker=False, add_jenkins=False):
    ec2 = boto3.resource("ec2")
    user_data = "#!/bin/bash\n"
    if add_docker:
        user_data += "sudo apt update && sudo apt -y install docker.io\n"
    if add_jenkins:
        user_data += "sudo docker pull jenkins/jenkins:lts && sudo docker run -p 8080:8080 -p 50000:50000 --name Jenkins_master -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts\n"
        print(user_data)
    instance = ec2.create_instances(
        ImageId=image_id,
        InstanceType=instance_type,
        KeyName=key_pair_name,
        SecurityGroupIds=[security_group_id],
        MinCount=instance_count,
        MaxCount=instance_count,
        UserData=user_data,
        TagSpecifications=[{
            'ResourceType': "instance",
            'Tags': [{'Key': 'Name', 'Value': instance_name}]
        }]
    )[0]
    print(f"Instance ID: {instance.instance_id}")
    while instance.public_ip_address is None:
        print("Waiting for public IP address...")
        time.sleep(5)
        instance.reload()

    public_ip = instance.public_ip_address
    print(f"Public IP: {public_ip}")
    dict_instance = {instance_name: public_ip}
    return public_ip
