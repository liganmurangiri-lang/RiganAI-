
from flask import Flask, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

HTML = "<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width, initial-scale=1'><title>RIGAN V6</title><style>*{margin:0;padding:0;box-sizing:border-box;font-family:sans-serif}body{background:#0f172a;color:#fff;display:flex;justify-content:center;height:100vh}.box{width:100%;max-width:500px;background:#1e293b;display:flex;flex-direction:column;height:100vh}.head{padding:15px;text-align:center;color:#38bdf8;font-weight:800;border-bottom:1px solid #334155}.chat{flex:1;overflow-y:auto;padding:15px;display:flex;flex-direction:column;gap:10px}.b{padding:10px 14px;border-radius:15px;max-width:85%}.u{background:#38bdf8;color:#000;align-self:flex-end}.a{background:#334155;align-self:flex-start}.in{display:flex;gap:8px;padding:10px;border-top:1px solid #334155}input{flex:1;padding:12px;border-radius:10px;border:1px solid #334155;background:#0f172a;color:#fff}button{padding:12px 18px;border-radius:10px;border:none;background:#38bdf8;font-weight:800}</style></head><body><div class='box'><div class='head'>RIGAN MARINA V6</div><div class='chat' id='c'><div class='b a'>Habari Regan! Mimi ni V6. Niulize chochote!</div></div><div class='in'><input id='i' placeholder='Andika...' onkeypress=\"if(event.key=='Enter')s()\"><button onclick='s()'>Tuma</button></div></div><script>function add(t,cl){let d=document.createElement('div');d.className='b '+cl;d.innerText=t;document.getElementById('c').appendChild(d);document.getElementById('c').scrollTop=99999}async function s(){let e=document.getElementById('i');let v=e.value.trim();if(!v)return;add(v,'u');e.value='';let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:v})});let j=await r.json();add(j.reply,'a')}</script></body></html>"

@app.route('/')
def home():
    return HTML

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    msg = data.get('message','') if data else ''
    m = msg.lower()
    now = datetime.now().strftime("%I:%M %p")
    if 'saa ngapi' in m:
        return jsonify(reply=f"Saa sasa ni {now} - Nairobi")
    if 'nani' in m:
        return jsonify(reply="Mimi ni RIGAN MARINA V6 AI ya RIGAN MARINA kutoka Kenya!")
    if 'habari' in m or 'mambo' in m:
        return jsonify(reply=f"Poa sana Regan! Saa ni {now}, niko fiti!")
    return jsonify(reply=f"Nimekuelewa: {msg} - Saa ni {now}. Mimi ni V6 niko tayari!")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
