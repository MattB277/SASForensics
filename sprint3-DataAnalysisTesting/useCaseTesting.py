# This document will be used to showcase the use cases of each function within the data analysis system
from AnalysisFunctions import *
# Testing constants:
bucket = "s3-sh06-testing"                      # name of S3 bucket 
filename = "Day-1B_Firearms-NIBIN_Final.pdf"    # name of target file in S3 bucket

# API setups
s3_secret_key = os.getenv("S3_SECRET_ACCESS_KEY") 
s3_key = os.getenv("S3_ACCESS_KEY")
s3_client = boto3.client('s3', aws_access_key_id=s3_key, aws_secret_access_key=s3_secret_key)

openAI_key = os.getenv("OPENAI_API_KEY")        # openAI key
openAI_Client = OpenAI(api_key=openAI_key)      # create openAI client

# Transforming a pdf document in an s3 bucket into text
converted_s3_PDF_text = getPDFtextfromS3(s3_client, 'Day-1A_Incident-Report_Final3.pdf')

# sending that text to the OpenAI API (simple prompt as of now)
analysed_text_JSON=analyseTextIntoJSON(openAI_Client, converted_s3_PDF_text)



