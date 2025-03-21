from django.conf import settings
import pymupdf, boto3, os
from botocore.exceptions import ClientError
from openai import APIStatusError, OpenAI
from typing import List, Optional
from pydantic import BaseModel, Field, PastDatetime
import boto3
import json
from backend_core.settings import MEDIA_ROOT, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

# Structured Output Pydantic model
class AnalysisOutput(BaseModel):
    # nested data structures
    class Person(BaseModel):
        name:str = Field(description="The name of a person mentioned in the document")
        address: Optional[str] = Field(description="The address of a person if it is given")
        relevance: str = Field(description="How this person is related to the document, officer, victim, suspect etc.")
    class Event(BaseModel):
        event_type: str = Field(description="What type of event is it?")
        details: str = Field(description="What happened in this event?")
        time_of_event: str = Field(description="The datetime of the event, in the format of DD/MM/YYYY-HH:MM, exclude hours and minutes if not applicable") 
    class Evidence(BaseModel):
        item_number: str = Field(description="The item number specified for this peice of evidence")
        description: List[str] = Field(description="The descriptions of the peice of evidence")

    # top level data containers/variables
    case_number: str = Field(description="the case number stated on the document")
    date_on_document: str = Field(description="The date of the document, sometimes stated under Date of report, in the format DD/MM/YYYY")
    document_type: str = Field(description="What type of document it is, Interview, Forensic report etc")
    summary: str = Field(description="A three sentence long description of the document.")
    conclusion: Optional[str] = Field(description="A short conclusion highlighting any findings made in the document.")
    location: List[str] = Field(description="Any locations mentioned in the document")
    people: List[Person] = Field(description="Names of people mentioned, their address and their role in the document if given.")
    events: List[Event] = Field(description="A list of each event described.")
    evidence: List[Evidence] = Field(description="A list of each piece of evidence")

# PDF Conversion Util
def getPDFtext(document_path):
    """Takes a PDF path and returns the document's text as a single string"""
    # open PDF reader
    document = pymupdf.open(filename=document_path, filetype='pdf')
    # read contents
    content = ""
    for page in document:
        content += page.get_text()
    return content

# .txt File Reading Util
def openTXT(document_path):
    """Used for analysis of handwritten notes, takes a path and returns the string of the txt contents"""
    with open(document_path, "r") as file:
        content = file.read()
    return content

def summariseCaseAnalysis(file_list, case_id):
    """Takes a list of JSON file paths, creates a case summary and returns the JSON dictionary as a string."""
    #extract the data from the individual analysis files
    extracted_data = []

    for file in file_list:
        try:
            with open(file, "r") as f:
                data = json.load(f)
                extracted_data.append(data)
        except Exception as e:
            print(f"Error reading JSON: {file}", e)
    
    # create prompt
    prompt = ("I have had AI extract information from some individual documents belonging to the same case, and have had a human review them for accuracy."
            "I now would like you to summarize and condense the information into a case summary, highlighting where references to other case numbers or documents have been made."
            "I would also like a list of next steps to be taken, including highlighting prime suspects, these should be closely linked with the following JSON data"
            "Ensure the response is a valid JSON dictionary:\n\n"
            f"{json.dumps(extracted_data, indent=2)}"
            )
    system_prompt = "You are a helpful assistant whose task is to reduce the time required by detectives in analysing cold case documents by ingesting documents and returning valuable information"

    # create AI client
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
    
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {'role':'system', 'content':system_prompt},
            {'role':'user', 'content':prompt}
        ],
        response_format={"type":"json_object"},
        max_tokens=3500, # larger than other prompt due to much higher volume of input data
    )

    # parse response into python object
    parsed_json = json.loads(response.choices[0].message.content)
    print(parsed_json)
    # save summary to file (this could probably be refactored into a read/write function instead)
    summary_filename = f"case_{case_id}_summary.json"
    summary_file_path = os.path.join(settings.MEDIA_ROOT, "json", summary_filename)
    with open(summary_file_path, "w") as f:
        f.write(json.dumps(parsed_json)) # slice quotes off of string
    print(f"case {case_id} summary saved to file {summary_filename}")

    return parsed_json   # return analysis output to cut down Read/writes on json file. 

# Analyse Document Text
def analyseTextIntoJSON(document_text):
    """This function analyses a string, and returns a JSON dictionary result."""
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
    - date_of_incident (Formatted as DD/MM/YYYY)
    - people (list of objects with "name", "address" and "relevance" if available)
    - summary (a concise overview of the document, max 3 sentences long)
    - evidence (list of objects with "item_number", "description" containing any results or analysis per peice of evidence.)
    - conclusions (final remarks based on the document)

    Use only information contained in the provided text. Leave fields as null if not applicable or no information regarding that field was found.
    """

    response = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",  # models to be experimented with
        messages=[
            {'role':'system', 'content':system_prompt},
            {'role':'user', 'content':prompt}
        ],
        response_format=AnalysisOutput,
        max_tokens=2560,
        temperature=0.2,
        n=1,
    )

    return response.choices[0].message.parsed


def upload_to_based_on_type(instance, filename):
    ext = filename.split('.')[-1]
    base_filename = '.'.join(filename.split('.')[:-1])
    if ext.lower() in ['pdf', 'docx', 'jpeg', 'mp4']:
        subdir = 'pdfs' if ext.lower() == 'pdf' else 'images' if ext.lower() in ['jpeg', 'jpg'] else 'videos'
        return f"{subdir}/{base_filename}.{ext}"
    else:
        return f"others/{base_filename}.{ext}"
    


def ocr(file_name, upload = False, bucket_name = "textract-sasforensics"):

    # Upload file to S3
    if upload:        
        s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        s3.upload_file(os.path.join(MEDIA_ROOT, file_name), bucket_name, file_name)

    textract = boto3.client("textract", region_name="eu-west-1")

    response = textract.detect_document_text(
        Document={"S3Object": {"Bucket": bucket_name, "Name": file_name}}
    )

    # Extract and print text
    text = "\n".join([block["Text"] for block in response["Blocks"] if block["BlockType"] == "LINE"])
    return text
