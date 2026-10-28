
import os
import requests
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="sw">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>RIGAN MARINA V5</title>
<style>
body {
  margin: 0;
  font-family: Arial, sans-serif;
  background: #101827;
  color: white;
}
header {
  padding: 20px;
  text-align: center;
  background: #17243a;
}
header h2 { margin: 0 0 8px; }
header p { margin: 0; color: #b8c7dc; }
#chat {
  max-width: 700px;
  margin: auto;
  padding: 15px;
  height: 60vh;
  overflow-y: auto;
}
.msg {
  padding: 12px 15px;
  border-radius: 14px;
  margin: 12px 0;
  white-space: pre-wrap;
  overflow-wrap: anywhere;
  line-height: 1.5;
}
.user { background: #254a79; margin-left: 35px; }
.ai { background: #202d41; margin-right: 25px; }
#controls {
  max-width: 700px;
  margin: auto;
  padding: 12px;
  display: flex;
  gap: 8px;
}
textarea {
  flex: 1;
  resize: vertical;
  min-width: 0;
  min-height: 48px;
  padding: 12px;
  border-radius: 10px;
  border: 1px solid #52637b;
  background: #17243a;
  color: white;
  font-size: 16px;
}
button {
  border: 0;
  border-radius: 10px;
  padding: 12px 16px;
  background: #2878ee;
  color: white;
  font-size: 16px;
}
button:disabled { opacity: 0.5; }
#status {
  text-align: center;
  color: #b8c7dc;
  padding: 5px 10px 18px;
}
</style>
</head>
<body>
<header>
  <h2>RIGAN MARINA V5</h2>
  <p>Msaidizi wako wa AI</p>
</header>

<div id="chat">
  <div class="msg ai">Habari! Mimi ni RIGAN MARINA V5.
  Niulize swali lolote ili tuanze.</div>
</div>

<div id="controls">
  <textarea id="question" placeholder="Andika swali lako..."></textarea>
  <button id="send" onclick="sendMessage()">Tuma</button>
</div>
<div id="status">Tayari kuzungumza</div>

<script>
const chat = document.getElementById("chat");
const input = document.getElementById("question");
const send = document.getElementById("send");
const statusText = document.getElementById("status");
let history = [];

function addMessage(text, who) {
  const div = document.createElement("div");
  div.className = "msg " + who;
  div.textContent = text;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

async function sendMessage() {
  const message = input.value.trim();
  if (!message || send.disabled) return;

  addMessage(message, "user");
  input.value = "";
  send.disabled = true;
  statusText.textContent = "RIGAN inafikiria...";

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        message: message,
        history: history
      })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Kuna hitilafu.");
    }

    addMessage(data.reply, "ai");
    history.push(
      {role: "user", content: message},
      {role: "assistant", content: data.reply}
    );
    history = history.slice(-20);
    statusText.textContent = "RIGAN iko tayari";
  } catch (error) {
    addMessage("Samahani: " + error.message, "ai");
    statusText.textContent = "Jaribu tena";
  } finally {
    send.disabled = false;
    input.focus();
  }
}

input.addEventListener("keydown", function(event) {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    sendMessage();
  }
});
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/health")
def health():
    return jsonify({"status": "ok", "app": "RIGAN MARINA V5"})

@app.route("/chat", methods=["POST"])
def chat():
    body = request.get_json(silent=True) or {}
    message = str(body.get("message", "")).strip()

    if not message:
        return jsonify({"error": "Tafadhali andika swali."}), 400

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return jsonify({
            "error": "OPENAI_API_KEY haijawekwa kwenye Render Environment."
        }), 500

    messages = [{
        "role": "system",
        "content": (
            "You are RIGAN MARINA V5, a helpful AI assistant. "
            "Answer the user's actual question directly and accurately. "
            "Give clear explanations and examples when useful. "
            "Respond in the language used by the user, including Swahili. "
            "Do not merely repeat the user's question."
        )
    }]

    history = body.get("history", [])
    if isinstance(history, list):
        for item in history[-20:]:
            if not isinstance(item, dict):
                continue
            role = item.get("role")
            content = item.get("content")
            if role in ("user", "assistant") and isinstance(content, str):
                messages.append({
                    "role": role,
                    "content": content[:8000]
                })

    messages.append({"role": "user", "content": message})

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": "Bearer " + api_key,
                "Content-Type": "application/json"
            },
            json={
                "model": os.environ.get(
                    "OPENAI_MODEL", "gpt-4o-mini"
                ),
                "messages": messages,
                "temperature": 0.7
            },
            timeout=60
        )

        if not response.ok:
            print("OpenAI API error:", response.status_code, response.text[:1000])
            if response.status_code == 401:
                error = "API key haikubalika. Kagua key kwenye Render."
            elif response.status_code == 429:
                error = "API imekataa ombi. Kagua salio, matumizi au kikomo cha API."
            else:
                error = "Huduma ya AI imeleta hitilafu. Kagua Render Logs."
            return jsonify({"error": error}), 502

        data = response.json()
        reply = data["choices"][0]["message"]["content"].strip()

        if not reply:
            raise ValueError("Jibu lilikuwa tupu")

        return jsonify({"reply": reply})

    except requests.exceptions.Timeout:
        return jsonify({
            "error": "AI imechelewa kujibu. Tafadhali jaribu tena."
        }), 504
    except requests.exceptions.RequestException:
        app.logger.exception("Tatizo la muunganisho wa AI")
        return jsonify({
            "error": "Imeshindikana kuwasiliana na huduma ya AI."
        }), 502
    except (KeyError, IndexError, ValueError):
        app.logger.exception("Jibu la AI halikutarajiwa")
        return jsonify({
            "error": "Jibu la AI halikuweza kusomwa."
        }), 502

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
