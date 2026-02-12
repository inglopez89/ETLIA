import pandas as pd
import os
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from .models import UploadedFile

# Create your views here.

def upload_files(request):
    context = {}
    if request.method == 'POST':
        file1 = request.FILES.get('file1')
        file2 = request.FILES.get('file2')

        if file1 and file2:
            df1 = pd.read_csv(file1, encoding='utf-8', delimiter=',',header=0)
            df2 = pd.read_csv(file2, encoding='utf-8', delimiter=',',header=0)

            context['file1_columns'] = df1.columns.tolist()
            context['file2_columns'] = df2.columns.tolist()
            context['file1_name'] = file1.name
            context['file2_name'] = file2.name
        else:
            context['error'] = "Please upload both files."
            
    return render(request, 'upload.html', context)


def file_upload_interface(request):
    """View for uploading files with image preview"""
    error_message = None
    
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        
        if uploaded_file:
            # Get file information
            file_name = uploaded_file.name
            file_extension = os.path.splitext(file_name)[1].lower()
            
            # Validate file type - only accept Excel and TXT files
            allowed_extensions = ['.xlsx', '.xls', '.txt']
            
            if file_extension not in allowed_extensions:
                error_message = f"Invalid file type. Only Excel (.xlsx, .xls) and Text (.txt) files are allowed."
            else:
                # Save file to model
                file_obj = UploadedFile(
                    file=uploaded_file,
                    file_name=file_name,
                    file_type=file_extension
                )
                file_obj.save()
                
                return redirect('file_upload_interface')
    
    # Get all uploaded files
    uploaded_files = UploadedFile.objects.all()
    
    return render(request, 'file_upload_interface.html', {
        'uploaded_files': uploaded_files,
        'error_message': error_message
    })