from flask import Flask, request, jsonify
import os
import datetime

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>RiganAI - RIGAN MARINA</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:sans-serif}
body{background:#0a0a0f;color:white;height:100vh;display:flex;flex-direction:column}
header{padding:15px;background:#15151f;border-bottom:1px solid #2a2a3a;display:flex;justify-content:space-between;align-items:center}
.logo{font-weight:900;font-size:20px;letter-spacing:1px}
.logo span{color:#7c3aed}
.status{font-size:12px;background:#10b98120;color:#10b981;padding:5px 10px;border-radius:20px}
.chat{flex:1;overflow-y:auto;padding:20px;display:flex;flex-direction:column;gap:15px}
.msg{max-width:80%;padding:12px 16px;border-radius:18px;line-height:1.5;font-size:15px}
.user{align-self:flex-end;background:#7c3aed}
.ai{align-self:flex-start;background:#1e1e2e;border:1px solid #2a2a3a}
.input-area{padding:15px;background:#15151f;border-top:1px solid #2a2a3a;display:flex;gap:10px}
input{flex:1;background:#0a0a0f;border:1px solid #2a2a3a;padding:14px;border-radius:25px;color:white;outline:none}
button{background:#7c3aed;border:none;color:white;padding:14px 22px;border-radius:25px;font-weight:bold}
h2{margin:50px auto 10px;color:#666}
p.sub{margin:0 auto 20px;color:#444;font-size:13px}
</style>
</head>
<body>
<header>
<div class="logo">RIGAN <span>MARINA</span> V4</div>
<div class="status">● ONLINE</div>
</header>
<div class="chat" id="chat">
<h2>Poa Regan! 👋</h2>
<p class="sub">Mimi ni RiganAI, niko tayari kukusaidia</p>
<div class="msg ai">Mambo Regan! Karibu RiganAI. Niulize chochote! 🔥</div>
</div>
<div class="input-area">
<input id="inp" placeholder="Andika ujumbe hapa..." onkeypress="if(event.key==='Enter')send()">
<button onclick="send()">Tuma</button>
</div>
<script>
function addMsg(t,c){let d=document.createElement('div');d.className='msg '+c;d.innerText=t;document.getElementById('chat').appendChild(d);document.getElementById('chat').scrollTop=99999}
async function send(){
 let i=document.getElementById('inp');let txt=i.value.trim();if(!txt)return;
 addMsg(txt,'user');i.value='';
 let res=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:txt})});
 let data=await res.json();addMsg(data.reply,'ai');
}
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return HTML

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    msg = data.get('message','').lower()
    
    if 'mambo' in msg or 'poa' in msg:
        reply = "Poa sana Regan! 🔥 RiganAI iko fiti, iko ONLINE 24/7. Unataka tufanye nini leo?"
    elif 'nani' in msg and 'wewe' in msg:
        reply = "Mimi ni RiganAI, AI iliyotengenezwa na RIGAN MARINA. Niko hapa kukusaidia coding, biashara, na mawazo yote!"
    elif 'render' in msg or 'deploy' in msg:
        reply = "Tayari tume-deploy! Link yako ni riganai.onrender.com na iko Live 🟢"
    elif 'saa' in msg or 'muda' in msg:
        reply = f"Saa sasa ni {datetime.datetime.now().strftime('%H:%M')} - RiganAI iko macho!"
    else:
        reply = f"Nice! Umesema: '{data.get('message')}'. Mimi RiganAI niko tayari kukujengea chochote unachotaka. Niambie idea yako next! 🚀"

    return jsonify({"reply": reply})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
