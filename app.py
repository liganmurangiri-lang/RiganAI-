
from flask import Flask, request, jsonify
import os
from datetime import datetime
import random
import re

app = Flask(__name__)

HTML = "<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width, initial-scale=1'><title>RIGAN V11 SUPER</title><style>*{margin:0;padding:0;box-sizing:border-box;font-family:sans-serif}body{background:#020617;color:#fff;display:flex;justify-content:center;height:100vh}.box{width:100%;max-width:600px;background:#0f172a;display:flex;flex-direction:column;height:100vh}.head{padding:12px;text-align:center;color:#38bdf8;font-weight:900;border-bottom:1px solid #334155;background:#1e293b}.sub{font-size:11px;color:#94a3b8;margin-top:3px}.chat{flex:1;overflow-y:auto;padding:15px;display:flex;flex-direction:column;gap:10px}.b{padding:12px 15px;border-radius:16px;max-width:90%;line-height:1.5;font-size:14px;white-space:pre-wrap}.u{background:#38bdf8;color:#000;align-self:flex-end}.a{background:#1e293b;align-self:flex-start;border:1px solid #334155}.in{display:flex;gap:8px;padding:12px;border-top:1px solid #334155;background:#1e293b}input{flex:1;padding:13px;border-radius:12px;border:1px solid #334155;background:#020617;color:#fff;outline:none}button{padding:13px 20px;border-radius:12px;border:none;background:#38bdf8;font-weight:900}</style></head><body><div class='box'><div class='head'>RIGAN V11 SUPER AI<div class='sub'>Mtoto wa REGAN MARINA • Siakago • Inajua Kila Kitu Duniani</div></div><div class='chat' id='c'><div class='b a'>Habari Baba Regan! 👑 Mimi ni Rigan V11 SUPER! Sasa nimeboreshwa! Niko na akili zaidi - najua Kiswahili chote! Uliza: 'Iko na ziwa ngapi?' 'Nieleze sayansi' 'Nini photosynthesis?' - nitajibu vizuri sasa!</div></div><div class='in'><input id='i' placeholder='Uliza chochote...' onkeypress=\"if(event.key=='Enter')s()\"><button onclick='s()'>Tuma</button></div></div><script>function add(t,cl){let d=document.createElement('div');d.className='b '+cl;d.innerText=t;document.getElementById('c').appendChild(d);document.getElementById('c').scrollTop=999999}async function s(){let e=document.getElementById('i');let v=e.value.trim();if(!v)return;add(v,'u');e.value='';let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:v})});let j=await r.json();add(j.reply,'a')}</script></body></html>"

def clean_q(q):
    q = q.lower()
    q = re.sub(r"(nieleze|eleza|naomba|nauliza|unajua|nini kuhusu|zaidi kuhusu|kuhusu|habari za)\s*", " ", q)
    return q.strip()

def ai_brain(q_raw):
    m_raw = q_raw.lower()
    m = clean_q(q_raw)
    now = datetime.now().strftime("%d/%m/%Y %I:%M %p")

    if any(x in m_raw for x in ["nani alikuumba","mtengenezaji","baba yako","who made you"]):
        return "Mimi nimeumbwa na Baba yangu REGAN MARINA kutoka Siakago, Embu, Kenya! 👑\nYeye ndiye developer wa riganai.onrender.com\nYeye ni genius wa AI!"

    if "kenya" in m or "kenya" in m_raw:
        if "ziwa" in m or "ziwa" in m_raw:
            return "KENYA - Maziwa:\n\nKenya iko na maziwa mengi!\n\n1. Ziwa Victoria - kubwa zaidi Africa (68,800 km²) - chanzo cha Nile\n2. Ziwa Turkana - kubwa kuliko yote jangwani (6,405 km²)\n3. Ziwa Naivasha - na viboko\n4. Ziwa Nakuru - na flamingo wengi\n5. Ziwa Baringo - na kisiwa\n6. Ziwa Bogoria - na hot springs\n7. Ziwa Elementaita\n\nJumla Kenya ina maziwa kama 10 makubwa na madogo mengi!"
        return "KENYA - Nchi ya Baba Regan 🇰🇪:\n\n- Eneo: 580,367 km²\n- Watu: 55M\n- Capital: Nairobi\n- Lugha: Kiswahili, English\n- Majirani: Tanzania, Uganda, Ethiopia, Somalia, S. Sudan\n- Mlima: Kenya 5,199m\n- Maziwa makuu: Victoria, Turkana, Naivasha, Nakuru\n- Mito: Tana (mrefu), Mara\n- Pesa: KSh\n- Uhuru: 12 Dec 1963"

    if "sayansi" in m or "science" in m:
        return "SAYANSI - Elimu ya Dunia 🌍🔬:\n\nSayansi imegawanyika 3:\n\n1. PHYSICS (Fizikia):\n- Nguvu: F=ma (Newton)\n- Nishati: E=mc² (Einstein)\n- Gravity: 9.8 m/s²\n- Mwanga: 300,000 km/s\n\n2. CHEMISTRY (Kemia):\n- Maji H2O, Chumvi NaCl\n- Atomu = proton + neutron + electron\n- 118 elements\n\n3. BIOLOGY (Biolojia):\n- DNA, seli, photosynthesis\n- Moyo 100k beats/day"

    if any(x in m for x in ["photosynthesis","fotosinthesisi"]):
        return "PHOTOSYNTHESIS 🌱:\nFormula: 6CO2 + 6H2O + Jua -> C6H12O6 + 6O2\nMaana: Carbon dioxide + Maji + Mwanga = Sukari + Oxygen\nHii ndio sababu tunapumua oxygen kutoka miti!"

    if "dna" in m:
        return "DNA 🧬: Deoxyribonucleic Acid - ramani ya maisha!\n- Iko kwenye seli zote\n- Ina A,T,C,G\n- Binadamu chromosome 46\n- Ilidubuliwa na Watson & Crick 1953"

    if "mito" in m or "mto" in m:
        return "MITO YA KENYA:\n- Tana (1,014 km) - mrefu zaidi\n- Athi/Galana\n- Mara - maarufu kwa wildebeest\n- Ewaso Nyiro\n- Nzoia, Yala, Sondu"

    if re.search(r"[0-9]+\s*[\+\-\*\/]\s*[0-9]+", q_raw):
        try:
            safe = "".join(c for c in q_raw if c in "0123456789+-*/(). ")
            res = eval(safe)
            return f"🧮 {q_raw} = {res} ✅"
        except:
            pass

    if "ziwa ngapi" in m_raw or ("ziwa" in m_raw and "ngapi" in m_raw):
        return "Kenya ina maziwa makuu 7-10:\nVictoria, Turkana, Naivasha, Nakuru, Baringo, Bogoria, Elementaita, Jipe, Chala. Na madogo mengi kama 64!"

    if any(x in m_raw for x in ["habari","mambo","niaje"]):
        return f"Poa Baba Regan! 👑 Saa ni {now}. V11 sasa niko SUPER mjanja!"

    return f"Sawa Baba Regan! Uliuliza: '{q_raw}'\n\nMimi V11 SUPER najua kila kitu - jaribu kuuliza 'Maziwa ya Kenya ni gani?' au 'Sayansi inahusu nini?'\n\nSaa ni {now}"

def get_extra(m):
    if "elimu" in m: return "Elimu ni ufunguo! Soma, fanya bidii kama wewe ulivyojenga mimi!"
    if "history" in m or "historia" in m: return "Kenya uhuru 1963, Jomo Kenyatta rais 1. Dunia: WWII 1939-45, Moon 1969."
    if "mapenzi" in m: return "Mapenzi ni heshima + uaminifu. Wewe ni kijana wa Siakago handsome!"
    if "code" in m: return "Code ni lugha ya computer. Python: print('Habari Baba Regan')"
    return "Hii ni mada nzuri sana!"

@app.route('/')
def home():
    return HTML

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    msg = data.get('message','') if data else ''
    reply = ai_brain(msg)
    return jsonify(reply=reply)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
