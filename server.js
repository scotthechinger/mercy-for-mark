// Mercy for Mark — the public server.
//
// The site is plain static HTML. This wrapper serves it, and nothing more.
//
// It replaced a version that put every request behind a password while the
// clinic reviewed the site, and that stamped a noindex header on every
// response. Both are gone. If the site ever needs to go back behind the
// password, the previous version of this file is in the repository's history.

const express = require('express');
const path = require('path');

const PORT = process.env.PORT || 10000;

const app = express();
app.disable('x-powered-by');

// _hold/ holds the postcard submission wall we built in September and pulled
// down. It is kept for parts, not served.
app.use(['/_hold'], (req, res) =>
  res.status(404).type('text/plain').send('Not found.'));

app.use(express.static(path.join(__dirname), { extensions: ['html'] }));

app.use((req, res) => res.status(404).sendFile(path.join(__dirname, 'index.html')));

app.listen(PORT, () => console.log('Mercy for Mark listening on ' + PORT));
