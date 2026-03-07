import boto3
from botocore.exceptions import NoCredentialsError, ClientError

def check_aws_connection():
    try:
        # Create an STS client
        sts = boto3.client('sts')
        
        # Call get_caller_identity to verify credentials
        identity = sts.get_caller_identity()
        print("Connected to AWS!")
        print(f"Account: {identity['Account']}")
        print(f"User ARN: {identity['Arn']}")
        
    except NoCredentialsError:
        print("Error: AWS credentials not found.")
    except ClientError as e:
        print(f"Error: {e.response['Error']['Message']}")

if __name__ == "__main__":
    check_aws_connection()
