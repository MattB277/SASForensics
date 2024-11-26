# This document will be used to showcase the use cases of each function within the data analysis system
from AnalysisFunctions import *
# Testing constants:
bucket = "s3-sh06-testing"                      # name of S3 bucket 
filename = "Day-1B_Firearms-NIBIN_Final.pdf"    # name of target file in S3 bucket

# API setups
s3_secret_key = os.getenv("S3_SECRET_ACCESS_KEY") 
s3_key = os.getenv("S3_ACCESS_KEY")
s3_client = boto3.client('s3', aws_access_key_id=s3_key, aws_secret_access_key=s3_secret_key)

#openAI_key = os.getenv("OPENAI_API_KEY")        # redundant enviroment variable assignment, see AnalysisFunctions.analyseTextIntoJSON() for client establishment!

# Transforming a pdf document in an s3 bucket into text
# converted_s3_PDF_text = getPDFtextfromS3(s3_client, 'Day-1A_Incident-Report_Final3.pdf')

# transforming a pdf from local directory into text
local_pdf_converted = getPDFtext(openLocalPDF("sh06-main\sprint3-DataAnalysisTesting\Day-1A_Incident-Report_Final3.pdf"))
# sending that text to the OpenAI API (simple prompt as of now)
analysed_text_JSON=analyseTextIntoJSON(local_pdf_converted)

# example finished output
"""ChatCompletionMessage(content='```json\n{\n  "case_number": "B2022-16584",\n  "incident_type": "Found Property",\n  "date_of_incident": "May 4, 2022",\n  "incident_address": "620 Mason Street",\n  "organisations": [\n    "Bramblewood County Sheriff’s Office",\n    "ABC Forensic Services Laboratory"\n  ],\n  "telephones": [],\n  "complainants": [\n    {\n      "name": "Julie Hodges",\n      "address": "620 Mason Street"\n    },\n    {\n      "name": "Jeff Hodges",\n      "address": "620 Mason Street"\n    }\n  ],\n  "summary": "On May 
4, 2022, while doing landscaping, Jeff and Julie Hodges discovered a box containing a firearm and other items in their yard at 620 Mason Street. They reported it to the Bramblewood County Sheriff’s Office, and Investigator Carrie Fitz collected and secured the items for forensic analysis.",\n  "description": "The document 
details the discovery of a firearm and other items by Jeff and Julie Hodges at their home, with subsequent handling by law enforcement for forensic testing.",\n  "evidence": [\n    {\n      "item_number": "BC', refusal=None, role='assistant', audio=None, function_call=None, tool_calls=None)"""
print(analysed_text_JSON)
with open("PydanticResult.json", "w") as output:
    output.write(analysed_text_JSON.model_dump_json())

