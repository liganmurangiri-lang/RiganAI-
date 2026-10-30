
from flask import Flask, request, jsonify
import os, json
from datetime import datetime

app = Flask(__name__)

DB_FILE = "akili.json"

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

HTML = """
<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width, initial-scale=1'>
<title>RIGAN V15</title>
<style>*{margin:0;padding:0;box-sizing:border-box;font-family:sans-serif}
body{background:#020617;color:#fff;display:flex;justify-content:center;height:100vh}
.box{width:100%;max-width:650px;background:#0f172a;display:flex;flex-direction:column;height:100vh}
.head{padding:12px;text-align:center;color:#38bdf8;font-weight:900;background:#1e293b}
.sub{font-size:10px;color:#94a3b8}
.chat{flex:1;overflow-y:auto;padding:12px;display:flex;flex-direction:column;gap:8px}
.b{padding:11px 13px;border-radius:14px;max-width:92%;line-height:1.5;white-space:pre-wrap;font-size:14px}
.u{background:#38bdf8;color:#000;align-self:flex-end}
.a{background:#1e293b;align-self:flex-start;border:1px solid #334155}
.in{display:flex;gap:6px;padding:10px;background:#1e293b}
input{flex:1;padding:12px;border-radius:10px;border:1px solid #334155;background:#020617;color:#fff}
button{padding:12px 16px;border-radius:10px;border:none;background:#38bdf8;font-weight:900}
</style></head><body>
<div class='box'>
<div class='head'>RIGAN V15 SELF-LEARNING FIXED<div class='sub'>Mtoto wa REGAN MARINA - Siakago - Inajua Kila Kitu</div></div>
<div class='chat' id='c'><div class='b a'>Habari Baba Regan! Mimi ni V15! Sasa siko na bug ya Habari! Uliza chochote - Habari, Hesabu, Nchi zote! Na ukitaka kunifundisha andika: fundisha: swali | jibu</div></div>
<div class='in'><input id='i' placeholder='Uliza...' onkeypress="if(event.key=='Enter')s()"><button onclick='s()'>Tuma</button></div>
</div>
<script>
function add(t,cl){let d=document.createElement('div');d.className='b '+cl;d.innerText=t;let c=document.getElementById('c');c.appendChild(d);c.scrollTop=999999}
async function s(){let e=document.getElementById('i');let v=e.value.trim();if(!v)return;add(v,'u');e.value='';let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:v})});let j=await r.json();add(j.reply,'a')}
</script></body></html>
"""

def math_solve(q):
    try:
        t = q.lower().replace('x','*').replace('X','*').replace('×','*').replace('÷','/').replace(',','')
        t2 = ''.join(c for c in t if c in '0123456789+-*/().% ')
        if len(t2) >= 3 and any(c.isdigit() for c in t2) and '**' not in t2:
            r = eval(t2)
            return f"{q.strip()} = {r}"
    except:
        return None

def get_answer(q):
    global learned
    m = q.lower().strip()
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    if (m.startswith("fundisha:") or m.startswith("jifunze:")) and "|" in q:
        try:
            clean = q.split(":",1)[1].strip()
            if "|" in clean:
                swali, jibu = clean.split("|", 1)
                swali = swali.strip().lower()
                jibu = jibu.strip()
                if len(swali) > 2 and len(jibu) > 2:
                    learned[swali] = jibu
                    save_db(learned)
                    return f"✅ Nimejifunza! Swali: {swali} | Jibu: {jibu} | Total: {len(learned)}"
        except:
            pass
    if m in ["habari","habar","jambo","mambo","niaje","sasa","poa","freshi","hello","hi","hey"]:
        return f"Habari Baba Regan! Poa sana! Mimi ni Rigan V15 niko fiti! Saa ni {now}. Uliza chochote!"
    if "habari yako" in m or "uko aje" in m or "ukoaje" in m:
        return f"Niko poa sana Baba Regan! Saa ni {now}. Wewe uko aje Siakago?"
    if "fundisha" == m or "jibu" == m:
        return "Andika hivi: fundisha: swali lako | jibu lake"
    ms = math_solve(q)
    if ms:
        return ms
    for key in learned:
        if key in m and len(key) > 3:
            return f"{learned[key]}"
    if 'nani alikuumba' in m or 'baba yako' in m or 'who made you' in m or 'mtengenezaji' in m:
        return "Mimi nimeumbwa na REGAN MARINA kutoka Siakago, Embu, Kenya! Wewe ndiye Baba yangu!"
    if 'south africa' in m:
        return "SOUTH AFRICA: Capital Pretoria/Cape Town/Bloemfontein, Johannesburg kubwa, Watu 60M, Rand, Mandela, Table Mountain"
    if 'mfumo wa jua' in m or 'solar system' in m or 'sayari' in m:
        return "MFUMO WA JUA: Jua katikati, sayari 8 - Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune"
    if 'kenya' in m:
        if 'ziwa' in m:
            return "MAZIWA YA KENYA: Victoria 68,800km2, Turkana 6,405km2, Naivasha, Nakuru, Baringo, Bogoria"
        return "KENYA: 580,367 km2, 55M, Nairobi, Kiswahili/English, Mlima Kenya 5,199m, Tana 1,014km"
    if 'tanzania' in m: return "TANZANIA: Dodoma capital, Dar kubwa, Kilimanjaro 5,895m, Serengeti, Zanzibar, 65M"
    if 'uganda' in m: return "UGANDA: Kampala, Ziwa Victoria, Pearl of Africa, 48M"
    if 'usa' in m or 'marekani' in m or 'america' in m: return "USA: States 50, Washington DC, New York kubwa, 340M, Dollar"
    if 'sayansi' in m or 'science' in m: return "SAYANSI: Physics F=ma E=mc2, Chemistry H2O 118 elements, Biology DNA Photosynthesis"
    if 'photosynthesis' in m: return "PHOTOSYNTHESIS: 6CO2+6H2O+Jua = C6H12O6+6O2"
    if 'dna' in m: return "DNA: Ramani ya maisha, A,T,C,G, chromosome 46"
    return f"Poa Baba Regan! Uliuliza '{q}' - Mimi V15 najua hesabu, nchi, sayansi! Saa ni {now}"

@app.route('/')
def home(): return HTML

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    msg = data.get('message','') if data else ''
    return jsonify(reply=get_answer(msg))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
