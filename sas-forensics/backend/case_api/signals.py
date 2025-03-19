import io
from django.db.models.signals import post_save, post_delete, m2m_changed, pre_delete
from django.dispatch import receiver
from django.core.files.base import ContentFile
from .models import File, Case, AnalysedDocs, CaseChangelog, DocChangelog, UserCaseAccessRecord, User
from .utils import analyseTextIntoJSON, getPDFtext, openTXT, ocr
import os, json
from backend_core.settings import MEDIA_ROOT
from docx import Document
import docx
# from spire.doc import *	
# from spire.doc.common import Document as D


### Document Analysis ### 
@receiver(post_save, sender=File)
def analyse_upload(sender, instance, created, **kwargs):
    if created: # only analyse newly uploaded documents
        print("Database record for file: ", instance.file.name, " created")
        # extract text based upon file type
        if instance.file_extension() == "pdf":
            if os.path.exists(instance.file.path):
                extracted_text = getPDFtext(instance.file.path)
            else:
                return
        elif instance.file_extension() ==  "docx":    # placeholder until logic implemented
                print("Docx analysis not implemented yet!")
                return
        elif instance.file_extension() ==  "png": # placeholder until logic implemented
            extracted_text = ocr(instance.file.name,True)
            # print(extracted_text)
            return
        else: # default value
            print("Datatype not supported!")
            return 
        
        try:
            # open existing json file
            json_filename = os.path.splitext(os.path.basename(instance.file.name))[0] + ".json"
            json_path = os.path.join(MEDIA_ROOT, "json", json_filename)
            
            # save its contents
            with open(json_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            print("Found existing json analysis, saved contents to memory")

            # delete the file
            os.remove(json_path)
            print("Removed existing json file")
            json_data = json.dumps(json_data)

        except FileNotFoundError:
            # no analysis exists, call AI analysis function
            print("Analysing ", instance.file.name)
            analysis_output = analyseTextIntoJSON(extracted_text)
            json_data = analysis_output.model_dump_json()  # Convert JSON to string

        finally:
            # Store JSON in memory
            json_bytes_io = io.BytesIO(json_data.encode("utf-8"))
            json_file = ContentFile(json_bytes_io.getvalue(), name=f"{os.path.splitext(os.path.basename(instance.file.name))[0]}.json")

            # Create database record with in-memory file
            AnalysedDocs.objects.create(
                file_id=instance,
                JSON_file=json_file,  # Pass in-memory file to be written to disk
                case_number=instance.case_id.case_number if instance.case_id else "",
                reviewed=False
            )
            print(f"Analysis saved to: {os.path.splitext(os.path.basename(instance.file.name))[0]}.json")
        


### Changelog signals ###

# Update Case and Doc changelog upon file upload/change
@receiver(post_save, sender=File)
def log_file_upload(sender, instance, created, **kwargs):
    if not instance.case_id:
        return

    # Get extra change details from the instance, if set
    change_details = getattr(instance, "_change_details", None)
    change_author = getattr(instance, "_change_author", None)
    try:
        analysed_doc = instance.analysed_document   # get Files analysis instance
    except:
        analysed_doc = None # set to none if the file has no analysis (eg. docx file)
    
    # default messages if no metadata is found
    if change_details is None:
        change_details = f"File {instance.display_name()} updated."
    if created:
        change_details = f"File {instance.display_name()} uploaded."
        # creation entry in doc changelog 
        DocChangelog.objects.create(
        file_id = instance,
        analysis_id=analysed_doc,
        change_details=change_details,
        change_author=change_author,
        type_of_change="File Uploaded"
        )
    # update case changelog based on upload/ general file change
    CaseChangelog.objects.create(
        case_id = instance.case_id,
        change_details=change_details,
        change_author=change_author,
        type_of_change="Added Evidence" if created else "Updated Information"
    )


    # clean up metadata
    if hasattr(instance, "_change_details"):
        delattr(instance, "_change_details")
    if hasattr(instance, "_change_author"):
        delattr(instance, "_change_author")

#Log file deletion in Case changelog
@receiver(pre_delete, sender=File)
def log_file_deletion(sender, instance, **kwargs):
    if instance.case_id:
        CaseChangelog.objects.create(
            case_id = instance.case_id,
            change_details=f"File {instance.display_name()} deleted.",
            change_author=None,
            type_of_change="Removed Evidence"
        )

# log changes to assigned users
@receiver(m2m_changed, sender=Case.assigned_users.through)
def log_assigned_users_change(sender, instance, action, pk_set, **kwargs):
    if action in ["post_add", "post_remove"]:
        # Get the user objects from the provided primary keys
        users = User.objects.filter(pk__in=pk_set)
        user_names = ", ".join(user.username for user in users)

        # Determine the type of change and details based on the action
        if action == "post_add":
            change_details = f"Added user(s): {user_names} to {instance.case_number}."
            change_type = "Assigned Detective"  
        else:  # "post_remove"
            change_details = f"Removed user(s): {user_names} from {instance.case_number}."
            change_type = "Updated Information" 
            
        change_author = getattr(instance, "_change_author", None)

        # Create a changelog entry
        CaseChangelog.objects.create(
            case_id=instance,
            change_details=change_details,
            change_author=change_author,
            type_of_change=change_type
        )

## Analysis Changelog signals ##
@receiver(post_save, sender=AnalysedDocs)
def log_analysis_changes(sender, instance, created, **kwargs):
    change_details = getattr(instance, "_change_details", None) # only set if User changed JSON data
    change_author = getattr(instance, "_change_author", None)
    
    # if no change details passed, and was created, make creation entry and return 
    if change_details != "Altered analysis": 
        if created:
            DocChangelog.objects.create(
            file_id = instance.file_id,
            analysis_id=instance,
            change_details="Document was analysed with AI.",
            change_author=change_author,
            type_of_change="Analysis Created"
            )
            return
    else:
        #else if change details = Altered analysis, create changelog for changes first, then another for approval
        if change_details == "Altered analysis":
            DocChangelog.objects.create(
                file_id = instance.file_id,
                analysis_id=instance,
                change_details=change_details,
                change_author=change_author,
                type_of_change="Updated Analysis"
            )

    # analysis must have been approved if not created.
    DocChangelog.objects.create(
        file_id = instance.file_id,
        analysis_id=instance,
        change_details="Analysis was reviewed and approved",
        change_author=change_author,
        type_of_change="Analysis Reviewed"
    )

    # create Case changelog for analysis approval
    file_instance = instance.file_id
    case_instance = file_instance.case_id
    CaseChangelog.objects.create(
        case_id = case_instance,
        change_details=f"Analysis Approved for {file_instance.display_name()}",
        change_author=change_author,
        type_of_change="Updated Information"
    )

## Document Changelog signals ##
