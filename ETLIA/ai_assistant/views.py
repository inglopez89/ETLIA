import json
import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render
from .services.promp_builder import build_prompt_1, build_prompt_2
from .services.ai_client import call_model
from data_processing.services.actions import AVAILABLE_ACTIONS


def interpretet_intent(request):
     from data_processing.models import UploadedFile
 
     # Load uploaded files from DB
     uploaded_files = list(UploadedFile.objects.all())
     if not uploaded_files:
         return JsonResponse(
             {"error": "No hay archivos cargados. Por favor sube al menos un archivo."},
             status=400,
         )
 
     # Read each file as a dataframe
     dfs = []
     for f in uploaded_files:
         try:
             path = f.file.path
             if f.file_type in ['.csv', '.txt']:
                 df = pd.read_csv(path)
             else:
                 df = pd.read_excel(path)
             dfs.append(df)
         except Exception as e:
             return JsonResponse(
                 {"error": f"Error al leer '{f.file_name}': {str(e)}"},
                 status=400,
             )
 
     file1_cols = dfs[0].columns.tolist() if len(dfs) > 0 else []
     file2_cols = dfs[1].columns.tolist() if len(dfs) > 1 else []
 
     # Step 1: Interpret the user's intent in plain language
     prompt1 = build_prompt_1(file1_cols, file2_cols)
     interpreted_intent = call_model(prompt1)
     return JsonResponse({
            "rows_file1": len(file1_cols),
            "rows_file2": len(file2_cols),
            "columns_file1": file1_cols,
            "columns_file2": file2_cols,
            "interpretation": interpreted_intent ,
        })



def execute_action(request, dfs, intent):

    # Step 2: Map interpreted intent to an available function
    prompt2 = build_prompt_2(intent, list(AVAILABLE_ACTIONS.keys()))
    action_name = call_model(prompt2).strip()

    if action_name not in AVAILABLE_ACTIONS:
        return JsonResponse(
            {
                "interpretation": intent,
                "error": "No encontré una función adecuada para tu solicitud.",
            },
            status=400,
        )

    # Step 3: Parse optional params from request body
    try:
        body = json.loads(request.body) if request.body else {}
    except json.JSONDecodeError:
        body = {}
    params = body.get('params', {})

    # Step 4: Execute action
    func = AVAILABLE_ACTIONS[action_name]
    try:
        if action_name == 'merge_data':
            if len(dfs) < 2:
                return JsonResponse(
                    {
                        "interpretation": intent,
                        "error": "merge_data necesita al menos 2 archivos cargados.",
                    },
                    status=400,
                )
            result_df = func(dfs[0], dfs[1], **params)
        elif action_name == 'filter_data':
            result_df = func(dfs[0], params.get('filter_conditions', {}))
        else:
            result_df = func(dfs[0], **params)

        return JsonResponse({
            "interpretation": intent,
            "action": action_name,
            "rows": len(result_df),
            "columns": result_df.columns.tolist(),
            "preview": result_df.head(5).to_dict(orient='records'),
        })
    except Exception as e:
        return JsonResponse(
            {
                "interpretation": intent,
                "action": action_name,
                "error": str(e),
            },
            status=500,
        )
