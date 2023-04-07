import boto3
import sys

iam = boto3.client("iam")

user_name = sys.argv[1]
password = sys.argv[2]

response = iam.create_user(UserName=user_name)
response =iam.add_user_to_group(
    GroupName='admin_permissions',
    UserName=user_name
)
response = iam.create_login_profile(
    UserName=user_name,
    Password=password,
    PasswordResetRequired=False
)
response = iam.create_access_key(
    UserName=user_name
)
print(f"Full response:{response}")
print(f"Access Key ID:{response['AccessKey']['AccessKeyId']}")
print(f"Secret Access Key: {response['AccessKey']['SecretAccessKey']}")
print("Login link: https://676000770422.signin.aws.amazon.com/console")



