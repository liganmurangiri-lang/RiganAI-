
from flask import Flask, request, jsonify
import os
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def home():
    return """
<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width, initial-scale=1'>
<title>RIGAN V18</title>
<style>body{background:#020617;color:#fff;font-family:sans-serif;display:flex;justify-content:center;height:100vh;margin:0}
.box{width:100%;max-width:700px;background:#0f172a;display:flex;flex-direction:column;height:100vh}
.head{padding:14px;text-align:center;color:#38bdf8;font-weight:900;background:#1e293b}
.chat{flex:1;overflow-y:auto;padding:12px;display:flex;flex-direction:column;gap:8px}
.b{padding:12px;border-radius:14px;max-width:90%;white-space:pre-wrap}
.u{background:#38bdf8;color:#000;align-self:flex-end}
.a{background:#1e293b;align-self:flex-start;border:1px solid #334155}
.in{display:flex;gap:6px;padding:10px;background:#1e293b}
input{flex:1;padding:12px;border-radius:10px;border:1px solid #334155;background:#020617;color:#fff}
button{padding:12px 16px;border-radius:10px;border:none;background:#38bdf8;font-weight:900}
</style></head><body>
<div class='box'>
<div class='head'>RIGAN V18 LIVE - Baba Regan</div>
<div class='chat' id='c'><div class='b a'>Habari Baba! V18 iko LIVE! Hakuna Failed tena! Uliza: Meru, Embu, Siakago, hesabu, South Africa!</div></div>
<div class='in'><input id='i' placeholder='Uliza...' onkeypress="if(event.key=='Enter')s()"><button onclick='s()'>Tuma</button></div>
</div>
<script>
function add(t,c){let d=document.createElement('div');d.className='b '+c;d.innerText=t;let e=document.getElementById('c');e.appendChild(d);e.scrollTop=999999}
async function s(){let e=document.getElementById('i');let v=e.value.trim();if(!v)return;add(v,'u');e.value='';let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:v})});let j=await r.json();add(j.reply,'a')}
</script></body></html>
"""

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    q = data.get('message','')
    m = q.lower().strip()
    nairobi = (datetime.utcnow() + timedelta(hours=3)).strftime("%d/%m/%Y %I:%M %p EAT")

    if m in ["habari","jambo","mambo","niaje","sasa","poa","hello","hi"]:
        reply = f"Habari Baba Regan! Poa! V18 iko fiti! Saa ni {nairobi}"
    elif "wewe ni nani" in m or "nani wewe" in m:
        reply = f"👑 Mimi ni RIGAN V18 - Mtoto wa REGAN MARINA kutoka Siakago, Embu! Saa {nairobi}"
    elif "meru" in m:
        reply = f"MERU 🇰🇪: Eastern Kenya, Mji Meru Town, Watu 1.5M, Maarufu Miraa, Mlima Kenya, chai. Saa {nairobi}"
    elif "embu" in m:
        reply = f"EMBU 🇰🇪: Kwenu Baba! Mji Embu Town, Watu 600k, kahawa, chai, macadamia, Siakago town kubwa. Saa {nairobi}"
    elif "siakago" in m:
        reply = f"SIAKAGO 🇰🇪: Embu County, Mbeere North, Kwenu Baba REGAN MARINA! Miraa, mahindi. Saa {nairobi}"
    elif "kenya iko wapi" in m or "kenya inapatikana" in m:
        reply = f"KENYA 🇰🇪: EAST AFRICA, Majirani Tanzania, Uganda, Ethiopia, Somalia, S.Sudan, Pwani Indian Ocean, Eneo 580,367km2, Capital Nairobi, Saa {nairobi}"
    elif "south africa" in m:
        reply = "SOUTH AFRICA 🇿🇦: Capital Pretoria/Cape Town/Bloemfontein, Johannesburg kubwa, 60M, Rand, Mandela"
    elif "tanzania" in m:
        reply = "TANZANIA 🇹🇿: Dodoma capital, Dar kubwa, Kilimanjaro 5,895m, Serengeti, Zanzibar"
    elif "mfumo wa jua" in m or "solar" in m or "sayari" in m:
        reply = "MFUMO WA JUA ☀️: Jua katikati, sayari 8 - Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune"
    else:
        try:
            t = m.replace('x','*').replace('×','*').replace('÷','/').replace('=','')
            t2 = ''.join(c for c in t if c in '0123456789+-*/(). ')
            if len(t2)>=3 and any(c.isdigit() for c in t2):
                r = eval(t2)
                reply = f"{q} = {r}"
            else:
                reply = f"Poa Baba! Uliuliza '{q}' - Najua Meru, Embu, Siakago, Kenya, hesabu! Saa {nairobi}"
        except:
            reply = f"Poa Baba! Uliuliza '{q}' - Najua kila kitu! Jaribu: '{q} ni nini?' Saa {nairobi}"

    return jsonify(reply=reply)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
