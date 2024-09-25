import boto3
from botocore.exceptions import NoCredentialsError, ClientError

def check_aws_caller_identity():
    try:
        # Create an STS client
        sts_client = boto3.client('sts')
        
        # Call the get_caller_identity method
        response = sts_client.get_caller_identity()
        
        # Extract UserId and Arn from the response
        user_id = response['UserId']
        arn = response['Arn']

        return (f"UserId: {user_id}, Arn: {arn}")
    
    except Exception as e:
        return f"Failed - {e}"
        
# Run the function
status = check_aws_caller_identity()
print(f"{status}")
