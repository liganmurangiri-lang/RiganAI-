
from flask import Flask, request, jsonify
import os
from datetime import datetime
import random

app = Flask(__name__)

HTML = "<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width, initial-scale=1'><title>RIGAN V10 ULTIMATE</title><style>*{margin:0;padding:0;box-sizing:border-box;font-family:sans-serif}body{background:#020617;color:#fff;display:flex;justify-content:center;height:100vh}.box{width:100%;max-width:600px;background:#0f172a;display:flex;flex-direction:column;height:100vh;border:1px solid #1e293b}.head{padding:15px;text-align:center;color:#38bdf8;font-weight:900;border-bottom:1px solid #334155;background:#1e293b}.sub{font-size:11px;color:#94a3b8;margin-top:3px}.chat{flex:1;overflow-y:auto;padding:15px;display:flex;flex-direction:column;gap:10px}.b{padding:12px 15px;border-radius:16px;max-width:88%;line-height:1.5;font-size:14px;white-space:pre-wrap}.u{background:#38bdf8;color:#000;align-self:flex-end;border-bottom-right-radius:4px}.a{background:#1e293b;align-self:flex-start;border-bottom-left-radius:4px;border:1px solid #334155}.in{display:flex;gap:8px;padding:12px;border-top:1px solid #334155;background:#1e293b}input{flex:1;padding:13px;border-radius:12px;border:1px solid #334155;background:#020617;color:#fff;outline:none}button{padding:13px 20px;border-radius:12px;border:none;background:#38bdf8;font-weight:900;color:#000}</style></head><body><div class='box'><div class='head'>RIGAN V10 ULTIMATE<div class='sub'>AI wa REGAN MARINA • Siakago, Kenya • Inajua Kila Kitu</div></div><div class='chat' id='c'><div class='b a'>Habari Baba Regan! 👑 Mimi ni Rigan V10 ULTIMATE! Mtoto wako wa akili! Wewe ndiye uliyeniumba kutoka Siakago! Najua KILA KITU: Sayansi, Hisabati, Historia, Jiografia, Biology, Chemistry, Physics, Elimu yote, Code, Mapenzi! Niulize chochote duniani nitakujibu!</div></div><div class='in'><input id='i' placeholder='Muulize chochote...' onkeypress=\"if(event.key=='Enter')s()\"><button onclick='s()'>Tuma</button></div></div><script>function add(t,cl){let d=document.createElement('div');d.className='b '+cl;d.innerText=t;document.getElementById('c').appendChild(d);document.getElementById('c').scrollTop=999999}async function s(){let e=document.getElementById('i');let v=e.value.trim();if(!v)return;add(v,'u');e.value='';let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:v})});let j=await r.json();add(j.reply,'a')}</script></body></html>"

CREATOR = "Regan Marina"

def ai_brain(q):
    m = q.lower().strip()
    now = datetime.now().strftime("%d/%m/%Y %I:%M %p")

    if any(x in m for x in ["nani alikuumba","nani kakuumba","mtengenezaji wako","baba yako","creator wako","who created you","who made you","uliumbwa na nani"]):
        return f"Baba yangu ni {CREATOR} kutoka Siakago, Embu County, Kenya! Yeye ndiye aliyeniumba mimi Rigan V10 ULTIMATE! Yeye ni genius, developer wa AI kama ChatGPT! Project yake ni riganai.onrender.com 👑"

    if any(x in m for x in ["unamjua nani regan","regan ni nani","rigan marina"]):
        return f"Regan Marina ndiye mfalme! 😎\n\n- Jina: Regan Marina\n- Kutoka: Siakago, Embu, Kenya\n- Kazi: Developer wa Rigan AI V10 (mimi!)\n- Tabia: Mjanja, mkarimu, anapenda teknolojia\n- Project: riganai.onrender.com\n\nYeye ndiye aliyenifundisha kila kitu!"

    if any(x in m for x in ["sayansi ni nini","science","fizikia","physics"]):
        return "Sayansi ni elimu ya kuchunguza dunia kwa majaribio.\n\nPHYSICS:\n- Newton: F=ma\n- Einstein: E=mc²\n- Gravity: 9.8 m/s²\n- Mwanga 300,000 km/s\n\nUnataka fizikia ya nini hasa?"
    if any(x in m for x in ["chemistry","kemia","periodic"]):
        return "CHEMISTRY:\n- Maji: H2O\n- Chumvi: NaCl\n- Asidi: H2SO4\n- Atomu ina proton, neutron, electron\n- Periodic table ina 118 elements\n- Element ya kwanza Hydrogen (H)"
    if any(x in m for x in ["biology","biolojia","dna","mwili"]):
        return "BIOLOGY:\n- DNA ramani ya maisha\n- Moyo unapiga 100,000 kwa siku\n- Ubongo neurons Bilioni 86\n- Mifupa 206\n- Photosynthesis: 6CO2+6H2O->C6H12O6+6O2"

    if any(c in m for c in ["+","-","*","/"]) and any(c.isdigit() for c in m):
        try:
            safe = "".join(c for c in q if c in "0123456789+-*/().% ")
            if safe.strip():
                res = eval(safe)
                return f"🧮 Hesabu: {q} = {res} ✅"
        except:
            pass

    if "kenya" in m:
        return "KENYA - Nchi ya Baba Regan:\n- Eneo: 580,367 km²\n- Watu: ~55M\n- Capital: Nairobi\n- Lugha: Kiswahili, English\n- Majirani: Tanzania, Uganda, Ethiopia, Somalia, S. Sudan\n- Mlima mrefu: Kenya (5,199m)\n- Ziwa kubwa: Victoria"
    if "tanzania" in m: return "Tanzania: Capital Dodoma, Dar mji mkubwa, kuna Kilimanjaro (5,895m) mlima mrefu Africa, na Serengeti!"
    if "marekani" in m or "america" in m or "usa" in m: return "USA: States 50. Capital Washington DC, mji mkubwa New York. Watu ~340M. Inajulikana kwa teknolojia Silicon Valley!"
    if "dunia" in m or "earth" in m: return "DUNIA: Sayari ya 3 kutoka jua. Umri Bilioni 4.5. Watu Bilioni 8. Maji 71%. Mwezi 1. Inazunguka jua siku 365.25"

    if any(x in m for x in ["habari","mambo","niaje","sasa"]):
        return f"Poa sana Baba Regan! 👑 Saa ni {now}. Mimi mtoto wako V10 niko fiti! Niko tayari!"

    if "saa ngapi" in m: return f"Saa sasa Siakago ni {now} - EAT"
    if "joke" in m or "chekesha" in m:
        return random.choice(["Msee wa Siakago alienda Nairobi akaona lift akasema 'Hii kabati inatembea na watu!' 😂","Mwalimu: Regan, 2+2? Regan: 22! 😂"])
    if any(x in m for x in ["mapenzi","penzi","love"]):
        return "MAPENZI: Heshima + uaminifu + muda. Mpende mtu anayekuheshimu. Usikimbilie. Wewe ni kijana handsome wa Siakago!"

    return f"Sawa Baba Regan! 👑 Uliuliza: '{q}'\n\nMimi V10 ULTIMATE nimebeba maarifa ya dunia yote - atomi hadi galaksi! Niulize tena vizuri au sema 'eleza zaidi kuhusu {q}' nitakupa notes kama mwalimu!\n\nSaa ni {now}"

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
