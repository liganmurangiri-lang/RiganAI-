
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

HTML = """<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1"><title>RIGAN MARINA V5</title><style>
*{margin:0;padding:0;box-sizing:border-box;font-family:Inter,sans-serif}
body{background:#0f172a;color:#e2e8f0;display:flex;justify-content:center;height:100vh}
.box{width:100%;max-width:500px;background:#1e293b;display:flex;flex-direction:column;height:100vh}
.header{padding:18px;text-align:center;background:#1e293b;border-bottom:1px solid #334155;font-weight:700;font-size:18px;color:#38bdf8}
.chat{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:12px}
.bubble{padding:12px 16px;border-radius:18px;max-width:85%;line-height:1.5;font-size:14px}
.user{background:#38bdf8;color:#000;align-self:flex-end;border-bottom-right-radius:4px}
.ai{background:#334155;color:#fff;align-self:flex-start;border-bottom-left-radius:4px}
.input-area{display:flex;gap:10px;padding:14px;background:#1e293b;border-top:1px solid #334155}
input{flex:1;padding:14px;border-radius:12px;border:1px solid #334155;background:#0f172a;color:#fff;outline:none}
button{padding:14px 18px;border-radius:12px;border:none;background:#38bdf8;color:#000;font-weight:700;cursor:pointer}
</style></head><body>
<div class="box"><div class="header">RIGAN MARINA V5<br><span style="font-size:12px;color:#94a3b8">Msaidizi wako wa AI</span></div>
<div class="chat" id="chat"><div class="bubble ai">Habari! Mimi ni RIGAN MARINA V5. Niulize swali lolote ili tuanze.</div></div>
<div class="input-area"><input id="inp" placeholder="Andika swali lako..." onkeypress="if(event.key==='Enter')send()"><button onclick="send()">Tuma</button></div></div>
<script>
function add(t,c){let d=document.createElement('div');d.className='bubble '+c;d.innerText=t;document.getElementById('chat').appendChild(d);document.getElementById('chat').scrollTop=99999}
async function send(){let i=document.getElementById('inp');let v=i.value.trim();if(!v)return;add(v,'user');i.value='';let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:v})});let j=await r.json();add(j.reply,'ai')}
</script></body></html>"""

def get_ai_reply(msg):
    m = msg.lower()
    if "habari" in m or "mambo" in m or "poa" in m:
        return "Poa sana Regan! Mimi ni RIGAN MARINA V5, niko fiti sana. Unataka nikusaidie nini leo?"
    elif "nani wewe" in m or "wewe ni nani" in m:
        return "Mimi ni RIGAN MARINA V5 AI iliyotengenezwa na RIGAN MARINA. Niko hapa kukusaidia kama ChatGPT!"
    elif "kenya" in m:
        return "Kenya ni nchi ya Afrika Mashariki. Nairobi ndio mji mkuu!"
    elif "code" in m or "tengeneza" in m or "jenga" in m:
        return f"Naweza kukutengenezea! Umeomba: '{msg}'. Niambie unataka website, app, au bot?"
    else:
        return f"Nimekuelewa: '{msg}' - Mimi ni RIGAN MARINA V5, niko tayari kukusaidia!"

@app.route('/')
def home():
    return HTML

@app.route('/chat', methods=['POST'])
def chat():
    msg = request.get_json().get('message','')
    return jsonify({"reply": get_ai_reply(msg)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT",10000)))
