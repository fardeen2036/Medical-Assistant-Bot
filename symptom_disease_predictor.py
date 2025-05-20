symptom_disease_map = {
    "fever cough fatigue": "flu",
    "shortness of breath cough wheezing": "copd",
    "chest pain shortness of breath": "heart disease"
    # Add more mappings
}

def predict_disease_from_symptoms(user_input):
    user_input = user_input.lower()
    for symptoms, disease in symptom_disease_map.items():
        if all(word in user_input for word in symptoms.split()):
            return disease
    return None
