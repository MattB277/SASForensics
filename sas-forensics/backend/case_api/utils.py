def upload_to_based_on_type(instance, filename):
    ext = filename.split('.')[-1]
    base_filename = '.'.join(filename.split('.')[:-1])
    if ext.lower() in ['pdf', 'docx', 'jpeg', 'mp4']:
        subdir = 'pdfs' if ext.lower() == 'pdf' else 'images' if ext.lower() in ['jpeg', 'jpg'] else 'videos'
        return f"{subdir}/{base_filename}.{ext}"
    else:
        return f"others/{base_filename}.{ext}"