// Mercy for Mark — the review server.
//
// The site itself is plain static HTML. This wrapper exists for one reason: to
// put every request behind a password while the clinic reviews it, including
// the images and the PDFs. A static host cannot do that, and a client-side
// scheme such as PageCrypt cannot either, because the letter scans and the
// officers' photographs stay fetchable by URL whatever the HTML does.
//
// Credentials come from the environment and are never stored in this
// repository. Set SITE_USER and SITE_PASS in the Render dashboard.

const express = require('express');
const crypto = require('crypto');
const path = require('path');

const USER = process.env.SITE_USER;
const PASS = process.env.SITE_PASS;
const PORT = process.env.PORT || 10000;

const app = express();
app.disable('x-powered-by');

// A constant-time comparison, so the response time cannot be used to guess.
function same(a, b) {
  const x = Buffer.from(String(a));
  const y = Buffer.from(String(b));
  if (x.length !== y.length) return false;
  return crypto.timingSafeEqual(x, y);
}

app.use((req, res, next) => {
  // Fail closed. A missing password must never mean an open site.
  if (!USER || !PASS) {
    res.status(503).type('text/plain');
    return res.send('Not configured: SITE_USER and SITE_PASS are not set.');
  }

  const header = req.headers.authorization || '';
  const [scheme, encoded] = header.split(' ');
  if (scheme === 'Basic' && encoded) {
    const raw = Buffer.from(encoded, 'base64').toString('utf8');
    const i = raw.indexOf(':');
    const u = raw.slice(0, i);
    const p = raw.slice(i + 1);
    if (same(u, USER) && same(p, PASS)) {
      res.set('X-Robots-Tag', 'noindex, nofollow, noarchive');
      return next();
    }
  }

  res.set('WWW-Authenticate', 'Basic realm="Mercy for Mark", charset="UTF-8"');
  res.set('X-Robots-Tag', 'noindex, nofollow, noarchive');
  return res.status(401).type('text/plain').send('Authentication required.');
});

// The postcard project is held back until there are enough cards to show it.
// Everything for it still lives in _hold/. Delete this block to bring it back.
app.use(['/_hold', '/postcards', '/postcards.html'], (req, res) =>
  res.status(404).type('text/plain').send('Not found.'));

app.use(express.static(path.join(__dirname), {
  extensions: ['html'],
  setHeaders: (res) => res.set('X-Robots-Tag', 'noindex, nofollow, noarchive'),
}));

app.use((req, res) => res.status(404).sendFile(path.join(__dirname, 'index.html')));

app.listen(PORT, () => console.log('Mercy for Mark listening on ' + PORT));
