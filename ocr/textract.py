import boto3

s3 = boto3.client("s3")

# bucket_name = "2833791"

def ocr(file_name, bucket_name = "2833791"):

    # Upload file to S3
    s3.upload_file(file_name, bucket_name, file_name)

    textract = boto3.client("textract")

    response = textract.detect_document_text(
        Document={"S3Object": {"Bucket": bucket_name, "Name": file_name}}
    )

    # Extract and print text
    text = "\n".join([block["Text"] for block in response["Blocks"] if block["BlockType"] == "LINE"])
    return text
