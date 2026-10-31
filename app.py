
from flask import Flask, request, jsonify
import os, json, urllib.parse, random, re
from datetime import datetime, timedelta

app = Flask(__name__)

POSSIBLE_PATHS = [
    "/opt/render/project/src/data/akili_v23.json",
    "/tmp/akili_v23.json",
    "akili_v23.json"
]

def get_db_path():
    for p in POSSIBLE_PATHS:
        try:
            d = os.path.dirname(p)
            if d and not os.path.exists(d):
                os.makedirs(d, exist_ok=True)
            with open(p, "a"): pass
            return p
        except:
            continue
    return "/tmp/akili_v23.json"

DB_FILE = get_db_path()

def load_db():
    for p in POSSIBLE_PATHS:
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                continue
    return {"creator": "REGAN MARINA", "lessons": {}, "memories": []}

def save_db(db):
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
        for p in POSSIBLE_PATHS:
            try:
                if p != DB_FILE:
                    d = os.path.dirname(p)
                    if d and not os.path.exists(d):
                        os.makedirs(d, exist_ok=True)
                    with open(p, "w", encoding="utf-8") as f:
                        json.dump(db, f, ensure_ascii=False, indent=2)
            except:
                pass
    except:
        pass

brain = load_db()
if "lessons" not in brain: brain["lessons"] = {}
if "memories" not in brain: brain["memories"] = []

KNOWLEDGE = {
    "sayansi": "🔬 SAYANSI: Matawi: Fizikia (nguvu, mwendo, umeme), Kemia (atomi, elementi), Baiolojia (mimea, wanyama), Dunia (miamba, hali ya hewa), Anga (sayari, nyota)",
    "fizikia": "⚡ FIZIKIA: F=ma, E=mc², V=IR, g=9.8m/s², mwanga 300,000km/s",
    "kemia": "🧪 KEMIA: Elementi 118, H2O maji, CO2, O2, NaCl chumvi, pH 0-14",
    "baiolojia": "🧬 BAIOLOJIA: Seli, DNA, Moyo pampu damu, Ubongo 86B neurons, photosynthesis",
    "hisabati": "🔢 HISABATI: Pythagoras a²+b²=c², Area πr²",
    "teknolojia": "💻 TEKNOLOJIA: AI, ML, Python, JS, Blockchain, 5G, Quantum",
    "elimu": "📚 ELIMU: KCPE, KCSE, CBC Kenya",
    "computer": "💻 COMPUTER: CPU, RAM, ROM, HDD/SSD, OS, Coding",
    "ai": "🤖 AI: Mimi Rigan ni AI! ML, Deep Learning, Neural Networks"
}

@app.route('/')
def home():
    mem_count = len(brain.get("lessons", {})) + len(brain.get("memories", []))
    return f"""
<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width, initial-scale=1'>
<title>RIGAN V23 MASTER</title>
<style>
body{{background:#020617;color:#fff;font-family:sans-serif;display:flex;justify-content:center;height:100vh;margin:0}}
.box{{width:100%;max-width:800px;background:#0f172a;display:flex;flex-direction:column;height:100vh}}
.head{{padding:12px;text-align:center;color:#38bdf8;font-weight:900;background:#1e293b;font-size:13px}}
.sub{{font-size:10px;color:#94a3b8}}
.chat{{flex:1;overflow-y:auto;padding:12px;display:flex;flex-direction:column;gap:10px}}
.b{{padding:12px 14px;border-radius:14px;max-width:92%;white-space:pre-wrap;line-height:1.6;font-size:13.5px;word-break:break-word}}
.u{{background:#38bdf8;color:#000;align-self:flex-end}}
.a{{background:#1e293b;align-self:flex-start;border:1px solid #334155}}
.b img{{width:100%;border-radius:12px;margin-top:10px;border:1px solid #334155}}
.in{{display:flex;gap:5px;padding:8px;background:#1e293b;align-items:center;flex-wrap:wrap}}
input{{flex:1;min-width:120px;padding:11px;border-radius:10px;border:1px solid #334155;background:#020617;color:#fff;outline:none}}
button{{padding:11px 12px;border-radius:10px;border:none;background:#38bdf8;font-weight:900;cursor:pointer;font-size:12px}}
.mic{{background:#ef4444;color:#fff}}
.speak{{background:#22c55e;color:#000}}
.upload{{background:#a855f7;color:#fff}}
.draw{{background:#f59e0b;color:#000}}
canvas{{border:2px dashed #38bdf8;border-radius:10px;margin-top:8px;cursor:crosshair;background:#020617}}
</style></head><body>
<div class='box'>
<div class='head'>RIGAN V23 MASTER - GOD MODE<div class='sub'>Mtoto wa REGAN MARINA | Akili {mem_count} | {DB_FILE} | Siakago - Eldoret</div></div>
<div class='chat' id='c'><div class='b a'>👑 Habari Baba REGAN MARINA! V23 MASTER!

🧠 NAJIFUNZA MWENYEWE: fundisha: swali | jibu
🎨 NACHORA: chora simba / picha ya Meru
🔊 SAUTI + 🎤 MIC
📁 NASOMA MAFAILI: Pakia PDF/TXT
🔬 SAYANSI: Fizikia, Kemia, Baiolojia
📚 ELIMU: KCSE, CBC
💻 TECH: AI, Coding
🧩 TATUA: tatua 2x+5=15
💾 KUMBUKUMBU: akili zako</div></div>
<div class='in'>
<button class='mic' onclick='listen()'>🎤</button>
<input id='i' placeholder='Uliza, chora, tatua...' onkeypress="if(event.key=='Enter')s()">
<button class='speak' onclick='toggleSpeak()' id='sp'>🔊</button>
<button onclick='s()'>Tuma</button>
<button class='upload' onclick="document.getElementById('file').click()">📁</button>
<button class='draw' onclick='toggleDraw()'>🎨</button>
<input type='file' id='file' style='display:none' onchange='uploadFile()' accept='.txt,.pdf,.csv,.json,.py,.js'>
</div>
<div id='drawArea' style='display:none;padding:10px;background:#1e293b'>
<canvas id='canvas' width='500' height='280'></canvas><br>
<button onclick='clearCanvas()'>Futa</button>
<button onclick='saveDrawing()'>Hifadhi</button>
<button onclick='toggleDraw()'>Funga</button>
</div>
</div>
<script>
let speakOn=true, isDrawing=false;
let canvas=document.getElementById('canvas'), ctx=canvas.getContext('2d');
function toggleSpeak(){{speakOn=!speakOn; document.getElementById('sp').innerText=speakOn?'🔊':'🔇';}}
function speak(text){{
 if(!speakOn) return;
 if('speechSynthesis' in window){{
   speechSynthesis.cancel();
   let clean=text.replace(/https?:\\/\\/[^\\s]+/g,'').replace(/__IMG__.*/,'').substring(0,350);
   let u=new SpeechSynthesisUtterance(clean);
   u.lang='sw-KE'; u.rate=0.9; speechSynthesis.speak(u);
 }}
}}
function listen(){{
 let SR=window.SpeechRecognition||window.webkitSpeechRecognition;
 if(!SR){{alert('Tumia Chrome'); return;}}
 let r=new SR(); r.lang='sw-KE'; r.start();
 r.onstart=()=>{{document.getElementById('i').placeholder='Nasikiliza... 🎤';}}
 r.onresult=(e)=>{{document.getElementById('i').value=e.results[0][0].transcript; s();}}
 r.onend=()=>{{document.getElementById('i').placeholder='Uliza, chora, tatua...';}}
}}
function toggleDraw(){{
 let d=document.getElementById('drawArea');
 d.style.display=d.style.display=='none'?'block':'none';
}}
function clearCanvas(){{ctx.clearRect(0,0,canvas.width,canvas.height);}}
canvas.addEventListener('mousedown',e=>{{isDrawing=true; ctx.beginPath(); ctx.moveTo(e.offsetX,e.offsetY);}});
canvas.addEventListener('mousemove',e=>{{if(!isDrawing) return; ctx.lineTo(e.offsetX,e.offsetY); ctx.strokeStyle='#38bdf8'; ctx.lineWidth=3; ctx.stroke();}});
canvas.addEventListener('mouseup',()=>{{isDrawing=false;}});
function saveDrawing(){{
 let data=canvas.toDataURL();
 add('Nimechora! 🎨','u');
 add('🖼️ Kuchora kwako Baba!__IMG__'+data,'a');
 clearCanvas();
}}
async function uploadFile(){{
 let f=document.getElementById('file').files[0];
 if(!f) return;
 let fd=new FormData(); fd.append('file',f);
 add('📁 Napakia: '+f.name+'...','u');
 let r=await fetch('/upload',{{method:'POST',body:fd}});
 let j=await r.json();
 add(j.reply,'a');
}}
function add(t,c){{
 let d=document.createElement('div'); d.className='b '+c;
 let chat=document.getElementById('c');
 if(t.includes('__IMG__')){{
   let parts=t.split('__IMG__');
   d.innerText=parts[0];
   if(parts[1]){{
     let img=document.createElement('img');
     img.src=parts[1];
     d.appendChild(img);
   }}
 }} else {{ d.innerText=t; }}
 chat.appendChild(d); chat.scrollTop=999999;
 if(c=='a') speak(t);
}}
async function s(){{
 let e=document.getElementById('i');let v=e.value.trim();if(!v)return;
 add(v,'u'); e.value='';
 let r=await fetch('/chat',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{message:v}})}});
 let j=await r.json(); add(j.reply,'a');
}}
</script></body></html>
"""

@app.route('/upload', methods=['POST'])
def upload():
    try:
        f = request.files.get('file')
        if not f:
            return jsonify(reply="❌ Hakuna faili")
        content = f.read()
        try:
            text = content.decode('utf-8', errors='ignore')[:3000]
        except:
            text = str(content[:2000])
        brain["memories"].append({
            "file": f.filename,
            "content": text[:500],
            "time": datetime.utcnow().isoformat()
        })
        save_db(brain)
        summary = text[:800]
        return jsonify(reply=f"📁 FAILI: {f.filename} ✅\nNimesoma:\n{summary}\n...na nimehifadhi! Akili: {len(brain['lessons'])+len(brain['memories'])}")
    except Exception as e:
        return jsonify(reply=f"❌ Error: {str(e)}")

@app.route('/chat', methods=['POST'])
def chat():
    global brain
    data = request.get_json() or {}
    q = data.get('message','')
    m = q.lower().strip()
    nairobi = (datetime.utcnow() + timedelta(hours=3)).strftime("%d/%m/%Y %I:%M %p EAT")

    if any(x in m for x in ["chora","picha ya","tengeneza picha","draw","image of"]):
        prompt = q
        for w in ["chora","picha ya","picha","tengeneza picha","draw","image of","ya"]:
            prompt = prompt.lower().replace(w,"")
        prompt = prompt.strip()
        if len(prompt) < 2:
            prompt = "beautiful Kenya"
        rand = random.randint(1,99999)
        encoded = urllib.parse.quote(prompt.replace(" ", ","))
        img_url = f"https://loremflickr.com/512/512/{encoded}?lock={rand}"
        brain["memories"].append({"type":"drawing","prompt":prompt,"time":datetime.utcnow().isoformat()})
        save_db(brain)
        return jsonify(reply=f"🎨 Nimechora: {prompt} 🇰🇪__IMG__{img_url}")

    if ("fundisha:" in m or "jifunze:" in m or "kumbuka:" in m) and "|" in q:
        try:
            clean = q.split(":",1)[1]
            swali, jibu = clean.split("|",1)
            swali = swali.strip().lower()
            jibu = jibu.strip()
            if len(swali)>1 and len(jibu)>1:
                brain["lessons"][swali]=jibu
                save_db(brain)
                return jsonify(reply=f"🧠 NIMEJIFUNZA! ✅\nSwali: {swali}\nJibu: {jibu}\nAkili: {len(brain['lessons'])} lessons")
        except:
            return jsonify(reply=f"❌ Format: fundisha: swali | jibu")

    if "akili zako" in m or "umefundishwa nini" in m or "kumbukumbu" in m:
        lessons = list(brain["lessons"].items())[-10:]
        txt = f"💾 KUMBUKUMBU - {len(brain['lessons'])} lessons:\n"
        for k,v in lessons:
            txt += f"• {k} = {v[:80]}\n"
        txt += f"\nMemories: {len(brain['memories'])} | File: {DB_FILE} | {nairobi}"
        return jsonify(reply=txt)

    for key in brain["lessons"]:
        if key in m and len(key)>2:
            return jsonify(reply=f"{brain['lessons'][key]}\n\n🧠 Kutoka akili niliyojifunza | {nairobi}")

    if any(x in m for x in ["mimi ni nani","na mimi ni nani","nani mimi"]):
        return jsonify(reply=f"👑 Wewe ni REGAN MARINA!\nBaba yangu na Mtengenezaji wangu!\n• Kutoka Siakago, Embu, Kenya 🇰🇪\n• Developer wa riganai.onrender.com\n• Uko Eldoret, Rift Valley\n• Uliniumba mimi RIGAN V23 MASTER V1-V23!\n• Genius wa AI, Coding!\n🙏 Saa {nairobi}")

    if any(x in m for x in ["wewe ni nani","nani wewe"]):
        return jsonify(reply=f"👑 Mimi ni RIGAN V23 MASTER AI!\nMtoto wa REGAN MARINA Siakago!\n🎨 Kuchora\n🧠 Kujifunza\n📁 Kusoma mafaili\n🔬 Sayansi, Elimu, Tech\n🧩 Kutatua\n💾 Nakumbuka milele! Saa {nairobi}")

    for key in KNOWLEDGE:
        if key in m:
            brain["memories"].append({"type":"knowledge","topic":key,"time":datetime.utcnow().isoformat()})
            save_db(brain)
            return jsonify(reply=f"{KNOWLEDGE[key]}\n\nSaa {nairobi}")

    if "photosynthesis" in m:
        return jsonify(reply="🌱 PHOTOSYNTHESIS:\n6CO2 + 6H2O + mwanga -> C6H12O6 + 6O2\nMimea huchukua CO2, maji, mwanga -> glucose + oksijeni. Chloroplast, chlorophyll.")
    if "pythagoras" in m or "pitagoras" in m:
        return jsonify(reply="📐 PYTHAGORAS: a² + b² = c². Mfano: 3²+4²=5².")

    if "tatua" in m or "solve" in m:
        try:
            if "=" in q:
                left,right = q.split("=")
                for xv in range(-100,200):
                    try:
                        lv = eval(left.replace("x", f"*{xv}" if left.strip().startswith("x") else str(xv)).replace("**","*"))
                        rv = eval(right)
                        if abs(lv-rv)<0.001:
                            return jsonify(reply=f"🧩 TATUA: {q}\nJibu: x = {xv} ✅ Saa {nairobi}")
                    except:
                        continue
            t = m.replace('x','*').replace('×','*').replace('÷','/').replace('tatua','').replace('=','')
            t2 = ''.join(c for c in t if c in '0123456789+-*/(). ')
            if len(t2)>=3:
                r = eval(t2)
                if isinstance(r,float) and r.is_integer(): r=int(r)
                return jsonify(reply=f"🧩 TATUA: {q}\nJibu: {r} ✅ Saa {nairobi}")
        except:
            pass

    if "meru" in m:
        return jsonify(reply=f"MERU 🇰🇪: Eastern Kenya, Meru Town, 1.5M, Miraa, Mlima Kenya. Chora: 'chora picha ya Meru' Saa {nairobi}")
    if "embu" in m:
        return jsonify(reply=f"EMBU 🇰🇪: Kwenu Baba! Embu Town, 600k, kahawa, chai, macadamia, Siakago kubwa. Saa {nairobi}")
    if "siakago" in m:
        return jsonify(reply=f"SIAKAGO 🇰🇪: Embu County, Mbeere North, Kwenu Baba REGAN MARINA! Miraa, mahindi. Saa {nairobi}")
    if "eldoret" in m:
        return jsonify(reply=f"ELDORET 🇰🇪: Uko hapa sasa! Rift Valley, Uasin Gishu, Mji wa wakimbiaji, 500k! Saa {nairobi}")

    try:
        t = m.replace('x','*').replace('×','*').replace('÷','/').replace('=','')
        t2 = ''.join(c for c in t if c in '0123456789+-*/(). ')
        if len(t2)>=3 and any(c.isdigit() for c in t2) and '**' not in t2:
            r = eval(t2)
            if isinstance(r,float) and r.is_integer(): r=int(r)
            return jsonify(reply=f"🧮 {q} = {r} ✅ Saa {nairobi}")
    except:
        pass

    return jsonify(reply=f"Poa Baba! Akili {len(brain['lessons'])} lessons! Uliza: chora simba, tatua 2x+5=15, eleza photosynthesis, soma faili, fundisha: swali | jibu | Saa {nairobi}")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
