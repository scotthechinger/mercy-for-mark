/* The email sign-up.
 *
 * The form posts straight to a Google Form, whose responses land in a Sheet
 * the campaign owns. There is no server here to receive an address, and no
 * third party holding the list.
 *
 * The form works with JavaScript switched off: it is a real form with a real
 * action, targeting a hidden iframe, so the page never navigates away. What
 * this file adds is the confirmation message, the honeypot check, and a
 * fallback if the post does not come back.
 *
 * Google's form endpoint is cross-origin, so we cannot read what it returns.
 * The iframe's load event is the only signal that anything happened, which is
 * why a timeout reveals the mailto link rather than leaving someone looking
 * at a button that appears to have done nothing.
 */
(function () {
  var MAILTO = 'mailto:teammarkjenkins@gmail.com' +
    '?subject=Sign%20me%20up%20for%20updates%20about%20Mark' +
    '&body=Please%20add%20me%20to%20the%20list%20for%20updates%20about%20Mark%20Jenkins%E2%80%99s%20case.';

  function init(form) {
    var input = form.querySelector('.sub-in');
    var hp = form.querySelector('.sub-hp');
    var msg = form.querySelector('.sub-msg');
    var btn = form.querySelector('.sub-go');
    var sink = document.getElementById(form.getAttribute('target'));
    var waiting = false, done = false, timer = null;

    function say(text, kind) {
      msg.textContent = text;
      msg.className = 'sub-msg' + (kind ? ' is-' + kind : '');
    }

    function succeed() {
      if (done) return;
      done = true;
      clearTimeout(timer);
      form.classList.add('is-done');
      say('Thank you — you’re on the list.', 'ok');
    }

    function fail() {
      if (done) return;
      done = true;
      waiting = false;
      btn.disabled = false;
      msg.innerHTML = 'That didn’t go through. You can ' +
        '<a class="textlink" href="' + MAILTO + '">email us instead</a>.';
      msg.className = 'sub-msg is-err';
    }

    // The iframe fires load once when it is first inserted, before anything
    // has been submitted. Only a load that happens while we are waiting on a
    // submission means the form was received.
    sink.addEventListener('load', function () {
      if (waiting) succeed();
    });

    form.addEventListener('submit', function (e) {
      // A bot filled the field no human can see. Say nothing, send nothing.
      if (hp && hp.value) { e.preventDefault(); succeed(); return; }

      if (!input.value || input.validity.typeMismatch || !input.validity.valid) {
        e.preventDefault();
        say('Please enter an email address we can reach you at.', 'err');
        input.focus();
        return;
      }

      waiting = true;
      btn.disabled = true;
      say('Sending…');
      timer = setTimeout(fail, 8000);
      // The form submits normally from here, into the hidden iframe.
    });
  }

  var forms = document.querySelectorAll('form.sub');
  for (var i = 0; i < forms.length; i++) init(forms[i]);
})();
