import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-1.0-pro')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/impressum')
def impressum():
    return render_template('impressum.html')

@app.route('/datenschutz')
def datenschutz():
    return render_template('datenschutz.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/agb')
def agb():
    return render_template('agb.html')

@app.route('/find_consultants', methods=['POST'])
def find_consultants():
    try:
        # Get form data
        needs = request.form.get('needs')
        industry = request.form.get('industry')
        consulting_field = request.form.get('consulting_field')
        location = request.form.get('location', 'München')

        # Construct prompt for the Gemini API
        search_prompt = f"""Du bist ein Experte für Unternehmensberatungen in Deutschland. Finde 5 real existierende Beratungsfirmen in {location}, die folgende Kriterien erfüllen:
        - Geschäftliche Anforderungen: {needs}
        - Branche: {industry}
        - Beratungsfeld: {consulting_field}

        WICHTIG: Gib deine Antwort AUSSCHLIESSLICH als valides JSON zurück. Kein zusätzlicher Text davor oder danach.
        Verwende exakt diese JSON-Struktur:

        {{
            "firms": [
                {{
                    "name": "Name der Beratungsfirma",
                    "website": "https://www.firma-website.de",
                    "reasoning": "Begründung warum diese Firma passt"
                }}
            ]
        }}

        Beachte:
        1. Stelle sicher, dass die Firmen wirklich existieren
        2. Die Website-URLs müssen korrekt und vollständig sein (mit https://)
        3. Begründe kurz und präzise, warum die Firma zu den Anforderungen passt
        4. Gib NUR das JSON zurück, keinen weiteren Text
        5. Verwende keine Markdown-Formatierung oder Codeblöcke"""

        # Get response from Gemini
        response = model.generate_content(search_prompt)
        
        # Clean up and parse the response as JSON
        try:
            # Get the response text and clean it up
            response_text = response.text.strip()
            
            # Extract everything between the first { and last }
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start != -1 and end != 0:
                response_text = response_text[start:end]
            
            print(f"Cleaned response text: {response_text}")
            
            # Parse as JSON
            result = json.loads(response_text)
            if "firms" in result and isinstance(result["firms"], list):
                print(f"Successfully parsed JSON: {json.dumps(result, indent=2)}")
                return jsonify(result)
            else:
                print(f"Invalid JSON structure. Content: {result}")
                return jsonify({"error": "Ungültige JSON-Struktur in der Antwort"}), 500
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {str(e)}")
            print(f"Content that failed to parse: {response_text}")
            return jsonify({"error": "Fehler beim JSON-Parsing"}), 500

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)