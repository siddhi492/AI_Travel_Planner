import os
import json
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# ---------------- LOAD ENV ----------------
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# ---------------- APP SETUP ----------------
app = Flask(__name__)
CORS(app)

# ---------------- AI PROMPT ----------------
SYSTEM_PROMPT = """
You are a professional AI travel planner.

STRICT RULES:
1. Respond ONLY with valid JSON
2. Do NOT include any explanation, markdown, or text
3. JSON must strictly follow the schema
4. NEVER omit any key
5. Arrays must have 3 or more items

JSON SCHEMA:
{
  "plans": [
    {
      "planId": number,
      "transportCost": number,
      "totalCost": number,
      "budgetWarning": boolean,
      "days": [
        {
          "day": number,
          "spots": [string, string, string],
          "restaurants": [string, string, string],
          "stay": [string, string, string],
          "dayCost": number
        }
      ]
    }
  ]
}
"""

# ---------------- ROUTE ----------------
@app.route("/plan", methods=["POST"])
def generate_plan():
    try:
        data = request.json

        from_city = data.get("from_city")
        to_city = data.get("to_city")
        days = int(data.get("days"))
        budget = int(data.get("budget"))
        transport_mode = data.get("transport_mode")

        user_prompt = f"""
Create 5 different travel plans.

From city: {from_city}
To city: {to_city}
Number of days: {days}
Total budget: ₹{budget}
Transport mode: {transport_mode}

Each plan MUST include:
- Attractions
- Temples
- Shopping areas
- Food experiences
- Nature places

Cost breakup:
- Transport cost
- Hotel stay
- Food
- Local travel

If budget exceeds, set budgetWarning true.

Return ONLY JSON.
"""

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.4
            },
            timeout=60
        )

        # ---------------- SAFE PARSING ----------------
        raw = response.json()["choices"][0]["message"]["content"]

        start = raw.find("{")
        end = raw.rfind("}") + 1
        clean_json = raw[start:end]

        ai_data = json.loads(clean_json)

        return jsonify({"plans": ai_data["plans"]})

    except Exception as e:
        print("BACKEND ERROR:", e)
        return jsonify({"error": "AI processing failed"}), 500


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
