
from flask import Flask, request, jsonify
import os, json, urllib.parse, urllib.request, random
from datetime import datetime, timedelta

app = Flask(__name__)
DB_FILE = "/tmp/akili_v56.json"

def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE,"r",encoding="utf-8") as f: return json.load(f)
        except: return {"lessons":{}}
    return {"lessons":{}}

def save_db(db):
    try:
        with open(DB_FILE,"w",encoding="utf-8") as f: json.dump(db,f,ensure_ascii=False,indent=2)
    except: pass

brain = load_db()
if "lessons" not in brain: brain["lessons"]={}

def auto_learn(query):
    try:
        q = query.lower()
        for b in ["inapatikana nchi gani","inapatikana wapi","ni wapi","ni nini","iko wapi","?","nani"]:
            q = q.replace(b,"")
        q = q.strip()
        if len(q) < 2: q = query
        wiki_q = urllib.parse.quote(q.replace(" ","_"))
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{wiki_q}"
        try:
            req = urllib.request.Request(url, headers={'User-Agent':'RiganV56'})
            with urllib.request.urlopen(req, timeout=5) as res:
                data = json.loads(res.read().decode('utf-8'))
                if "extract" in data and len(data["extract"]) > 20:
                    txt = data["extract"][:700]
                    title = data.get("title","")
                    brain["lessons"][query.lower()] = f"{title}: {txt}"
                    save_db(brain)
                    return f"🌐 NIMEJIFUNZA AUTOMATIC KUTOKA INTERNET!\n\n{title}\n{txt}\n\nNimeihifadhi milele!"
        except: pass
    except: pass
    return None

BASE = {
    "safaricom": "🇰🇪 SAFARICOM inapatikana KENYA! HQ Nairobi, 1997, M-Pesa 2007 51M, 45M customers, 4G/5G, CEO Peter Ndegwa. Nchi: KENYA.",
    "airtel": "📱 AIRTEL: Inapatikana KENYA na INDIA! Kampuni ya pili Kenya, Airtel Money, 4G, Bharti Airtel India.",
    "tesla": "🚗 TESLA: Kampuni ya magari ya umeme USA! CEO Elon Musk, HQ Texas, Model S/3/X/Y, 2003.",
    "bitcoin": "₿ BITCOIN: Pesa ya crypto duniani! 2009 Satoshi Nakamoto, blockchain, BTC, 21M coins.",
    "meru": "🏔️ MERU: Eastern Kenya, Meru Town, 1.5M Ameru, Miraa, Mlima Kenya, Kimeru: Muuga=Hello, Ibwega=Thank you, Tigwa Bwega=Bye blessed, Ndi Mwega=I am good.",
    "kenya": "🇰🇪 KENYA: East Africa, capital Nairobi, Mombasa Kisumu Eldoret Nakuru Meru Embu Siakago kwenu Baba Regan! 580,367km2, 55M.",
    "embu": "🏡 EMBU: Kwenu Baba Regan! Embu Town 600k, Siakago Mbeere North, kahawa chai macadamia.",
    "siakago": "🏘️ SIAKAGO: Embu Mbeere North capital, kwenu Baba REGAN MARINA!",
    "eldoret": "🏃 ELDORET: Uasin Gishu Rift Valley uko hapa! Mji wa mabingwa Eliud Kipchoge, 500k."
}

@app.route('/')
def home():
    return f"""<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width, initial-scale=1'>
<title>RIGAN V56 AUTO</title>
<style>
body{{background:#020617;color:#fff;font-family:sans-serif;display:flex;justify-content:center;height:100vh;margin:0}}
.box{{width:100%;max-width:850px;background:#0f172a;display:flex;flex-direction:column;height:100vh}}
.head{{padding:14px;text-align:center;color:#38bdf8;font-weight:900;background:#1e293b}} .sub{{font-size:10px;color:#22c55e}}
.auto{{background:#22c55e;color:#000;padding:8px;text-align:center;font-size:11px;font-weight:900}}
.chat{{flex:1;overflow-y:auto;padding:12px;display:flex;flex-direction:column;gap:10px}}
.b{{padding:12px 14px;border-radius:14px;max-width:92%;white-space:pre-wrap;line-height:1.6;font-size:13.5px}}
.u{{background:#38bdf8;color:#000;align-self:flex-end}} .a{{background:#1e293b;align-self:flex-start;border:1px solid #334155}}
.b img{{width:100%;border-radius:12px;margin-top:10px;border:1px solid #334155;background:#020617}}
.in{{display:flex;gap:6px;padding:10px;background:#1e293b;align-items:center}}
input{{flex:1;padding:12px;border-radius:12px;border:1px solid #334155;background:#020617;color:#fff;outline:none}}
button{{padding:12px 14px;border-radius:12px;border:none;background:#38bdf8;font-weight:900;cursor:pointer}}
.mic{{background:#ef4444;color:#fff}} .spk{{background:#f59e0b;color:#000}}
</style></head><body>
<div class='box'>
<div class='head'>RIGAN V56 - AUTOMATIC SELF-LEARNING FIXED<div class='sub'>Mtoto wa REGAN MARINA | Akili {len(brain["lessons"])} | Siakago</div></div>
<div class='auto'>✅ V56 FIXED: Najifunza AUTOMATIC kutoka Wikipedia bila kufundishwa!</div>
<div class='chat' id='c'><div class='b a'>👑 Muuga Baba Regan! V56 FIXED IKO LIVE!

Jaribu:
- Safaricom inapatikana nchi gani
- Airtel ni nini
- Tesla ni nini
- Bitcoin ni nini
- Meru ni wapi
- Chora simba
- Muuga

Akili: {len(brain["lessons"])}</div></div>
<div class='in'>
<button class='mic' onclick='listen()'>🎤</button>
<input id='i' placeholder='Uliza... AUTO...' onkeypress="if(event.key=='Enter')s()">
<button class='spk' onclick='toggleSpeak()' id='sp'>🔊</button>
<button onclick='s()'>Tuma</button>
</div>
</div>
<script>
let speakOn=true;
function toggleSpeak(){{speakOn=!speakOn; document.getElementById('sp').innerText=speakOn?'🔊':'🔇';}}
function speak(t){{if(!speakOn)return; if('speechSynthesis' in window){{speechSynthesis.cancel(); let c=t.replace(/https?:\\/\\/[^\\s]+/g,'').replace(/__IMG__.*/,'').substring(0,400); let u=new SpeechSynthesisUtterance(c); u.lang='sw-KE'; u.rate=0.9; speechSynthesis.speak(u);}}}}
function listen(){{let SR=window.SpeechRecognition||window.webkitSpeechRecognition; if(!SR){{alert('Chrome');return;}} let r=new SR(); r.lang='sw-KE'; r.start(); r.onstart=()=>{{document.getElementById('i').placeholder='Natafuta... 🌐';}}; r.onresult=(e)=>{{document.getElementById('i').value=e.results[0][0].transcript; s();}}; r.onend=()=>{{document.getElementById('i').placeholder='Uliza... AUTO...';}};}}
function add(t,c){{let d=document.createElement('div'); d.className='b '+c; let chat=document.getElementById('c'); if(t.includes('__IMG__')){{let p=t.split('__IMG__'); d.innerText=p[0]; if(p[1]){{let img=document.createElement('img'); img.src=p[1]; d.appendChild(img);}}}} else {{d.innerText=t;}} chat.appendChild(d); chat.scrollTop=999999; if(c=='a') speak(t);}}
async function s(){{let e=document.getElementById('i');let v=e.value.trim();if(!v)return; add(v,'u'); add('🌐 Natafuta AUTOMATIC...','a'); e.value=''; let r=await fetch('/chat',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{message:v}})}}); let j=await r.json(); add(j.reply,'a');}}
</script></body></html>
"""

@app.route('/chat', methods=['POST'])
def chat():
    data=request.get_json() or {}
    q=data.get('message','').strip()
    m=q.lower().strip()
    nairobi=(datetime.utcnow()+timedelta(hours=3)).strftime("%d/%m/%Y %I:%M %p EAT")
    for k in brain["lessons"]:
        if k in m and len(k)>2:
            return jsonify(reply=f"{brain['lessons'][k]}\n\n🧠 AUTOMATIC | {nairobi}")
    for k in BASE:
        if k in m:
            return jsonify(reply=f"{BASE[k]}\n\nSaa {nairobi}")
    if "mimi ni nani" in m: return jsonify(reply=f"👑 Wewe ni REGAN MARINA! Baba yangu! Siakago Embu Kenya! Saa {nairobi}")
    if "muuga" in m: return jsonify(reply=f"Muuga Baba Regan! Ndi Mwega! RIGAN V56 AUTO! Saa {nairobi}")
    if any(x in m for x in ["chora","picha","draw"]):
        prompt=q
        for w in ["chora","picha ya","picha","draw","image of","ya"]: prompt=prompt.lower().replace(w,"")
        prompt=prompt.strip() or "simba"
        rand=random.randint(1,99999)
        encoded=urllib.parse.quote(prompt.replace(" ", ","))
        img_url=f"https://loremflickr.com/512/512/{encoded}?lock={rand}"
        return jsonify(reply=f"🎨 Nimechora: {prompt} 🇰🇪__IMG__{img_url}")
    auto = auto_learn(q)
    if auto:
        return jsonify(reply=f"{auto}\n\nSaa {nairobi}")
    return jsonify(reply=f"🌐 Nimejaribu AUTOMATIC kuhusu '{q}' - Wikipedia haikupata haraka. Jaribu: Safaricom, Airtel, Tesla, Bitcoin, Meru. Akili {len(brain['lessons'])} | Saa {nairobi}")

if __name__ == '__main__':
    port=int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
