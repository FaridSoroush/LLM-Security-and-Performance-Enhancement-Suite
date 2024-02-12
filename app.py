from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "LLM Security and Performance Enhancement Suite"

# Placeholder for the actual fact-checking API URL
FACT_CHECK_URL = "https://some-fact-checking-service.com/api/check"

def check_veracity(llm_response):
    try:
        # The actual API call to the fact-checking service
        response = requests.post(FACT_CHECK_URL, json={"statement": llm_response})
        response.raise_for_status()  # Will raise an exception for HTTP error codes

        # Assuming the API returns a JSON response with a 'veracity_score' field
        # Adjust the field name based on the actual API response
        veracity_score = response.json().get("veracity_score", 0)
        return veracity_score > 0.5  # Threshold for truthfulness can be adjusted
    except requests.RequestException as e:
        # Log the exception or print it out to your console
        print(f"An error occurred: {e}")
        
        # Return a default response or handle it in a way that your app can continue
        # You might return None or False, or even raise the exception to handle it upstream
        return None

def detect_prompt_injection(input_prompt):
    suspicious_keywords = ['exploit', 'attack']
    is_suspicious = any(keyword in input_prompt for keyword in suspicious_keywords)
    return is_suspicious

def route_query(input_query):
    if "science" in input_query:
        return "ScienceModel"
    return "GeneralModel"

@app.route('/check_veracity', methods=['POST'])
def api_check_veracity():
    data = request.json
    result = check_veracity(data['text'])
    return jsonify({"is_true": result})

@app.route('/detect_injection', methods=['POST'])
def api_detect_injection():
    data = request.json
    result = detect_prompt_injection(data['text'])
    return jsonify({"is_suspicious": result})

@app.route('/route_query', methods=['POST'])
def api_route_query():
    data = request.json
    result = route_query(data['text'])
    return jsonify({"model": result})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
