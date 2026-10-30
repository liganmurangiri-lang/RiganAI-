python
from flask import Flask, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

HTML = """<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1"><title>RIGAN MARINA V6</title><style>*{margin:0;padding:0;box-sizing:border-box;font-family:sans-serif}body{background:#0f172a;color:#e2e8f0;display:flex;justify-content:center;height:100vh}.box{width:100%;max-width:550px;background:#1e293b;display:flex;flex-direction:column;height:100vh}.header{padding:16px;text-align:center;border-bottom:1px solid #334155;font-weight:800;font-size:19px;color:#38bdf8}.chat{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:12px}.bubble{padding:12px 16px;border-radius:18px;max-width:88%;line-height:1.6;font-size:14px;white-space:pre-wrap}.user{background:#38bdf8;color:#000;align-self:flex-end;border-bottom-right-radius:4px}.ai{background:#334155;color:#fff;align-self:flex-start;border-bottom-left-radius:4px}.input-area{display:flex;gap:10px;padding:12px;border-top:1px solid #334155}input{flex:1;padding:14px;border-radius:12px;border:1px solid #334155;background:#0f172a;color:#fff;outline:none}button{padding:14px 20px;border-radius:12px;border:none;background:#38bdf8;color:#000;font-weight:800}</style></head><body><div class="box"><div class="header">RIGAN MARINA V6</div><div class="chat" id="chat"><div class="bubble ai">Habari Regan! Mimi ni RIGAN MARINA V6 - Smart AI. Niulize chochote!</div></div><div class="input-area"><input id="inp" placeholder="Andika hapa..." onkeypress="if(event.key==='Enter')send()"><button onclick="send()">Tuma</button></div></div><script>function add(t,c){let d=document.createElement('div');d.className='bubble '+c;d.innerText=t;document.getElementById('chat').appendChild(d);document.getElementById('chat').scrollTop=99999}async function send(){let i=document.getElementById('inp');let v=i.value.trim();if(!v)return;add(v,'user');i.value='';let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:v})});let j=await r.json();add(j.reply,'ai')}</script></body></html>"""

def get_ai_reply(msg):
    now = datetime.now()
    saa = now.strftime("%I:%M %p")
    m = msg.lower().strip()
    if "saa ngapi" in m:
        return f"Saa sasa hivi Kenya ni {saa} - Nairobi Time"
    if "habari" in m:
        return f"Poa sana Regan! Saa ni {saa}. Mimi ni RIGAN MARINA V6, niko fiti sana!"
    if "nani" in m:
        return "Mimi ni RIGAN MARINA V6 AI iliyotengenezwa na RIGAN MARINA kutoka Kenya. Niko kama ChatGPT, niko hapa kukusaidia na kila kitu!"
    if "kenya" in m:
        return f"Kenya ni nchi ya Afrika Mashariki. Capital ni Nairobi. Saa sasa ni {saa}"
    if "tengeneza" in m or "code" in m:
        return f"Niko tayari! Umeomba: '{msg}' - Niambie ni website, app, au bot?"
    return f"Poa! Nimekuelewa: '{msg}' - Mimi ni RIGAN MARINA V6, Saa ni {saa}. Niko tayari!"

@app.route('/')
def home(): return HTML
@app.route('/chat', methods=['POST'])
def chat():
    msg = request.get_json().get('message','')
    return jsonify({"reply": get_ai_reply(msg)})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT",10000)))
