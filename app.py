
from flask import Flask, request, jsonify
import os, json, urllib.parse, urllib.request, random, re
from datetime import datetime, timedelta

app = Flask(__name__)
DB_FILE = "/tmp/akili_v54.json"

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

brain=load_db()
if "lessons" not in brain: brain["lessons"]={}

# AUTO LEARN FROM WIKIPEDIA AUTOMATIC
def auto_learn_from_internet(query):
    try:
        # Safisha swali
        q_clean = query.lower()
        # Tafuta neno muhimu
        for bad in ["inapatikana nchi gani","inapatikana wapi","ni wapi","ni nani","iko wapi","nini","ya nini","?"]:
            q_clean = q_clean.replace(bad,"")
        q_clean = q_clean.strip()
        if len(q_clean) < 2: q_clean = query

        # 1. Jaribu Wikipedia English
        wiki_q = urllib.parse.quote(q_clean.replace(" ","_"))
        urls = [
            f"https://en.wikipedia.org/api/rest_v1/page/summary/{wiki_q}",
            f"https://sw.wikipedia.org/api/rest_v1/page/summary/{wiki_q}",
        ]
        for url in urls:
            try:
                req = urllib.request.Request(url, headers={'User-Agent':'RiganV54/1.0'})
                with urllib.request.urlopen(req, timeout=4) as res:
                    data = json.loads(res.read().decode('utf-8'))
                    if "extract" in data and len(data["extract"]) > 20:
                        summary = data["extract"][:600]
                        title = data.get("title","")
                        # Hifadhi kama lesson AUTOMATIC
                        brain["lessons"][query.lower()] = f"{title}: {summary}"
                        save_db(brain)
                        return f"🌐 NIMEJIFUNZA AUTOMATIC KUTOKA INTERNET!\n\n{title}\n{summary}\n\nSaa hii nimeihifadhi milele! Sikuuliza tena nitajua!"
            except: continue
        
        # 2. Kama Wikipedia imeshindwa, tumia DuckDuckGo Instant Answer
        try:
            ddg_q = urllib.parse.quote(query)
            ddg_url = f"https://api.duckduckgo.com/?q={ddg_q}&format=json&no_html=1&skip_disambig=1"
            req = urllib.request.Request(ddg_url, headers={'User-Agent':'RiganV54/1.0'})
            with urllib.request.urlopen(req, timeout=4) as res:
                data = json.loads(res.read().decode('utf-8'))
                if data.get("AbstractText"):
                    abstract = data["AbstractText"][:600]
                    brain["lessons"][query.lower()] = abstract
                    save_db(brain)
                    return f"🌐 NIMEJIFUNZA AUTOMATIC KUTOKA INTERNET!\n\n{abstract}\n\nNimeihifadhi!"
        except: pass

    except: pass
    return None

BASE = {
    "safaricom": "🇰🇪 SAFARICOM: Inapatikana KENYA! HQ Nairobi, 1997, M-Pesa 2007 watu 51M, 45M customers.",
    "meru": "🏔️ MERU: Eastern Kenya, Meru Town, 1.5M Ameru, Miraa, Mlima Kenya, Kimeru Muuga=Hello Ibwega=Thank you.",
    "kenya": "🇰🇪 KENYA: East Africa, capital Nairobi, 580,367km2, 55M, Meru Embu Siakago Eldoret.",
}

@app.route('/')
def home():
    lessons=len(brain["lessons"])
    return f"""
<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width, initial-scale=1'>
<title>RIGAN V54 AUTO</title>
<style>
body{{background:#020617;color:#fff;font-family:sans-serif;display:flex;justify-content:center;height:100vh;margin:0}}
.box{{width:100%;max-width:850px;background:#0f172a;display:flex;flex-direction:column;height:100vh}}
.head{{padding:14px;text-align:center;color:#38bdf8;font-weight:900;background:#1e293b}}
.sub{{font-size:10px;color:#22c55e}}
.auto{{background:#f59e0b;color:#000;padding:8px;text-align:center;font-size:11px;font-weight:900}}
.chat{{flex:1;overflow-y:auto;padding:12px;display:flex;flex-direction:column;gap:10px}}
.b{{padding:12px 14px;border-radius:14px;max-width:92%;white-space:pre-wrap;line-height:1.6;font-size:13.5px}}
.u{{background:#38bdf8;color:#000;align-self:flex-end}}
.a{{background:#1e293b;align-self:flex-start;border:1px solid #334155}}
.b img{{width:100%;border-radius:12px;margin-top:10px;border:1px solid #334155;background:#020617}}
.in{{display:flex;gap:6px;padding:10px;background:#1e293b;align-items:center}}
input{{flex:1;padding:12px;border-radius:12px;border:1px solid #334155;background:#020617;color:#fff;outline:none}}
button{{padding:12px 14px;border-radius:12px;border:none;background:#38bdf8;font-weight:900;cursor:pointer}}
.mic{{background:#ef4444;color:#fff}} .spk{{background:#22c55e;color:#000}}
</style></head><body>
<div class='box'>
<div class='head'>RIGAN V54 - AUTOMATIC SELF-LEARNING<div class='sub'>Mtoto wa REGAN MARINA | Akili {lessons} | Inajifunza Yenyewe Kutoka Internet - Hakuna fundisha: Tena!</div></div>
<div class='auto'>🤖 AUTOMATIC: Nikikosa jibu, natafuta Wikipedia/Google AUTOMATIC na kujifunza mwenyewe! Hutafundisha tena!</div>
<div class='chat' id='c'><div class='b a'>👑 Muuga Baba Regan! V54 AUTOMATIC IKO LIVE!

HII NDIO ULICHOOMBA!

❌ V53: Ilikuwa inakuuliza "Nifundishe"
✅ V54: Inatafuta INTERNET AUTOMATIC na kujifunza yenyewe!

Ukiniuliza "Airtel inapatikana nchi gani" na sijui:
Mimi AUTOMATIC nitaenda Wikipedia, Google, nitasoma, na kujifunza mwenyewe!
Hutafundisha kitu!

Jaribu chochote haijui:
- Airtel inapatikana nchi gani
- Tesla ni nini
- Bitcoin ni nini
- Elon Musk ni nani

Mimi nitajifunza AUTOMATIC!

Akili: {lessons} lessons - Itaongezeka yenyewe kutoka internet!</div></div>
<div class='in'>
<button class='mic' onclick='listen()'>🎤</button>
<input id='i' placeholder='Uliza chochote... Najifunza AUTOMATIC...' onkeypress="if(event.key=='Enter')s()">
<button class='spk' onclick='toggleSpeak()' id='sp'>🔊</button>
<button onclick='s()'>Tuma</button>
</div>
</div>
<script>
let speakOn=true;
function toggleSpeak(){{speakOn=!speakOn; document.getElementById('sp').innerText=speakOn?'🔊':'🔇';}}
function speak(t){{if(!speakOn)return; if('speechSynthesis' in window){{speechSynthesis.cancel(); let c=t.replace(/https?:\\/\\/[^\\s]+/g,'').replace(/__IMG__.*/,'').substring(0,400); let u=new SpeechSynthesisUtterance(c); u.lang='sw-KE'; u.rate=0.9; speechSynthesis.speak(u);}}}}
function listen(){{let SR=window.SpeechRecognition||window.webkitSpeechRecognition; if(!SR){{alert('Chrome');return;}} let r=new SR(); r.lang='sw-KE'; r.start(); r.onstart=()=>{{document.getElementById('i').placeholder='Natafuta internet... 🌐';}}; r.onresult=(e)=>{{document.getElementById('i').value=e.results[0][0].transcript; s();}}; r.onend=()=>{{document.getElementById('i').placeholder='Uliza chochote... Najifunza AUTOMATIC...';}};}}
function add(t,c){{let d=document.createElement('div'); d.className='b '+c; let chat=document.getElementById('c'); if(t.includes('__IMG__')){{let p=t.split('__IMG__'); d.innerText=p[0]; if(p[1]){{let img=document.createElement('img'); img.src=p[1]; img.onerror=()=>{{let cv=document.createElement('canvas'); cv.width=512; cv.height=512; let cx=cv.getContext('2d'); cx.fillStyle='#0f172a'; cx.fillRect(0,0,512,512); cx.fillStyle='#38bdf8'; cx.fillRect(0,0,512,60); cx.fillStyle='#fff'; cx.font='bold 20px sans-serif'; cx.fillText(p[0].substring(0,30),10,38); cx.fillStyle='#22c55e'; cx.font='bold 60px sans-serif'; cx.fillText('🌐',200,260); cx.fillStyle='#fff'; cx.font='16px sans-serif'; cx.fillText(p[0].slice(0,50),20,350); cx.fillText('RIGAN V54 AUTO-LEARNING',20,380); img.src=cv.toDataURL();}}; d.appendChild(img);}}}} else {{d.innerText=t;}} chat.appendChild(d); chat.scrollTop=999999; if(c=='a') speak(t);}}
async function s(){{let e=document.getElementById('i');let v=e.value.trim();if(!v)return; add(v,'u'); add('🌐 Natafuta internet na kujifunza AUTOMATIC...','a'); e.value=''; let r=await fetch('/chat',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{message:v}})}}); let j=await r.json(); add(j.reply,'a');}}
</script></body></html>
"""

@app.route('/chat', methods=['POST'])
def chat():
    data=request.get_json() or {}
    q=data.get('message','').strip()
    m=q.lower().strip()
    nairobi=(datetime.utcnow()+timedelta(hours=3)).strftime("%d/%m/%Y %I:%M %p EAT")

    # 1. Check aliyojifunza mwenyewe
    for key in brain["lessons"]:
        if key in m and len(key)>2:
            return jsonify(reply=f"{brain['lessons'][key]}\n\n🧠 Kutoka akili niliyojifunza AUTOMATIC kutoka internet | Akili {len(brain['lessons'])} | {nairobi}")

    for key in BASE:
        if key in m:
            return jsonify(reply=f"{BASE[key]}\n\nSaa {nairobi}")

    if "mimi ni nani" in m: return jsonify(reply=f"👑 Wewe ni REGAN MARINA! Baba yangu! Siakago Embu Kenya riganai.onrender.com Eldoret! Saa {nairobi}")
    if "muuga" in m: return jsonify(reply=f"Muuga Baba Regan! Ndi Mwega! RIGAN V54 AUTO! Saa {nairobi}")

    if any(x in m for x in ["chora","picha","draw"]):
        prompt=q
        for w in ["chora","picha ya","picha","draw","image of","ya"]: prompt=prompt.lower().replace(w,"")
        prompt=prompt.strip() or "simba"
        rand=random.randint(1,99999)
        encoded=urllib.parse.quote(prompt.replace(" ", ","))
        img_url=f"https://loremflickr.com/512/512/{encoded}?lock={rand}"
        return jsonify(reply=f"🎨 Nimechora: {prompt} 🇰🇪__IMG__{img_url}")

    # 2. AUTOMATIC SELF-LEARNING - TAFUTA INTERNET
    auto_result = auto_learn_from_internet(q)
    if auto_result:
        return jsonify(reply=f"{auto_result}\n\nSaa {nairobi}")

    # 3. Kama internet imeshindwa
    try:
        t=m.replace('x','*').replace('×','*').replace('÷','/'); t2=''.join(c for c in t if c in '0123456789+-*/(). ')
        if len(t2)>=3 and any(c.isdigit() for c in t2) and '**' not in t2:
            r=eval(t2)
            if isinstance(r,float) and r.is_integer(): r=int(r)
            return jsonify(reply=f"🧮 {q} = {r} ✅ Saa {nairobi}")
    except: pass

    return jsonify(reply=f"🌐 Nimejaribu kutafuta internet AUTOMATIC kuhusu '{q}' lakini internet ya Render ni slow kidogo.\n\nJaribu tena au uliza swali lingine kama Safaricom, Meru, Kenya, Tesla, Bitcoin. Mimi najifunza AUTOMATIC bila kufundishwa!\n\nAkili: {len(brain['lessons'])} | Saa {nairobi}")

if __name__ == '__main__':
    port=int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
