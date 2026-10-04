(function(){
var d=document,de=d.documentElement;de.classList.add('js');
function ready(f){d.readyState!=='loading'?f():d.addEventListener('DOMContentLoaded',f)}
ready(function(){
  var h=d.querySelector('.hdr'),tick=false;
  function onScroll(){if(tick)return;tick=true;requestAnimationFrame(function(){h.classList.toggle('scrolled',window.scrollY>24);tick=false})}
  if(h){window.addEventListener('scroll',onScroll,{passive:true});onScroll()}

  // mobile menu
  var bg=d.getElementById('burger'),mn=d.getElementById('mnav'),sc=d.getElementById('scrim'),cl=d.getElementById('mclose');
  function setMenu(o){
    mn.classList.toggle('open',o);sc.classList.toggle('open',o);bg.setAttribute('aria-expanded',o);
    mn.setAttribute('aria-hidden',!o);d.body.style.overflow=o?'hidden':'';
    if(o){cl.focus()}else{bg.focus()}
  }
  if(bg&&mn){
    mn.setAttribute('aria-hidden','true');
    bg.addEventListener('click',function(){setMenu(!mn.classList.contains('open'))});
    cl.addEventListener('click',function(){setMenu(false)});
    sc.addEventListener('click',function(){setMenu(false)});
    mn.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){mn.classList.remove('open');sc.classList.remove('open');bg.setAttribute('aria-expanded','false');mn.setAttribute('aria-hidden','true');d.body.style.overflow=''})});
    d.addEventListener('keydown',function(e){
      if(!mn.classList.contains('open'))return;
      if(e.key==='Escape'){setMenu(false)}
      else if(e.key==='Tab'){ // keep focus inside the open menu
        var f=mn.querySelectorAll('a,button'),first=f[0],last=f[f.length-1];
        if(e.shiftKey&&d.activeElement===first){e.preventDefault();last.focus()}
        else if(!e.shiftKey&&d.activeElement===last){e.preventDefault();first.focus()}
      }
    });
    window.matchMedia('(min-width:861px)').addEventListener('change',function(m){if(m.matches&&mn.classList.contains('open'))setMenu(false)});
  }

  // reveal product cards once, staggered; pause the hero diagram off screen
  var rv=d.querySelectorAll('.rv');
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.15,rootMargin:'0px 0px -6% 0px'});
    rv.forEach(function(el){io.observe(el)});
    var eco=d.querySelector('.eco-wrap');
    if(eco){new IntersectionObserver(function(es){es.forEach(function(e){eco.classList.toggle('off',!e.isIntersecting)})},{threshold:.05}).observe(eco)}
  }else{rv.forEach(function(el){el.classList.add('in')})}

  var y=d.getElementById('yr');if(y)y.textContent=new Date().getFullYear();
});
})();
