import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# List all available models
print("Available models:\n")
models = genai.list_models()
for model in models:
    print(f"Name: {model.name}")
    print(f"Display Name: {model.display_name}")
    if hasattr(model, 'supported_generation_methods'):
        print(f"Supported Methods: {model.supported_generation_methods}")
    print()
