from flask import Flask, request, jsonify
import os, datetime
app = Flask(__name__)
HTML = """<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1"><title>RiganAI</title><style>*{margin:0;padding:0;box-sizing:border-box;font-family:sans-serif}body{background:#0a0a0f;color:#fff;height:100vh;display:flex;flex-direction:column}header{padding:15px;background:#15151f;border-bottom:1px solid #2a2a3a;display:flex;justify-content:space-between} .logo{font-weight:900} .logo span{color:#7c3aed} .status{font-size:12px;background:#10b98120;color:#10b981;padding:5px 10px;border-radius:20px} .chat{flex:1;overflow-y:auto;padding:20px;display:flex;flex-direction:column;gap:15px} .msg{max-width:80%;padding:12px 16px;border-radius:18px;font-size:15px} .user{align-self:flex-end;background:#7c3aed} .ai{align-self:flex-start;background:#1e1e2e;border:1px solid #2a2a3a} .input-area{padding:15px;background:#15151f;display:flex;gap:10px} input{flex:1;background:#0a0a0f;border:1px solid #2a2a3a;padding:14px;border-radius:25px;color:#fff;outline:none} button{background:#7c3aed;border:none;color:#fff;padding:14px 22px;border-radius:25px;font-weight:bold}</style></head><body><header><div class="logo">RIGAN <span>MARINA</span> V4</div><div class="status">● ONLINE</div></header><div class="chat" id="chat"><div class="msg ai">Mambo Regan! Karibu RiganAI. Niulize chochote! 🔥</div></div><div class="input-area"><input id="inp" placeholder="Andika ujumbe..." onkeypress="if(event.key==='Enter')send()"><button onclick="send()">Tuma</button></div><script>function addMsg(t,c){let d=document.createElement('div');d.className='msg '+c;d.innerText=t;document.getElementById('chat').appendChild(d);document.getElementById('chat').scrollTop=99999}async function send(){let i=document.getElementById('inp');let txt=i.value.trim();if(!txt)return;addMsg(txt,'user');i.value='';let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:txt})});let d=await r.json();addMsg(d.reply,'ai');}</script></body></html>"""
@app.route('/')
def home(): return HTML
@app.route('/chat', methods=['POST'])
def chat():
 m=request.get_json().get('message','').lower()
 if 'mambo' in m or 'poa' in m: r="Poa sana Regan! 🔥 RiganAI iko fiti, iko ONLINE 24/7."
 elif 'nani' in m: r="Mimi ni RiganAI, AI ya RIGAN MARINA. Niko hapa kukusaidia!"
 else: r=f"Umesema: {request.get_json().get('message')}. Niko tayari kukujengea chochote! 🚀"
 return jsonify({"reply":r})
if __name__ == '__main__': app.run(host='0.0.0.0', port=int(os.environ.get("PORT",10000)))
