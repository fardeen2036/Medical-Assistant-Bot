import google.generativeai as genai

try:
    genai.configure(api_key="AIzaSyC0TfL96Oc_qWwaho7xqEqiC1QP884GEPQ")  # Ensure your API key is set

    # Attempt to list available models
    models = genai.list_models()
    for model_info in models:
        print(f"Model Name: {model_info.name}")
        print(f"Supported Methods: {model_info.supported_generation_methods}")
        print("-" * 20)

except Exception as e:
    print(f"Error listing models: {e}")