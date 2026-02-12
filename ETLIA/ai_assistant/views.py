from django.http import JsonResponse
from .services.promp_builder import build_prompt_1
from .services.ai_client import call_model

# Create your views here.
def interpretet_intent(request):
    if request.method == 'POST':
        user_text = request.POST.get("user_text")
        file1_cols = request.POST.GET.getlist("file1_cols[]")
        file2_cols = request.POST.GET.getlist("file2_cols[]")

        prompt = build_prompt_1(user_text, file1_cols, file2_cols)
        response = call_model(prompt)
        
        return JsonResponse({"result": response})