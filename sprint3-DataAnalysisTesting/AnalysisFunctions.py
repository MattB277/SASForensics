from PyPDF2 import PdfFileReader
import pymupdf
import boto3
from botocore.exceptions import ClientError
import os
from openai import OpenAI
# Pdf conversion functions

def pyMuPDFconvert(pdf):
    """takes a byte stream of a pdf document and returns it's text"""
    document = pymupdf.open(stream=pdf, filetype="pdf")
    content = getPDFtext(document)
    return content


# reader -> extracted text
def getPDFtext(document):
    """takes a pyMuPDF reader and returns the documents text as a string"""
    content = ""
    for page in document:
        content += page.get_text()
    return content

# pdf path to text file (local testing function)
def PDFDoctoTextDoc(source):
    """takes pdf path and saves to local directory txt file"""
    pdf = open(source, "rb")
    pdfDoc = PdfFileReader(pdf)
    text = parsePDFtoText(pdfDoc)

    # create destination path
    source = str(source) # cast to string type
    destPath = source.split(".")[0] # split off pdf extension
    
    # create text file
    with open(destPath+".txt", "w") as f:
        f.write(text)

    return destPath

def parsePDFtoText(pdf):
    """Takes a pdf in byte format and local and returns its text in a string"""
    text = ""
    for page in range(0,pdf.getNumPages()):
        text += pdf.getPage(page).extract_text()
    return text
    
# local path -> reader (testing function)
def openLocalPDF(path):
    pdf = pymupdf.open(filename=path, filetype='pdf')
    return pdf


# AI analysis functions

def analyseTextIntoJSON(client, document_text):
    # The prompt to instruct the model
    prompt = f"""
    Analyze the following document independently and generate a structured JSON response:
    {document_text}

    Output a JSON object with the following fields:
    - case_number
    - incident_type
    - date_of_incident
    - incident_address
    - complainants (list of objects with "name" and "address" if available)
    - summary (a concise overview of the document)
    - description (a one-sentence description of the document)
    - evidence (list of objects with "item_number", "description", and any results or analysis)
    - responding_officer (name, badge number, and report date if available)
    - forensic_report (details of the lab report including lab number, agency, report date, and services requested)
    - conclusions (final remarks based on the document)

    Use only information contained in the provided text. Leave fields blank or null if not applicable.
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Or other preferred model
        messages=prompt,
        max_tokens=256,
        temperature=1,
        n=1,
        stop=None
    )

    print(response.choices[0].text.strip())
    return response.choices[0].text.strip()


# S3 functions

# upload a pdf into specific bucket 
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
    return pyMuPDFconvert(content)