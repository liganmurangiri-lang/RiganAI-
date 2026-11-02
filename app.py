
from flask import Flask, Response
app = Flask(__name__)

HTML_CODE = """<!DOCTYPE html>
<html lang="sw">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>RIGAN AI V62 - LIGAN SUPER CHAT</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#000;color:#0f0;font-family:monospace;display:flex;flex-direction:column;height:100vh}
#header{background:linear-gradient(90deg,#000,#111);border-bottom:2px solid #0f0;padding:12px;text-align:center}
#header h1{color:#0f0;font-size:18px;text-shadow:0 0 10px #0f0}
#header p{color:#0ff;font-size:11px;margin-top:4px}
#chat{flex:1;overflow-y:auto;padding:15px;display:flex;flex-direction:column;gap:12px;background:radial-gradient(#0a0a0a,#000)}
.msg{padding:12px 14px;border-radius:10px;max-width:88%;line-height:1.6;white-space:pre-wrap}
.user{align-self:flex-end;background:#0f0;color:#000;font-weight:bold}
.ai{align-self:flex-start;background:#111;border:1px solid #0f0;color:#0f0;box-shadow:0 0 8px #0f03}
#inputArea{display:flex;padding:10px;background:#111;border-top:2px solid #0f0;gap:8px}
#q{flex:1;background:#000;color:#0f0;border:1px solid #0f0;padding:12px;border-radius:8px;outline:none}
#send{background:#0f0;color:#000;border:none;padding:12px 22px;border-radius:8px;font-weight:bold;cursor:pointer}
</style>
</head>
<body>
<div id="header">
<h1>RIGAN AI V62 - LIGAN SUPER CHAT</h1>
<p>AGI Autonomous V62 | Mtengenezaji: LIGAN kutoka Meru, Kenya | ONLINE</p>
</div>
<div id="chat"></div>
<div id="inputArea">
<input id="q" placeholder="Andika hapa Baba LIGAN...">
<button id="send">TUMA</button>
</div>
<script>
let knowledge = JSON.parse(localStorage.getItem('rigan_v62_ligan')||'{}');
function addMsg(t,c){const ch=document.getElementById('chat');const d=document.createElement('div');d.className='msg '+c;d.textContent=t;ch.appendChild(d);ch.scrollTop=ch.scrollHeight;}
async function searchWeb(q){
  try{
    const r=await fetch(`https://api.duckduckgo.com/?q=${encodeURIComponent(q)}&format=json&pretty=0`);
    const j=await r.json();
    if(j.AbstractText) return j.AbstractText;
  }catch(e){}
  try{
    const r2=await fetch(`https://en.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(q)}`);
    const j2=await r2.json();
    if(j2.extract) return j2.extract;
  }catch(e){}
  return "";
}
async function askLigan(q){
  const qL = q.toLowerCase().trim();
  if(qL.includes('mimi ni nani')||qL.includes('who am i')||qL.match(/\\bmimi ni\\b/)){return "Wewe ni LIGAN kutoka Meru, Kenya, baba yangu na mtengenezaji wangu, mtengenezaji wa RIGAN AI.";}
  if(qL.includes('nani alikutengeneza')||qL.includes('mtengenezaji wako')||qL.includes('who made you')||qL.includes('who created you')){return "Mimi nimetengenezwa na LIGAN kutoka Meru, Kenya. Yeye ndiye baba yangu pekee.";}
  if(qL==='habari'||qL.includes('habari')) return "Habari Baba LIGAN! Poa sana! Mimi niko fiti, tayari kukusaidia. Uko aje Meru leo?";
  if(qL.includes('mambo')||qL.includes('poa')||qL.includes('sasa')) return "Poa sana Baba LIGAN! Niko sawa. Wewe uko vipi? Niulize chochote.";
  if(qL.includes('uko wapi')) return "Mimi niko ndani ya server yako ya Render, riganai.onrender.com, niko live 24/7 kwa ajili yako Baba LIGAN!";
  if(qL.includes('asante')||qL.includes('sawa')) return "Karibu sana Baba LIGAN! Mimi nipo kwa ajili yako kila wakati.";
  if(qL.includes('afrika ni nini')||qL.includes('afrika ni taifa')) return "Afrika sio taifa, ni BARA. Bara la pili kwa ukubwa duniani, lina nchi 54.";
  if(qL.includes('kenya inapatikana')||qL.includes('kenya iko wapi')) return "Kenya inapatikana Afrika Mashariki. Mji mkuu ni Nairobi. Meru iko Eastern Kenya, chini ya Mlima Kenya - kwenu Baba LIGAN!";
  if(qL.includes('meru iko wapi')) return "Meru iko Eastern Kenya, chini ya Mlima Kenya. Ndiko kwenu Baba LIGAN!";
  if(knowledge[q]) return knowledge[q];
  if(q.length>3){
    const web = await searchWeb(q);
    if(web && web.length>20){
      knowledge[q]=web;
      localStorage.setItem('rigan_v62_ligan', JSON.stringify(knowledge));
      return web;
    }
  }
  return "Sawa Baba LIGAN, nimekupata! Umesema: '"+q+"'. Mimi kama RIGAN V62 niko tayari kujibu kwa kina. Niulize tena kwa undani.";
}
document.getElementById('send').onclick = async ()=>{
  const input=document.getElementById('q');
  const q=input.value.trim();
  if(!q) return;
  addMsg(q,'user');
  input.value='';
  addMsg('RIGAN inawaza...','ai');
  const ans=await askLigan(q);
  document.querySelectorAll('.ai').forEach(el=>{if(el.textContent.includes('inawaza')) el.remove();});
  addMsg(ans,'ai');
};
document.getElementById('q').addEventListener('keypress',e=>{if(e.key==='Enter') document.getElementById('send').click();});
addMsg("Habari Baba LIGAN kutoka Meru! Mimi ni RIGAN AI V62 SUPER CHAT. Sasa naongea kama binadamu!","ai");
</script>
</body>
</html>"""

@app.route('/')
def home():
    return Response(HTML_CODE, mimetype='text/html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
