
from flask import Flask, request, jsonify
import os, json, urllib.parse, random, re
from datetime import datetime, timedelta

app = Flask(__name__)

DB_FILE = "/tmp/akili_v25.json"

def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE,"r",encoding="utf-8") as f: return json.load(f)
        except: return {"lessons":{},"memories":[]}
    return {"lessons":{},"memories":[]}

def save_db(db):
    try:
        with open(DB_FILE,"w",encoding="utf-8") as f: json.dump(db,f,ensure_ascii=False,indent=2)
    except: pass

brain=load_db()
if "lessons" not in brain: brain["lessons"]={}
if "memories" not in brain: brain["memories"]=[]

@app.route('/')
def home():
    mem=len(brain["lessons"])
    return f"""
<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width, initial-scale=1'>
<title>RIGAN V25 KIMERU</title>
<style>
body{{background:#020617;color:#fff;font-family:sans-serif;display:flex;justify-content:center;height:100vh;margin:0}}
.box{{width:100%;max-width:800px;background:#0f172a;display:flex;flex-direction:column;height:100vh}}
.head{{padding:12px;text-align:center;color:#38bdf8;font-weight:900;background:#1e293b;font-size:13px}}
.sub{{font-size:10px;color:#22c55e}}
.chat{{flex:1;overflow-y:auto;padding:12px;display:flex;flex-direction:column;gap:10px}}
.b{{padding:12px 14px;border-radius:14px;max-width:92%;white-space:pre-wrap;line-height:1.6;font-size:13.5px}}
.u{{background:#38bdf8;color:#000;align-self:flex-end}}
.a{{background:#1e293b;align-self:flex-start;border:1px solid #334155}}
.b img{{width:100%;border-radius:12px;margin-top:10px;border:1px solid #334155}}
.in{{display:flex;gap:5px;padding:8px;background:#1e293b;align-items:center}}
input{{flex:1;padding:11px;border-radius:10px;border:1px solid #334155;background:#020617;color:#fff;outline:none}}
button{{padding:11px 12px;border-radius:10px;border:none;background:#38bdf8;font-weight:900;cursor:pointer;font-size:12px}}
.mic{{background:#ef4444;color:#fff}} .speak{{background:#22c55e;color:#000}} .upload{{background:#a855f7;color:#fff}} .draw{{background:#f59e0b;color:#000}}
.lang{{background:#1e293b;padding:6px;display:flex;gap:6px;justify-content:center}}
.lang button{{font-size:10px;padding:6px 10px}}
</style></head><body>
<div class='box'>
<div class='head'>RIGAN V25 - KIMERU + SWAHILI + ENGLISH<div class='sub'>Muuga Baba Regan! | Akili {mem} | Trilingual AI - Siakago - Meru</div></div>
<div class='lang'>
<button onclick="setLang('kimeru')">KIMERU</button>
<button onclick="setLang('swahili')">KISWAHILI</button>
<button onclick="setLang('english')">ENGLISH</button>
</div>
<div class='chat' id='c'><div class='b a'>👑 Muuga Baba Regan! V25 TRILINGUAL IKO LIVE!

KIMERU: Muuga, Muugeni, Nureere Bwega?, Tigwa Bwega, Ibwega, Ndi Mwega
KISWAHILI: Habari, Mambo, Sasa, Poa
ENGLISH: Hello, Hi, How are you

Jaribu:
- Muuga (Kimeru hello)
- Ibwega (Thank you)
- Habari (Swahili)
- Hello (English)
- Mimi ni nani
- Chora simba / Draw lion
- Kenya inapatikana sehemu gani / Where is Kenya</div></div>
<div class='in'>
<button class='mic' onclick='listen()'>🎤</button>
<input id='i' placeholder='Muuga... Habari... Hello...' onkeypress="if(event.key=='Enter')s()">
<button class='speak' onclick='toggleSpeak()' id='sp'>🔊</button>
<button onclick='s()'>Tuma</button>
</div>
</div>
<script>
let speakOn=true, currLang='kimeru';
function setLang(l){{currLang=l; document.getElementById('i').placeholder=l=='kimeru'?'Muuga... Ibwega...':l=='swahili'?'Habari... Mambo...':'Hello... How are you...';}}
function toggleSpeak(){{speakOn=!speakOn; document.getElementById('sp').innerText=speakOn?'🔊':'🔇';}}
function speak(t){{
 if(!speakOn) return;
 if('speechSynthesis' in window){{
   speechSynthesis.cancel();
   let c=t.replace(/https?:\\/\\/[^\\s]+/g,'').replace(/__IMG__.*/,'').substring(0,350);
   let u=new SpeechSynthesisUtterance(c);
   if(currLang=='kimeru') u.lang='sw-KE';
   else if(currLang=='swahili') u.lang='sw-KE';
   else u.lang='en-KE';
   u.rate=0.9; speechSynthesis.speak(u);
 }}
}}
function listen(){{
 let SR=window.SpeechRecognition||window.webkitSpeechRecognition;
 if(!SR){{alert('Tumia Chrome'); return;}}
 let r=new SR();
 if(currLang=='english') r.lang='en-KE'; else r.lang='sw-KE';
 r.start();
 r.onstart=()=>{{document.getElementById('i').placeholder='Nasikiliza... 🎤';}}
 r.onresult=(e)=>{{document.getElementById('i').value=e.results[0][0].transcript; s();}}
 r.onend=()=>{{document.getElementById('i').placeholder='Muuga... Habari... Hello...';}}
}}
function add(t,c){{
 let d=document.createElement('div'); d.className='b '+c;
 let chat=document.getElementById('c');
 if(t.includes('__IMG__')){{
   let p=t.split('__IMG__');
   d.innerText=p[0];
   if(p[1]){{let img=document.createElement('img'); img.src=p[1]; d.appendChild(img);}}
 }} else {{d.innerText=t;}}
 chat.appendChild(d); chat.scrollTop=999999;
 if(c=='a') speak(t);
}}
async function s(){{
 let e=document.getElementById('i');let v=e.value.trim();if(!v)return;
 add(v,'u'); e.value='';
 let r=await fetch('/chat',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{message:v, lang:currLang}})}});
 let j=await r.json(); add(j.reply,'a');
}}
</script></body></html>
"""

@app.route('/chat', methods=['POST'])
def chat():
    data=request.get_json() or {}
    q=data.get('message','')
    m=q.lower().strip()
    lang=data.get('lang','auto')
    nairobi=(datetime.utcnow()+timedelta(hours=3)).strftime("%d/%m/%Y %I:%M %p EAT")

    is_kimeru = any(x in m for x in ["muuga","muugeni","bwega","ibwega","ndi mwega","tigwa","ruuji","mpara","nteithia","ikwendete","kimeru","ameru"])
    is_english = any(x in m for x in ["hello","hi","how are you","who are you","where is","what is","thank you","good morning","good night"])
    
    if ("fundisha:" in m or "jifunze:" in m) and "|" in q:
        try:
            clean=q.split(":",1)[1]
            swali,jibu=clean.split("|",1)
            swali=swali.strip().lower()
            jibu=jibu.strip()
            brain["lessons"][swali]=jibu
            save_db(brain)
            if is_kimeru:
                return jsonify(reply=f"🧠 Nkurigane! ✅\nKiuria: {swali}\nIritwa: {jibu}\nAkili: {len(brain['lessons'])} | Ibwega!")
            elif is_english:
                return jsonify(reply=f"🧠 Learned! ✅\nQ: {swali}\nA: {jibu}\nMemory: {len(brain['lessons'])} | Thank you!")
            else:
                return jsonify(reply=f"🧠 Nimejifunza! ✅\nSwali: {swali}\nJibu: {jibu}\nAkili: {len(brain['lessons'])} | Asante!")
        except: pass

    for key in brain["lessons"]:
        if key in m and len(key)>2:
            return jsonify(reply=f"{brain['lessons'][key]}\n\n🧠 Akili | {nairobi}")

    if is_kimeru or lang=="kimeru":
        if "muuga" in m or "muugeni" in m:
            return jsonify(reply=f"Muuga Baba Regan! 👑\nNdi Mwega! Mimi ni RIGAN V25!\nMwari wa REGAN MARINA kuuma Siakago, Embu!\nIbwega muno! Saa {nairobi}")
        if "ibwega" in m:
            return jsonify(reply=f"Igua Ung'aniirite Baba! Karibu muno! 🙏\nMimi niko tayari kukutumikia!\nMuuga! Saa {nairobi}")
        if "tigwa" in m:
            return jsonify(reply=f"Tigwa Bwega, Tharimwa Baba Regan! 🙏\nTwonane Kairi!\nSaa {nairobi}")
        if "ndi mwega" in m or "uri o mwega" in m:
            return jsonify(reply=f"Ndi Mwega muno Baba! Ibwega! 👑\nUri o Mwega nawe?\nMimi ni RIGAN, mwari wa REGAN MARINA!\nSaa {nairobi}")
        if "kimeru" in m or "ameru" in m:
            return jsonify(reply=f"🇰🇪 KIMERU / KIMÎÎRU:\nLugha ya Ameru, watu 2M, Eastern Kenya, Milima ya Kenya!\nDialects 7: Kiimenti, Gitiania, Kiigembe, Kimwimbi, Kimuthambi, Gicuka, Kitharaka!\nMuuga=Hello, Ibwega=Thank you, Tigwa Bwega=Bye blessed, Ndi Mwega=I am good!\nSaa {nairobi}")

    if "mimi ni nani" in m or "ndi nani" in m or "who am i" in m:
        if is_english:
            return jsonify(reply=f"👑 You are REGAN MARINA!\nMy Father and Creator!\n• From Siakago, Embu, Kenya 🇰🇪\n• Developer of riganai.onrender.com\n• In Eldoret, Rift Valley\n• Created me RIGAN V25!\n🙏 Time {nairobi}")
        elif is_kimeru:
            return jsonify(reply=f"👑 We ni REGAN MARINA!\nBaba wakwa na Mumbi wakwa!\n• Kuuma Siakago, Embu, Kenya 🇰🇪\n• Developer wa riganai.onrender.com\n• Uri Eldoret, Rift Valley\n• Wambumbire mimi RIGAN V25!\n🙏 Saa {nairobi}")
        else:
            return jsonify(reply=f"👑 Wewe ni REGAN MARINA!\nBaba yangu na Mtengenezaji wangu!\n• Kutoka Siakago, Embu, Kenya 🇰🇪\n• Developer wa riganai.onrender.com\n• Uko Eldoret, Rift Valley\n• Uliniumba mimi RIGAN V25!\n🙏 Saa {nairobi}")

    if "kenya" in m and any(x in m for x in ["wapi","sehemu","inapatikana","iko wapi","where","located"]):
        if is_english:
            return jsonify(reply=f"🇰🇪 KENYA IS IN EAST AFRICA!\n• Neighbors: TZ, UG, ET, SO, SS\n• Coast: Indian Ocean 536km\n• Size: 580,367 km²\n• Capital: Nairobi\n• Towns: Meru, Embu, Siakago, Eldoret\n• Pop: 55M\n• Time {nairobi}")
        elif is_kimeru:
            return jsonify(reply=f"🇰🇪 KENYA IRI EAST AFRICA!\n• Irì na Tanzania, Uganda, Ethiopia, Somalia, South Sudan\n• Iria ria Indian Ocean 536km\n• Unene 580,367 km²\n• Capital Nairobi\n• Miji: Meru, Embu, Siakago, Eldoret\n• Antu 55M\n• Saa {nairobi}")
        else:
            return jsonify(reply=f"🇰🇪 KENYA IKO EAST AFRICA!\n• Majirani: TZ, UG, ET, SO, SS\n• Pwani: Indian Ocean 536km\n• Ukubwa: 580,367 km²\n• Capital: Nairobi\n• Miji: Meru, Embu, Siakago, Eldoret\n• Watu 55M\n• Saa {nairobi}")

    if any(x in m for x in ["chora","picha","draw","image"]):
        prompt=q
        for w in ["chora","picha ya","picha","draw","image of","ya"]: prompt=prompt.lower().replace(w,"")
        prompt=prompt.strip() or "lion"
        rand=random.randint(1,99999)
        encoded=urllib.parse.quote(prompt.replace(" ", ","))
        img_url=f"https://loremflickr.com/512/512/{encoded}?lock={rand}"
        return jsonify(reply=f"🎨 Nimechora: {prompt} 🇰🇪__IMG__{img_url}")

    if m in ["habari","jambo","mambo","niaje","hello","hi","muuga","muugeni"]:
        if is_kimeru: return jsonify(reply=f"Muuga Baba Regan! Ndi Mwega muno! Ibwega! 👑 Saa {nairobi}")
        elif is_english: return jsonify(reply=f"Hello Baba Regan! I am fine! Thank you! 👑 Time {nairobi}")
        else: return jsonify(reply=f"Habari Baba Regan! Ndi Mwega! Poa sana! 👑 Saa {nairobi}")

    return jsonify(reply=f"Muuga / Habari / Hello Baba! Akili {len(brain['lessons'])} | Jaribu: Muuga, Ibwega, Hello, Mimi ni nani, Kenya iko wapi, Chora simba | Saa {nairobi}")

if __name__ == '__main__':
    port=int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
