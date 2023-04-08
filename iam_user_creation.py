import boto3

iam = boto3.client("iam")

def create_iam_user_and_access_key(user_name, password):
    response = iam.create_user(UserName=user_name)
    iam.add_user_to_group(GroupName='admin_permissions', UserName=user_name)
    iam.create_login_profile(UserName=user_name, Password=password, PasswordResetRequired=False)
    access_key = iam.create_access_key(UserName=user_name)
    return access_key
