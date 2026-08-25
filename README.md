# Mercy for Mark

The clemency site for Mark Allen Jenkins (ADOC #Z-527), built for the UC Berkeley
Law Death Penalty Clinic.

**This repository is private and the deployed site is behind a login. It is not
for public distribution.**

## What is here

The repository root is the deployable site: plain HTML, one stylesheet, no build
step and no dependencies. Point a static host at the root and it serves.

    index.html  mark.html  officers.html  why-clemency.html
    faq.html    help.html  postcards.html
    style.css
    img/    103 images, including the redacted letter scans
    docs/   the neuropsychological assessment and Atkins v. Virginia
    build/  the generator that produces the HTML

## Names

No officer's name appears anywhere on this site. Names are removed from the
**data** before the pages are built, so the site's own search cannot find one,
and the scans shown are the redacted PDFs rather than the originals. Record ids
and image filenames are opaque (`L07`, `l-L07.jpg`).

`build/officers.py` refuses to build if any writer's name survives, in their own
letter or in anybody else's. To restore a name once that person has consented,
set `"consent_public": true` on their record in `final.json` and rebuild.

Seventeen photographs of officers are still displayed. Consent for photographs
is a separate question from consent for names and was outstanding as of
25 August 2026.

## Rebuilding

`build/` needs `final.json` (the letter archive, which holds real names and is
deliberately **not** in this repository) and the risk-factor data. With those in
place:

    python3 build/build.py

Every page carries `noindex, nofollow`. Remove that when the site should be
found.
