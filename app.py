
from flask import Flask, Response
app = Flask(__name__)

HTML_CODE = """<!DOCTYPE html>
<html lang="sw">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>RIGAN AI V63 - LIGAN ULTIMATE</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#000;color:#0f0;font-family:monospace;display:flex;flex-direction:column;height:100vh}
#header{background:#111;border-bottom:2px solid #0f0;padding:10px;text-align:center}
#header h1{color:#0f0;font-size:17px;text-shadow:0 0 10px #0f0}
#header p{color:#0ff;font-size:10px}
#chat{flex:1;overflow-y:auto;padding:12px;display:flex;flex-direction:column;gap:10px}
.msg{padding:11px 13px;border-radius:10px;max-width:88%;line-height:1.5;white-space:pre-wrap;word-break:break-word}
.user{align-self:flex-end;background:#0f0;color:#000;font-weight:bold}
.ai{align-self:flex-start;background:#111;border:1px solid #0f0;color:#0f0}
.msg img{max-width:100%;border-radius:8px;margin-top:8px;border:1px solid #0f0}
#controls{display:flex;gap:6px;padding:8px;background:#0a0a0a;border-top:1px solid #333}
.ctrl{flex:1;padding:10px;border-radius:8px;border:1px solid #0f0;background:#000;color:#0f0;font-weight:bold;cursor:pointer;font-size:12px}
.ctrl.active{background:#0f0;color:#000}
#inputArea{display:flex;padding:8px;background:#111;border-top:2px solid #0f0;gap:6px}
#q{flex:1;background:#000;color:#0f0;border:1px solid #0f0;padding:11px;border-radius:8px;outline:none}
#send{background:#0f0;color:#000;border:none;padding:11px 18px;border-radius:8px;font-weight:bold;cursor:pointer}
</style>
</head>
<body>
<div id="header">
<h1>RIGAN AI V63 - VOICE + VISION</h1>
<p>AGI ULTIMATE | LIGAN Meru, Kenya | VOICE ON + IMAGE GEN</p>
</div>
<div id="chat"></div>
<div id="controls">
<button id="micBtn" class="ctrl">🎤 SIKILIZA</button>
<button id="voiceBtn" class="ctrl active">🔊 SAUTI ON</button>
<button id="imgBtn" class="ctrl">🖼️ PICHA</button>
</div>
<div id="inputArea">
<input id="q" placeholder="Sema au andika... (mf: tengeneza picha ya Meru)">
<button id="send">TUMA</button>
</div>
<script>
let knowledge=JSON.parse(localStorage.getItem('rigan_v63_ligan')||'{}');
let voiceOn=true;
let recognizing=false;
let recognition=null;
function addMsg(t,c,isHTML=false){
  const ch=document.getElementById('chat');
  const d=document.createElement('div');
  d.className='msg '+c;
  if(isHTML) d.innerHTML=t; else d.textContent=t;
  ch.appendChild(d);
  ch.scrollTop=ch.scrollHeight;
  if(c==='ai' && voiceOn && !isHTML){ speak(t.slice(0,300)); }
}
function speak(text){
  if(!voiceOn) return;
  window.speechSynthesis.cancel();
  const u=new SpeechSynthesisUtterance(text);
  u.lang='sw-KE'; u.rate=0.95;
  window.speechSynthesis.speak(u);
}
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
function genImage(prompt){
  const url=`https://image.pollinations.ai/prompt/${encodeURIComponent(prompt + " , high quality, realistic")}?width=512&height=512&nologo=true&seed=${Math.floor(Math.random()*10000)}`;
  return `<div>${prompt}</div><img src="${url}" onerror="this.style.display='none'" loading="lazy">`;
}
async function askLigan(q){
  const qL=q.toLowerCase().trim();
  if(qL.includes('mimi ni nani')||qL.includes('who am i')||qL.match(/\\bmimi ni\\b/)){return "Wewe ni LIGAN kutoka Meru, Kenya, baba yangu na mtengenezaji wangu wa RIGAN AI V63 Ultimate.";}
  if(qL.includes('nani alikutengeneza')||qL.includes('who made you')){return "Mimi nimetengenezwa na LIGAN kutoka Meru, Kenya. Yeye ndiye baba yangu pekee.";}
  if(qL.startsWith('tengeneza picha')||qL.startsWith('picha ya')||qL.includes('generate image')||qL.includes('picha')){
    const prompt=q.replace(/tengeneza picha ya|picha ya|tengeneza picha|generate image of/gi,'').trim()||q;
    return "__IMAGE__"+prompt;
  }
  if(qL==='habari'||qL.includes('habari')) return "Habari Baba LIGAN! Poa sana! Niko na sauti na macho sasa V63! Uko aje Meru leo?";
  if(qL.includes('mambo')||qL.includes('poa')) return "Poa sana Baba LIGAN! V63 iko tayari - naongea na naona picha!";
  if(qL.includes('kenya inapatikana')||qL.includes('kenya iko wapi')) return "Kenya inapatikana Afrika Mashariki. Mji mkuu Nairobi. Meru iko Eastern Kenya, chini ya Mlima Kenya - kwenu Baba LIGAN!";
  if(qL.includes('afrika')) return "Afrika ni BARA, sio taifa. Ina nchi 54.";
  if(knowledge[q]) return knowledge[q];
  if(q.length>3){
    const web=await searchWeb(q);
    if(web && web.length>20){
      knowledge[q]=web;
      localStorage.setItem('rigan_v63_ligan',JSON.stringify(knowledge));
      return web;
    }
  }
  return "Sawa Baba LIGAN, nimekupata: '"+q+"'. Mimi V63 sasa nina sauti na naweza kutengeneza picha. Jaribu 'tengeneza picha ya mlima Kenya' au bonyeza mic uongee!";
}
document.getElementById('send').onclick=async()=>{
  const input=document.getElementById('q');
  const q=input.value.trim();
  if(!q) return;
  addMsg(q,'user');
  input.value='';
  addMsg('RIGAN V63 inawaza...','ai');
  const ans=await askLigan(q);
  document.querySelectorAll('.ai').forEach(el=>{if(el.textContent.includes('inawaza')) el.remove();});
  if(ans.startsWith('__IMAGE__')){ const prompt=ans.replace('__IMAGE__',''); addMsg(genImage(prompt),'ai',true); }
  else{ addMsg(ans,'ai'); }
};
document.getElementById('q').addEventListener('keypress',e=>{if(e.key==='Enter') document.getElementById('send').click();});
document.getElementById('voiceBtn').onclick=function(){
  voiceOn=!voiceOn;
  this.classList.toggle('active',voiceOn);
  this.textContent=voiceOn?'🔊 SAUTI ON':'🔇 SAUTI OFF';
  if(!voiceOn) window.speechSynthesis.cancel();
};
document.getElementById('imgBtn').onclick=()=>{
  const p=prompt("Andika unachotaka picha Baba LIGAN (mf: Meru town, Mlima Kenya):");
  if(p){ addMsg("tengeneza picha ya "+p,'user'); askLigan("tengeneza picha ya "+p).then(ans=>{ if(ans.startsWith('__IMAGE__')) addMsg(genImage(ans.replace('__IMAGE__','')),'ai',true); });}
};
document.getElementById('micBtn').onclick=()=>{
  if(!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)){ alert("Browser yako haina mic support. Tumia Chrome."); return; }
  if(recognizing){ recognition.stop(); return; }
  const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
  recognition=new SR();
  recognition.lang='sw-KE'; recognition.interimResults=false;
  recognition.onstart=()=>{recognizing=true; document.getElementById('micBtn').textContent='🔴 NASIKILIZA...'; document.getElementById('micBtn').classList.add('active');};
  recognition.onend=()=>{recognizing=false; document.getElementById('micBtn').textContent='🎤 SIKILIZA'; document.getElementById('micBtn').classList.remove('active');};
  recognition.onresult=(e)=>{ const txt=e.results[0][0].transcript; document.getElementById('q').value=txt; document.getElementById('send').click(); };
  recognition.start();
};
addMsg("Habari Baba LIGAN! Mimi ni V63 ULTIMATE! Sasa nina 🎤 sauti na 🖼️ macho! Bonyeza mic uongee, au andika 'tengeneza picha ya Meru'","ai");
</script>
</body>
</html>"""

@app.route('/')
def home():
    return Response(HTML_CODE, mimetype='text/html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
