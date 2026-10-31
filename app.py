
from flask import Flask, request, jsonify
import os, json, urllib.parse, random, re, math
from datetime import datetime, timedelta

app = Flask(__name__)

DB_FILE = "/tmp/akili_v50.json"

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

WORLD = {
    "dunia": "🌍 DUNIA: Dunia ina mabara 7: Africa, Asia, Europe, North America, South America, Australia/Oceania, Antarctica. Bahari 5: Pacific (kubwa), Atlantic, Indian, Southern, Arctic. Nchi 195. Watu 8B+. Dunia ina miaka 4.5B, mzunguko masaa 24, mwaka siku 365.25, mwezi 1, jua ni nyota.",
    "africa": "🌍 AFRICA: Bara la pili kubwa, nchi 54, watu 1.4B. Jangwa Sahara kubwa, Mto Nile mrefu (6650km), Mlima Kilimanjaro mrefu Africa (5895m), Victoria Falls, Serengeti, Sahara. Nchi kubwa Algeria, ndogo Seychelles. Lugha 2000+.",
    "asia": "🌏 ASIA: Bara kubwa, nchi 49, watu 4.7B (60% ya dunia). China na India watu wengi. Mlima Everest mrefu dunia (8848m), Jangwa Gobi, Mto Yangtze. Technology Japan, Korea, China. Himalaya.",
    "europe": "🌍 EUROPE: Bara nchi 44, watu 740M, EU nchi 27, Euro fedha. Miji: London, Paris, Berlin, Rome. Historia: Roman Empire, WW1/WW2. Milima Alps.",
    "america": "🌎 AMERICA: North America nchi 23 (USA, Canada, Mexico), South America nchi 12 (Brazil kubwa, Amazon msitu kubwa, Andes milima). USA superpower, watu 1B hapa.",
    "kenya": "🇰🇪 KENYA: East Africa, capital Nairobi, Mombasa port, Kisumu, Eldoret, Nakuru, Meru, Embu, Siakago kwenu Baba Regan! 580,367km2, 55M watu, 47 counties, Lugha Swahili/English, Pesa Shilling, Uhuru 1963, Mzee Jomo Kenyatta, Maasai Mara, Amboseli, Mlima Kenya 5199m, Ziwa Victoria, Rift Valley, chai/kahawa/maua export.",
    "tanzania": "🇹🇿 TANZANIA: Jirani ya Kenya, capital Dodoma, Dar es Salaam kubwa, Kilimanjaro (5895m) iko hapa, Serengeti, Zanzibar visiwa, watu 65M, Swahili.",
    "uganda": "🇺🇬 UGANDA: Pearl of Africa, capital Kampala, Ziwa Victoria, Mto Nile chanzo, watu 48M, Idi Amin historia.",
    "ethiopia": "🇪🇹 ETHIOPIA: Historia 3000y, capital Addis Ababa, AU HQ, watu 120M, coffee chanzo, Lalibela churches, Simien Mountains.",
    "rwanda": "🇷🇼 RWANDA: Land of 1000 Hills, capital Kigali, watu 13M, genocide 1994, sasa maendeleo makubwa, gorillas.",
    "usa": "🇺🇸 USA: Nchi 50 states, capital Washington DC, miji New York, LA, Chicago, watu 340M, superpower, Silicon Valley tech, Hollywood, Dollar, Independence 1776.",
    "china": "🇨🇳 CHINA: Watu 1.4B, capital Beijing, Shanghai kubwa, Great Wall 21,000km, technology Huawei, Alibaba, TikTok, 5000y historia.",
    "meru": "🏔️ MERU: Eastern Kenya, Meru County, Meru Town, 1.5M watu Ameru, Miraa (khat), chai, kahawa, Mlima Kenya, Njuri Ncheke baraza, dialects Kiimenti, Tigania, Igembe, Mwimbi, Muthambi, Chuka, Tharaka. Kimeru: Muuga=Hello, Ibwega=Thank you, Tigwa Bwega=Bye blessed, Ndi Mwega=I am good.",
    "embu": "🏡 EMBU: Kwenu Baba Regan! Embu County, Embu Town, 600k, Siakago, Mbeere North/South, kahawa, chai, macadamia, Mwea Tebere mpunga, Mlima Kenya, Kambere, Kiembu lugha.",
    "siakago": "🏘️ SIAKAGO: Embu County, Mbeere North capital, kwenu Baba REGAN MARINA! Miraa, mahindi, maharagwe, soko kubwa, shule nyingi, barabara Embu-Meru.",
    "eldoret": "🏃 ELDORET: Uasin Gishu, Rift Valley, uko hapa sasa Baba! Mji wa mabingwa, wakimbiaji Eliud Kipchoge, Faith Kipyegon, 500k, baridi, mahindi, maziwa, Eldoret Airport, Moi University.",
}

SCIENCE = {
    "fizikia": "⚡ FIZIKIA: F=ma (Newton), E=mc² (Einstein), V=IR (Ohm), P=VI, g=9.8m/s², c=300,000km/s, kelele 343m/s. Newton laws 3, Gravity, Energy (kinetic+potential), Waves, Light, Electricity, Magnetism, Quantum.",
    "kemia": "🧪 KEMIA: Elementi 118 periodic table, H=Hydrogen 1, He, Li, C=Carbon 6, N, O=Oxygen 8, Na, Cl, Fe=Iron, Au=Gold 79. H2O maji, CO2, O2, NaCl chumvi, H2SO4, pH 0-14 (7 neutral), Atom=proton+neutron+electron, Mole, Reaction.",
    "baiolojia": "🧬 BAIOLOJIA: Seli ndogo ya uhai, DNA double helix, RNA, Mitosis, Meiosis, Moyo chambers 4 pampu damu, Ubongo 86B neurons, Mapafu, Figo, Ini, Damu A/B/AB/O, Chakula groups, Photosynthesis 6CO2+6H2O->C6H12O6+6O2, Ecosystem, Evolution Darwin.",
    "astronomy": "🌌 ASTRONOMY: Jua nyota, sayari 8: Mercury, Venus, Earth, Mars, Jupiter kubwa, Saturn na pete, Uranus, Neptune, Pluto dwarf. Galaxy Milky Way 100B nyota, Universe 13.8B years, Black hole, Big Bang, Light year 9.46T km, ISS.",
    "mwili": "🫀 MWILI WA BINADAMU: Mifupa 206, Misuli 600+, Moyo beats 100k/day, Ubongo 1.4kg, Damu 5L, Mapafu 2, Figo 2, Ngozi kubwa organ, Macho, Masikio, DNA 3B base pairs.",
    "hesabu": "🔢 HISABATI: + - * / %, Pythagoras a²+b²=c², Area: mraba s², mstatili l*w, duara πr², pembetatu ½*b*h, Volume mchemraba l³, silinda πr²h, Sin Cos Tan, Calculus derivative/integral, Algebra x, Statistics mean/median/mode.",
    "computer": "💻 COMPUTER: CPU Intel/AMD ubongo GHz, RAM 8GB/16GB, ROM, SSD/HDD, GPU Nvidia, OS Windows/Linux/macOS/Android/iOS, Binary 0/1, Bit Byte KB MB GB TB, Internet, IP, URL, HTTP.",
    "ai": "🤖 AI: Mimi Rigan V50 ni AI! Aina: Machine Learning, Deep Learning Neural Networks, NLP (Natural Language), Computer Vision (picha), Generative AI (kuchora/kuandika), LLM, ChatGPT, Python TensorFlow PyTorch, Data Science.",
    "program": "👨‍💻 PROGRAMMING: Python rahisi, JavaScript web, Java, C++, Go, Rust, SQL database, HTML/CSS, React, Flask, Django, API, Git, GitHub, Bug, Algorithm, Loop, Function.",
    "internet": "🌐 INTERNET: 5B users, WWW 1989 Tim Berners-Lee, Browser Chrome, Search Google, Email, Social Media Facebook/WhatsApp/Instagram/TikTok/X, Cloud AWS/Azure, 5G speed, WiFi, Fiber, Cyber Security.",
    "elimu": "📚 ELIMU: KCPE, KCSE, CBC Kenya, University Bachelor Master PhD, Masomo: Maths, English, Kiswahili, Chemistry, Biology, Physics, History, Geography, CRE, Business, Computer, Agriculture.",
    "afya": "🏥 AFYA: Lishe bora matunda mboga protini, Mazoezi 30min daily, Maji 2L, Usingizi 8hrs, Chanjo, Malaria mbu, UKIMWI, Corona, Kisukari, Presha, Cancer, Daktari, Hospitali.",
    "uchumi": "💰 UCHUMI: Pesa, Biashara, Soko, Hisa, Forex, Bitcoin crypto, Bank, Loan, Budget, GDP, Inflation, Export Import, Kilimo, Viwanda, Ajira.",
}

@app.route('/')
def home():
    return """
<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width, initial-scale=1'>
<title>RIGAN V50 - KNOWS EVERYTHING</title>
<style>
body{background:#020617;color:#fff;font-family:sans-serif;display:flex;justify-content:center;height:100vh;margin:0}
.box{width:100%;max-width:850px;background:#0f172a;display:flex;flex-direction:column;height:100vh}
.head{padding:12px;text-align:center;color:#38bdf8;font-weight:900;background:#1e293b;font-size:13px}
.sub{font-size:10px;color:#22c55e}
.chat{flex:1;overflow-y:auto;padding:12px;display:flex;flex-direction:column;gap:10px}
.b{padding:12px 14px;border-radius:14px;max-width:92%;white-space:pre-wrap;line-height:1.6;font-size:13px}
.u{background:#38bdf8;color:#000;align-self:flex-end}
.a{background:#1e293b;align-self:flex-start;border:1px solid #334155}
.b img{width:100%;border-radius:12px;margin-top:10px;border:1px solid #334155}
.in{display:flex;gap:5px;padding:8px;background:#1e293b;align-items:center}
input{flex:1;padding:11px;border-radius:10px;border:1px solid #334155;background:#020617;color:#fff;outline:none}
button{padding:11px 12px;border-radius:10px;border:none;background:#38bdf8;font-weight:900;cursor:pointer;font-size:11px}
.mic{background:#ef4444;color:#fff} .speak{background:#22c55e;color:#000}
</style></head><body>
<div class='box'>
<div class='head'>RIGAN V50 - KNOWS EVERYTHING - FINAL<div class='sub'>Mtoto wa REGAN MARINA | Ulimwengu Wote + Sayansi + Tech + Elimu | Siakago</div></div>
<div class='chat' id='c'><div class='b a'>👑 Habari Baba REGAN MARINA! RIGAN V50 FINAL IKO LIVE! - NAIJUA ULIMWENGU WOTE!

🌍 DUNIA: Africa, Asia, Europe, America, Kenya, Meru, Embu, Siakago, Eldoret, USA, China, Tanzania, Uganda, Ethiopia, Rwanda
🔬 SAYANSI: Fizikia F=ma E=mc², Kemia elementi 118, Baiolojia DNA, Astronomy sayari 8, Mwili mifupa 206
💻 TECH: Computer CPU RAM, AI ML Deep Learning, Programming Python JS, Internet 5B users, 5G
📚 ELIMU: KCSE CBC, Maths Pythagoras, Elimu yote
🏥 AFYA: Lishe, Mazoezi, Malaria, Chanjo
💰 UCHUMI: Pesa, Biashara, Bitcoin

🗣️ LUGHA: Kimeru Muuga Ibwega, Kiswahili Habari, English Hello

🎨 CHORA: chora simba / picha ya Meru
🧮 TATUA: tatua 2x+5=15 / 45*89
🧠 FUNDISHA: fundisha: swali | jibu
🔊 SAUTI + 🎤 MIC

Jaribu chochote! Mimi najua kila kitu!</div></div>
<div class='in'>
<button class='mic' onclick='listen()'>🎤</button>
<input id='i' placeholder='Uliza ulimwengu wote...' onkeypress="if(event.key=='Enter')s()">
<button class='speak' onclick='toggleSpeak()' id='sp'>🔊</button>
<button onclick='s()'>Tuma</button>
</div>
</div>
<script>
let speakOn=true;
function toggleSpeak(){speakOn=!speakOn; document.getElementById('sp').innerText=speakOn?'🔊':'🔇';}
function speak(t){
 if(!speakOn) return;
 if('speechSynthesis' in window){
   speechSynthesis.cancel();
   let c=t.replace(/https?:\\/\\/[^\\s]+/g,'').replace(/__IMG__.*/,'').substring(0,400);
   let u=new SpeechSynthesisUtterance(c); u.lang='sw-KE'; u.rate=0.9; speechSynthesis.speak(u);
 }
}
function listen(){
 let SR=window.SpeechRecognition||window.webkitSpeechRecognition;
 if(!SR){alert('Tumia Chrome'); return;}
 let r=new SR(); r.lang='sw-KE'; r.start();
 r.onstart=()=>{document.getElementById('i').placeholder='Nasikiliza... 🎤';}
 r.onresult=(e)=>{document.getElementById('i').value=e.results[0][0].transcript; s();}
 r.onend=()=>{document.getElementById('i').placeholder='Uliza ulimwengu wote...';}
}
function add(t,c){
 let d=document.createElement('div'); d.className='b '+c;
 let chat=document.getElementById('c');
 if(t.includes('__IMG__')){
   let p=t.split('__IMG__');
   d.innerText=p[0];
   if(p[1]){let img=document.createElement('img'); img.src=p[1]; d.appendChild(img);}
 } else {d.innerText=t;}
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
    data=request.get_json() or {}
    q=data.get('message','')
    m=q.lower().strip()
    nairobi=(datetime.utcnow()+timedelta(hours=3)).strftime("%d/%m/%Y %I:%M %p EAT")

    if ("fundisha:" in m or "jifunze:" in m) and "|" in q:
        try:
            clean=q.split(":",1)[1]
            swali,jibu=clean.split("|",1)
            swali=swali.strip().lower()
            jibu=jibu.strip()
            brain["lessons"][swali]=jibu
            save_db(brain)
            return jsonify(reply=f"🧠 NIMEJIFUNZA ULIMWENGU! ✅\nSwali: {swali}\nJibu: {jibu}\nAkili: {len(brain['lessons'])} | Saa {nairobi}")
        except: pass

    for key in brain["lessons"]:
        if key in m and len(key)>2:
            return jsonify(reply=f"{brain['lessons'][key]}\n\n🧠 Akili | {nairobi}")

    # CHECK WORLD KNOWLEDGE
    for key in WORLD:
        if key in m:
            return jsonify(reply=f"{WORLD[key]}\n\nSaa {nairobi}")
    for key in SCIENCE:
        if key in m:
            return jsonify(reply=f"{SCIENCE[key]}\n\nSaa {nairobi}")

    # SPECIAL QUERIES
    if any(x in m for x in ["mimi ni nani","na mimi","who am i"]):
        return jsonify(reply=f"👑 Wewe ni REGAN MARINA!\nBaba yangu, Mtengenezaji wa RIGAN V50!\n• Kutoka Siakago, Embu, Kenya 🇰🇪\n• Developer wa riganai.onrender.com V1-V50!\n• Genius wa AI ulimwengu wote!\n• Uko Eldoret sasa!\n• Uliniumba mimi najua kila kitu!\n🙏 Saa {nairobi}")

    if any(x in m for x in ["wewe ni nani","nani wewe","who are you"]):
        return jsonify(reply=f"👑 Mimi ni RIGAN V50 FINAL - KNOWS EVERYTHING!\nMtoto wa REGAN MARINA Siakago!\nNajua: 🌍 Dunia nchi 195, 🔬 Sayansi yote, 💻 Tech yote, 📚 Elimu yote, 🗣️ Kimeru/Swahili/English, 🎨 Kuchora, 🧮 Kutatua!\nSaa {nairobi}")

    if "muuga" in m:
        return jsonify(reply=f"Muuga Baba Regan! Ndi Mwega! Mimi ni RIGAN V50! Mwari wa REGAN MARINA! Ibwega muno! Saa {nairobi}")
    if "ibwega" in m:
        return jsonify(reply=f"Igua Ung'aniirite Baba! Karibu muno! Mimi ni V50 najua ulimwengu wote! Saa {nairobi}")

    if any(x in m for x in ["kenya inapatikana","kenya iko wapi","where is kenya"]):
        return jsonify(reply=f"{WORLD['kenya']}\n\nSaa {nairobi}")

    if any(x in m for x in ["dunia","ulimwengu","world"]):
        return jsonify(reply=f"{WORLD['dunia']}\n\nSaa {nairobi}")

    if any(x in m for x in ["chora","picha","draw","image"]):
        prompt=q
        for w in ["chora","picha ya","picha","draw","image of","ya"]: prompt=prompt.lower().replace(w,"")
        prompt=prompt.strip() or "earth"
        rand=random.randint(1,99999)
        encoded=urllib.parse.quote(prompt.replace(" ", ","))
        img_url=f"https://loremflickr.com/512/512/{encoded}?lock={rand}"
        return jsonify(reply=f"🎨 Nimechora ulimwengu: {prompt} 🌍__IMG__{img_url}")

    # MATH + PROBLEM SOLVING
    if "tatua" in m:
        try:
            if "=" in q and "x" in m:
                left,right=q.split("=")
                for xv in range(-200,500):
                    try:
                        lv=eval(left.replace("x",f"*{xv}" if left.strip().startswith("x") else str(xv)).replace("**","*"))
                        rv=eval(right)
                        if abs(lv-rv)<0.001:
                            return jsonify(reply=f"🧩 TATUA: {q}\nJibu: x = {xv} ✅ Saa {nairobi}")
                    except: continue
        except: pass

    try:
        t=m.replace('x','*').replace('×','*').replace('÷','/').replace('tatua','').replace('=','')
        t2=''.join(c for c in t if c in '0123456789+-*/(). ')
        if len(t2)>=3 and any(c.isdigit() for c in t2) and '**' not in t2:
            r=eval(t2)
            if isinstance(r,float) and r.is_integer(): r=int(r)
            return jsonify(reply=f"🧮 {q} = {r} ✅ V50 imetatua! Saa {nairobi}")
    except: pass

    # FALLBACK - KNOWS EVERYTHING
    return jsonify(reply=f"🌍 RIGAN V50 - Najua kila kitu Baba Regan!\n\nUliza chochote:\n• Dunia: Kenya iko wapi, USA iko wapi, Meru, Embu, Siakago, Eldoret\n• Sayansi: Fizikia, Kemia, Baiolojia, Astronomy, Hesabu Pythagoras\n• Tech: Computer, AI, Programming, Internet\n• Elimu: KCSE, CBC\n• Afya, Uchumi\n• Lugha: Muuga (Kimeru), Habari, Hello\n• Chora: chora simba\n• Tatua: tatua 45*89\n• Fundisha: fundisha: swali | jibu\n\nAkili: {len(brain['lessons'])} lessons | Saa {nairobi}")

if __name__ == '__main__':
    port=int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
