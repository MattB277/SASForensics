from openai import OpenAI 
from AnalysisFunctions import *
import os
# create openAI client
key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

document_text = parsePDFtoText(openLocalPDF('PythonTests\Day-1A_Incident-Report_Final3.pdf'))
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
