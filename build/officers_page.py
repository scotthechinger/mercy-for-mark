# -*- coding: utf-8 -*-
"""Renders officers.html."""
import json, html
import officers as O

E = lambda s: html.escape(s, quote=True)

CSS = """
<style>
.arch-controls{position:sticky;top:66px;z-index:40;background:var(--paper);
  border-bottom:1px solid var(--rule);padding:14px 0}
.ctrl-row{display:flex;gap:14px;align-items:center;flex-wrap:wrap}
.search{flex:1;min-width:230px;position:relative}
.search input{width:100%;font:inherit;font-size:15.5px;padding:11px 14px 11px 38px;
  border:1px solid var(--rule);border-radius:2px;background:var(--card);color:var(--ink)}
.search input:focus{outline:2px solid var(--accent);outline-offset:-1px;border-color:transparent}
.search svg{position:absolute;left:13px;top:13px;opacity:.4}
.chipbar{display:flex;flex-wrap:wrap;gap:7px;margin-top:12px}
.chip{font:inherit;font-size:12.5px;padding:6px 11px;border:1px solid var(--rule);
  background:var(--card);border-radius:2px;cursor:pointer;color:var(--ink-2)}
.chip:hover{border-color:var(--ink-3)}
.chip.on{background:var(--accent);color:#fff;border-color:var(--accent)}
.chip small{opacity:.6;margin-left:5px}
.countline{font-size:13.5px;color:var(--ink-3);margin-top:12px;display:flex;
  gap:14px;align-items:center}
.countline button{font:inherit;font-size:13px;background:none;border:0;
  color:var(--accent);cursor:pointer;text-decoration:underline;padding:0}

.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin:34px 0 0}
.lc{background:var(--card);border:1px solid var(--rule);border-radius:3px;
  overflow:hidden;display:flex;flex-direction:column;text-align:left;
  font:inherit;color:inherit;cursor:pointer;padding:0;transition:transform .18s ease,
  box-shadow .18s ease}
.lc:hover{transform:translateY(-2px);box-shadow:0 6px 22px rgba(22,21,15,.09)}
.lc:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.lc.gone{display:none}
.lc-img{height:186px;overflow:hidden;background:var(--paper-2);
  border-bottom:1px solid var(--rule);display:flex;align-items:flex-start;
  justify-content:center}
.lc-img img.letter{width:100%;height:auto}
.lc-img img.photo{width:100%;height:186px;object-fit:cover;object-position:center 24%}
.lc-b{padding:15px 16px 16px;display:flex;flex-direction:column;gap:10px;flex:1}
.lc-q{font-family:var(--serif);font-size:15.5px;line-height:1.45;margin:0}
.lc-q mark{background:#F7E2B8;color:inherit;padding:0 1px}
.lc-m{margin:0;font-size:11px;letter-spacing:.06em;text-transform:uppercase;
  color:var(--ink-3);font-weight:600}
.lc-d{margin:auto 0 0;display:flex;flex-wrap:wrap;gap:5px}
.lc-d span{font-size:11px;padding:3px 7px;border:1px solid var(--rule);
  border-radius:2px;color:var(--ink-2);background:var(--paper)}

.qlist{margin:34px 0 0;columns:2;column-gap:34px}
.qi{break-inside:avoid;margin:0 0 24px;padding-left:18px;
  border-left:2px solid var(--accent)}
.qi p{font-family:var(--serif);font-size:18px;line-height:1.5;margin:0 0 6px}
.qi span{font-size:11.5px;letter-spacing:.06em;text-transform:uppercase;
  color:var(--ink-3);font-weight:600;cursor:pointer}
.qi span:hover{color:var(--accent)}

.tchart{margin:34px 0 0;display:flex;flex-direction:column;gap:2px}
.tr{display:grid;grid-template-columns:230px 1fr 44px;gap:14px;align-items:center;
  padding:7px 0;cursor:pointer;border:0;background:none;font:inherit;text-align:left}
.tr:hover .tlab{color:var(--accent)}
.tlab{font-size:14px;color:var(--ink-2)}
.tbarwrap{background:var(--paper-2);height:19px;border-radius:2px;overflow:hidden}
.tbar{display:block;height:100%;background:var(--accent);border-radius:2px}
.tnum{font-family:var(--serif);font-size:16px;color:var(--ink-3);text-align:right}

dialog{border:0;padding:0;max-width:820px;width:calc(100% - 34px);
  border-radius:4px;background:var(--paper);color:var(--ink)}
dialog::backdrop{background:rgba(22,21,15,.62)}
.dl-h{position:sticky;top:0;background:var(--paper);border-bottom:1px solid var(--rule);
  padding:18px 26px;display:flex;justify-content:space-between;align-items:flex-start;
  gap:16px;z-index:2}
.dl-h h3{margin:0 0 3px;font-size:22px}
.dl-h p{margin:0;font-size:12.5px;color:var(--ink-3);letter-spacing:.05em;
  text-transform:uppercase;font-weight:600}
.dl-h button{font:inherit;font-size:22px;line-height:1;background:none;border:0;
  cursor:pointer;color:var(--ink-3);padding:2px 6px}
.dl-b{padding:24px 26px 34px}
.dl-b img{border:1px solid var(--rule);margin-bottom:22px;max-height:330px;
  object-fit:contain;width:auto;max-width:100%}
.dl-b h4{font-size:11px;letter-spacing:.14em;text-transform:uppercase;
  color:var(--ink-3);margin:26px 0 10px;font-family:var(--sans);font-weight:700}
.dl-q{font-family:var(--serif);font-size:17px;line-height:1.5;margin:0 0 12px;
  padding-left:16px;border-left:2px solid var(--accent)}
.dl-t{white-space:pre-wrap;font-size:15px;line-height:1.7;color:var(--ink-2);
  background:var(--card);border:1px solid var(--rule);border-radius:3px;
  padding:20px 22px;max-height:420px;overflow:auto}
.notice{background:var(--accent-soft);border-left:3px solid var(--accent);
  padding:15px 19px;font-size:14.5px;color:var(--ink-2);margin:0 0 8px}
.notice b{color:var(--accent)}
@media(max-width:900px){.grid{grid-template-columns:1fr 1fr}.qlist{columns:1}
  .tr{grid-template-columns:150px 1fr 36px}}
@media(max-width:560px){.grid{grid-template-columns:1fr}}
</style>
"""


def render():
    rows, tc, payload, leaks = O.build()
    if leaks:
        raise SystemExit('REFUSING TO BUILD — name leaks: %r' % leaks[:10])

    n_dr = sum(1 for r in rows if r['dr'])
    n_first = sum(1 for r in rows if r['first'])
    n_exec = sum(1 for r in rows if r['exec'])
    yrs = sum(r['yrs'] for r in rows if r['yrs'])
    nq = sum(len(r['q']) for r in rows)

    cards = ''.join(
      '<button class="lc" data-i="%d">%s<div class="lc-b">'
      '<p class="lc-q"></p><p class="lc-m">%s</p>'
      '<p class="lc-d">%s</p></div></button>' % (
        i,
        ('<div class="lc-img"><img class="%s" src="img/%s" alt="" loading="lazy"></div>'
         % (r['kind'], r['img'])) if r['img'] else '',
        E(' · '.join(filter(None, [
            ('%s years of service' % r['yrs']) if r['yrs'] else None,
            'death row' if r['dr'] else None]))) or 'Holman Correctional Facility',
        ''.join('<span>%s</span>' % E(d) for d in r['desc'][:3]))
      for i, r in enumerate(rows))

    chips = ''.join(
      '<button class="chip" data-t="%s">%s<small>%d</small></button>'
      % (t, E(O.THEME_LABELS[t]), c)
      for t, c in sorted(tc.items(), key=lambda kv: -kv[1]))

    return CSS + """
<section class="hero officers-hero" style="padding:56px 0 30px"><div class="wrap">
  <div>
    <p class="eyebrow">Alabama law enforcement</p>
    <h1 style="max-width:18ch">Sixty letters from the officers who guarded him.</h1>
    <p class="lede measure">Between 2023 and 2026, sixty people who worked at
    Holman Correctional Facility wrote individually to the Governor of Alabama
    about a man on death row. They had never done anything like it before. Every
    word here is theirs.</p>
  </div>
  <div class="wordfield" role="img" aria-label="Words the officers used about Mark, cut from their letters: animals, bible, calm, change, changed, christian, church, cooperative, courtesy, decent, dependable, easygoing, exceptional, faith, forgiveness, friendly, funny, gentle, genuine, good, helpful, kind, kindness, mercy, model, peaceful, pleasant, polite, prayer, quiet, redemption, reliable, remorse, remorseful, respect, respectful, safe, sincere, spare, special, thoughtful, trust, trusted, trustworthy">
      <span class="w" style="--r:2.2deg;--i:0"><img src="img/words/w-friendly.png" alt="" style="height:20px"></span>
      <span class="w" style="--r:-2.3deg;--i:1"><img src="img/words/w-change.png" alt="" style="height:30px"></span>
      <span class="w" style="--r:-0.2deg;--i:2"><img src="img/words/w-thoughtful.png" alt="" style="height:20px"></span>
      <span class="w" style="--r:3.2deg;--i:3"><img src="img/words/w-safe.png" alt="" style="height:33px"></span>
      <span class="w" style="--r:-0.5deg;--i:4"><img src="img/words/w-cooperative.png" alt="" style="height:27px"></span>
      <span class="w" style="--r:-0.3deg;--i:5"><img src="img/words/w-funny.png" alt="" style="height:33px"></span>
      <span class="w" style="--r:-2.3deg;--i:6"><img src="img/words/w-peaceful.png" alt="" style="height:25px"></span>
      <span class="w" style="--r:3.0deg;--i:7"><img src="img/words/w-polite.png" alt="" style="height:27px"></span>
      <span class="w" style="--r:0.8deg;--i:8"><img src="img/words/w-kindness.png" alt="" style="height:27px"></span>
      <span class="w" style="--r:-0.3deg;--i:9"><img src="img/words/w-forgiveness.png" alt="" style="height:22px"></span>
      <span class="w" style="--r:1.8deg;--i:10"><img src="img/words/w-trustworthy.png" alt="" style="height:20px"></span>
      <span class="w" style="--r:-2.8deg;--i:11"><img src="img/words/w-respectful.png" alt="" style="height:20px"></span>
      <span class="w" style="--r:-1.9deg;--i:12"><img src="img/words/w-spare.png" alt="" style="height:30px"></span>
      <span class="w" style="--r:1.8deg;--i:13"><img src="img/words/w-exceptional.png" alt="" style="height:22px"></span>
      <span class="w" style="--r:-0.5deg;--i:14"><img src="img/words/w-prayer.png" alt="" style="height:22px"></span>
      <span class="w" style="--r:-0.6deg;--i:15"><img src="img/words/w-helpful.png" alt="" style="height:25px"></span>
      <span class="w" style="--r:-0.0deg;--i:16"><img src="img/words/w-dependable.png" alt="" style="height:25px"></span>
      <span class="w" style="--r:-2.6deg;--i:17"><img src="img/words/w-gentle.png" alt="" style="height:30px"></span>
      <span class="w" style="--r:0.1deg;--i:18"><img src="img/words/w-trust.png" alt="" style="height:30px"></span>
      <span class="w" style="--r:-0.7deg;--i:19"><img src="img/words/w-pleasant.png" alt="" style="height:25px"></span>
      <span class="w" style="--r:-0.2deg;--i:20"><img src="img/words/w-remorseful.png" alt="" style="height:20px"></span>
      <span class="w" style="--r:2.4deg;--i:21"><img src="img/words/w-respect.png" alt="" style="height:22px"></span>
      <span class="w" style="--r:1.7deg;--i:22"><img src="img/words/w-good.png" alt="" style="height:33px"></span>
      <span class="w" style="--r:-2.1deg;--i:23"><img src="img/words/w-redemption.png" alt="" style="height:27px"></span>
      <span class="w" style="--r:0.9deg;--i:24"><img src="img/words/w-calm.png" alt="" style="height:36px"></span>
      <span class="w" style="--r:-3.0deg;--i:25"><img src="img/words/w-genuine.png" alt="" style="height:25px"></span>
      <span class="w" style="--r:-2.6deg;--i:26"><img src="img/words/w-remorse.png" alt="" style="height:36px"></span>
      <span class="w" style="--r:-1.5deg;--i:27"><img src="img/words/w-christian.png" alt="" style="height:20px"></span>
      <span class="w" style="--r:-1.1deg;--i:28"><img src="img/words/w-model.png" alt="" style="height:25px"></span>
      <span class="w" style="--r:1.7deg;--i:29"><img src="img/words/w-changed.png" alt="" style="height:27px"></span>
      <span class="w" style="--r:3.1deg;--i:30"><img src="img/words/w-church.png" alt="" style="height:27px"></span>
      <span class="w" style="--r:-1.8deg;--i:31"><img src="img/words/w-easygoing.png" alt="" style="height:20px"></span>
      <span class="w" style="--r:1.3deg;--i:32"><img src="img/words/w-decent.png" alt="" style="height:20px"></span>
      <span class="w" style="--r:-0.6deg;--i:33"><img src="img/words/w-sincere.png" alt="" style="height:20px"></span>
      <span class="w" style="--r:2.3deg;--i:34"><img src="img/words/w-animals.png" alt="" style="height:33px"></span>
      <span class="w" style="--r:-0.3deg;--i:35"><img src="img/words/w-reliable.png" alt="" style="height:20px"></span>
      <span class="w" style="--r:-1.0deg;--i:36"><img src="img/words/w-special.png" alt="" style="height:25px"></span>
      <span class="w" style="--r:-0.4deg;--i:37"><img src="img/words/w-trusted.png" alt="" style="height:25px"></span>
      <span class="w" style="--r:0.8deg;--i:38"><img src="img/words/w-courtesy.png" alt="" style="height:22px"></span>
      <span class="w" style="--r:-2.0deg;--i:39"><img src="img/words/w-kind.png" alt="" style="height:36px"></span>
      <span class="w" style="--r:2.0deg;--i:40"><img src="img/words/w-quiet.png" alt="" style="height:36px"></span>
      <span class="w" style="--r:3.1deg;--i:41"><img src="img/words/w-faith.png" alt="" style="height:30px"></span>
      <span class="w" style="--r:-1.3deg;--i:42"><img src="img/words/w-mercy.png" alt="" style="height:36px"></span>
      <span class="w" style="--r:-2.5deg;--i:43"><img src="img/words/w-bible.png" alt="" style="height:27px"></span>
    <p class="wordfield-cap">Every word is cut from one of the letters.</p>
  </div>
</div></section>

<div class="statband"><div class="wrap">
  <div class="head">
    <h3>What is in the archive</h3>
    <p>Counted conservatively: a writer is included in a figure only where their
    own letter says so.</p>
  </div>
  <div class="stats">
    <div class="stat"><b>60</b><span>letters, each written separately</span></div>
    <div class="stat"><b>__YRS__+</b><span>years of service among the writers</span></div>
    <div class="stat"><b>__DR__</b><span>worked on death row itself</span></div>
    <div class="stat"><b>__EXEC__</b><span>served on or witnessed executions</span></div>
  </div>
</div></div>

<section class="tight" style="padding-bottom:20px"><div class="wrap">
  <p class="notice"><b>Names are not shown.</b> These letters were written to the
  Governor, not for a website. Most of the writers have not been asked whether
  their names may appear publicly, and until they are asked and say yes, every
  name is removed: from the letters, from the transcripts, and from the
  search. What remains is what they said.</p>
</div></section>

<div class="arch-controls"><div class="wrap">
  <div class="ctrl-row">
    <div class="search">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor"
        stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
      <input id="q" type="search" placeholder="Search every word of every letter"
        aria-label="Search the letters">
    </div>
    <div class="views" role="tablist">
      <button class="on" data-v="cards">Cards</button>
      <button data-v="quotes">Quotes</button>
      <button data-v="themes">Themes</button>
    </div>
  </div>
  <div class="chipbar" id="chips">__CHIPS__</div>
  <div class="countline"><span id="count"></span>
    <button id="clear" hidden>Clear all</button></div>
</div></div>

<section style="padding-top:0"><div class="wrap">
  <div class="grid" id="grid">__CARDS__</div>
  <div class="qlist" id="qlist" hidden></div>
  <div class="tchart" id="tchart" hidden></div>
  <p id="empty" hidden style="margin:60px 0;text-align:center;color:var(--ink-3)">
    Nothing matches that. <button onclick="document.getElementById('clear').click()"
    style="background:none;border:0;color:var(--accent);text-decoration:underline;
    cursor:pointer;font:inherit">Clear the filters</button></p>
</div></section>

<dialog id="dl"><div class="dl-h">
  <div><h3 id="dl-title"></h3><p id="dl-sub"></p></div>
  <button id="dl-x" aria-label="Close">&times;</button>
</div><div class="dl-b" id="dl-body"></div></dialog>

<script>
const ROWS = __PAYLOAD__;
const LABELS = __LABELS__;
const $ = s => document.querySelector(s);
let view = 'cards', term = '', picked = new Set();

const norm = s => (s||'').toLowerCase();
ROWS.forEach(r => r._h = norm(r.text + ' ' + r.q.join(' ') + ' ' + r.desc.join(' ')));

function esc(s){ return s.replace(/[&<>]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[c])); }

/* the snippet a card shows: a matching line if searching, else the best quote */
function snippet(r){
  if(term){
    const i = r._h.indexOf(term);
    if(i > -1){
      const s = Math.max(0, i - 60), t = r.text.length ? r.text : r.q.join(' ');
      const src = r._h.indexOf(term) > -1 && norm(r.text).indexOf(term) > -1 ? r.text : r.q.join(' · ');
      const j = norm(src).indexOf(term);
      if(j > -1){
        const a = Math.max(0, j - 70), b = Math.min(src.length, j + term.length + 90);
        return (a ? '…' : '') + esc(src.slice(a, j)) + '<mark>' + esc(src.slice(j, j + term.length))
             + '</mark>' + esc(src.slice(j + term.length, b)) + (b < src.length ? '…' : '');
      }
    }
  }
  return r.q.length ? '“' + esc(r.q[0]) + '”' : '';
}

function matches(r){
  if(term && r._h.indexOf(term) === -1) return false;
  for(const t of picked) if(r.themes.indexOf(t) === -1) return false;
  return true;
}

function render(){
  const hits = ROWS.filter(matches);
  const ids = new Set(hits.map(r => r.id));

  document.querySelectorAll('.lc').forEach(el => {
    const r = ROWS[+el.dataset.i];
    const on = ids.has(r.id);
    el.classList.toggle('gone', !on);
    if(on) el.querySelector('.lc-q').innerHTML = snippet(r);
  });

  $('#count').textContent = hits.length === ROWS.length
    ? ROWS.length + ' letters' : hits.length + ' of ' + ROWS.length + ' letters';
  $('#clear').hidden = !(term || picked.size);
  $('#empty').hidden = hits.length > 0 || view === 'themes';
  $('#grid').hidden = view !== 'cards';
  $('#qlist').hidden = view !== 'quotes';
  $('#tchart').hidden = view !== 'themes';

  if(view === 'quotes'){
    $('#qlist').innerHTML = hits.flatMap(r => r.q.map(q =>
      '<div class="qi"><p>“' + esc(q) + '”</p><span data-open="' + r.id + '">'
      + (r.yrs ? r.yrs + ' years of service' : 'Holman Correctional Facility')
      + (r.dr ? ' · death row' : '') + '</span></div>')).join('')
      || '<p style="color:var(--ink-3)">No quotes match that.</p>';
  }
  if(view === 'themes'){
    const c = {};
    hits.forEach(r => r.themes.forEach(t => c[t] = (c[t]||0) + 1));
    const rowsT = Object.entries(c).sort((a,b) => b[1] - a[1]);
    const max = rowsT.length ? rowsT[0][1] : 1;
    $('#tchart').innerHTML = rowsT.map(([t, n]) =>
      '<button class="tr" data-t="' + t + '"><span class="tlab">' + LABELS[t]
      + '</span><span class="tbarwrap"><span class="tbar" style="width:'
      + Math.max(2, n / max * 100) + '%"></span></span><span class="tnum">'
      + n + '</span></button>').join('')
      || '<p style="color:var(--ink-3)">Nothing to chart.</p>';
  }
}

$('#q').addEventListener('input', e => { term = norm(e.target.value.trim()); render(); });
$('#chips').addEventListener('click', e => {
  const b = e.target.closest('.chip'); if(!b) return;
  const t = b.dataset.t;
  picked.has(t) ? picked.delete(t) : picked.add(t);
  b.classList.toggle('on', picked.has(t));
  render();
});
document.querySelector('.views').addEventListener('click', e => {
  const b = e.target.closest('button'); if(!b) return;
  view = b.dataset.v;
  document.querySelectorAll('.views button').forEach(x => x.classList.toggle('on', x === b));
  render();
});
$('#clear').addEventListener('click', () => {
  term = ''; picked.clear(); $('#q').value = '';
  document.querySelectorAll('.chip').forEach(c => c.classList.remove('on'));
  render();
});
$('#tchart').addEventListener('click', e => {
  const b = e.target.closest('.tr'); if(!b) return;
  picked.add(b.dataset.t);
  document.querySelectorAll('.chip').forEach(c => c.classList.toggle('on', picked.has(c.dataset.t)));
  view = 'cards';
  document.querySelectorAll('.views button').forEach(x => x.classList.toggle('on', x.dataset.v === 'cards'));
  render();
});

/* ---- detail ---- */
const dl = $('#dl');
function open(r){
  $('#dl-title').textContent = r.name || 'A letter to the Governor';
  $('#dl-sub').textContent = [r.role, r.yrs ? r.yrs + ' years of service' : null,
    r.dr ? 'worked death row' : null, r.date].filter(Boolean).join(' · ');
  $('#dl-body').innerHTML =
    (r.img ? '<img src="img/' + r.img + '" alt="">' : '')
    + (r.q.length ? '<h4>In their words</h4>'
        + r.q.map(q => '<p class="dl-q">“' + esc(q) + '”</p>').join('') : '')
    + (r.themes.length ? '<h4>What this letter says</h4><p class="lc-d">'
        + r.themes.map(t => '<span>' + LABELS[t] + '</span>').join('') + '</p>' : '')
    + (r.desc.length ? '<h4>How they describe Mark</h4><p class="lc-d">'
        + r.desc.map(d => '<span>' + esc(d) + '</span>').join('') + '</p>' : '')
    + '<h4>The full letter</h4><div class="dl-t">' + esc(r.text) + '</div>';
  dl.showModal();
}
document.addEventListener('click', e => {
  const card = e.target.closest('.lc');
  if(card){ open(ROWS[+card.dataset.i]); return; }
  const q = e.target.closest('[data-open]');
  if(q){ open(ROWS.find(r => r.id === q.dataset.open)); return; }
});
$('#dl-x').addEventListener('click', () => dl.close());
dl.addEventListener('click', e => { if(e.target === dl) dl.close(); });

render();
</script>
""".replace('__CARDS__', cards).replace('__CHIPS__', chips) \
   .replace('__PAYLOAD__', payload) \
   .replace('__LABELS__', json.dumps(O.THEME_LABELS, ensure_ascii=False)) \
   .replace('__YRS__', str(yrs)).replace('__DR__', str(n_dr)) \
   .replace('__EXEC__', str(n_exec))
