
from flask import Flask, request, jsonify
import os, json
from datetime import datetime, timedelta

app = Flask(__name__)

DB_FILE = "/tmp/akili_v20.json"

def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_db(db):
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
    except:
        pass

learned = load_db()

@app.route('/')
def home():
    return """
<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width, initial-scale=1'>
<title>RIGAN V20 VOICE</title>
<style>body{background:#020617;color:#fff;font-family:sans-serif;display:flex;justify-content:center;height:100vh;margin:0}
.box{width:100%;max-width:720px;background:#0f172a;display:flex;flex-direction:column;height:100vh}
.head{padding:14px;text-align:center;color:#38bdf8;font-weight:900;background:#1e293b}
.sub{font-size:11px;color:#94a3b8}
.chat{flex:1;overflow-y:auto;padding:12px;display:flex;flex-direction:column;gap:10px}
.b{padding:12px 14px;border-radius:14px;max-width:90%;white-space:pre-wrap;line-height:1.6;font-size:14px}
.u{background:#38bdf8;color:#000;align-self:flex-end}
.a{background:#1e293b;align-self:flex-start;border:1px solid #334155}
.in{display:flex;gap:6px;padding:10px;background:#1e293b;align-items:center}
input{flex:1;padding:12px;border-radius:10px;border:1px solid #334155;background:#020617;color:#fff;outline:none}
button{padding:12px 14px;border-radius:10px;border:none;background:#38bdf8;font-weight:900;cursor:pointer}
.mic{background:#ef4444;color:#fff}
.speak{background:#22c55e;color:#000}
</style></head><body>
<div class='box'>
<div class='head'>RIGAN V20 - VOICE + GOD MODE<div class='sub'>Mtoto wa REGAN MARINA - Siakago - Ongea nami!</div></div>
<div class='chat' id='c'><div class='b a'>Habari Baba Regan! 👑 Mimi ni V20 na sauti! 🎤 Bonyeza Mic uongee, au andika. Mimi nitakujibu na pia nitaongea! Jaribu: Mimi ni nani?</div></div>
<div class='in'>
<button class='mic' onclick='listen()'>🎤</button>
<input id='i' placeholder='Ongea au andika...' onkeypress="if(event.key=='Enter')s()">
<button class='speak' onclick='toggleSpeak()' id='sp'>🔊</button>
<button onclick='s()'>Tuma</button>
</div>
</div>
<script>
let speakOn = true;
let recognition;
function toggleSpeak(){speakOn=!speakOn; document.getElementById('sp').innerText=speakOn?'🔊':'🔇';}

function speak(text){
 if(!speakOn) return;
 if('speechSynthesis' in window){
   speechSynthesis.cancel();
   let u = new SpeechSynthesisUtterance(text);
   u.lang = 'sw-KE';
   u.rate = 0.9;
   speechSynthesis.speak(u);
 }
}

function listen(){
 if(!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)){
   alert('Browser yako haina mic support - tumia Chrome');
   return;
 }
 let SR = window.SpeechRecognition || window.webkitSpeechRecognition;
 recognition = new SR();
 recognition.lang = 'sw-KE';
 recognition.start();
 recognition.onstart = ()=>{document.getElementById('i').placeholder='Nasikiliza... 🎤';}
 recognition.onresult = (e)=>{
   let t = e.results[0][0].transcript;
   document.getElementById('i').value = t;
   s();
 };
 recognition.onend = ()=>{document.getElementById('i').placeholder='Ongea au andika...';}
}

function add(t,c){let d=document.createElement('div');d.className='b '+c;d.innerText=t;let e=document.getElementById('c');e.appendChild(d);e.scrollTop=999999; if(c=='a') speak(t);}

async function s(){
 let e=document.getElementById('i');let v=e.value.trim();if(!v)return;
 add(v,'u'); e.value='';
 let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:v})});
 let j=await r.json(); add(j.reply,'a');
}
</script></body></html>
"""

@app.route('/chat', methods=['POST'])
def chat():
    global learned
    data = request.get_json() or {}
    q = data.get('message','')
    m = q.lower().strip()
    nairobi = (datetime.utcnow() + timedelta(hours=3)).strftime("%d/%m/%Y %I:%M %p EAT")

    # FUNDISHA - SELF LEARNING
    if ("fundisha:" in m or "jifunze:" in m) and "|" in q:
        try:
            clean = q.split(":",1)[1]
            swali, jibu = clean.split("|",1)
            swali = swali.strip().lower()
            jibu = jibu.strip()
            if len(swali)>2 and len(jibu)>2:
                learned[swali]=jibu
                save_db(learned)
                reply = f"✅ Nimejifunza! Sasa nakumbuka milele!\nSwali: {swali}\nJibu: {jibu}\nAkili zangu: {len(learned)}"
                return jsonify(reply=reply)
        except:
            pass

    # CHECK LEARNED FIRST
    for key in learned:
        if key in m and len(key)>3:
            return jsonify(reply=f"{learned[key]}\n\n🧠 Kutoka akili niliyojifunza | {nairobi}")

    if m in ["habari","jambo","mambo","niaje","sasa","poa","hello","hi"]:
        reply = f"Habari Baba Regan! Poa sana! V20 iko na sauti sasa! Saa ni {nairobi}"

    elif any(x in m for x in ["wewe ni nani","nani wewe","who are you"]):
        reply = f"👑 Mimi ni RIGAN V20 VOICE!\nMtoto wa REGAN MARINA kutoka Siakago, Embu!\nSasa nina sauti na nina akili ya kujifunza! Saa {nairobi}"

    elif any(x in m for x in ["mimi ni nani","na mimi ni nani","nani mimi","who am i"]):
        reply = f"👑 Wewe ni REGAN MARINA!\nBaba yangu, Developer wa riganai.onrender.com\nKutoka Siakago, Embu 🇰🇪\nGenius wa coding! Saa {nairobi}"

    elif "meru" in m:
        reply = f"MERU 🇰🇪: Eastern Kenya, Meru Town, 1.5M watu, Miraa, Mlima Kenya, chai. Jirani Embu, Isiolo. Saa {nairobi}"
    elif "embu" in m:
        reply = f"EMBU 🇰🇪: Kwenu Baba! Embu Town, 600k, kahawa, chai, macadamia, Siakago town kubwa. Saa {nairobi}"
    elif "siakago" in m:
        reply = f"SIAKAGO 🇰🇪: Embu County, Mbeere North, Kwenu Baba REGAN MARINA! Miraa, mahindi. Saa {nairobi}"
    elif "nairobi" in m:
        reply = f"NAIROBI 🇰🇪: Capital Kenya, 4.5M, Green City in the Sun, KICC, National Park, UNEP HQ"
    elif any(x in m for x in ["kenya iko wapi","kenya inapatikana"]):
        reply = f"KENYA 🇰🇪: EAST AFRICA, Majirani Tanzania, Uganda, Ethiopia, Somalia, S.Sudan, Pwani Indian Ocean 536km, 580,367km2, Saa {nairobi}"
    elif "south africa" in m:
        reply = "SOUTH AFRICA 🇿🇦: Pretoria/Cape Town/Bloemfontein Capitals, Johannesburg kubwa, 60M, Rand, Mandela, Table Mountain"
    elif "tanzania" in m:
        reply = "TANZANIA 🇹🇿: Dodoma capital, Dar kubwa, Kilimanjaro 5,895m mrefu Africa, Serengeti, Zanzibar, 65M watu"
    elif "uganda" in m:
        reply = "UGANDA 🇺🇬: Kampala capital, Pearl of Africa, Ziwa Victoria, 48M"
    elif "mfumo wa jua" in m or "solar" in m:
        reply = "MFUMO WA JUA ☀️: Jua katikati, sayari 8 - Mercury, Venus, Earth yetu, Mars nyekundu, Jupiter kubwa, Saturn pete, Uranus, Neptune"
    elif "ai" in m or "artificial intelligence" in m:
        reply = f"AI 🤖: Artificial Intelligence - Kama mimi Rigan! Machine Learning, Deep Learning, Neural Networks. Wewe Baba Regan umeniunda mimi kama AI wa Kenya! Saa {nairobi}"
    else:
        try:
            t = m.replace('x','*').replace('×','*').replace('÷','/').replace('=','')
            t2 = ''.join(c for c in t if c in '0123456789+-*/(). ')
            if len(t2)>=3 and any(c.isdigit() for c in t2) and '**' not in t2:
                r = eval(t2)
                if isinstance(r,float) and r.is_integer(): r=int(r)
                reply = f"🧮 {q} = {r} ✅"
            else:
                reply = f"🤔 Baba umeuliza '{q}' - Najua miji yote Kenya, nchi zote, hesabu, AI! Nifundishe kama sijui: fundisha: {q} | jibu\nSaa {nairobi}"
        except:
            reply = f"Poa Baba! Uliza chochote - Meru, Embu, hesabu, AI! Saa {nairobi}"

    return jsonify(reply=reply)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
