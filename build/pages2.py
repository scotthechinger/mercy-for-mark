# -*- coding: utf-8 -*-
"""Why Clemency, How to Help, FAQ. The clinic's own language, cut and reordered."""
import sys, json, html
sys.path.insert(0, '/home/claude/work/id')
from data import GRID, OUTSIDE, DIAGNOSIS, PERIODS, TYPES, SOURCE

E = lambda s: html.escape(s, quote=True)


# ---------------------------------------------------------------- the instrument
def risk_tool():
    """The AAIDD framework as three accordions, with the source docked alongside.

    Two states only, in one colour: marked, or not established. Whether a marked
    factor is documented or reported is disclosed in the panel rather than by a
    second colour, which was doing more to confuse the eye than to inform it.
    """
    total = sum(len(v) for v in GRID.values())
    marked = sum(1 for v in GRID.values() for _, t, _ in v if t > 0)
    doc = sum(1 for v in GRID.values() for _, t, _ in v if t == 2)
    R, accs, n = {}, [], 0

    for period in PERIODS:
        cols, pm, pt = [], 0, 0
        for typ in TYPES:
            chips = []
            for label, tier, src in GRID[(period, typ)]:
                pt += 1
                if tier == 0:
                    chips.append('<p class="rfc off">%s</p>' % E(label)); continue
                pm += 1; n += 1; rid = 'r%d' % n
                R[rid] = {'label': label, 'where': '%s &middot; %s' % (period, typ),
                          'tier': tier, 'src': src}
                chips.append('<button class="rfc" data-r="%s" aria-pressed="false">'
                             '%s</button>' % (rid, E(label)))
            cols.append('<div class="rf-col">%s</div>' % ''.join(chips))
        accs.append(
            '<details class="acc"><summary><b>%s</b><em>%d of %d marked</em>'
            '<span class="caret">+</span></summary>'
            '<div class="acc-body"><div class="rf-cols">%s</div>'
            '<aside class="rf-side" hidden></aside></div></details>'
            % (E(period), pm, pt, ''.join(cols)))

    out = []
    for label, tier, src in OUTSIDE:
        n += 1; rid = 'r%d' % n
        R[rid] = {'label': label, 'tier': tier, 'src': src,
                  'where': 'Named by Dr. Ouaou &middot; outside the framework'}
        out.append('<button class="rfc" data-r="%s" aria-pressed="false">%s</button>' % (rid, E(label)))

    diag = []
    for label, val, gloss, src in DIAGNOSIS:
        n += 1; rid = 'd%d' % n
        R[rid] = {'label': label, 'where': 'Diagnostic finding', 'tier': 2, 'src': src}
        diag.append('<button class="dt" data-d="%s" aria-pressed="false"><i>%s</i>'
                    '<b>%s</b><span>%s</span></button>'
                    % (rid, E(label), E(val), E(gloss)))

    types_head = ''.join('<h5>%s</h5>' % E(t) for t in TYPES)

    return """
  <aside class="insert rftool" id="framework">
    <div class="insert-head">
      <p class="k">The framework</p>
      <h3>%d of the 43 recognised risk factors for intellectual disability are
      documented in Mark's record.</h3>
      <p class="dek">The American Association on Intellectual and Developmental
      Disabilities, the body that defines the condition, sorts its
      causes into four kinds across three periods of life.
      <b>Explore the framework as it applies to Mark.</b></p>
    </div>

    <div class="rf-legend">
      <i><span class="rf-key on"></span> Documented or reported in Mark's record</i>
      <i style="color:var(--ink-3)">Select any marked factor to see where it comes
      from.</i>
    </div>

    <div class="rf-table">
      <div class="rf-head">
        <p class="rf-lab">Life periods &darr;</p>
        <div class="rf-types"><span class="rf-lab">Causes &rarr;</span>%s</div>
      </div>
      %s
    </div>

    <div class="rf-outside">
      <p class="rf-lab">Outside the framework</p>
      <div class="rf-outside-body">
        <p>Dr. Ouaou identifies two further causes of central nervous system damage in
        Mark's history that the standard grid does not have a box for.</p>
        <div class="rf-outside-chips">%s</div>
      </div>
      <aside class="rf-side" hidden></aside>
    </div>
  </aside>

  <p class="k eyebrow-k" style="margin-top:56px">The diagnosis</p>
  <h3 style="margin-top:0">How the diagnosis was established</h3>
  <p class="dek" style="max-width:70ch">Intellectual disability has three diagnostic
  criteria. Dr. Ouaou examined Mark over two days at Holman, tested him, and read the
  records of his childhood. All three criteria were met.</p>
  <div class="dstrip" style="margin-top:22px">%s</div>
  <div class="dpanel" id="dpanel"><p class="empty">Select a finding above to see the
  line from Dr. Ouaou's report that supports it.</p></div>
  <p class="small" style="margin-top:16px">%s</p>
  <script>window.__R = %s;</script>
""" % (doc, types_head, ''.join(accs), ''.join(out),
       ''.join(diag), E(SOURCE), json.dumps(R, ensure_ascii=False))


# ---------------------------------------------------------------- why clemency
def why_clemency():
    return """
<section class="hero full mid" id="headtoc"><div class="wrap">
  <div>
    <p class="eyebrow">Why clemency</p>
    <h1>Four powerful reasons for mercy.</h1>
    <p class="lede">Mark Jenkins was sentenced to death before the Supreme Court
    forbade executing people who were <a href="#disability">intellectually
    disabled</a>, by a jury that never heard of his <a href="#childhood">childhood
    abuse</a>, by a vote that was <a href="#jury">not unanimous</a>, and despite
    <a href="#transformation">Mark's transformation</a> over the last thirty-five
    years.</p>
    <div class="btnrow">
      <a class="btn arrow" href="#disability">Explore the case<span>&darr;</span></a>
    </div>
  </div>
</div></section>

<div class="longform">

<article class="chapter tone" id="disability">
  <p class="num">01. <span>Intellectual disability</span></p>
  <h2>Mark Jenkins is on Alabama's death row even though he is intellectually
  disabled.</h2>

  <div class="intro sans">
    <p>The U.S. Supreme Court has ruled that it is unconstitutional to execute an
    individual with intellectual disability. Governor Ivey must stop Alabama from
    doing so.</p>
  </div>

  <div class="splitmedia tall">
    <div>
      <p>Mark Jenkins is intellectually disabled and has been his entire life.</p>
      <p>Even when Mark was a baby, his grandmother recognized that he seemed slow.
      He read at a third-grade level in fifth grade and stalled there into his
      twenties. Throughout his life he has been taken advantage of by others,
      including his own mother, who extorted money from him, and employers, who
      overworked and underpaid him.</p>
      <p style="margin-bottom:0">Based on extensive testing, a lengthy evaluation,
      and voluminous records from Mark's childhood, neuropsychologist Robert Ouaou,
      Ph.D., diagnosed Mark with intellectual disability.</p>
    </div>
    <figure class="reportfig">
      <a href="docs/neuropsychological-assessment.pdf" target="_blank" rel="noopener">
        <img src="img/report-p1.jpg" alt="First page of the forensic neuropsychological assessment of Mark Jenkins by Robert H. Ouaou, Ph.D.">
      </a>
      <figcaption><a class="textlink"
        href="docs/neuropsychological-assessment.pdf" target="_blank"
        rel="noopener">Read the report</a></figcaption>
    </figure>
  </div>

  
  

  <p class="k eyebrow-k" style="margin-top:56px">The diagnosis</p>
  <h3 style="margin-top:0">How the diagnosis was established</h3>
  <p class="dek" style="max-width:70ch">Intellectual disability has three diagnostic
  criteria. Dr. Ouaou examined Mark over two days at Holman, tested him, and read the
  records of his childhood. All three criteria were met.</p>
  <div class="dstrip" style="margin-top:22px"><button class="dt" data-d="d23" aria-pressed="false"><i>Full-Scale IQ</i><b>69.8</b><span>Flynn-adjusted, from 74. 95% confidence interval 67–75. The threshold for intellectual disability is approximately 70 ± 5.</span></button><button class="dt" data-d="d24" aria-pressed="false"><i>Executive function</i><b>1st percentile</b><span>Planning, mental flexibility, and reasoning. On several measures, at or below the 1st percentile.</span></button><button class="dt" data-d="d25" aria-pressed="false"><i>Adaptive functioning</i><b>All three domains</b><span>Deficits documented across the conceptual, social, and practical domains, the second of the three diagnostic criteria.</span></button><button class="dt" data-d="d26" aria-pressed="false"><i>Onset</i><b>Before age 18</b><span>The third criterion. Documented in school records from age eight forward.</span></button><button class="dt" data-d="d27" aria-pressed="false"><i>Effort testing</i><b>No malingering</b><span>Four independent measures. He was not exaggerating.</span></button></div>
  <div class="dpanel" id="dpanel"><p class="empty">Select a finding above to see the
  line from Dr. Ouaou's report that supports it.</p></div>
  <p class="small" style="margin-top:16px">Robert H. Ouaou, Ph.D., Forensic Neuropsychological Assessment of Mark Jenkins, May 3, 2023. Evaluation conducted at Holman Correctional Facility, November 8–9, 2022.</p>
  <script>window.__R = {"r1": {"label": "Maternal illness", "where": "Prenatal &middot; Biomedical", "tier": 2, "src": "Donna experienced kidney pain on admission to the hospital, and she was found to have a urinary tract infection due to E.coli at the time of the birth."}, "r2": {"label": "Domestic violence", "where": "Prenatal &middot; Social", "tier": 1, "src": "He stated that his father beat his mother and he (Mr. Jenkins) had to clean up after the violence."}, "r3": {"label": "Parental drug use", "where": "Prenatal &middot; Behavioral", "tier": 1, "src": "His mother, father (i.e., his stepfather), and other family members used and manufactured methamphetamines"}, "r4": {"label": "Prematurity", "where": "Perinatal &middot; Biomedical", "tier": 2, "src": "Mark Jenkins was born 09/13/1967 and noted to be a premature infant who weighed 5 pounds 1 ounce."}, "r5": {"label": "Neonatal disorders", "where": "Perinatal &middot; Biomedical", "tier": 2, "src": "Medical records indicate multiple complications during birth. His mother Donna's membranes ruptured prematurely, and doctors were forced to induce labor approximately two weeks early."}, "r6": {"label": "Parental rejection of caretaking", "where": "Perinatal &middot; Behavioral", "tier": 2, "src": "His mother initially put Mr. Jenkins up for adoption, and Mr. Jenkins was discharged from the hospital to an adoption agency."}, "r7": {"label": "Traumatic brain injury", "where": "Postnatal &middot; Biomedical", "tier": 2, "src": "head injuries to the frontal area of the brain during the developmental period, like the ones Mr. Jenkins suffered, are a critical etiology of significant impairments in behavior and emotion."}, "r8": {"label": "Malnutrition", "where": "Postnatal &middot; Biomedical", "tier": 2, "src": "He stated that the methamphetamine use took away his hunger, which was helpful because he had no money for food."}, "r9": {"label": "Impaired child–caregiver interaction", "where": "Postnatal &middot; Social", "tier": 2, "src": "Financially extorted by his own mother"}, "r10": {"label": "Lack of adequate stimulation", "where": "Postnatal &middot; Social", "tier": 1, "src": "His entire adolescence was marked by instability, neglect, physical violence, and substance abuse."}, "r11": {"label": "Family poverty", "where": "Postnatal &middot; Social", "tier": 2, "src": "At time of crime, living in messy, largely empty bungalow with no electricity and that others found for him"}, "r12": {"label": "Institutionalization", "where": "Postnatal &middot; Social", "tier": 2, "src": "placed in special education when in custody of juvenile justice system"}, "r13": {"label": "Child abuse and neglect", "where": "Postnatal &middot; Behavioral", "tier": 2, "src": "it was noted that his parents physically abused him, he suffered from neglect, he experienced possible auditory hallucinations, and he had a history of suicide attempts by head banging."}, "r14": {"label": "Domestic violence", "where": "Postnatal &middot; Behavioral", "tier": 2, "src": "His father and mother were physically violent toward Mr. Jenkins. His father hit him regularly and knocked him out on multiple occasions."}, "r15": {"label": "Social deprivation", "where": "Postnatal &middot; Behavioral", "tier": 2, "src": "Mr. Jenkins was periodically homeless during childhood and adolescence from the age of 13 to 19"}, "r16": {"label": "Impaired parenting", "where": "Postnatal &middot; Educational", "tier": 2, "src": "Steve Jenkins beat Mr. Jenkins daily with pieces of wood, belt buckles, and other objects around the house."}, "r17": {"label": "Delayed diagnosis", "where": "Postnatal &middot; Educational", "tier": 2, "src": "A 1981 psychological evaluation in San Bernardino County Juvenile Hall found that Mr. Jenkins “appears to be suffering from a definite learning disability.”"}, "r18": {"label": "Inadequate early intervention services", "where": "Postnatal &middot; Educational", "tier": 2, "src": "the evaluator expressed “grave concern” for Mr. Jenkins ’s emotional wellbeing and requested immediate psychotherapeutic intervention as well as long-term treatment."}, "r19": {"label": "Inadequate special education services", "where": "Postnatal &middot; Educational", "tier": 2, "src": "He needed but never received specialized attention for his intellectual deficits."}, "r20": {"label": "Inadequate family support", "where": "Postnatal &middot; Educational", "tier": 2, "src": "Mr. Jenkins also ran away from home to avoid being violated."}, "r21": {"label": "Severe methamphetamine use on a developing brain", "tier": 2, "src": "He reported that he abused methamphetamines every day from approximately age 15 until age 19.", "where": "Named by Dr. Ouaou &middot; outside the framework"}, "r22": {"label": "Posttraumatic stress", "tier": 2, "src": "These etiologies include posttraumatic stress, neglect, abuse, the effects of severe methamphetamine use on a developing brain and traumatic brain injury.", "where": "Named by Dr. Ouaou &middot; outside the framework"}, "d23": {"label": "Full-Scale IQ", "where": "Diagnostic finding", "tier": 2, "src": "Mr. Jenkins’ IQ of 69.8 (after adjusting for the Flynn Effect) is significantly impaired and within the range for intellectual disability."}, "d24": {"label": "Executive function", "where": "Diagnostic finding", "tier": 2, "src": "His severe executive functioning deficits mean that, in a room of 100 randomly selected people his age, Mr. Jenkins’ ability to plan, adapt, adjust, and have insight into his behavior is likely to be more impaired than every other person in the room."}, "d25": {"label": "Adaptive functioning", "where": "Diagnostic finding", "tier": 2, "src": "[V]oluminous records that contain correlative data related to Mr. Jenkins’ birth, childhood, and adolescence and demonstrate significant deficits in all three domains of adaptive functioning"}, "d26": {"label": "Onset", "where": "Diagnostic finding", "tier": 2, "src": "The onset of Mr. Jenkins’ intellectual and adaptive deficits occurred during the developmental period, specifically before the age of eighteen, and continue to this day."}, "d27": {"label": "Effort testing", "where": "Diagnostic finding", "tier": 2, "src": "On multiple tests of effort and motivation (TOMM, Rey 15, CVLT3 Forced Choice, embedded measures), Mr. Jenkins performed within normal limits, well above designated cutoffs."}};</script>


  <div class="splitmedia tall" style="margin-top:56px">
    <div>
      <p class="k eyebrow-k" style="margin-top:0">Atkins v. Virginia</p>
      <h3 style="margin-top:0">A path forward</h3>
      <p>In 2002, the U.S. Supreme Court ruled in <i>Atkins v. Virginia</i> that
      executing intellectually disabled individuals violates the Eighth Amendment's
      ban on cruel and unusual punishment.</p>
      <p>Since his diagnosis, Mark has been seeking an opportunity to prove in an
      Alabama court that he is intellectually disabled. To date, no court has given
      him the chance.</p>
      <p><strong>Governor Ivey is not bound by court rules.</strong> Even if the
      courts decline to hear Mark's evidence, she can listen to it and ensure that
      Alabama does not wrongfully execute an intellectually disabled man.</p>
      <div class="btnrow" style="margin-bottom:0"><a class="btn"
        href="help.html">Take action</a></div>
    </div>
    <figure class="fill">
      <a href="docs/atkins-v-virginia.pdf" target="_blank" rel="noopener"
        style="display:block">
        <img src="img/atkins-p1.jpg" alt="First page of the Supreme Court's decision in Atkins v. Virginia, 536 U.S. 304 (2002)"
          style="border:1px solid var(--rule);width:100%">
      </a>
      <figcaption><i>Atkins v. Virginia</i>, 536 U.S. 304 (2002).
      <a class="textlink" href="docs/atkins-v-virginia.pdf" target="_blank"
        rel="noopener">Read the decision</a>.</figcaption>
    </figure>
  </div>
  <button class="contread" data-to="#childhood"><i></i><span>Continue</span>
    <em>&darr;</em></button>
</article>

<article class="chapter tone" id="childhood">
  <p class="num">02. <span>Childhood abuse unheard</span></p>
  <h2>A childhood the jury was never told about</h2>
  <div class="splitmedia">
    <div>
      <p>Dr. Sara Boyd, a board-certified forensic psychologist and associate faculty
      at the University of Virginia, has said that Mark's childhood is one of the
      worst cases of abuse she has seen in her entire career.</p>
      <p>During Mark's trial, his attorneys did not tell the jury a single word about
      it. The Supreme Court has ruled that juries in death penalty cases must be
      allowed to consider exactly this kind of evidence. Mark's jury heard none.</p>
      <p style="margin-bottom:0">That childhood is told in full, with the
      contemporaneous records that document it:</p>
      <div class="btnrow"><a class="btn" href="mark.html#before">Read Mark's
      story</a></div>
    </div>
    <figure class="docstack">
      <button class="zoom" type="button" style="--r:-2.4deg;--x:0%;--y:0%;z-index:12">
        <img class="doc" src="img/doc-a.jpg" alt="Excerpt from a 1981 collateral report describing Mark constantly running away and his parents' indifference"></button>
      <button class="zoom" type="button" style="--r:1.8deg;--x:9%;--y:19%;z-index:13">
        <img class="doc" src="img/doc-c.jpg" alt="Excerpt from an evidentiary report recording that Mark's parents were going to beat him"></button>
      <button class="zoom" type="button" style="--r:-1.2deg;--x:2%;--y:40%;z-index:14">
        <img class="doc" src="img/doc-e.jpg" alt="Excerpt from a report recording that Mark came from a dysfunctional home and wanted to be loved by his family"></button>
      <button class="zoom" type="button" style="--r:2.6deg;--x:14%;--y:62%;z-index:15">
        <img class="doc" src="img/doc-b.jpg" alt="Handwritten note in a record reading that the family blatantly rejected Mark"></button>
      <figcaption>Contemporaneous records, 1981&ndash;1983. Select any page to read
      it.</figcaption>
    </figure>
  </div>
  <button class="contread" data-to="#jury"><i></i><span>Continue</span>
    <em>&darr;</em></button>
</article>

<article class="chapter" id="jury">
  <p class="num">03. <span>Non-unanimous</span></p>
  <h2>Mark Jenkins was sentenced to death even though two jurors voted for a life
  sentence.</h2>

  <div class="intro sans">
    <p>Two jurors thought that Mark should get a life sentence instead of the death
    penalty. Despite this non-unanimous verdict, Mark was sentenced to death.</p>
  </div>

  <div class="splitmedia">
    <div>
      <p>This country has a long and proud tradition of requiring a jury to be
      unanimous when delivering a verdict. When it comes to the death penalty,
      without consensus from all twelve jurors, the jury cannot channel the voice of
      the community, and there remains doubt as to whether a person is the
      &ldquo;worst of the worst.&rdquo;</p>
      <p>Alabama is one of only two states in the country that allows a death
      sentence without a unanimous jury. Former Alabama governors, both a Republican
      and a Democrat, have recognized that this practice is flawed and that people
      sentenced to death without a unanimous jury should be re-sentenced to life in
      prison without parole.</p>
      <p style="margin-bottom:0">In nearly all states, Mark would have been sentenced
      to life. That is not what happened in Alabama.</p>
    </div>
    <figure class="vidfig">
      <video controls playsinline preload="none" poster="img/video/spiker-poster.jpg">
        <source src="img/video/spiker.mp4" type="video/mp4">
        <track kind="captions" src="img/video/spiker.vtt" srclang="en"
          label="English" default>
        <p>Your browser cannot play this recording. The transcript is below.</p>
      </video>
      <figcaption>Richard Spiker of St. Clair County, one of the jurors who voted for
      a life sentence at Mark's sentencing trial, still feels regret for the outcome
      more than thirty-five years later.</figcaption>
      <details class="vtx">
        <summary>Read the transcript</summary>
        <div class="tx">
          <p><b>Richard Spiker.</b> Governor Ivey, I've supported you both terms, and
          I was a juror on the Mark Jenkins capital murder case, and I'm asking you to
          give him life in prison.</p>
          <p class="sd">On screen: In 1991, Mark Jenkins stood trial in St. Clair
          County for the murder of Tammy Hogeland. Only ten of the twelve jurors voted
          for the death penalty. Two voted for life. Even though the jury was not
          unanimous, Mark was sentenced to death. Richard Spiker was one of the jurors
          who voted for life without the possibility of parole.</p>
          <p><b>Spiker.</b> I mean, it brings up a lot of hurt, because I wasn't proud
          when I walked out of that courthouse.</p>
          <p><b>Interviewer.</b> Why not?</p>
          <p class="sd">A long pause.</p>
          <p><b>Spiker.</b> I don't think he got the right verdict.</p>
          <p class="sd">He stops, and gathers himself.</p>
          <p><b>Spiker.</b> Sorry.</p>
        </div>
      </details>
    </figure>
  </div>
  <button class="contread" data-to="#transformation"><i></i><span>Continue</span>
    <em>&darr;</em></button>
</article>

<article class="chapter" id="transformation">
  <p class="num">04. <span>Transformation</span></p>
  <h2>The man Alabama would execute is not the man it sentenced.</h2>

  <div class="intro sans">
    <p>Mark was twenty-one at the time of the offense. He is fifty-eight. Thirty-five
    years of an unbroken institutional record sit between those two men, and the
    people who kept that record are asking the Governor to spare him.</p>
  </div>

  <div class="splitmedia tall">
    <div>
      <p>In September 2026, Sara E. Boyd, Ph.D., a board-certified forensic
      psychologist, completed a psychological evaluation of Mark. She assessed his
      history, his current psychological status, and his risk of future violence.</p>
      <p>Dr. Boyd found that Mark is at very low risk of violence, in prison or
      anywhere else. That finding matched a separate assessment by Dr. Jonathan
      Sorensen, a prison violence risk expert, and it matched what the officers at
      Holman had been saying for years.</p>
      <p>She also found something she had not seen before in a capital case. In
      twenty years of this work, she could not recall another person she had
      evaluated with even two correctional officers willing to write on his behalf.
      More than sixty have written for Mark.</p>
      <p style="margin-bottom:0">The remorse, she wrote, is of a degree that is
      highly unusual in her experience.</p>
    </div>
    <figure class="reportfig">
      <a href="docs/boyd-assessment.pdf" target="_blank" rel="noopener">
        <img src="img/boyd-p1.jpg" alt="First page of the psychological evaluation of Mark Jenkins by Sara E. Boyd, Ph.D.">
      </a>
      <figcaption><a class="textlink"
        href="docs/boyd-assessment.pdf" target="_blank"
        rel="noopener">Read the report</a></figcaption>
    </figure>
  </div>

  <section class="cwband" style="margin-top:52px"><div class="wrap"><div class="inner">
    <p>&ldquo;I cannot recall another individual whom I&rsquo;ve evaluated for a
    capital or other serious felony case who had two, let alone more than 60,
    correctional officers willing to write letters on their behalf.&rdquo;</p>
  </div></div></section>

  <p class="small" style="margin-top:36px">Sara E. Boyd, Ph.D., ABPP, Psychological
  Evaluation of Mark Jenkins, September 4, 2026.</p>
</article>


<article class="chapter actblock">
  <h2>Only one person can act now.</h2>
  <p>Under the Alabama Constitution, the Governor has the authority, and the right,
  to commute a death sentence to life in prison without the possibility of parole.
  Some critical considerations, including the support of more than sixty Alabama
  correctional officers, could not be considered by any court.</p>
  <div class="btnrow">
    <a class="btn" href="officers.html">Read the officers' letters</a>
    <a class="btn ghost" href="help.html">Write to the Governor</a>
    <a class="btn ghost" href="postcards.html">View the postcard project</a>
  </div>
</article>

</div>

<nav class="chapnav" id="rail"><div class="wrap">
  <button class="railbtn" id="railtop">&uarr; Top</button>
  <div class="links">
    <a href="#disability">01. Disability</a>
    <a href="#childhood">02. His childhood</a>
    <a href="#jury">03. The jury</a>
    <a href="#transformation">04. Transformation</a>
  </div>
  <button class="railbtn" id="railnext">Next <span>&darr;</span></button>
</div></nav>
"""


# ---------------------------------------------------------------- FAQ
FAQ = [
 ("Who is Mark Jenkins?",
  "<p>Mark Jenkins is a 58-year-old intellectually disabled man who has been on "
  "Alabama's death row for over 35 years. He was born into a family in Southern "
  "California that subjected him to horrific sexual, physical, and emotional abuse "
  "throughout his childhood. His parents abandoned him when he was only thirteen "
  "years old, and he lived on the streets and in group homes until he finally moved "
  "to Alabama when he was 20 for what he was hoping would be a fresh start. When "
  "Mark was 21, he killed Tammy Hogeland, and for that crime he was convicted of "
  "capital murder and sentenced to death.</p>"
  "<p>Since his trial, Mark has been at Holman Correctional Facility in Atmore, "
  "Alabama, where he has both grappled with his profound remorse for his crime and "
  "has transformed himself. He has grown in his faith into the Christian man he is "
  "today, one whom correctional officers recognize deserves mercy. And, through the "
  "structured life of prison, he has learned to contend with his intellectual "
  "disability and to still serve as a support and helper to the officers and other "
  "prisoners around him.</p>"),
 ("Why is Mark on death row?",
  "<p>In 1991, Mark was convicted of capital murder and sentenced to death in "
  "St. Clair County for the murder of Tammy Hogeland. The crime occurred early in "
  "the morning of April 18, 1989, when Mark was 21 years old and Tammy was 22. Mark "
  "was drinking heavily that night and drove to the diner where Tammy worked. Tammy "
  "left the diner with Mark. At some point, the two got into an argument. During "
  "that argument, Mark strangled Tammy to death.</p>"
  "<p>Mark was horrified by his actions from the moment he became conscious of them "
  "and feels tremendous remorse to this day. Those who know him, from family members "
  "to correctional officers, have seen how Mark's remorse for the terrible harm he "
  "caused has stayed with him over the decades.</p>"),
 ("What is going on in Mark's case now?",
  "<p>In 2002, the U.S. Supreme Court barred the execution of people with "
  "intellectual disability. But that decision came long after Mark's trial and death "
  "sentence, and Mark's legal team has never had the opportunity to present evidence "
  "of his intellectual disability in court. Although his traditional appeals have "
  "ended, his lawyers continue to ask for his &ldquo;day in court&rdquo; to prove "
  "that his execution would be illegal.</p>"
  "<p>Other than a court ruling that he is intellectually disabled, Mark's only "
  "chance for a sentence of life in prison, as opposed to execution, is for the "
  "Governor to grant him clemency.</p>"),
 ("What does &ldquo;clemency&rdquo; mean, and who decides?",
  "<p>Under the Alabama Constitution, the Governor has the authority, and the "
  "right, to extend mercy and commute a prisoner's death sentence to life in "
  "prison without the possibility of parole. This fail-safe is separate from judicial "
  "proceedings and exists precisely because the judicial process is not infallible. "
  "Some critical considerations, including the support of over 60 Alabama "
  "correctional officers, could not be considered by courts.</p>"
  "<p>Mark will never be released from prison. Mark and his legal team are not asking "
  "for any possibility of future release from prison. They are asking that the "
  "Governor allow Mark the opportunity to die a natural death within the prison walls "
  "instead of being executed.</p>"),
 ("Why does Mark deserve clemency?",
  "<p>Mark took an innocent life, but, as his many supporters recognize, the "
  "appropriate punishment is life in prison without any chance of release, not "
  "execution.</p>"
  "<p>Mark had a horrific, abuse-filled childhood that set him on a terrible path. "
  "Even so, he was a loving child and young adult; he never caused harm until he took "
  "Tammy Hogeland's life. That terrible crime was an aberration in an otherwise "
  "peaceful life.</p>"
  "<p>Moreover, Mark's court proceedings have not been fair. Because he had "
  "inexperienced capital lawyers, his jurors never heard why they should spare Mark's "
  "life. Still, two jurors thought he should get a sentence of life in prison. Mark "
  "was sentenced to death despite the fact that his jury was not unanimous. Moreover, "
  "even though the U.S. Supreme Court has barred the execution of intellectually "
  "disabled people, and even though an expert has diagnosed Mark as intellectually "
  "disabled, Mark has not had the opportunity to present evidence in court that his "
  "disability makes him ineligible for execution.</p>"
  "<p>Most of all, Mark has transformed in prison. Mark has spent the past 35 years "
  "trying to spread positivity and warmth and trying to repent for the harm he "
  "caused. At his request, Mark was baptized in the county jail and accepted Jesus "
  "into his life. In prison, he has been able to grow in his faith and into the "
  "Christian man that he is today. He now spreads Jesus's love in the ways he can, "
  "including by being a good influence on those around him, trying to defuse tense "
  "situations, lifting people up when they are down, and more. Mark is such an "
  "exemplary prisoner that over 60 correctional officers, as well as the former "
  "prison chaplain who knew Mark over the course of decades, support clemency. They "
  "know Mark as peaceful, trustworthy, and good-natured. They see that he is a "
  "different person from the one who entered prison more than three decades ago. Even "
  "knowing that Mark has killed someone, they believe that he would pose no threat if "
  "allowed to die of natural causes in prison. They believe that he deserves to be "
  "spared the death penalty.</p>"),
 ("Who supports clemency for Mark?",
  "<p>Numerous Alabamians have voiced their strong support for clemency for Mark.</p>"
  "<p>Mark has extraordinary support from law enforcement officers who have served as "
  "correctional officers at Holman Correctional Facility during the 35 years Mark has "
  "been incarcerated there. More than 60 correctional officers have written "
  "personalized, individual letters to the Governor explaining why they believe he is "
  "entitled to mercy and should not be executed. "
  "<a class=\"textlink\" href=\"officers.html\">Read more about this unprecedented "
  "support</a>.</p>"
  "<p>Many others support Mark as well, including Richard Spiker, who sat on Mark's "
  "jury in 1991 and voted for a life sentence over the death penalty. Even though "
  "Mr. Spiker and another juror voted for life, Mark was still sentenced to death "
  "because Alabama is one of only two states that does not require jury unanimity for "
  "a death sentence. <a class=\"textlink\" href=\"why-clemency.html#jury\">Listen to "
  "Mr. Spiker's words</a>.</p>"
  "<p>Other supporters include faith leaders across the state, state legislators and "
  "other local leaders, and state advocates for people with disabilities.</p>"),
 ("How can I help?",
  "<p>There are many ways you can help Mark. It is important that as many people as "
  "possible are aware of Mark's case and that he is at risk of being executed. "
  "<a class=\"textlink\" href=\"help.html\">Here are some concrete things you can "
  "do</a>.</p>"),
]


def faq_page():
    items = ''.join(
        '<details%s><summary>%s</summary><div class="a">%s</div></details>'
        % (' open' if i == 0 else '', q, a) for i, (q, a) in enumerate(FAQ))
    return """
<section class="hero" style="padding:52px 0 20px"><div class="wrap"
  style="grid-template-columns:1fr">
  <div style="max-width:840px">
    <p class="eyebrow">Questions</p>
    <h1>Frequently asked questions</h1>
    <p class="lede" style="max-width:60ch;margin-bottom:0">The case, the crime, what
    clemency means, and what happens next, answered plainly.</p>
  </div>
</div></section>

<section style="padding-top:34px"><div class="wrap" style="max-width:900px">
  <div class="faq">%s</div>
  <div class="btnrow" style="margin-top:40px">
    <a class="btn" href="mark.html">Explore Mark's story</a>
    <a class="btn ghost" href="why-clemency.html">Why clemency</a>
    <a class="btn ghost" href="help.html">Take action</a>
  </div>
</div></section>
""" % items


HELP = """
<section class="hero" style="padding:52px 0 20px"><div class="wrap"
  style="grid-template-columns:1fr">
  <div style="max-width:840px">
    <p class="eyebrow">Take action</p>
    <h1>You can help Mark.</h1>
    <p class="lede" style="max-width:60ch;margin-bottom:0">It matters that as many
    people as possible know about Mark's case and that he is at risk of being
    executed. Here are concrete things you can do.</p>
  </div>
</div></section>

<section class="tight"><div class="wrap">
  <div class="cards two">
    <article class="card">
      <span class="n">One</span>
      <h3>Share his story</h3>
      <p>Share this website on social media, and with your friends, family and
      networks. Most people have never heard that sixty correctional officers
      asked a governor to spare a man on death row.</p>
    </article>
    <article class="card">
      <span class="n">Two</span>
      <h3>Write to Governor Ivey</h3>
      <p>Send a message letting her know that you support clemency for Mark and
      why it matters to you.</p>
      <a class="textlink" href="mailto:teammarkjenkins@gmail.com">Ask us how</a>
    </article>
    <article class="card">
      <span class="n">Three</span>
      <h3>Get email updates</h3>
      <p>Sign up for updates about Mark's case, including events and actions that
      will spotlight it in the months ahead.</p>
      <a class="textlink" href="mailto:teammarkjenkins@gmail.com">Sign up</a>
    </article>
    <article class="card">
      <span class="n">Four</span>
      <h3>Bring it to your congregation</h3>
      <p>Let us know if your church or house of worship is interested in hosting
      an event to spread awareness about Mark's case, or in taking part in
      the postcard project.</p>
      <a class="textlink" href="mailto:teammarkjenkins@gmail.com">Get in touch</a>
    </article>
  </div>
</div></section>

<section class="dark"><div class="wrap">
  <div class="media">
    <div>
      <p class="eyebrow">The postcard project</p>
      <h2>One card, one question, one governor.</h2>
      <p>Across Alabama, people of faith are answering a single question in their
      own handwriting and mailing it to Montgomery: <i>if you were to speak to the
      Governor, why would you say Mark Jenkins deserves clemency?</i></p>
      <p>Every card that comes back is photographed and added to a growing wall on
      this site. If your congregation would like a stack, tell us how many.</p>
      <div class="btnrow">
        <a class="btn" href="postcards.html">See the cards</a>
        <a class="btn ghost" href="mailto:teammarkjenkins@gmail.com">Request cards</a>
      </div>
    </div>
    <div class="placeholder" style="border-color:rgba(255,255,255,.25);
      background:rgba(255,255,255,.04)">
      <b style="color:#EFEBE2">Cards are arriving now</b>
      <span style="color:#8A857A">The wall fills as they come back in the mail.</span>
    </div>
  </div>
</div></section>

<section><div class="wrap narrow" style="text-align:center">
  <h2>Questions, comments, or ideas?</h2>
  <p class="lede">Email <a class="textlink"
  href="mailto:teammarkjenkins@gmail.com">teammarkjenkins@gmail.com</a>.</p>
</div></section>
"""
