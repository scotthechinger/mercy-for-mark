# -*- coding: utf-8 -*-
"""The postcard project — a tapestry of cards you can turn over."""
import json, html

E = lambda s: html.escape(s, quote=True)
CARDS = json.load(open('/home/claude/work/site2/img/pc/cards.json'))

PROMPT = ("If you were to speak to the Governor, why would you say Mark Jenkins "
          "deserves clemency?")

CSS = """
<style>
.pc-controls{position:sticky;top:66px;z-index:40;background:var(--paper);
  border-bottom:1px solid var(--rule);padding:14px 0}
.pc-controls .wrap{display:flex;gap:16px;align-items:center;flex-wrap:wrap;
  justify-content:space-between}
.pc-hint{font-size:13.5px;color:var(--ink-3)}

.tapestry{columns:4;column-gap:20px;margin-top:34px}
.pc{break-inside:avoid;margin:0 0 20px;perspective:1400px;background:none;
  border:0;padding:0;font:inherit;cursor:pointer;display:block;width:100%}
.pc:focus-visible{outline:2px solid var(--accent);outline-offset:4px}
.pc-in{position:relative;transform-style:preserve-3d;
  transition:transform .62s cubic-bezier(.2,.7,.2,1)}
.pc:hover .pc-in,.tapestry.backs .pc-in,.pc.flipped .pc-in{transform:rotateY(180deg)}
.tapestry.backs .pc:hover .pc-in{transform:rotateY(360deg)}
.pc-face{backface-visibility:hidden;-webkit-backface-visibility:hidden;
  border:1px solid var(--rule);background:#fff;
  box-shadow:0 1px 2px rgba(22,21,15,.06),0 8px 24px rgba(22,21,15,.07)}
.pc-front img{width:100%;display:block}
.pc-back{position:absolute;inset:0;transform:rotateY(180deg);overflow:hidden}

/* the printed reverse of the card */
.bk{height:100%;display:flex;flex-direction:column;background:#FDFCF9;
  padding:7% 7% 5%;font-family:var(--serif);color:#2A2820;
  container-type:inline-size}
.bk-prompt{font-size:5.6cqw;line-height:1.32;margin:0 0 4%;color:#3A372E}
.bk-cols{display:flex;gap:5%;flex:1;border-top:1px solid #DED8CB;padding-top:4%}
.bk-lines{flex:1.15;display:flex;flex-direction:column;justify-content:flex-start;
  gap:9%;padding-top:3%}
.bk-lines i{display:block;border-bottom:1px solid #E6E0D3;height:1px}
.bk-addr{flex:1;border-left:1px solid #DED8CB;padding-left:5%;position:relative;
  display:flex;flex-direction:column;justify-content:flex-end;gap:6%}
.bk-stamp{position:absolute;top:0;right:0;width:34%;aspect-ratio:.82;
  border:1px dashed #CFC7B6;border-radius:2px}
.bk-addr b{font-family:var(--sans);font-size:3.6cqw;letter-spacing:.1em;
  text-transform:uppercase;color:#8A857A;font-weight:700;display:block}
.bk-addr span{font-size:4.6cqw;line-height:1.4;display:block;color:#3A372E}
.bk-foot{font-family:var(--sans);font-size:3.1cqw;line-height:1.45;color:#8A857A;
  border-top:1px solid #EDE7DA;margin-top:4%;padding-top:3%}

dialog{border:0;padding:0;max-width:760px;width:calc(100% - 34px);border-radius:4px;
  background:transparent}
dialog::backdrop{background:rgba(22,21,15,.72)}
.dg{perspective:1600px}
.dg-in{position:relative;transform-style:preserve-3d;
  transition:transform .62s cubic-bezier(.2,.7,.2,1)}
.dg.flipped .dg-in{transform:rotateY(180deg)}
.dg-face{backface-visibility:hidden;-webkit-backface-visibility:hidden;
  background:#fff;border-radius:3px;overflow:hidden;
  box-shadow:0 20px 60px rgba(0,0,0,.4)}
.dg-front img{width:100%;display:block}
.dg-back{position:absolute;inset:0;transform:rotateY(180deg)}
.dg-bar{display:flex;justify-content:space-between;align-items:center;gap:14px;
  margin-top:18px;color:#EFEBE2}
.dg-bar p{margin:0;font-size:14px;color:#CFC9BC}
.dg-bar button{font:inherit;font-size:14.5px;font-weight:600;padding:10px 18px;
  border-radius:2px;cursor:pointer;background:var(--accent);color:#fff;border:0}
.dg-bar .x{background:none;border:1px solid rgba(255,255,255,.4);color:#fff}
@media(max-width:1100px){.tapestry{columns:3}}
@media(max-width:800px){.tapestry{columns:2}}
@media(max-width:520px){.tapestry{columns:1}}
</style>
"""


def back_html():
    return """<div class="bk">
  <p class="bk-prompt">%s</p>
  <div class="bk-cols">
    <div class="bk-lines"><i></i><i></i><i></i><i></i><i></i></div>
    <div class="bk-addr">
      <span class="bk-stamp"></span>
      <b>Mail to</b>
      <span>Mercy for Mark<br>[Alabama address]</span>
    </div>
  </div>
  <p class="bk-foot">Cards may be shown publicly, in print or online, as part of
  Mark's clemency campaign. Signing your name is optional.</p>
</div>""" % E(PROMPT)


def render():
    back = back_html()
    tiles = ''.join(
      '<button class="pc" data-i="%d" aria-label="%s postcard, select to enlarge">'
      '<div class="pc-in" style="aspect-ratio:%s">'
      '<div class="pc-face pc-front"><img src="img/pc/%s" alt="%s" loading="lazy"></div>'
      '<div class="pc-face pc-back">%s</div>'
      '</div></button>'
      % (c['i'], E(c['title']), '%d/%d' % (c['w'], c['h']), c['f'], E(c['title']), back)
      for c in CARDS)

    n_land = sum(1 for c in CARDS if c['orient'] == 'landscape')

    return CSS + """
<section class="hero" style="padding:56px 0 26px"><div class="wrap"
  style="grid-template-columns:1fr">
  <div>
    <p class="eyebrow">The postcard project</p>
    <h1 style="max-width:17ch">One card, one question, one Governor.</h1>
    <p class="serif-lede measure" style="margin-bottom:16px">&ldquo;__PROMPT__&rdquo;</p>
    <p class="lede measure">Across Alabama, people of faith are answering that
    question in their own handwriting and mailing it to Montgomery. Every card
    that comes back is photographed and joins this wall.</p>
    <div class="btnrow">
      <a class="btn" href="mailto:teammarkjenkins@gmail.com?subject=Postcards%20for%20Mark">Request cards for your congregation</a>
    </div>
  </div>
</div></section>

<div class="pc-controls"><div class="wrap">
  <div class="views" role="tablist">
    <button class="on" data-side="front">Picture side</button>
    <button data-side="back">Written side</button>
  </div>
  <p class="pc-hint">__N__ cards &middot; hover any card to turn it over,
  or select one to open it</p>
</div></div>

<section style="padding-top:0"><div class="wrap">
  <div class="tapestry" id="tap">__TILES__</div>
</div></section>

<section class="band"><div class="wrap narrow">
  <p class="eyebrow">Coming back in the mail</p>
  <h2>The wall fills as they arrive.</h2>
  <p class="lede">The first cards were handed out in August 2026. As they are
  returned, each one is scanned and its written side replaces the blank reverse
  above, so this page grows all the way to the decision.</p>
</div></section>

<section class="pc-ask"><div class="wrap">
  <div class="media">
    <div>
      <p class="eyebrow">Add your card</p>
      <h2>There is room on this wall for yours.</h2>
      <p>If your congregation, class, or group would like a stack of cards, tell
      us how many and where to send them. If you already have one, fill it in and
      mail it to Montgomery; every card that comes back is scanned and added
      here.</p>
      <div class="btnrow">
        <a class="btn" href="mailto:teammarkjenkins@gmail.com?subject=Postcards%20for%20Mark%20Jenkins">Request cards</a>
        <a class="btn ghost" href="mailto:teammarkjenkins@gmail.com?subject=A%20card%20on%20its%20way">Tell us yours is coming</a>
      </div>
    </div>
    <div class="pc-ways">
      <p class="rf-lab">Other ways to help</p>
      <ul>
        <li><a href="help.html"><b>Write to Governor Ivey</b>
          <span>A letter in your own words carries further than a signature.</span></a></li>
        <li><a href="officers.html"><b>Read the officers' letters</b>
          <span>Sixty of the people paid to watch Mark asked for his life.</span></a></li>
        <li><a href="why-clemency.html"><b>Learn the grounds for clemency</b>
          <span>Three reasons, and what a court was never allowed to weigh.</span></a></li>
        <li><a href="mailto:teammarkjenkins@gmail.com"><b>Get updates</b>
          <span>Events and actions in the months ahead.</span></a></li>
      </ul>
    </div>
  </div>
</div></section>

<dialog id="pcdl">
  <div class="dg" id="dg"><div class="dg-in">
    <div class="dg-face dg-front"><img id="dg-img" src="" alt=""></div>
    <div class="dg-face dg-back">__BACK__</div>
  </div></div>
  <div class="dg-bar">
    <p id="dg-cap"></p>
    <div style="display:flex;gap:10px">
      <button id="dg-flip">Turn it over</button>
      <button class="x" id="dg-x">Close</button>
    </div>
  </div>
</dialog>

<script>
const CARDS = __CARDS__;
const tap = document.getElementById('tap');
const dl = document.getElementById('pcdl');
const dg = document.getElementById('dg');

document.querySelector('.pc-controls .views').addEventListener('click', e => {
  const b = e.target.closest('button'); if(!b) return;
  document.querySelectorAll('.pc-controls .views button')
    .forEach(x => x.classList.toggle('on', x === b));
  tap.classList.toggle('backs', b.dataset.side === 'back');
});

tap.addEventListener('click', e => {
  const b = e.target.closest('.pc'); if(!b) return;
  const c = CARDS.find(x => x.i === +b.dataset.i); if(!c) return;
  const img = document.getElementById('dg-img');
  img.src = 'img/pc/' + c.f; img.alt = c.title;
  dg.querySelector('.dg-in').style.aspectRatio = c.w + '/' + c.h;
  dg.classList.remove('flipped');
  document.getElementById('dg-cap').textContent = c.title;
  dl.showModal();
});
document.getElementById('dg-flip').addEventListener('click',
  () => dg.classList.toggle('flipped'));
document.getElementById('dg-x').addEventListener('click', () => dl.close());
dl.addEventListener('click', e => { if(e.target === dl) dl.close(); });
</script>
""".replace('__TILES__', tiles).replace('__BACK__', back) \
   .replace('__PROMPT__', E(PROMPT)).replace('__N__', str(len(CARDS))) \
   .replace('__CARDS__', json.dumps(CARDS, ensure_ascii=False))
