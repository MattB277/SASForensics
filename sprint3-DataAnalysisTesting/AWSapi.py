import boto3
from botocore.exceptions import ClientError
import os
from AnalysisFunctions import *
from io import BytesIO

s3_secret_key = os.getenv("S3_SECRET_ACCESS_KEY") 
s3_key = os.getenv("S3_ACCESS_KEY")
bucket = "s3-sh06-testing"
filepath = "PythonTests\Day-1B_Firearms-NIBIN_Final.pdf"

def uploadPDFtoS3(filepath, bucket, client):
    """THIS FUNCTION CALLS S3 API.
    Takes a filepath string, bucket name and S3 client, and will upload the file
    to the specified bucket keeping the same file name."""
    object_name = os.path.basename(filepath)
    try:
        response = client.upload_file(filepath, bucket, object_name)
    except ClientError as e:
        print(e)
        return False
    return True

# S3 bucket -> PDF content string (production function)
def getPDFtextfromS3(s3_client, filename):
    """THIS FUNCTION CALLS S3 API.
    Returns the text in a pdf in an s3 bucket by filename"""
    response = s3_client.get_object(Bucket='s3-sh06-testing', Key = filename)
    content = response['Body'].read()
    pdfDoc = PdfFileReader(BytesIO(content))
    return parsePDFtoText(pdfDoc)

s3_client = boto3.client('s3', aws_access_key_id=s3_key, aws_secret_access_key=s3_secret_key)

#response = getPDFtextfromS3(s3_client, 'Day-1A_Incident-Report_Final3.pdf')
#response = uploadPDFtoS3(filepath, bucket, s3_client)
