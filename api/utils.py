# api/utils.py
import os
import shutil
import re
from datetime import datetime

def allowed_file(filename, allowed_extensions):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def get_file_size(filepath):
    """Get file size in human readable format"""
    size = os.path.getsize(filepath)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"

def cleanup_temp_files(base_path, files_to_keep=None):
    """Clean up temporary files"""
    try:
        if files_to_keep is None:
            files_to_keep = []
        
        for filename in os.listdir(base_path):
            if filename in files_to_keep:
                continue
            filepath = os.path.join(base_path, filename)
            if os.path.isfile(filepath):
                os.remove(filepath)
    except Exception as e:
        print(f"Error cleaning up files: {e}")

def validate_pdf_file(filepath):
    """Validate PDF file"""
    try:
        import PyPDF2
        with open(filepath, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            return len(reader.pages) > 0
    except:
        return False