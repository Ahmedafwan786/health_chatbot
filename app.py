from flask import Flask, render_template, request, jsonify
import json, os

app = Flask(__name__)

# Load dataset (assumes disease_data.json is in the same folder)
DATA_PATH = os.path.join(os.path.dirname(__file__), "disease_data.json")
with open(DATA_PATH, "r") as f:
    diseases = json.load(f)

def predict_disease(age, user_symptoms):
    max_match = 0
    probable_disease = None

    for disease in diseases:
        symptoms = disease["symptoms"]
        match_count = len(set(symptoms) & set(user_symptoms))
        if match_count > max_match:
            max_match = match_count
            probable_disease = disease

    if probable_disease and max_match > 0:
        age_group = "child" if age < 18 else "adult"
        return {
            "disease": probable_disease["disease"],
            "severity": probable_disease["severity"],
            "precautions": probable_disease["precautions"],
            "medicines": probable_disease["medicines"].get(age_group, probable_disease["medicines"].get("adult", []))
        }
    else:
        return {"message": "No matching disease found. Please provide more symptoms or check spelling."}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json or {}
    try:
        age = int(data.get('age', 0))
    except Exception:
        age = 0
    symptoms_input = data.get('message', '') or ''
    user_symptoms = [s.strip().lower() for s in symptoms_input.split(',') if s.strip()]
    result = predict_disease(age, user_symptoms)

    if 'disease' in result:
        response = f"Disease: {result['disease']}\nSeverity: {result['severity']}\nPrecautions:\n"
        response += "\n".join(f"- {p}" for p in result['precautions'])
        response += "\nMedicines:\n"
        response += "\n".join(f"- {m}" for m in result['medicines'])
    else:
        response = result.get('message', 'Sorry, something went wrong.')

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
