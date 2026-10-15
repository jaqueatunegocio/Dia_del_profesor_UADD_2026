"""Genera test/index.html: copia exacta de index.html + animaciones y transiciones.

Uso:  python3 scripts/build_test.py
No modifica el contenido; solo agrega CSS y JS de animación.
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

BASE = '<base href="/"><meta name="robots" content="noindex">'
HEAD = """<style id="anim-css">
:root{--ease:cubic-bezier(.2,.8,.2,1)}
html{scroll-behavior:smooth}
/* --- carga inicial --- */
@keyframes fadeDown{from{opacity:0;transform:translateY(-24px)}to{opacity:1;transform:none}}
@keyframes fadeUp{from{opacity:0;transform:translateY(40px)}to{opacity:1;transform:none}}
@keyframes growX{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@keyframes zoomIn{from{opacity:0;transform:scale(.92)}to{opacity:1;transform:none}}
@keyframes glow{0%,100%{box-shadow:0 0 0 0 #ffb80000}50%{box-shadow:0 0 0 10px #ffb80022}}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.06)}}
@keyframes floaty{0%,100%{transform:translateY(0) rotate(0)}50%{transform:translateY(-10px) rotate(-3deg)}}
@keyframes shine{from{transform:translateX(-120%) skewX(-20deg)}to{transform:translateX(320%) skewX(-20deg)}}
@keyframes beat{0%,100%{transform:scale(1)}15%{transform:scale(1.25)}30%{transform:scale(1)}45%{transform:scale(1.18)}}
.shell{animation:zoomIn .9s var(--ease) both}
.brand>div{animation:fadeDown .8s var(--ease) both}
.brand>div:last-child{animation-delay:.15s}
.brand{position:relative;border-bottom-color:transparent!important}
.brand:after{content:"";position:absolute;left:0;right:0;bottom:-4px;height:4px;background:#FFB800;transform-origin:left;animation:growX 1.2s .3s var(--ease) both}
.hero .eyebrow{animation:fadeUp .8s .35s var(--ease) both}
.video-player{animation:zoomIn 1s .5s var(--ease) both}
.video-player:not(.playing){animation:zoomIn 1s .5s var(--ease) both,glow 2.8s 1.6s ease-in-out infinite}
.big-play span{animation:pulse 2.2s 1.5s ease-in-out infinite}
.hero .herotext{animation:fadeUp .9s .8s var(--ease) both}
/* --- aparición al hacer scroll --- */
.rv{opacity:0;transform:translateY(46px);transition:opacity .9s var(--ease),transform .9s var(--ease);transition-delay:var(--d,0s)}
.rv.rv-left{transform:translateX(-50px)}.rv.rv-right{transform:translateX(50px)}.rv.rv-zoom{transform:scale(.85)}
.rv.in{opacity:1;transform:none}
.thanks img{animation:floaty 5s ease-in-out infinite}
/* --- categorías --- */
.category{transition:box-shadow .35s var(--ease),transform .35s var(--ease),border-color .35s}
.category:hover{transform:translateY(-3px);box-shadow:0 14px 34px #0000001a;border-color:#ffb80088}
.category summary{transition:background .3s}
.category .icon{transition:transform .5s var(--ease),background .3s}
.category:hover .icon,.category[open] .icon{transform:rotate(-8deg) scale(1.12);background:#fff4d1}
.category .link span{display:inline-block;transition:transform .35s var(--ease)}
.category:hover .link span{transform:translate(4px,-4px)}
.category[open] .link span{transform:rotate(90deg)}
.category .story{overflow:hidden}
.pop{opacity:0;transform:translateY(26px) scale(.98)}
.pop.in{opacity:1;transform:none;transition:opacity .6s var(--ease),transform .6s var(--ease);transition-delay:var(--d,0s)}
.teacher{transition:transform .35s var(--ease),box-shadow .35s var(--ease)}
.teacher:hover{transform:translateY(-6px);box-shadow:0 16px 30px #00000022}
.photo.has-img{overflow:hidden}
.photo.has-img img{transition:transform 1.2s var(--ease)}
.teacher:hover .photo.has-img img{transform:scale(1.07)}
.story-card{transition:box-shadow .35s}
.story-card:hover{box-shadow:0 12px 28px #00000014}
/* --- formulario y cierre --- */
.share{position:relative;overflow:hidden}
.cta{position:relative;overflow:hidden;transition:transform .3s var(--ease),box-shadow .3s}
.cta:after{content:"";position:absolute;top:0;bottom:0;width:30%;background:linear-gradient(90deg,#fff0,#ffffff55,#fff0);animation:shine 3.2s 1s ease-in-out infinite}
.cta:hover{transform:translateY(-3px) scale(1.03);box-shadow:0 10px 24px #00000033}
.closing h2 .heart{display:inline-block;animation:beat 1.8s ease-in-out infinite}
footer{transition:letter-spacing .6s}
footer.in{letter-spacing:.6px}
@media (prefers-reduced-motion:reduce){*,*:before,*:after{animation:none!important;transition:none!important}.rv,.pop{opacity:1!important;transform:none!important}}
</style>"""

BODY = """<script id="anim-js">
(function(){
  if(matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var $=function(s,r){return [].slice.call((r||document).querySelectorAll(s))};
  function mark(sel,cls,step,base){$(sel).forEach(function(el,i){el.classList.add('rv');if(cls)el.classList.add(cls);el.style.setProperty('--d',((base||0)+i*(step||0))+'s')})}
  mark('.thanks .eyebrow','rv-left');
  $('.thanks h1').forEach(function(h){h.classList.add('rv');h.style.setProperty('--d','.1s')});
  mark('.thanks p',null,.12,.25);
  mark('.thanks img','rv-zoom',0,.3);
  mark('.section>.eyebrow,.section>h2,.section>.intro,.section>.small',null,.1);
  mark('.category',null,.09);
  mark('.share>*',null,.1);
  mark('.closing>*',null,.12);
  // corazón del cierre
  $('.closing h2').forEach(function(h){h.innerHTML=h.innerHTML.replace('💛','<span class="heart">💛</span>')});
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.15,rootMargin:'0px 0px -40px 0px'});
  $('.rv').forEach(function(el){io.observe(el)});
  var f=document.querySelector('footer');if(f)io.observe(f);

  // apertura/cierre suave de categorías + aparición escalonada del contenido
  $('details.category').forEach(function(d){
    var sum=d.querySelector('summary'), body=d.querySelector('.story');
    if(!sum||!body) return;
    var items=$('.teacher,.story-card,.story>p,.story>strong',body);
    items.forEach(function(el){el.classList.add('pop')});
    function reveal(){items.forEach(function(el,i){el.classList.remove('in');el.style.setProperty('--d',Math.min(i*.07,.8)+'s');requestAnimationFrame(function(){requestAnimationFrame(function(){el.classList.add('in')})})})}
    var anim=null;
    sum.addEventListener('click',function(e){
      e.preventDefault(); if(anim) anim.cancel();
      if(!d.open){
        d.open=true; var h=body.scrollHeight;
        anim=body.animate([{height:'0px',opacity:0},{height:h+'px',opacity:1}],{duration:Math.min(900,350+h*.25),easing:'cubic-bezier(.2,.8,.2,1)'});
        reveal(); anim.onfinish=function(){anim=null};
      }else{
        var h2=body.scrollHeight;
        anim=body.animate([{height:h2+'px',opacity:1},{height:'0px',opacity:0}],{duration:420,easing:'cubic-bezier(.4,0,.2,1)'});
        anim.onfinish=function(){d.open=false;anim=null;items.forEach(function(el){el.classList.remove('in')})};
      }
    });
  });
})();
</script>"""


def main():
    src = (ROOT / "index.html").read_text(encoding="utf-8")
    assert "</head>" in src and "</body>" in src
    cs = '<meta charset="UTF-8">'
    assert cs in src
    out = src.replace(cs, cs + BASE, 1).replace("</head>", HEAD + "</head>", 1).replace("</body>", BODY + "</body>", 1)
    (ROOT / "test").mkdir(exist_ok=True)
    (ROOT / "test" / "index.html").write_text(out, encoding="utf-8")
    print("test/index.html generado")


if __name__ == "__main__":
    main()
