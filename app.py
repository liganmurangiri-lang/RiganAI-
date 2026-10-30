
from flask import Flask, request, jsonify
import os
import json
import urllib.request
import urllib.error

app = Flask(__name__)

DB_FILE = "akili.json"
API_KEY = os.environ.get("OPENAI_API_KEY")

def load_db():
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"maarifa": []}

def save_db(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

@app.route("/")
def home():
    return "RIGAN AI V14 iko tayari!"

@app.route("/chat", methods=["POST"])
@app.route("/ask", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message") or data.get("question") or ""

    if not message:
        return jsonify({"reply": "Andika swali kwanza."})

    db = load_db()

    if message.lower().startswith("nifundishe"):
        maarifa = message[len("nifundishe"):].strip(" :|")
        if maarifa:
            db["maarifa"].append(maarifa)
            save_db(db)
            return jsonify({"reply": "Nimejifunza na kuhifadhi maarifa hayo!"})

        return jsonify({"reply": "Niambie unataka kunifundisha nini."})

    if not API_KEY:
        return jsonify({"reply": "OPENAI_API_KEY haijapatikana. Weka API Key kwenye Environment Variables."})

    knowledge = "\n".join(db["maarifa"][-100:])

    prompt = (
        "Wewe ni RIGAN AI, msaidizi mwenye akili. "
        "Jibu kwa Kiswahili au lugha anayotumia mtumiaji. "
        "Tumia maarifa haya yaliyofundishwa pale yanapohusika:\n"
        + knowledge
    )

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": message}
        ]
    }

    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": "Bearer " + API_KEY,
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))

        answer = result["choices"][0]["message"]["content"]
        return jsonify({"reply": answer})

    except urllib.error.HTTPError as e:
        error = e.read().decode("utf-8")
        return jsonify({"reply": "API ERROR: " + error}), 500

    except Exception as e:
        return jsonify({"reply": "Kuna tatizo: " + str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
        
