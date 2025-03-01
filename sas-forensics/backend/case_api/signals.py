import io
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.base import ContentFile
from .models import File, AnalysedDocs
from .utils import analyseTextIntoJSON, getPDFtext, openTXT, ocr
import os, json
from backend_core.settings import MEDIA_ROOT

@receiver(post_save, sender=File)
def analyse_upload(sender, instance, created, **kwargs):
    if created: # only analyse newly uploaded documents
        # extract text based upon file type
        match instance.file_extension():
            case "pdf":
                if os.path.exists(instance.file.path):
                    extracted_text = getPDFtext(instance.file.path)
                else:
                    return
            case "docx":    # placeholder until logic implemented
                print("Docx analysis not implemented yet!")
                return
            case "png": # placeholder until logic implemented
                extracted_text = ocr(instance.file.name,True)
                # print(extracted_text)
                return
            case _: # default value
                print("Datatype not supported!")
                return 
        
        # Save original file basename (no extension)
        file_basename = f"{os.path.splitext(os.path.basename(instance.file.name))[0]}.json"

        # Analyse document
        analysis_output = analyseTextIntoJSON(extracted_text)
        json_data = analysis_output.model_dump_json()  # Convert JSON to string

        # Store JSON in memory
        json_bytes_io = io.BytesIO(json_data.encode("utf-8"))
        json_file = ContentFile(json_bytes_io.getvalue(), name=file_basename)

        # Create database record with in-memory file
        AnalysedDocs.objects.create(
            file_id=instance,
            JSON_file=json_file,  # Pass in-memory file to be written to disk
            case_number=instance.case_id.case_number if instance.case_id else "",
            reviewed=False
        )
        print(f"Analysis saved to: {file_basename}")