let selected='signal-clean',language='id';
const config=document.querySelector('#config'),status=document.querySelector('.status');
const frames=[...document.querySelectorAll('iframe')];
document.fonts.load('400 28px "Helvetica"').then(faces=>{
  document.querySelector('#helvetica-status').textContent=faces.length
    ?'Helvetica lokal tersedia. File font tidak dibundel.'
    :'Helvetica belum tersedia; contoh ini memakai Roboto.';
}).catch(()=>{
  document.querySelector('#helvetica-status').textContent='Helvetica belum tersedia; contoh ini memakai Roboto.';
});
function update(){config.value=JSON.stringify({theme:selected,language});}
function translateFrame(frame){
  const doc=frame.contentDocument;
  if(!doc)return;
  doc.documentElement.lang=language;
  doc.querySelectorAll('[data-id]').forEach(element=>{element.textContent=element.dataset[language];});
}
const resize=new ResizeObserver(entries=>entries.forEach(({target})=>{
  target.querySelector('iframe').style.transform=`scale(${target.clientWidth/1080})`;
}));
document.querySelectorAll('.screen').forEach(screen=>resize.observe(screen));
frames.forEach(frame=>frame.addEventListener('load',()=>translateFrame(frame)));
document.querySelectorAll('.pick').forEach(button=>button.addEventListener('click',()=>{
  selected=button.dataset.theme;
  document.querySelectorAll('.pick').forEach(other=>{
    other.setAttribute('aria-pressed',String(other===button));
    other.firstChild.textContent=other===button?'Terpilih':'Pilih tema';
  });
  status.textContent=button.closest('.details').querySelector('h2').textContent+' terpilih';
  update();
}));
document.querySelector('#language').addEventListener('click',()=>{
  language=language==='id'?'en':'id';
  frames.forEach(translateFrame);
  document.querySelector('#language').textContent=language==='id'?'Contoh: Indonesia':'Sample: English';
  update();
});
document.querySelector('#replay').addEventListener('click',()=>{
  frames.forEach(frame=>frame.contentDocument?.body.classList.remove('replay'));
  requestAnimationFrame(()=>requestAnimationFrame(()=>frames.forEach(frame=>frame.contentDocument?.body.classList.add('replay'))));
});
document.querySelector('#copy').addEventListener('click',async()=>{
  try{await navigator.clipboard.writeText(config.value);status.textContent='Konfigurasi disalin';}
  catch{config.select();status.textContent='Tekan Ctrl+C untuk menyalin';}
});
document.querySelectorAll('audio').forEach(audio=>audio.addEventListener('play',()=>{
  document.querySelectorAll('audio').forEach(other=>{if(other!==audio)other.pause();});
}));
