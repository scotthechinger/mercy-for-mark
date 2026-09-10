# -*- coding: utf-8 -*-
"""The Officers — the letter archive, with no names anywhere.

Names are removed from the DATA, not hidden in the view: the transcript, the
quotes and the search index are all built from redacted text, so a name cannot
be found by searching the page for it. When consent comes back, flip a flag per
writer in final.json and the name reappears everywhere at once.
"""
import json, re, html, io, base64, os
from PIL import Image

E = lambda s: html.escape(s, quote=True)
HERE = os.path.dirname(os.path.abspath(__file__))
BLOCK = '█' * 6
_TITLES = {'jr.', 'sr.', 'ii', 'iii', 'pastor', 'rev.', 'reverend', 'chaplain',
           'officer', 'sgt.', 'sergeant', 'lt.', 'lieutenant', 'capt.', 'captain',
           'warden', 'mr.', 'mrs.', 'ms.', 'dr.'}

DATA = json.load(open('/home/claude/work/final.json'))['letters']
IMGS = json.load(open('/home/claude/work/images.json'))

THEME_LABELS = {
 'no-threat-in-population': 'Would pose no threat',
 'clean-disciplinary-record': 'Clean disciplinary record',
 'trusted-hall-runner': 'Trusted as a hall runner',
 'first-letter-ever': 'Never wrote such a letter before',
 'contrast-other-inmates': 'Unlike other men on the row',
 'service-to-staff': 'Helped the officers',
 'respectful': 'Respectful',
 'would-not-for-anyone': 'Would not do this for anyone else',
 'acknowledges-crime-severity': 'Acknowledges the crime',
 'writer-military-service': 'Writer served in the military',
 'recreation-interests': 'Sports, jokes, everyday life',
 'long-tenure-credibility': 'Decades of service',
 'remorse-accountability': 'Remorse and accountability',
 'made-prison-safer': 'Made the prison safer',
 'faith-practice': 'Faith',
 'warmth-humor': 'Warmth and humour',
 'writer-execution-team': 'Writer served on an execution team',
 'intellectual-disability': 'Noticed his disability',
 'redemption-change': 'Redemption and change',
 'cared-for-officers': 'Cared for the officers',
 'animals': 'Animals',
}


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


# Surnames that are also Alabama places. "Brewton, Alabama" in an address block
# is not a leak of the officer named Brewton, and blacking out the capital in
# every letter would be absurd.
_PLACES = {'montgomery', 'brewton', 'atmore', 'repton', 'escambia', 'lottie',
           'bessemer', 'clanton', 'jackson', 'jasper', 'florence', 'marion'}


def name_parts(name):
    """The tokens of a name, stripped of punctuation and of titles."""
    out = []
    for p in re.split(r'[\s,]+', name or ''):
        p = p.strip('.,;:()"\'')
        if len(p) > 1 and p.lower().rstrip('.') not in _TITLES:
            out.append(p)
    return out


# Contact details are never published, consent or not. They also hide names:
# "csummers0829@gmail.com" carries a surname inside a single token, so no
# \b-delimited name pattern can ever reach it. Strip these first.
CONTACT = re.compile(
    r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'          # e-mail
    r'|\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'                  # telephone
    , re.I)


def redactor(name):
    """Patterns that must never survive into the page for a non-consenting writer."""
    # Titles are not names. "Pastor", "Sergeant", "Warden" describe the job the
    # letter is written from, which is the substance, and blacking them out would
    # cost the archive its point without protecting anyone.
    parts = name_parts(name)
    pats = [re.escape(' '.join(parts))] + [re.escape(p) for p in parts]
    pats = [p for p in pats if p]
    pats.sort(key=len, reverse=True)
    return re.compile(r'\b(?:%s)\b\.?' % '|'.join(pats), re.I)


def cross_redactor(letters):
    """Every writer's name, removed from every letter, not only from their own.

    A colleague who names another officer in passing would otherwise put that
    officer on the internet. Full names and pairs go first, then surnames on
    their own, and only those long enough not to be a common word.
    """
    pats = []
    for l in letters:
        if l.get('consent_public'):
            continue
        parts = name_parts(l.get('writer_name'))
        if not parts:
            continue
        if len(parts) > 1:
            pats.append(re.escape(' '.join(parts)))
            for i in range(len(parts) - 1):
                pats.append(re.escape(parts[i] + ' ' + parts[i + 1]))
            for i in range(len(parts) - 2):
                pats.append(re.escape(' '.join(parts[i:i + 3])))
        last = parts[-1]
        if len(last) >= 5 and last.lower() not in _PLACES:
            pats.append(re.escape(last))
    pats = sorted(set(pats), key=len, reverse=True)
    return re.compile(r'\b(?:%s)\b\.?' % '|'.join(pats), re.I)


def build():
    global CROSS
    CROSS = cross_redactor(DATA)
    os.makedirs(f'{HERE}/img', exist_ok=True)
    rows, themecount = [], {}
    for n, l in enumerate(DATA, 1):
        oid = 'L%02d' % n
        consent = bool(l.get('consent_public'))          # all False until they say yes
        rx = redactor(l['writer_name'])
        red = ((lambda t: CROSS.sub(BLOCK, CONTACT.sub(BLOCK, t))) if consent
               else (lambda t: CROSS.sub(BLOCK, rx.sub(BLOCK, CONTACT.sub(BLOCK, t)))))

        key = l['writer_name'].split()[-1]
        im = IMGS.get(key) or IMGS.get(l['id'])
        kind, fname = 'letter', None
        if im:
            kind = im['kind']
            fname = f"{'p' if kind=='photo' else 'l'}-{oid}.jpg"
            p = f'{HERE}/img/{fname}'
            if not os.path.exists(p):
                b = base64.b64decode(im['src'].split(',', 1)[1])
                pic = Image.open(io.BytesIO(b)).convert('RGB')
                w = 520
                if pic.size[0] > w:
                    pic = pic.resize((w, round(pic.size[1] * w / pic.size[0])),
                                     Image.LANCZOS)
                pic.save(p, quality=82, optimize=True)

        quotes = [red(q['text']) for q in l['quotes'] if q.get('verified')]
        themes = [t for t in (l.get('themes') or []) if t in THEME_LABELS]
        for t in themes:
            themecount[t] = themecount.get(t, 0) + 1

        rows.append({
            'id': oid,
            'name': l['writer_name'] if consent else None,
            'role': l.get('rank_detail') or l.get('role') or 'Correctional officer',
            'yrs': l.get('years_service'),
            'dr': bool(l.get('worked_death_row')),
            'exec': bool(l.get('execution_team')),
            'mil': bool(l.get('military')),
            'first': bool(l.get('first_such_letter')),
            'date': l.get('letter_date'),
            'img': fname, 'kind': kind,
            'themes': themes,
            'desc': (l.get('descriptors') or [])[:8],
            'q': quotes,
            'text': red(l['text']),
        })

    # ---- the invariant: a writer's own name must not survive in their own record.
    # A different writer's letter that happens to contain the word "Montgomery"
    # (the capital, in every address block) is not a leak of the officer named
    # Montgomery, so the check is per-record rather than across the whole payload.
    leaks = []
    for l, r in zip(DATA, rows):
        if l.get('consent_public'):
            continue
        blob = json.dumps(r, ensure_ascii=False)
        for part in name_parts(l['writer_name']):
            if len(part) < 3:
                continue
            if re.search(r'\b%s\b' % re.escape(part), blob, re.I):
                leaks.append((r['id'], l['writer_name'], part))

    # and no writer's surname may survive anywhere in the archive, whoever wrote it
    whole = json.dumps(rows, ensure_ascii=False)
    for l in DATA:
        if l.get('consent_public'):
            continue
        parts = name_parts(l['writer_name'])
        if not parts:
            continue
        last = parts[-1]
        if len(last) >= 5 and last.lower() not in _PLACES:
            if re.search(r'\b%s\b' % re.escape(last), whole, re.I):
                leaks.append(('CROSS', l['writer_name'], last))

    # ---- no e-mail address or telephone number may survive anywhere
    for m in re.finditer(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
                         r'|\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', whole):
        leaks.append(('CONTACT', '-', m.group(0)))

    # ---- and the filenames must not carry it either
    for l, r in zip(DATA, rows):
        if r['img'] and any(p.lower() in r['img'].lower()
                            for p in re.split(r'\s+', l['writer_name'])
                            if len(p) > 2 and p.lower() not in _TITLES):
            leaks.append((r['id'], l['writer_name'], 'FILENAME ' + r['img']))

    payload = json.dumps(rows, ensure_ascii=False)
    return rows, themecount, payload, leaks
