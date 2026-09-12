# -*- coding: utf-8 -*-
"""Mercy for Mark — static site generator.

Text is the clinic's own language from the 20 Aug snapshot of the Squarespace
site, cleaned of typos and template leftovers and reordered. Nothing invented.
"""
import os, re
import mark_story as MS

OUT = os.path.dirname(os.path.abspath(__file__))

NAV = [('mark.html', 'Meet Mark'),
       ('officers.html', 'The Officers'),
       ('why-clemency.html', 'Why Clemency'),
       ('faq.html', 'FAQ')]

HEAD = """<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex, nofollow">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,300..600;1,6..72,300..500&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
</head><body>
<a class="skip" href="#main">Skip to content</a>
<header class="nav"><div class="wrap">
  <a class="wordmark" href="index.html">Mercy for <s>Mark</s></a>
  <button class="navtoggle" aria-expanded="false" aria-controls="navlinks">Menu</button>
  <nav class="navlinks" id="navlinks">{links}
    <a class="cta" href="help.html">Take action</a>
  </nav>
</div></header>
<main id="main">
"""

FOOT = """</main>
<footer class="foot"><div class="wrap">
  <div>
    <a class="wordmark" href="index.html">Mercy for <s>Mark</s></a>
    <p>Mark Allen Jenkins has been on Alabama's death row for more than
    thirty-five years. He will never be released. We are asking Governor Ivey
    to let him die of natural causes in prison.</p>
  </div>
  <div><h4>The case</h4><ul>
    <li><a href="mark.html">Mark's story</a></li>
    <li><a href="officers.html">The officers</a></li>
    <li><a href="why-clemency.html">Why clemency</a></li>
    <li><a href="faq.html">Questions</a></li>
  </ul></div>
  <div><h4>Take action</h4><ul>
    <li><a href="help.html">Ways to help</a></li>
    <li><a href="mailto:teammarkjenkins@gmail.com">teammarkjenkins@gmail.com</a></li>
  </ul></div>
  <span class="base">Questions, comments, or ideas on how to help Mark?
  Email <a href="mailto:teammarkjenkins@gmail.com">teammarkjenkins@gmail.com</a>.
  &nbsp;&middot;&nbsp; Legal representation by the UC Berkeley Law Death Penalty Clinic.</span>
</div></footer>
<script>
document.querySelector('.navtoggle').addEventListener('click', function(){
  var n = document.getElementById('navlinks');
  var open = n.classList.toggle('open');
  this.setAttribute('aria-expanded', open);
});
var chap = document.querySelectorAll('.chapnav a');
if(chap.length){
  var rail = document.getElementById('rail');
  document.body.classList.add('has-rail');
  var secs = [].map.call(chap, function(a){ return document.querySelector(a.getAttribute('href')); });
  var cur = 0;
  var nextBtn = document.getElementById('railnext');
  var topBtn = document.getElementById('railtop');

  var sync = function(){
    var y = window.scrollY + 180, i = 0;
    secs.forEach(function(s, n){ if(s && s.offsetTop <= y) i = n; });
    cur = i;
    chap.forEach(function(a, n){ a.classList.toggle('on', n === i); });
    if(nextBtn){
      var more = i < secs.length - 1;
      nextBtn.disabled = !more;
      nextBtn.firstChild.nodeValue = more
        ? 'Next: ' + chap[i + 1].textContent.replace(/^\d+\.\s*/, '') + ' '
        : 'End ';
    }
  };
  if(nextBtn) nextBtn.addEventListener('click', function(){
    var t = secs[cur + 1]; if(t) t.scrollIntoView({behavior:'smooth', block:'start'});
  });
  if(topBtn) topBtn.addEventListener('click', function(){
    window.scrollTo({top:0, behavior:'smooth'});
  });

  /* the rail takes over the moment the header's contents list scrolls away */
  var head = document.getElementById('headtoc') || document.querySelector('.hero');
  if(head && 'IntersectionObserver' in window){
    new IntersectionObserver(function(e){
      rail.classList.toggle('show', !e[0].isIntersecting);
    }, {threshold:0}).observe(head);
  } else {
    window.addEventListener('scroll', function(){
      rail.classList.toggle('show', window.scrollY > 420);
    }, {passive:true});
  }
  window.addEventListener('scroll', sync, {passive:true}); sync();
}
document.querySelectorAll('.scrolly').forEach(function(sc){
  var trig = sc.querySelectorAll('.track [data-fig]');
  var figs = sc.querySelectorAll('.stage figure');
  if(!trig.length || !figs.length) return;
  var sync = function(){
    var line = window.innerHeight * 0.42, cur = trig[0].getAttribute('data-fig');
    trig.forEach(function(t){
      if(t.getBoundingClientRect().top <= line) cur = t.getAttribute('data-fig');
    });
    figs.forEach(function(f){
      f.classList.toggle('on', f.getAttribute('data-fig') === cur);
    });
  };
  window.addEventListener('scroll', sync, {passive:true});
  window.addEventListener('resize', sync);
  sync();
});
/* the scroll-pinned blocks in Mark's story */
document.querySelectorAll('.pinned').forEach(function(sec){
  var pin = sec.querySelector('.pin');
  var kind = sec.getAttribute('data-kind');
  var cards = sec.querySelectorAll('.ccard');
  var steps = sec.querySelectorAll('.pin-text > p, .pin-text > .tstep');
  var figs = sec.querySelectorAll('.pin-media figure, .collage figure');
  var dots = sec.querySelectorAll('.pin-foot span');
  var cur = sec.querySelector('.pin-foot b');
  var num = function(a){ return (sec.getAttribute(a) || '').split(',')
              .filter(function(s){ return s !== ''; }).map(Number); };
  var map = num('data-map'), figmap = num('data-figs');
  var n = kind === 'cards' ? cards.length : map.length;
  var active = -1;
  if(!pin || !n) return;

  var top = 67;
  function size(){
    var vh = window.innerHeight - 67;
    top = Math.round(67 + Math.max(0, (vh - pin.offsetHeight) / 2));
    pin.style.top = top + 'px';
    sec.style.height = (vh * n) + 'px';
  }
  function sync(){
    var travel = sec.offsetHeight - pin.offsetHeight;
    var p = travel > 0
      ? Math.min(Math.max((top - sec.getBoundingClientRect().top) / travel, 0), 1) : 0;
    var i = Math.min(n - 1, Math.floor(p * n));
    if(i === active) return;
    active = i;
    if(kind === 'cards'){
      cards.forEach(function(el, k){ el.classList.toggle('on', k === i); });
      return;
    }
    steps.forEach(function(el, k){ el.classList.toggle('on', k === map[i]); });
    if(kind === 'collage'){
      figs.forEach(function(el, k){ el.classList.toggle('on', k <= i); });
    } else if(figmap.length === n){
      figs.forEach(function(el, k){ el.classList.toggle('on', k === figmap[i]); });
    }
    dots.forEach(function(el, k){ el.classList.toggle('on', k === i); });
    if(cur) cur.textContent = i + 1;
  }
  window.addEventListener('scroll', sync, {passive:true});
  window.addEventListener('resize', function(){ size(); active = -1; sync(); });
  window.addEventListener('load', function(){ size(); active = -1; sync(); });
  size(); sync();
});
if('IntersectionObserver' in window){
  var rio = new IntersectionObserver(function(es){
    es.forEach(function(e){
      if(e.isIntersecting){ e.target.classList.add('in'); rio.unobserve(e.target); }
    });
  }, {threshold:0.2});
  document.querySelectorAll('.reveal').forEach(function(el){ rio.observe(el); });
} else {
  document.querySelectorAll('.reveal').forEach(function(el){ el.classList.add('in'); });
}
document.querySelectorAll('.contread').forEach(function(b){
  b.addEventListener('click', function(){
    var t = document.querySelector(b.getAttribute('data-to'));
    if(t) t.scrollIntoView({behavior:'smooth', block:'start'});
  });
});
var zooms = document.querySelectorAll('button.zoom');
if(zooms.length){
  var lb = document.createElement('dialog');
  lb.className = 'lightbox';
  lb.innerHTML = '<img alt=""><div class="lb-bar"><span></span>' +
    '<button type="button">Close</button></div>';
  document.body.appendChild(lb);
  var lbImg = lb.querySelector('img'), lbCap = lb.querySelector('span');
  zooms.forEach(function(b){
    b.addEventListener('click', function(){
      var im = b.querySelector('img');
      lbImg.src = im.src; lbImg.alt = im.alt || '';
      var fc = b.parentNode.querySelector('figcaption');
      lbCap.textContent = fc ? fc.textContent : (im.alt || '');
      lb.showModal();
    });
  });
  lb.querySelector('.lb-bar button').addEventListener('click', function(){ lb.close(); });
  lb.addEventListener('click', function(e){ if(e.target === lb) lb.close(); });
}
if(window.__R){
  var TIERTXT = {
    2:['Documented in the record','This appears in records reviewed by Dr. Ouaou, or is affirmed in his own findings.'],
    1:['Reported, and consistent with the record',"His own account. Dr. Ouaou states that records corroborate and confirm nearly all aspects of the history he reported, but this specific factor is not independently documented."]};

  /* a marked factor opens its source in a panel beside the factor itself */
  var closeSide = function(body){
    var s = body.querySelector('.rf-side');
    if(s){ s.hidden = true; s.removeAttribute('style'); }
    body.querySelectorAll('[data-r]').forEach(function(o){
      o.setAttribute('aria-pressed', 'false'); });
  };
  var placeSide = function(side, btn, body){
    var b = body.getBoundingClientRect(), r = btn.getBoundingClientRect();
    var w = side.offsetWidth, h = side.offsetHeight;
    var left = r.right - b.left + 14;
    if(left + w > b.width) left = r.left - b.left - w - 14;
    if(left < 0) left = Math.max(0, (b.width - w) / 2);
    var top = r.top - b.top - 10;
    top = Math.max(0, Math.min(top, Math.max(0, body.offsetHeight - h)));
    side.style.left = Math.round(left) + 'px';
    side.style.top = Math.round(top) + 'px';
  };
  document.querySelectorAll('[data-r]').forEach(function(btn){
    btn.addEventListener('click', function(){
      var d = window.__R[btn.getAttribute('data-r')]; if(!d) return;
      var body = btn.closest('.acc-body') || btn.closest('.rf-outside');
      var side = body && body.querySelector('.rf-side');
      if(!side) return;
      var already = btn.getAttribute('aria-pressed') === 'true';
      closeSide(body);
      if(already) return;
      btn.setAttribute('aria-pressed', 'true');
      var t = TIERTXT[d.tier];
      side.innerHTML = '<button class="cls" type="button" aria-label="Close">&times;</button>' +
        '<p class="where">' + d.where + '</p><h4>' + d.label + '</h4>' +
        '<blockquote>&ldquo;' + d.src + '&rdquo;</blockquote>' +
        '<p class="tier"><s>' + t[0] + '.</s> ' + t[1] + '</p>';
      side.hidden = false;
      placeSide(side, btn, body);
      side.querySelector('.cls').addEventListener('click', function(e){
        e.stopPropagation(); closeSide(body);
      });
    });
  });
  /* closing a period puts it back the way it was found */
  document.querySelectorAll('.acc').forEach(function(acc){
    acc.addEventListener('toggle', function(){
      var body = acc.querySelector('.acc-body');
      if(body) closeSide(body);
    });
  });

  /* a diagnostic finding opens directly beneath the strip */
  var dpanel = document.getElementById('dpanel');
  document.querySelectorAll('[data-d]').forEach(function(btn){
    btn.addEventListener('click', function(){
      var d = window.__R[btn.getAttribute('data-d')]; if(!d || !dpanel) return;
      var already = btn.getAttribute('aria-pressed') === 'true';
      document.querySelectorAll('[data-d]').forEach(function(o){
        o.setAttribute('aria-pressed','false'); });
      if(already){
        dpanel.innerHTML = '<p class="empty">Select a finding above to see the supporting line from the report.</p>';
        return;
      }
      btn.setAttribute('aria-pressed','true');
      dpanel.innerHTML = '<p class="where">' + d.where + '</p>' +
        '<blockquote>&ldquo;' + d.src + '&rdquo;</blockquote>';
    });
  });
}
</script>
</body></html>
"""

def page(slug, title, desc, body):
    links = ''.join(
        '\n    <a href="%s"%s>%s</a>' % (h, ' class="on"' if h == slug else '', t)
        for h, t in NAV)
    html = HEAD.format(title=title, desc=desc, links=links) + body + FOOT
    open(os.path.join(OUT, slug), 'w', encoding='utf-8').write(html)
    return slug, len(html)

# ============================================================== HOME
HOME = """
<section class="hero full"><div class="wrap">
  <div>
    <p class="eyebrow">Clemency for Mark Allen Jenkins</p>
    <h1>The officers who guarded him are asking the Governor to <em class="hl">spare his life</em>.</h1>
    <p class="lede">More than sixty Alabama correctional officers have written to
    Governor Ivey on behalf of a man on death row at Holman. They are the people
    who understand best what a death sentence means. Not one of them believes
    Mark Jenkins should be executed.</p>
    <div class="btnrow">
      <a class="btn" href="officers.html">Read the letters</a>
      <a class="btn ghost" href="mark.html">Meet Mark</a>
      <a class="btn ghost arrow" href="#ask">Explore the site<span>&darr;</span></a>
    </div>
  </div>
  <figure class="whole">
    <img src="img/mark-2026.jpg" alt="Mark Jenkins photographed at Holman Correctional Facility in August 2026" width="1085" height="1450">
    <figcaption>Mark Jenkins at Holman Correctional Facility, August 2026.</figcaption>
  </figure>
</div></section>

<div class="statband"><div class="wrap">
  <div class="head">
    <h3>Where the case stands</h3>
    <p>Every figure here comes from the letters themselves or from the record of
    Mark's trial.</p>
  </div>
  <div class="stats">
    <div class="stat"><b>60</b><span>correctional officers have written to the Governor asking her to spare him</span></div>
    <div class="stat"><b>890+</b><span>years of service to the Alabama Department of Corrections among them</span></div>
    <div class="stat"><b>35</b><span>years Mark has lived on Alabama's death row</span></div>
    <div class="stat"><b>2</b><span>jurors voted for life. Alabama sentenced him to death anyway</span></div>
  </div>
</div></div>

<section><div class="wrap">
  <div class="media">
    <div>
      <p class="eyebrow">Meet Mark</p>
      <h2>He is fifty-eight, and he has been on death row since he was twenty-three.</h2>
      <p style="color:var(--ink-2);max-width:56ch">He has lived at Holman
      Correctional Facility since 1991. For much of that time he has worked as a
      hall runner, a job given only to the men the officers trust. His story is
      told in four parts, in order, and none of them is hidden behind the
      others.</p>
      <div class="btnrow"><a class="btn" href="mark.html">Explore Mark's story</a></div>
    </div>
    <div>
      <figure>
        <img class="full" src="img/mark-visit-1998.jpg" alt="A photograph of Mark Jenkins with his brother's family during a prison visit in 1998, inscribed in Mark's handwriting" style="border:1px solid var(--rule)">
        <figcaption>&ldquo;What a wonderful day I had. May 18, 1998. Thank you
        Bro!&rdquo; A visit from his brother, inscribed in Mark's own hand.</figcaption>
      </figure>
    </div>
  </div>
</div></section>

<section class="dark"><div class="wrap">
  <div class="media">
    <div>
      <p class="eyebrow">The Officers</p>
      <h2>Nobody has watched Mark Jenkins longer than the officers at Holman.</h2>
      <p>These correctional officers have known Mark for years and, in some
      cases, decades. As Mark has spent more than thirty-five years on death row,
      nobody knows him better. And these officers, the people who understand best
      what sentencing someone to death means, do not believe he should
      be executed.</p>
      <div class="btnrow"><a class="btn" href="officers.html">Explore the archive</a></div>
    </div>
    <div>
      <p class="pull">&ldquo;I hope that my experience as a career ADOC officer
      counts for something, that my word counts for something.&rdquo;</p>
      <p class="pull-attr">Retired correctional officer &middot; 23 years of service</p>
      <div class="faces" style="margin-top:30px">__FACES__</div>
      <p class="small" style="margin-top:22px;color:#8A857A">Sixty letters.
      Nine of the writers served on or witnessed executions.</p>
    </div>
  </div>
</div></section>

<section class="band" id="ask"><div class="wrap" style="text-align:center">
  <p class="eyebrow">What Mark is asking</p>
  <h2 style="max-width:21ch;margin-left:auto;margin-right:auto">Mark will never
  leave prison. The only question is how he dies there.</h2>
  <p class="serif-lede" style="max-width:60ch;margin:0 auto 26px;font-style:italic">
  Under the Alabama Constitution, the Governor has the authority, and the right,
  to commute a death sentence to life in prison without the
  possibility of parole.</p>
  <div class="twocol" style="max-width:920px;margin-left:auto;margin-right:auto">
    <p>Mark and his legal team are not asking for any possibility of future
    release. They are asking that the Governor allow Mark the opportunity to die a
    natural death within the prison walls instead of being executed.</p>
    <p>This power exists precisely because the judicial process is not infallible.
    Some critical considerations, including the support of more than sixty Alabama
    correctional officers, could not be considered by any court.</p>
  </div>
</div></section>

<section><div class="wrap">
  <p class="eyebrow">Why Clemency</p>
  <h2>Four things a court was never allowed to weigh.</h2>
  <div class="cards four" style="margin-top:34px">
    <article class="card">
      <span class="n">One</span>
      <h3>Mark is intellectually disabled</h3>
      <p>The Supreme Court has barred the execution of people with intellectual
      disability. A neuropsychologist has diagnosed Mark with it. No court has
      ever given him a chance to present that evidence.</p>
      <a class="textlink" href="why-clemency.html#disability">The diagnosis and the record</a>
    </article>
    <article class="card">
      <span class="n">Two</span>
      <h3>The jury never heard about his childhood</h3>
      <p>A forensic psychologist calls Mark&rsquo;s childhood one of the worst cases
      of abuse she has seen in her career. His trial attorneys told the jury not a
      single word about it.</p>
      <a class="textlink" href="why-clemency.html#childhood">What was never told</a>
    </article>
    <article class="card">
      <span class="n">Three</span>
      <h3>Mark&rsquo;s jury was not unanimous</h3>
      <p>Two jurors voted for a life sentence. In nearly every other state Mark
      would have received one. Alabama is one of only two states that allows a
      death sentence without a unanimous jury.</p>
      <a class="textlink" href="why-clemency.html#jury">What the jury was never told</a>
    </article>
    <article class="card">
      <span class="n">Four</span>
      <h3>Mark is not the man who arrived</h3>
      <p>Mark was twenty-one. He is fifty-eight. The officers who supervised him
      describe someone peaceful, trustworthy and good-natured, who they believe
      would pose no threat to anyone.</p>
      <a class="textlink" href="why-clemency.html#transformation">The thirty-five years</a>
    </article>
  </div>
  <div class="btnrow"><a class="btn" href="why-clemency.html">The full case for clemency</a></div>
</div></section>

<section class="band"><div class="wrap">
  <div style="text-align:center;max-width:760px;margin:0 auto">
    <p class="eyebrow">Take action</p>
    <h2>It matters that people know his name.</h2>
    <p class="lede measure" style="margin:0 auto">Three things you can do, none of
    them difficult.</p>
  </div>
  <div class="cards" style="margin-top:38px">
    <article class="card"><span class="n">One</span><h3>Share his story</h3>
      <p>Most people have never heard that sixty correctional officers asked a
      governor to spare a man on death row.</p></article>
    <article class="card"><span class="n">Two</span><h3>Write to Governor Ivey</h3>
      <p>Tell her you support clemency for Mark, and why it matters to you.</p>
      <a class="textlink" href="help.html">How to write</a></article>
    <article class="card"><span class="n">Three</span><h3>Get updates</h3>
      <p>Events and actions that will spotlight Mark's case in the months
      ahead.</p>
      <a class="textlink" href="mailto:teammarkjenkins@gmail.com">Sign up</a></article>
  </div>
</div></section>
"""

# ============================================================== MARK
MARK = """
<section class="hero full align-end" id="mhead" style="padding:34px 0 24px"><div class="wrap"
  style="grid-template-columns:1.06fr .94fr;gap:56px">
  <div>
    <p class="eyebrow">Mark Allen Jenkins</p>
    <h1>Mark is fifty-eight years old and he has been on death row since he was
    twenty-three.</h1>
    <p class="lede" style="max-width:46ch;margin-bottom:22px">This is his story: who
    he is today, what was done to him first, what he did, and what he has
    made of thirty-five years incarcerated.</p>
    <div class="btnrow" style="margin-top:4px">
      <a class="btn arrow" href="#now">Explore his story<span>&darr;</span></a>
    </div>
  </div>
  <figure class="natural">
    <img src="img/mark-visit-1998.jpg" alt="Mark Jenkins with his brother's family during a prison visit in 1998, inscribed in Mark's handwriting">
    <figcaption>A visit from Mark's brother, inscribed in Mark's own hand.</figcaption>
  </figure>
</div></section>

<section class="cwband"><div class="wrap"><div class="inner">
  <p>Parts of this page may be difficult to read. It describes the abuse Mark
  suffered as a child, including sexual abuse, beatings and violence inside his
  family, and it discusses the crime for which Mark was convicted.</p>
</div></div></section>

<div class="longform">

<article class="chapter" id="now">
__ACT0__
<button class="contread" data-to="#before"><i></i><span>Continue</span><em>&darr;</em></button>
</article>

<article class="chapter tone" id="before">
__ACT1__

  <div class="inset">
    <p class="k">The record of abuse</p>
    <h3>None of this was just a matter of anyone's word</h3>
    <p>It was written down at the time, by teachers, social workers, probation
    officers and doctors who saw it happening. Select any page to read it.</p>
    <div class="docgrid" style="margin-top:22px">
      <button class="zoom" type="button"><img class="doc" src="img/doc-a.jpg" alt="Excerpt from a 1981 collateral report describing Mark constantly running away and his parents' indifference"></button>
      <button class="zoom" type="button"><img class="doc" src="img/doc-c.jpg" alt="Excerpt from an evidentiary report recording that Mark's parents were going to beat him"></button>
      <button class="zoom" type="button"><img class="doc" src="img/doc-e.jpg" alt="Excerpt from a report recording that Mark came from a dysfunctional home and wanted to be loved by his family"></button>
      <button class="zoom" type="button"><img class="doc" src="img/doc-b.jpg" alt="Handwritten note in a record reading that the family substantially rejected Mark"></button>
    </div>
    <p class="small" style="margin:16px 0 0">Contemporaneous records,
    1981&ndash;1983.</p>
    <p class="boyd">Dr. Sara Boyd, a board-certified forensic psychologist and
    associate faculty at the University of Virginia, has said that Mark's childhood is
    one of the worst cases of abuse she has seen in her entire career. During Mark's
    trial, his attorneys did not tell the jury a single word about it, or about
    anything that might have led to the moment in which he took an innocent life.</p>
  </div>

__ACT2__

  <div class="inset">
    <p class="k">The record of disability</p>
    <h3>His disability is not a claim made for this case</h3>
    <p>It was measured and written down long before any of this mattered to a
    court, by the schools that held him back and by the neuropsychologist who
    examined him over two days at Holman. Select any passage to read it.</p>
    <div class="docgrid" style="margin-top:22px">
      <button class="zoom" type="button"><img class="doc" src="img/ouaou-a.jpg" alt="Excerpt from Dr. Ouaou's assessment concluding that Mr. Jenkins has an intellectual disability, with a Full-Scale IQ of 74, or 69.8 adjusted for the Flynn Effect"></button>
      <button class="zoom" type="button"><img class="doc" src="img/ouaou-b.jpg" alt="Table of Mark's WAIS-IV scores, showing a Full-Scale IQ of 74 at the 4th percentile and 69.8 with the Flynn Effect"></button>
      <button class="zoom" type="button"><img class="doc" src="img/ouaou-c.jpg" alt="Excerpt recording that Mark's executive functioning abilities are severely impaired, at or below the 1st percentile relative to age-matched peers"></button>
      <button class="zoom" type="button"><img class="doc" src="img/ouaou-d.jpg" alt="Excerpt recording that Mark's seventh-grade achievement scores were at second- and third-grade levels and that he was held back"></button>
    </div>
    <p class="small" style="margin:16px 0 0">Forensic neuropsychological
    assessment of Mark Jenkins, Robert H. Ouaou, Ph.D., May 2023.</p>
    <p class="boyd">Dr. Ouaou is a clinical and forensic neuropsychologist with more
    than twenty-five years of experience. He examined Mark at Holman over two days
    in November 2022 and reviewed the records of his childhood. His conclusion was
    that Mark has an intellectual disability, that it began before he was eighteen,
    and that it continues to this day. <a class="textlink"
    href="why-clemency.html#disability">What that means for clemency</a>.</p>
  </div>

<button class="contread" data-to="#crime"><i></i><span>Continue</span><em>&darr;</em></button>
</article>

<article class="chapter snug" id="crime">
__ACT3SIDE__
__ACT3CARDS__
<button class="contread" data-to="#since"><i></i><span>Continue</span><em>&darr;</em></button>
</article>

<article class="chapter tone" id="since">
__ACT4__
</article>

<article class="chapter actblock" id="next">
  <h2>What you can do next</h2>
  <p>Mark's case does not rest on his story alone. Read what the officers wrote,
  see the three grounds for clemency, or take an action of your own.</p>
  <div class="btnrow">
    <a class="btn" href="officers.html">Explore the letters</a>
    <a class="btn ghost" href="why-clemency.html">Why clemency</a>
    <a class="btn ghost" href="help.html">Take action</a>
  </div>
</article>

</div>

<nav class="chapnav" id="rail"><div class="wrap">
  <button class="railbtn" id="railtop">&uarr; Top</button>
  <div class="links">
    <a href="#now">01. Today</a>
    <a href="#before">02. Before</a>
    <a href="#crime">03. The crime</a>
    <a href="#since">04. Atonement</a>
  </div>
  <button class="railbtn" id="railnext">Next <span>&darr;</span></button>
</div></nav>
""" \
  .replace('__ACT0__', MS.side('act0', MS.A0_PARAS, [], still=MS.A0_STILL,
                               head=MS.head('01.', 'Today: Who Mark is now'))) \
  .replace('__ACT1__', MS.side('act1', MS.A1_PARAS, MS.A1_STEPS,
      head=MS.head('02.', 'Before: A childhood of extreme abuse and violence'))) \
  .replace('__ACT2__', MS.side('act2', MS.A2_PARAS, MS.A2_STEPS, tail=MS.A2_BTN,
      head=MS.head('02.', 'Before: A childhood of extreme abuse and violence',
                   quiet=True))) \
  .replace('__ACT3SIDE__', MS.side('act3', MS.A3_PARAS, MS.A3_STEPS,
      head=MS.head('03.', "Mark's crime"))) \
  .replace('__ACT3CARDS__', MS.cards('act3end', MS.A3_CARDS)) \
  .replace('__ACT4__', MS.collage('act4', MS.A4_PARAS, MS.A4_PHOTOS,
      tail=MS.A4_BTN,
      head=MS.head('04.', 'Thirty-five years: Atonement')))

def main():
    import json
    # four consented portraits for the home page face row
    imgs = json.load(open('/home/claude/work/images.json'))
    import glob, os
    faces = sorted(os.path.basename(f) for f in glob.glob(OUT + '/img/p-L*.jpg'))[:5]
    face_html = ''.join('<img src="img/%s" alt="">' % f for f in faces)

    built = []
    built.append(page('index.html', 'Mercy for Mark',
                      'More than sixty Alabama correctional officers are asking '
                      'Governor Ivey to commute the death sentence of Mark Allen Jenkins.',
                      HOME.replace('__FACES__', face_html)))
    built.append(page('mark.html', "Mark's Story | Mercy for Mark",
                      "Who Mark Jenkins is, what he did, what was done to him first, "
                      "and what he has made of thirty-five years.",
                      MARK))
    import pages2
    built.append(page('why-clemency.html', 'Why Clemency | Mercy for Mark',
                      "Mark Jenkins is intellectually disabled and his jury was not "
                      "unanimous. No court will weigh either now.",
                      pages2.why_clemency()))
    import officers_page
    built.append(page('officers.html', 'The Officers | Mercy for Mark',
                      "Sixty Alabama correctional officers wrote individually to the "
                      "Governor asking her to spare Mark Jenkins. Search every word.",
                      officers_page.render()))
    built.append(page('faq.html', 'Questions | Mercy for Mark',
                      "The case, the crime, what clemency means, and what happens "
                      "next, answered plainly.",
                      pages2.faq_page()))
    built.append(page('help.html', 'Take Action | Mercy for Mark',
                      "Concrete things you can do to help Mark Jenkins.",
                      pages2.HELP))
    # The postcard project is held back until there are enough cards.
    # Restore this block and move _hold/postcards.html back to the root.
    # import postcards
    # built.append(page('postcards.html', 'The Postcard Project | Mercy for Mark',
    # "People of faith across Alabama are writing to the Governor "
    # "by hand. Every card that comes back joins the wall.",
    # postcards.render()))
    for s, n in built:
        print(f'{s:22} {n:>8,} bytes')
    return faces

if __name__ == '__main__':
    print(main())
