import os
def upload_to_based_on_type(instance, filename):
    # Get the file extension
    extension = filename.split('.')[-1].lower()

    # Map extensions to folders
    folder_map = {
        'pdf': 'pdfs',
        'mp4': 'videos',
        'jpeg': 'images',
        'jpg': 'images',  # Include additional aliases
        'docx': 'documents',
    }

    # Determine folder based on the file extension
    folder = folder_map.get(extension, 'others')

    # Return the relative path where the file will be uploaded
    return os.path.join(folder, filename)