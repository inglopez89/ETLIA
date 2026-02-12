import pandas as pd
from django.shortcuts import render

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