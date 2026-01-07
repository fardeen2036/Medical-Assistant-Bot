from flask import Flask, request, jsonify, render_template
import pandas as pd
import redis
import google.generativeai as genai
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

# Load dataset
drug_df = pd.read_csv("final.csv")
all_diseases = drug_df['disease'].dropna().unique().tolist()
all_diseases_lower = [d.lower() for d in all_diseases]

# Redis
redis_url = os.getenv("REDIS_URL")
redis_client = redis.from_url(redis_url, decode_responses=True) if redis_url else None

# Gemini
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-2.0-flash-lite")
except Exception as e:
    print(f"Error configuring Gemini: {e}")
    model = None

# Emergency list
emergency_conditions = ['heart attack', 'stroke', 'cancer', 'sepsis', 'tuberculosis', 'dengue', 'covid']

def extract_disease_from_text(text):
    text = text.lower()
    for disease in all_diseases_lower:
        if disease in text:
            return disease
    return None

def check_emergency_condition(disease_name):
    if disease_name.lower() in emergency_conditions:
        return "⚠️ This may be a serious condition. Please consult a doctor immediately."
    return ""

def check_interactions_wrapper(drug_list):
    try:
        drugs = [d.strip().lower() for d in drug_list]
        interactions_found = []
        for i in range(len(drugs)):
            for j in range(i + 1, len(drugs)):
                d1, d2 = drugs[i], drugs[j]
                interaction_set = redis_client.smembers(f"drug:{d1}:interactions")
                for interaction in interaction_set:
                    other_drug, desc = interaction.split("|", 1)
                    if other_drug.strip().lower() == d2:
                        interactions_found.append(f"{d1} and {d2}: {desc.strip()}")
        return interactions_found
    except Exception as e:
        return [f"⚠️ Could not check interactions: {e}"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get('message', '')
    if not user_msg:
        return jsonify({"reply": "Please enter a message."}), 400

    disease = extract_disease_from_text(user_msg)

    if disease and model:
        drugs = drug_df[drug_df['disease'].str.lower() == disease]['drug'].tolist()
        interaction_info = check_interactions_wrapper(drugs)
        emergency_msg = check_emergency_condition(disease)

        # Gemini chat prompt
        chat = model.start_chat()
        prompt = f"""
A user says: "{user_msg}"

You identified the disease as: {disease}.
Recommended drugs: {', '.join(drugs)}.
Interactions: {', '.join(interaction_info) if interaction_info else "None"}.
{emergency_msg}

Respond like a helpful and fluent healthcare assistant summarizing everything for the user in natural, human-like language.
"""

        try:
            response = chat.send_message(prompt)
            return jsonify({"reply": response.text.strip()})
        except Exception as e:
            return jsonify({"reply": f"❌ Gemini error: {e}"}), 500

    elif model:
        # No disease matched, fallback to Gemini
        try:
            chat = model.start_chat()
            fallback = chat.send_message(f"""
The user said: "{user_msg}"

Respond in natural language like a smart healthcare assistant to help them understand what they might be experiencing.
""")
            return jsonify({"reply": fallback.text.strip()})
        except Exception as e:
            return jsonify({"reply": f"❌ Gemini fallback error: {e}"}), 500
    else:
        return jsonify({"reply": "❌ Gemini model is not initialized. Please check the API key."}), 500

if __name__ == '__main__':
    app.run()













