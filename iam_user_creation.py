import boto3

iam = boto3.client("iam")
def create_iam_user_and_login(user_name, password):
    response = iam.create_user(UserName=user_name)
    response = iam.add_user_to_group(GroupName='admin_permissions', UserName=user_name)
    response = iam.create_login_profile(UserName=user_name, Password=password, PasswordResetRequired=False)
    return response
def create_access_key(user_name):
    response = iam.create_access_key(UserName=user_name)
    return response
