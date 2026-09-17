# -*- coding: utf-8 -*-
"""Mark's story, sections 02 to 04: the scroll-pinned narrative blocks.

Three kinds of block, all driven by the same scroll maths:
  side     text on the left, one photograph on the right, both change per step
  cards    centred, no pictures, each card replaces the one before it
  collage  text on the left, photographs accumulate on the right, one per step
Every block also emits a stacked fallback for narrow screens and reduced motion.
"""

# ------------------------------------------------------------- act zero
A0_PARAS = [
 """Mark Jenkins is fifty-eight. He is incarcerated at Holman Correctional Facility in
 Atmore, Alabama and has been since 1991. For much of that time, he has worked as a
 &ldquo;hall runner,&rdquo; a job given only to the men the <a class="textlink"
 href="officers.html">officers trust</a>, the ones who stay out of trouble and can be
 let out of a cell to move around the tier.""",
 """Mark defuses arguments, lifts people up when they are down, tries to make people laugh with corny jokes, and has been, in the words of one officer, &ldquo;100% trustworthy.&rdquo; He has worked for years as a &ldquo;hall runner,&rdquo; a job reserved for the most reliable prisoners. Mark was baptized in the county jail before his trial and has grown in his faith over the years. Mark&rsquo;s relationship with God sustains him.""",
 """Mark has learned to contend with his <a class="textlink"
 href="why-clemency.html#disability">profound intellectual disability</a> and the abuse
 and trauma of his childhood to continue to serve as a support and helper to the
 officers and other incarcerated people around him.""",
]
A0_STILL = ('<figure class="still"><div class="ph"><b>Film to come</b>'
            '<span>The eleven-minute film about Mark\'s life will sit here.</span>'
            '</div></figure>')

# --------------------------------------------------------------- act one
A1_PARAS = [
 """Mark Jenkins was born in 1967, following an affair between his mother, Donna Jo Jenkins, and a sailor. At the time, Donna&rsquo;s husband, Steve Jenkins, was in prison. Mark has never met his biological father.""",
 """Following his birth, Donna abandoned Mark at the hospital. She was later persuaded to retrieve him, but his biological father declined to take responsibility for the newborn. Left alone, Donna raised Mark and his half-siblings in squalor for the first three years of his life, until her husband Steve returned from prison.""",
 """Donna treated Mark with contempt and abuse, even when he was an infant. She beat him, at times hard enough to leave welts on his body. She shook him, called him disparaging names, and hid him in a box under the bathroom sink when company came to visit. She treated him as though he were barely human.""",
 """When Mark was about four, he was left in the care of his grandfather, who sexually abused him. What Mark&rsquo;s grandfather did to Mark would be a capital crime in Alabama today. The sexual trauma led to severe emotional and physical struggles that lasted into Mark&rsquo;s adulthood.""",
]
A1_STEPS = [
 (0, 'child-01.jpg', 'Mark as a very young child, with his siblings.'),
 (1, 'child-03.jpg', 'Mark as a child with his mother, Donna, and his siblings.'),
 (2, 'child-02.jpg', 'Mark as a boy.'),
 (3, 'child-04.jpg', 'Mark as a young child with his grandfather and siblings.'),
]

# --------------------------------------------------------------- act two
A2_BTN = ('<a class="pinbtn" href="why-clemency.html#disability">Explore intellectual '
          'disability as one of the grounds for clemency</a>')
A2_PARAS = [
 """The physical and emotional torment intensified after Donna&rsquo;s husband, Steve, was released from prison. He beat and humiliated Mark, leaving welts, bruises and cuts. Mark was generally not allowed to eat with the family; he scrounged for scraps.""",
 """Mark suffered from incontinence after his grandfather sexually assaulted him. At least once, Steve punished Mark by forcing him to eat his own feces in front of the family.""",
 """Family members reported the abuse to authorities, only to recant when Steve threatened them.""",
 """When Mark&rsquo;s brother reported the abuse, Steve lashed out at the children, threatening, &ldquo;I'll kill you before I go back to prison.&rdquo;""",
 """Mark had one saving grace as a child: his animals. He had a soul-deep love of the family&rsquo;s horses, dogs, and a pig named Eva, and the animals loved him back. Even when he had only scraps of food, he shared what he had with the family dogs.""",
 """Mark&rsquo;s childhood struggles were exacerbated by his intellectual disability, a serious and lifelong neurodevelopmental condition. His IQ score is 74, and his executive functioning&mdash;which includes his ability to plan, to reason, and to adapt&mdash;is at or below the 1st percentile. Mark&rsquo;s disability made it difficult for him to cope with daily life.""",
]
A2_STEPS = [
 (0, 'xmas.jpg',    'Mark with his family at Christmas.'),
 (1, 'teen-01.jpg', "Mark's elementary school photograph."),
 (2, 'teen-03.jpg', 'Mark with his siblings and his mother.'),
 (3, 'teen-02.jpg', 'Mark with one of his brothers.'),
 (4, 'teen-06.jpg', 'Mark, pre-teen, with a fishing rod.'),
 (5, 'teen-04.jpg', "Mark&rsquo;s school photograph."),
]
A2_CLOSE = """Mark had one saving grace as a child: his animals. He had a soul-deep love of the family&rsquo;s horses, dogs, and a pig named Eva, and the animals loved him back. Even when he had only scraps of food, he shared what he had with the family dogs."""

# ------------------------------------------------------------- act three
A3_PARAS = [
 """Mark began running away around age eleven to escape the chaos of his parents'
 home.""",
 """At times, he lived on the streets and begged for change.""",
 """When Mark turned eighteen, he tried to turn his life around and enlist in the armed forces, but he failed the entrance exam. A couple of years later, a friend asked Mark to help the friend&rsquo;s family move to Alabama, and Mark went with them.""",
 """In Alabama, Mark tried to build a new life. But employers took advantage of him, and he still suffered from the emotional and physical effects of his parents&rsquo; abuse. He started drinking heavily.""",
]
A3_STEPS = [
 (0, 'teen-05.jpg',   'Mark in the school yearbook.'),
 (1, 'teen-07.jpg',   "Mark's yearbook portrait."),
 (2, 'lateteens.jpg', 'Mark and one of his brothers in their late teens.'),
 (3, 'lateteens.jpg', 'Mark and one of his brothers in their late teens.'),
]
A3_CARDS = [
 ('title tall', 'April 18, 1989'),
 ('para', """In the early hours of April 18, 1989, Mark had been drinking heavily and drove to a diner where Tammy Hogeland worked. He was just twenty-one years old. She was just twenty-two."""),
 ('para', """Mark and Tammy knew each other, and Tammy left the diner with Mark. At some point, the two got into an argument. During that argument, Mark strangled Tammy to death."""),
 ('para em', """Tammy Hogeland was a young woman with a full life ahead of her, and Mark took that life from her and from her loved ones. Nothing here diminishes the horror of Mark&rsquo;s crime, and neither Mark nor his legal team is asking anyone to ignore the terrible pain he has caused."""),
 ('para short', """In 1991, Mark was convicted of capital murder in St. Clair County and
  sentenced to death. Mark was alone at his trial. Not one member of his family
  came."""),
 ('para', """Mark was horrified by his actions and feels tremendous remorse to this day."""),
]

# -------------------------------------------------------------- act four
A4_PARAS = [
 """Those who know Mark, from family members to correctional officers, have seen how his remorse for the terrible harm he caused has stayed with him and shaped him over the decades.""",
 """Since his incarceration, Mark has worked relentlessly to better himself and to atone for his crime, doing everything from learning to read and working in the prison, to getting baptized and growing in his Christian faith.""",
 """He has become a different man&mdash;a better man&mdash;than the one who arrived on death row more than thirty-five years ago.""",
 """That is not a claim his lawyers are making about him. It is the claim made,
 independently and in their own handwriting, by sixty people who were paid to watch
 him.""",
]
A4_BTN = ('<div class="btnrow"><a class="btn" href="officers.html">'
          'Read what the officers wrote</a></div>')
# file, paragraph, left%, top%, width%, rotation, caption
A4_PHOTOS = [
 ('p4-01.jpg', 0,  1,  6, 38, -3.6, 'Mark with visitors at Holman, in the 1990s.'),
 ('p4-02.jpg', 0, 66,  0, 33,  2.8, 'Mark with visitors at Holman.'),
 ('p4-03.jpg', 1, 20, 52, 50,  1.4, 'Mark with other death row prisoners at Holman and their visitors.'),
 ('p4-04.jpg', 1, 63, 26, 35, -2.2, 'Mark with his brother, Billy, and Billy&rsquo;s friend, 2024.'),
 ('p4-05.jpg', 1,  0, 58, 42,  3.2, 'Mark in Holman&rsquo;s visiting yard, April 2026.'),
 ('p4-06.jpg', 2, 38, 10, 42, -2.6, 'Mark in Holman&rsquo;s visiting yard, April 2026.'),
 ('p4-07.jpg', 2, 60, 58, 43,  2.1, 'Mark in Holman&rsquo;s visiting yard, May 2026.'),
 ('p4-08.jpg', 3, 24, 24, 28, -1.4, 'Mark today.'),
]


# ----------------------------------------------------------------- render
def head(num, title, quiet=False):
    """The section title, carried inside the block so it stays on screen."""
    return ('<div class="pin-head%s"><p class="num">%s</p><h2>%s</h2></div>'
            % (' quiet' if quiet else '', num, title))

def _flow_steps(paras, steps):
    return ''.join(
        '<div class="flow-step"><p>%s</p><figure><img src="img/%s" alt="" loading="lazy">'
        '<figcaption>%s</figcaption></figure></div>' % (paras[p], f, c)
        for p, f, c in steps)


def side(aid, paras, steps, tail='', head='', still=''):
    """Text left, one photograph right; one step per photograph.

    With `still`, the right column holds one thing that does not change and the
    steps are simply the paragraphs.
    """
    if still and not steps:
        steps = [(i, '', '') for i in range(len(paras))]
    shots, figmap = [], []          # consecutive repeats share one figure
    for _, f, c in steps:
        if (f, c) not in shots:
            shots.append((f, c))
        figmap.append(shots.index((f, c)))
    return """
<section class="pinned" id="%s" data-kind="side" data-map="%s" data-figs="%s">
  <div class="pin"><div class="pin-in">
    %s
    <div class="pin-grid">
      <div class="pin-text">%s</div>
      <div class="pin-media">%s</div>
    </div>
    <div class="pin-foot">%s<em><b>1</b> / %d</em></div>
  </div></div>
</section>
<div class="pinflow">%s%s</div>""" % (
      aid, ','.join(str(s[0]) for s in steps),
      ','.join(str(k) for k in figmap), head,
      ''.join('<p>%s</p>' % (t + (tail if i == len(paras) - 1 else ''))
              for i, t in enumerate(paras)),
      still or ''.join(
          '<figure><div class="imgbox"><img src="img/%s" alt="" loading="lazy"></div>'
          '<figcaption>%s</figcaption></figure>' % (f, c) for f, c in shots),
      ''.join('<span></span>' for _ in steps), len(steps),
      (''.join('<p>%s</p>' % t for t in paras) if still
       else _flow_steps(paras, steps)), tail)


def cards(aid, items):
    """Centred, no pictures; each card replaces the one before it."""
    return """
<section class="pinned" id="%s" data-kind="cards">
  <div class="pin"><div class="pin-in"><div class="pin-centre">%s</div></div></div>
</section>
<div class="pinflow centred">%s</div>""" % (
      aid,
      ''.join('<div class="ccard %s">%s<p>%s</p></div>'
              % (k, '<i class="drop"></i>' if ('tall' in k or 'short' in k) else '', t)
              for k, t in items),
      ''.join('<p>%s</p>' % t for _, t in items))


def collage(aid, paras, photos, tail='', head=''):
    """Text left, photographs accumulate on the right, one per step."""
    return """
<section class="pinned" id="%s" data-kind="collage" data-map="%s" data-figs="">
  <div class="pin"><div class="pin-in">
    %s
    <div class="pin-grid wide">
      <div class="pin-text">%s</div>
      <div class="collage">%s</div>
    </div>
    <div class="pin-foot">%s<em><b>1</b> / %d</em></div>
  </div></div>
</section>
<div class="pinflow">%s%s%s</div>""" % (
      aid, ','.join(str(p[1]) for p in photos), head,
      ''.join('<div class="tstep"><p>%s</p>%s</div>'
              % (t, tail if i == len(paras) - 1 else '')
              for i, t in enumerate(paras)),
      ''.join('<figure style="left:%s%%;top:%s%%;width:%s%%;--r:%sdeg;z-index:%d">'
              '<img src="img/%s" alt="" loading="lazy">'
              '<figcaption>%s</figcaption></figure>'
              % (l, t, w, r, 10 + k, f, c)
              for k, (f, _, l, t, w, r, c) in enumerate(photos)),
      ''.join('<span></span>' for _ in photos), len(photos),
      ''.join('<p>%s</p>' % t for t in paras), tail,
      ''.join('<figure class="loose"><img src="img/%s" alt="" loading="lazy">'
              '<figcaption>%s</figcaption></figure>' % (f, c)
              for f, _, _, _, _, _, c in photos))
