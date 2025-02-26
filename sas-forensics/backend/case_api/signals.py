from django.db.models.signals import post_save
from django.dispatch import receiver
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

        # configure new JSON file
        json_filename = os.path.splitext(os.path.basename(instance.file.name))[0] + ".json" # same name as original file
        json_path = os.path.join(MEDIA_ROOT , "json", json_filename)

        # create json dir if it does not exist
        if not (os.path.exists(os.path.join(MEDIA_ROOT, 'json'))):
            os.makedirs(os.path.join(MEDIA_ROOT, 'json'))

        # check if analysis exists before analysing
        if not os.path.exists(json_path):
            # analyse text
            analysis_output = analyseTextIntoJSON(extracted_text)
            # write JSON file to disk
            with open(json_path, "w", encoding="utf-8") as json_file:
                json_file.write(analysis_output.model_dump_json())

        # create database record 
        AnalysedDocs.objects.create(
            file_id = instance, 
            JSON_file = json_path,
            case_number = instance.case_id.case_number if instance.case_id else "",
            reviewed = False
        )
