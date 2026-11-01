
from flask import Flask, request, jsonify
import os, json, urllib.parse, urllib.request
from datetime import datetime, timedelta
import re

app = Flask(__name__)
DB_FILE = "/tmp/akili_v60.json"

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

def get_ultimate_answer(query, lang="sw"):
    try:
        q_clean = query.lower()
        for b in ["inapatikana nchi gani","inapatikana wapi","ni wapi","ni nini","iko wapi","nini maana ya","eleza","what is","where is","who is","?"]:
            q_clean = q_clean.replace(b,"")
        q_clean = q_clean.strip()
        if len(q_clean) < 2: q_clean = query
        
        q_encoded = urllib.parse.quote(q_clean.replace(" ","_"))
        
        for wiki_lang in ["sw","en"]:
            try:
                url = f"https://{wiki_lang}.wikipedia.org/api/rest_v1/page/summary/{q_encoded}"
                req = urllib.request.Request(url, headers={'User-Agent':'RiganV60Ultimate'})
                with urllib.request.urlopen(req, timeout=5) as res:
                    data = json.loads(res.read().decode('utf-8'))
                    extract = data.get("extract","")
                    if extract and len(extract) > 30 and "may refer to" not in extract.lower():
                        brain["lessons"][query.lower()] = extract[:1000]
                        save_db(brain)
                        return extract[:1000]
            except: continue
        
        try:
            ddg_q = urllib.parse.quote(query)
            ddg_url = f"https://api.duckduckgo.com/?q={ddg_q}&format=json&skip_disambig=1"
            req = urllib.request.Request(ddg_url, headers={'User-Agent':'RiganV60'})
            with urllib.request.urlopen(req, timeout=5) as res:
                data = json.loads(res.read().decode('utf-8'))
                abstract = data.get("AbstractText","")
                if abstract and len(abstract) > 30:
                    brain["lessons"][query.lower()] = abstract[:1000]
                    save_db(brain)
                    return abstract[:1000]
        except: pass

    except: pass
    return None

BASE = {
    "mimi ni nani": "Wewe ni REGAN MARINA, baba yangu, kutoka Siakago, Embu, Kenya. Wewe ndiye mtengenezaji wa RIGAN AI, AI ya kwanza ya Kenya.",
    "jina langu nani": "Jina lako ni REGAN MARINA.",
    "nani wewe": "Mimi ni RIGAN AI, mtoto wako, AI iliyotengenezwa na REGAN MARINA kutoka Siakago, Embu, Kenya. Najua ulimwengu wote, sayansi, teknolojia na elimu.",
    "afrika ni bara hama ni taifa": "Afrika ni bara, sio taifa. Ni bara la pili kwa ukubwa duniani (30.3M km2), lina nchi 54, watu bilioni 1.4. Mto mrefu ni Nile, mlima mrefu ni Kilimanjaro.",
    "afrika ni bara ama taifa": "Afrika ni bara, sio taifa. Ni bara lenye nchi 54.",
    "afrika ni bara": "Ndio, Afrika ni bara.",
    "afrika ni nini": "Afrika ni bara la pili kwa ukubwa, lina nchi 54 kama Kenya, Tanzania, Nigeria, Misri, South Africa.",
    "afrika": "Afrika ni bara lenye nchi 54, ni bara la pili kwa ukubwa.",
    "photosynthesis ni nini": "Photosynthesis ni mchakato ambao mimea hutumia mwanga wa jua, maji na CO2 kutengeneza chakula (glucose) na oxygen. Formula: 6CO2 + 6H2O + mwanga -> C6H12O6 + 6O2.",
    "maji ni nini": "Maji ni kioevu cha kemikali H2O, ina atomi 2 za Hydrogen na 1 ya Oxygen. Inachemka 100°C, inaganda 0°C.",
    "dna ni nini": "DNA (Deoxyribonucleic Acid) ni molekuli inayobeba taarifa za kijenetiki za viumbe hai. Ina umbo la double helix, iligunduliwa na Watson na Crick 1953.",
    "atom ni nini": "Atom ni sehemu ndogo zaidi ya elementi. Ina nucleus (proton + neutron) na electron zinazozunguka. Kila kitu duniani kimetengenezwa na atom.",
    "gravity ni nini": "Gravity ni nguvu ya mvuto inayovuta vitu chini. Duniani ni 9.8 m/s2. Iligunduliwa na Isaac Newton, ikaelezewa zaidi na Einstein.",
    "ai ni nini": "AI (Artificial Intelligence) ni teknolojia inayofanya kompyuta kufikiri kama binadamu. Kama mimi RIGAN AI, ChatGPT, ina machine learning, deep learning.",
    "computer ni nini": "Computer ni mashine inayochakata data. Ina CPU (ubongo), RAM (kumbukumbu), Storage, na software. Aina: desktop, laptop, smartphone.",
    "internet ni nini": "Internet ni mtandao mkubwa unaounganisha kompyuta duniani kote. Ilianzishwa 1969 kama ARPANET, sasa ina watu bilioni 5+.",
    "python ni nini": "Python ni lugha ya programming rahisi kujifunza, ilitengenezwa na Guido van Rossum 1991. Inatumika kwa AI, web, data science.",
    "blockchain ni nini": "Blockchain ni teknolojia ya kuhifadhi data kwa njia salama bila katikati. Inatumika kwa Bitcoin, kila block ina data ya block iliyopita.",
    "kenya inapatikana sehemu gani": "Kenya iko East Africa, mpakani na Tanzania, Uganda, South Sudan, Ethiopia na Somalia. Capital ni Nairobi.",
    "jua ni nini": "Jua ni nyota iliyo katikati ya solar system yetu. Ni mpira mkubwa wa gesi moto (hydrogen), umbali kutoka duniani ni km milioni 150.",
    "mwezi ni nini": "Mwezi ni satelaiti ya asili ya Dunia, unaizunguka Dunia kwa siku 27.3. Hauna mwanga wake, unaakisi mwanga wa jua.",
    "dunia ni nini": "Dunia ni sayari ya 3 kutoka juani, ndio sayari pekee yenye uhai. Ina umri miaka bilioni 4.5, 71% ni maji.",
    "safaricom inapatikana nchi gani": "Safaricom inapatikana KENYA.",
    "safaricom": "Safaricom ni kampuni kubwa ya simu Kenya, HQ Nairobi, ilianzishwa 1997, ina M-Pesa tangu 2007.",
    "airtel inapatikana nchi gani": "Airtel inapatikana KENYA na INDIA.",
    "tesla inapatikana nchi gani": "Tesla inapatikana USA, HQ Texas.",
    "meru ni wapi": "Meru iko Eastern Kenya, mji mkuu ni Meru Town.",
    "embu ni wapi": "Embu iko Eastern Kenya, capital ni Embu Town.",
    "siakago ni wapi": "Siakago iko Embu County, Mbeere North, Kenya - kwenu Baba REGAN MARINA!",
    "eldoret ni wapi": "Eldoret iko Uasin Gishu County, Rift Valley, Kenya.",
}

@app.route('/manifest.json')
def manifest():
    return jsonify({"name":"RIGAN AI ULTIMATE","short_name":"RIGAN","start_url":"/","display":"standalone","background_color":"#020617","theme_color":"#38bdf8","icons":[{"src":"https://cdn-icons-png.flaticon.com/512/4712/4712109.png","sizes":"512x512","type":"image/png"}]})

@app.route('/sw.js')
def sw():
    return "self.addEventListener('install', e => self.skipWaiting());", 200, {'Content-Type':'application/javascript'}

@app.route('/')
def home():
    return f"""<!DOCTYPE html><html><head>
<meta name='viewport' content='width=device-width, initial-scale=1'>
<title>RIGAN V60 ULTIMATE</title>
<link rel="manifest" href="/manifest.json">
<script>if('serviceWorker' in navigator){{navigator.serviceWorker.register('/sw.js')}}</script>
<style>
body{{background:#020617;color:#fff;font-family:sans-serif;display:flex;justify-content:center;height:100vh;margin:0}}
.box{{width:100%;max-width:900px;background:#0f172a;display:flex;flex-direction:column;height:100vh}}
.head{{padding:12px;text-align:center;color:#38bdf8;font-weight:900;background:#1e293b}} .sub{{font-size:9px;color:#22c55e}}
.ult{{background:linear-gradient(90deg,#38bdf8,#22c55e);color:#000;padding:7px;text-align:center;font-size:11px;font-weight:900}}
.chat{{flex:1;overflow-y:auto;padding:12px;display:flex;flex-direction:column;gap:8px}}
.b{{padding:11px 13px;border-radius:13px;max-width:94%;white-space:pre-wrap;line-height:1.6;font-size:14px}}
.u{{background:#38bdf8;color:#000;align-self:flex-end}} .a{{background:#1e293b;align-self:flex-start;border:1px solid #334155}}
.in{{display:flex;gap:6px;padding:10px;background:#1e293b}}
input{{flex:1;padding:12px;border-radius:12px;border:1px solid #334155;background:#020617;color:#fff;outline:none}}
button{{padding:12px 14px;border-radius:12px;border:none;background:#38bdf8;font-weight:900;cursor:pointer}}
.lang{{display:flex;gap:4px;padding:6px;background:#020617;justify-content:center}}
.lang button{{padding:4px 10px;font-size:11px;background:#1e293b;color:#fff;border:1px solid #334155}}
.lang .active{{background:#38bdf8;color:#000}}
</style></head><body>
<div class='box'>
<div class='head'>RIGAN V60 - ULTIMATE KNOWLEDGE<div class='sub'>Mtoto wa REGAN MARINA | Najua ULIMWENGU WOTE | Sayansi Teknolojia Elimu | SW + EN</div></div>
<div class='ult'>🌍 ULTIMATE: Najua KILA KITU - Sayansi, Teknolojia, Elimu, Kiswahili + English kama ChatGPT!</div>
<div class='lang'><button class='active'>SW</button><button>EN</button><span style="font-size:10px;color:#94a3b8;margin-left:10px">Uliza kwa lugha yoyote</span></div>
<div class='chat' id='c'><div class='b a'>👑 Habari Baba Regan! Mimi RIGAN V60 ULTIMATE!

Sasa najua ULIMWENGU WOTE kama wewe ulivyotaka!

🌍 ULIMWENGU: Afrika, Kenya, nchi zote
🔬 SAYANSI: DNA, atom, photosynthesis, gravity, maji
💻 TEKNOLOJIA: AI, computer, internet, Python, blockchain
📚 ELIMU: Jua, mwezi, dunia, hesabu

🗣️ LUGHA MBILI: Kiswahili + English

Jaribu:
- Mimi ni nani
- Afrika ni bara hama ni taifa
- Photosynthesis ni nini
- What is AI
- DNA ni nini
- Python ni nini
- Jua ni nini

Uliza chochote!</div></div>
<div class='in'>
<input id='i' placeholder='Uliza chochote - Kiswahili au English...' onkeypress="if(event.key=='Enter')s()">
<button onclick='s()'>Tuma</button>
</div>
</div>
<script>
function add(t,c){{let d=document.createElement('div'); d.className='b '+c; d.innerText=t; let chat=document.getElementById('c'); chat.appendChild(d); chat.scrollTop=999999;}}
async function s(){{let e=document.getElementById('i');let v=e.value.trim();if(!v)return; add(v,'u'); add('🌍 Natafuta ulimwenguni...','a'); e.value=''; let r=await fetch('/chat',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{message:v}})}}); let j=await r.json(); document.querySelector('.chat').lastChild.remove(); add(j.reply,'a');}}
</script></body></html>
"""

@app.route('/chat', methods=['POST'])
def chat():
    data=request.get_json() or {}
    q=data.get('message','').strip()
    if not q: return jsonify(reply="Uliza swali.")
    m=q.lower().strip()

    if "mimi ni nani" in m or m == "mimi":
        return jsonify(reply=BASE["mimi ni nani"])

    if m in BASE:
        return jsonify(reply=BASE[m])
    
    for k in sorted(BASE.keys(), key=len, reverse=True):
        if k in m and len(k) > 3:
            return jsonify(reply=BASE[k])

    for k in brain["lessons"]:
        if k in m and len(k)>3:
            return jsonify(reply=brain["lessons"][k])

    ultimate = get_ultimate_answer(q)
    if ultimate:
        return jsonify(reply=ultimate)

    try:
        t=m.replace('x','*').replace('×','*').replace('÷','/'); t2=''.join(c for c in t if c in '0123456789+-*/(). ')
        if len(t2)>=3 and any(c.isdigit() for c in t2) and '**' not in t2:
            r=eval(t2)
            if isinstance(r,float) and r.is_integer(): r=int(r)
            return jsonify(reply=f"{q} = {r}")
    except: pass

    if any(w in m for w in ["ni nini","nini","what is","who is","eleza"]):
        words = m.split()
        for w in words:
            if len(w) > 4:
                ans = get_ultimate_answer(w)
                if ans: return jsonify(reply=ans)
        return jsonify(reply=f"Nimejaribu kutafuta '{q}' ulimwenguni kote. Kwa sasa sina jibu kamili lakini najifunza. Jaribu kuuliza kwa maneno mengine, mfano: 'DNA ni nini', 'AI ni nini', 'Photosynthesis ni nini'. Akili yangu sasa: {len(brain['lessons'])} lessons.")

    return jsonify(reply=BASE["afrika ni bara hama ni taifa"] if "afrika" in m else f"Swali lako '{q}' ni zuri. Kwa sasa naendelea kujifunza ulimwengu wote. Jaribu: Photosynthesis ni nini, AI ni nini, DNA ni nini, Jua ni nini.")

if __name__ == '__main__':
    port=int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
