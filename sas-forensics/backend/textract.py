import boto3
from case_api.utils import ocr
print(ocr("images\cat.png"))
print(ocr(r"images\text.png", True))

