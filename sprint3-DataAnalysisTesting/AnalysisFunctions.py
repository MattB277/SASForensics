from PyPDF2 import PdfFileReader
import pymupdf
import boto3
from botocore.exceptions import ClientError
import os
from openai import OpenAI
from openai import APIStatusError
from typing import List, Optional
from pydantic import BaseModel, Field

class AnalysisOutput(BaseModel):
    # nested data structures
    class Person(BaseModel):
        name:str = Field(description="The name of a person mentioned in the document")
        address: Optional[str] = Field(description="The address of a person if it is given")
        relevance: str = Field(description="How this person is related to the document, officer, victim, suspect etc.")
    class Event(BaseModel):
        event_type: str = Field(description="What type of event is it?")
        details: str = Field(description="What happened in this event?")
    class Evidence(BaseModel):
        item_number: str = Field(description="The item number specified for this peice of evidence")
        description: List[str] = Field(description="The descriptions of the peice of evidence")

    # top level data containers/variables
    case_number: str = Field(description="the case number stated on the document")
    document_type: str = Field(description="What type of document it is, Interview, Forensic report etc")
    summary: str = Field(description="A three sentence long description of the document.")
    conclusion: Optional[str] = Field(description="A short conclusion highlighting any findings made in the document.")
    location: List[str] = Field(description="Any locations mentioned in the document")
    people: List[Person] = Field(description="Names of people mentioned, their address and their role in the document if given.")
    events: List[Event] = Field(description="A list of each event described.")
    evidence: List[Evidence] = Field(description="A list of each piece of evidence")
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

def analyseTextIntoJSON(document_text):
    # try to create OpenAI client instance
    try:
        client = OpenAI()
        print("openAI client opened successfully!")
    except APIStatusError as e:
        # environment variables are misbehaving
        print("openAI client creation failed!")
        print(e)
        try:
            # try to manually retrieve the API key from environment
            client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        except:
            print("fatal error with OpenAI client!")
            print("Set the API key to an evironment variable with the name OPENAI_API_KEY")
    # Prompt to instruct the system
    system_prompt = "You are a helpful assistant whose task is to reduce the time required by detectives in analysing cold case documents by ingesting documents and returning valuable information"
    # The prompt to instruct the model
    prompt = f"""
    Analyze the following document independently and generate a structured JSON response, you must make sure that all information you give me is based solely upon this document:
    {document_text}

    Output a JSON object with the following fields:
    - case_number
    - document_type (is it an Interview, incident report, investigative report, analysis report, etc.)
    - date_of_incident
    - people (list of objects with "name", "address" and "relevance" if available)
    - summary (a concise overview of the document, max 3 sentences long)
    - evidence (list of objects with "item_number", "description" containing any results or analysis per peice of evidence.)
    - conclusions (final remarks based on the document)

    Use only information contained in the provided text. Leave fields as null if not applicable or no information regarding that field was found.
    """

    response = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",  # Or other preferred model
        messages=[
            {'role':'system', 'content':system_prompt},
            {'role':'user', 'content':prompt}
        ],
        response_format=AnalysisOutput,
        max_tokens=256,
        temperature=0.2,
        n=1,
    )

    return response.choices[0].message.parsed


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