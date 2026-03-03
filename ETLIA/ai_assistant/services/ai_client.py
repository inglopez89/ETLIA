import  anthropic
from load_dotenv import load_dotenv
import os
load_dotenv()  # Carga las variables de entorno desde el archivo .env
from openai import OpenAI


client =  OpenAI(
    api_key=os.getenv('LLM_API'),
    base_url="https://api.moonshot.ai/v1",
)

#api_key = os.getenv('LLM_API')
#lient = anthropic.Anthropic(api_key=api_key)
def call_model(prompt):
    # integracion proveedor de IA 

    completion = client.chat.completions.create(
    model="moonshot-v1-128k", # Or other available models like "kimi-k2.5"
    messages=[
        {"role": "system", "content": "You are Kimi, a helpful AI assistant."},
        {"role": "user", "content": f"{prompt}"},
    ],
    temperature=0.3,
    )

    # Print the response content
    print(completion.choices[0].message.content)