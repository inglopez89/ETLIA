import json
import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render
from .services.promp_builder import build_prompt_1
from .services.ai_client import call_model
from data_processing.services.actions import AVAILABLE_ACTIONS
from data_processing.models import UploadedFile

def interpretet_intent(request):
      
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
 
     # Read user message from POST body
     try:
         body = json.loads(request.body) if request.body else {}
     except json.JSONDecodeError:
         body = {}
     user_text = body.get('message', '')

     # Step 1: Interpret the user's intent in plain language
     prompt1 = build_prompt_1(user_text,file1_cols,file2_cols, list(AVAILABLE_ACTIONS.keys()))
     interpreted_intent = call_model(prompt1)
     if interpreted_intent not in AVAILABLE_ACTIONS and interpreted_intent != "No encontrada":
            return JsonResponse(
                {
                    "interpretation": interpreted_intent,
                },
                status=200,
            )
     else:
         interpreted_intent = execute_action(request,dfs,interpreted_intent)
     return JsonResponse({
            "interpretation": interpreted_intent ,
        }, status=200)



def execute_action(request, dfs, action_name):
    if action_name not in AVAILABLE_ACTIONS:
        return JsonResponse(
            {
                "interpretation": action_name,
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
                        "interpretation": action_name,
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
            "interpretation": action_name,
            "action": action_name,
            "rows": len(result_df),
            "columns": result_df.columns.tolist(),
            "preview": result_df.head(5).to_dict(orient='records'),
        })
    except Exception as e:
        return JsonResponse(
            {
                "interpretation": action_name,
                "action": action_name,
                "error": str(e),
            },
            status=500,
        )
