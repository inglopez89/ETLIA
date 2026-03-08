#import google.generativeai as genai
from google import genai
from load_dotenv import load_dotenv
import os
load_dotenv()  # Carga las variables de entorno desde el archivo .env

api_key = os.getenv('LLM_API')
client = genai.Client(api_key=api_key)

def call_model(prompt):
    # integracion proveedor de IA 
    message = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=prompt,
)
    # Print the response content
    return message.text