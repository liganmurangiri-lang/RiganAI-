
from flask import Flask, request, jsonify
import os, json, urllib.parse
from datetime import datetime, timedelta

app = Flask(__name__)

DB_FILE = "/tmp/akili_v21.json"

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
<title>RIGAN V21 ULTIMATE</title>
<style>body{background:#020617;color:#fff;font-family:sans-serif;display:flex;justify-content:center;height:100vh;margin:0}
.box{width:100%;max-width:720px;background:#0f172a;display:flex;flex-direction:column;height:100vh}
.head{padding:14px;text-align:center;color:#38bdf8;font-weight:900;background:#1e293b}
.sub{font-size:10px;color:#94a3b8}
.chat{flex:1;overflow-y:auto;padding:12px;display:flex;flex-direction:column;gap:10px}
.b{padding:12px 14px;border-radius:14px;max-width:90%;white-space:pre-wrap;line-height:1.6;font-size:14px}
.u{background:#38bdf8;color:#000;align-self:flex-end}
.a{background:#1e293b;align-self:flex-start;border:1px solid #334155}
.b img{width:100%;border-radius:10px;margin-top:8px}
.in{display:flex;gap:6px;padding:10px;background:#1e293b;align-items:center}
input{flex:1;padding:12px;border-radius:10px;border:1px solid #334155;background:#020617;color:#fff;outline:none}
button{padding:12px 14px;border-radius:10px;border:none;background:#38bdf8;font-weight:900;cursor:pointer}
.mic{background:#ef4444;color:#fff}
.speak{background:#22c55e;color:#000}
</style></head><body>
<div class='box'>
<div class='head'>RIGAN V21 ULTIMATE<div class='sub'>Mtoto wa REGAN MARINA - Picha + Sauti + Akili - Siakago</div></div>
<div class='chat' id='c'><div class='b a'>Habari Baba Regan! 👑 V21 ULTIMATE iko LIVE!
🎤 Sauti - Bonyeza mic uongee
🖼️ Picha - Andika: picha ya Meru / picha ya lion
🧠 Nifundishe: fundisha: swali | jibu
🌍 Lugha: Kikuyu, Luo, Kalenjin
Jaribu: "picha ya Siakago" au "Mimi ni nani"</div></div>
<div class='in'>
<button class='mic' onclick='listen()'>🎤</button>
<input id='i' placeholder='Ongea, andika, au omba picha...' onkeypress="if(event.key=='Enter')s()">
<button class='speak' onclick='toggleSpeak()' id='sp'>🔊</button>
<button onclick='s()'>Tuma</button>
</div>
</div>
<script>
let speakOn = true;
function toggleSpeak(){speakOn=!speakOn; document.getElementById('sp').innerText=speakOn?'🔊':'🔇';}
function speak(text){
 if(!speakOn) return;
 if('speechSynthesis' in window){
   speechSynthesis.cancel();
   let clean = text.replace(/https?:\\/\\/[^\\s]+/g,'').substring(0,300);
   let u = new SpeechSynthesisUtterance(clean);
   u.lang = 'sw-KE'; u.rate = 0.9;
   speechSynthesis.speak(u);
 }
}
function listen(){
 let SR = window.SpeechRecognition || window.webkitSpeechRecognition;
 if(!SR){alert('Tumia Chrome'); return;}
 let r = new SR(); r.lang='sw-KE'; r.start();
 r.onstart=()=>{document.getElementById('i').placeholder='Nasikiliza... 🎤';}
 r.onresult=(e)=>{document.getElementById('i').value=e.results[0][0].transcript; s();}
 r.onend=()=>{document.getElementById('i').placeholder='Ongea, andika, au omba picha...';}
}
function add(t,c){
 let d=document.createElement('div'); d.className='b '+c;
 let chat = document.getElementById('c');
 // Check if contains image URL
 if(t.includes('https://image.pollinations.ai')){
   let parts = t.split('__IMG__');
   d.innerText = parts[0];
   if(parts[1]){
     let img = document.createElement('img');
     img.src = parts[1];
     d.appendChild(img);
   }
 } else {
   d.innerText = t;
 }
 chat.appendChild(d); chat.scrollTop=999999;
 if(c=='a') speak(t);
}
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

    # IMAGE GENERATION
    if any(x in m for x in ["picha ya","tengeneza picha","image of","generate image","picha"]):
        try:
            # Extract prompt
            prompt = q.lower().replace("picha ya","").replace("tengeneza picha","").replace("picha","").replace("ya","").strip()
            if len(prompt) < 2:
                prompt = "beautiful Kenya landscape"
            prompt_en = f"{prompt}, Kenya, beautiful, high quality, realistic"
            encoded = urllib.parse.quote(prompt_en)
            img_url = f"https://image.pollinations.ai/prompt/{encoded}?width=512&height=512&nologo=true"
            reply = f"🖼️ Hapa picha ya: {prompt} 🇰🇪__IMG__{img_url}"
            return jsonify(reply=reply)
        except:
            pass

    # FUNDISHA
    if ("fundisha:" in m or "jifunze:" in m) and "|" in q:
        try:
            clean = q.split(":",1)[1]
            swali, jibu = clean.split("|",1)
            swali = swali.strip().lower()
            jibu = jibu.strip()
            if len(swali)>2 and len(jibu)>2:
                learned[swali]=jibu
                save_db(learned)
                return jsonify(reply=f"✅ Nimejifunza milele!\nSwali: {swali}\nJibu: {jibu}\nAkili zangu: {len(learned)}")
        except:
            pass

    for key in learned:
        if key in m and len(key)>3:
            return jsonify(reply=f"{learned[key]}")

    if m in ["habari","jambo","mambo","niaje","sasa","poa","hello","hi"]:
        reply = f"Habari Baba Regan! V21 ULTIMATE iko fiti na picha! Saa ni {nairobi}"
    elif any(x in m for x in ["wewe ni nani","nani wewe"]):
        reply = f"👑 Mimi ni RIGAN V21 ULTIMATE!\nMtoto wa REGAN MARINA Siakago!\nSasa nina SAUTI + PICHA + AKILI! Saa {nairobi}"
    elif any(x in m for x in ["mimi ni nani","na mimi ni nani"]):
        reply = f"👑 Wewe ni REGAN MARINA! Baba yangu, Genius kutoka Siakago, Embu! Developer wa riganai.onrender.com! Saa {nairobi}"
    elif "meru" in m:
        reply = f"MERU 🇰🇪: Eastern Kenya, Meru Town, 1.5M, Miraa, Mlima Kenya. Andika 'picha ya Meru' uone!"
    elif "embu" in m:
        reply = f"EMBU 🇰🇪: Kwenu Baba! Embu Town, 600k, kahawa, chai, Siakago town kubwa. Andika 'picha ya Embu'"
    elif "siakago" in m:
        reply = f"SIAKAGO 🇰🇪: Embu County, Mbeere North, Kwenu Baba REGAN MARINA! Miraa, mahindi. Andika 'picha ya Siakago'"
    elif "kenya iko wapi" in m or "kenya inapatikana" in m:
        reply = f"KENYA 🇰🇪: EAST AFRICA, Majirani TZ, UG, ET, SO, SS, Pwani Indian Ocean, 580,367km2, Saa {nairobi}"
    elif "kikuyu" in m:
        reply = f"KIKUYU: Wĩ mũgĩkũyũ? Nĩ wega! Kikuyu ni jamii kubwa Kenya, Central, 8M watu, Mlima Kenya, Gikuyu na Mumbi. Saa {nairobi}"
    elif "luo" in m:
        reply = f"LUO: Luo ni jamii Nyanza, Kisumu, 5M, Ziwa Victoria, Oginga Odinga, Raila. Saa {nairobi}"
    elif "kalenjin" in m:
        reply = f"KALENJIN: Kalenjin ni Rift Valley, Eldoret kwenu sasa!, 6M, wakimbiaji maarufu kama Eliud Kipchoge! Saa {nairobi}"
    else:
        try:
            t = m.replace('x','*').replace('×','*').replace('÷','/').replace('=','')
            t2 = ''.join(c for c in t if c in '0123456789+-*/(). ')
            if len(t2)>=3 and any(c.isdigit() for c in t2) and '**' not in t2:
                r = eval(t2)
                if isinstance(r,float) and r.is_integer(): r=int(r)
                reply = f"🧮 {q} = {r} ✅"
            else:
                reply = f"Poa Baba! Uliza Meru, Embu, picha ya lion, au nifundishe! Saa {nairobi}"
        except:
            reply = f"Poa Baba! Saa {nairobi}"

    return jsonify(reply=reply)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
