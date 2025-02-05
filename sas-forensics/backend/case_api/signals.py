from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import File, AnalysedDocs
from .utils import analyseTextIntoJSON, getPDFtext, openTXT
import os
from backend_core.settings import MEDIA_ROOT

@receiver(post_save, sender=File)
def analyse_upload(sender, instance, created, **kwargs):
    if created: # only analyse newly uploaded documents
        # extract text based upon file type
        match instance.file_extension():
            case "pdf":
                extracted_text = getPDFtext(instance.file.path)
            case "docx":    # placeholder until logic implemented
                print("Docx analysis not implemented yet!")
            case "png": # placeholder until logic implemented
                pass
            case _: # default value
                print("Datatype not supported!")
        
        analysis_output = analyseTextIntoJSON(extracted_text)
        
        # configure new JSON file
        json_filename = os.path.splitext(os.path.basename(instance.file.name))[0] + ".json" # same name as original file
        json_path = os.path.join(MEDIA_ROOT , "json", json_filename)

        # create database record 
        AnalysedDocs.objects.create(
            file_id = instance, 
            JSON_file = json_path,
            case_number = instance.case_id.case_number if instance.case_id else ""
        )
