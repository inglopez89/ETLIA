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
    """View for uploading Excel, CSV and TXT files with file preview"""
    error_message = None
    success_count = 0
    
    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('file')
        
        if uploaded_files:
            # Check maximum file limit
            if len(uploaded_files) > 4:
                error_message = "Maximum 4 files can be uploaded at once."
            else:
                # Validate file type - only accept Excel, CSV and TXT files
                allowed_extensions = ['.xlsx', '.xls', '.csv', '.txt']
                
                for uploaded_file in uploaded_files:
                    file_name = uploaded_file.name
                    file_extension = os.path.splitext(file_name)[1].lower()
                    
                    if file_extension not in allowed_extensions:
                        error_message = f"Invalid file type '{file_extension}'. Only Excel (.xlsx, .xls), CSV (.csv) and Text (.txt) files are allowed."
                        break
                    else:
                        # Save file to model
                        file_obj = UploadedFile(
                            file=uploaded_file,
                            file_name=file_name,
                            file_type=file_extension
                        )
                        file_obj.save()
                        success_count += 1
                
                if success_count > 0 and not error_message:
                    return redirect('file_upload_interface')
    
    # Get all uploaded files
    uploaded_files_list = UploadedFile.objects.all()
    
    return render(request, 'file_upload_interface.html', {
        'uploaded_files': uploaded_files_list,
        'error_message': error_message
    })