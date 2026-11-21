"""A tiny cat in the corner of the page. Click it twice for a surprise."""
import base64
import json
import mimetypes
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

STATIC = Path(__file__).parent / "static"
MAX_BYTES = 2_000_000  # skip files bigger than 2 MB


def _data_uri(names):
    """Return the first file found in ./static as a data: URI, or None."""
    for name in names:
        f = STATIC / name
        if f.is_file() and f.stat().st_size <= MAX_BYTES:
            mime = mimetypes.guess_type(f.name)[0] or "application/octet-stream"
            return "data:%s;base64,%s" % (mime, base64.b64encode(f.read_bytes()).decode())
    return None


JS = r"""
(function () {
  if (document.getElementById('cat-egg-root')) return;

  // Filled in by Python: static/oiia.mp3 if it exists, otherwise null (built-in synthesized beat).
  var CUSTOM_AUDIO_URL = __AUDIO__;

  // Filled in by Python: static/cat.png (or .jpg/.gif/.webp) if it exists, otherwise null (drawn cat).
  var CAT_IMAGE_URL = __IMAGE__;

  var css = `
  #cat-egg-root { position: fixed; right: 12px; bottom: 12px; z-index: 999999; }
  #cat-tiny { width: 40px; height: 40px; padding: 0; border: 0; background: none; cursor: pointer;
              transition: transform .15s ease; }
  #cat-tiny:hover { transform: scale(1.15) rotate(-6deg); }
  #cat-tiny:focus-visible, #cat-big:focus-visible { outline: 3px solid #3b82f6; outline-offset: 3px; border-radius: 50%; }
  #cat-big { display: none; position: fixed; right: 24px; bottom: 24px; width: 150px; height: 150px;
             padding: 0; border: 0; background: none; cursor: pointer; z-index: 999999; }
  #cat-big svg, #cat-big img, .cat-float svg, .cat-float img { animation: cat-spin .55s linear infinite; }
  #cat-label { display: none; position: fixed; right: 36px; bottom: 182px; z-index: 999999;
               font: 700 18px/1 system-ui, sans-serif; letter-spacing: .08em; color: #c2410c;
               background: #fff7ed; border: 2px solid #fdba74; border-radius: 999px; padding: 6px 14px; }
  .cat-float { display: none; position: fixed; left: 0; width: 64px; height: 64px; pointer-events: none;
               z-index: 999998; animation: cat-drift linear infinite; }
  body.cat-on #cat-big, body.cat-on #cat-label, body.cat-on .cat-float { display: block; }
  @keyframes cat-spin { to { transform: rotate(360deg); } }
  @keyframes cat-drift { from { transform: translateX(-12vw); } to { transform: translateX(112vw); } }
  @media (prefers-reduced-motion: reduce) {
    #cat-big svg, #cat-big img, .cat-float svg, .cat-float img { animation-duration: 2s; }
    .cat-float { display: none !important; }
  }`;
  var style = document.createElement('style');
  style.textContent = css;
  document.head.appendChild(style);

  var CAT = `<svg viewBox="0 0 100 100" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
    <polygon points="16,42 20,6 46,26" fill="#e8a24a"/><polygon points="84,42 80,6 54,26" fill="#e8a24a"/>
    <polygon points="22,34 24,16 38,27" fill="#f4a9b8"/><polygon points="78,34 76,16 62,27" fill="#f4a9b8"/>
    <ellipse cx="50" cy="60" rx="38" ry="33" fill="#f2b25c"/>
    <ellipse cx="36" cy="55" rx="4.5" ry="6.5" fill="#222"/><ellipse cx="64" cy="55" rx="4.5" ry="6.5" fill="#222"/>
    <circle cx="37.5" cy="52.5" r="1.6" fill="#fff"/><circle cx="65.5" cy="52.5" r="1.6" fill="#fff"/>
    <polygon points="46,67 54,67 50,72" fill="#d9667a"/>
    <path d="M50 72 Q44 79 38 75 M50 72 Q56 79 62 75" stroke="#222" stroke-width="2" fill="none" stroke-linecap="round"/>
    <path d="M30 68 L10 64 M30 72 L10 74 M70 68 L90 64 M70 72 L90 74" stroke="#222" stroke-width="1.5" stroke-linecap="round"/>
  </svg>`;

  if (CAT_IMAGE_URL) {
    CAT = '<img src="' + CAT_IMAGE_URL + '" alt="" draggable="false" style="width:100%;height:100%;object-fit:contain;display:block">';
  }

  var root = document.createElement('div');
  root.id = 'cat-egg-root';
  var tiny = document.createElement('button');
  tiny.id = 'cat-tiny';
  tiny.setAttribute('aria-label', 'Tiny cat');
  tiny.innerHTML = CAT;
  root.appendChild(tiny);
  document.body.appendChild(root);

  var big = document.createElement('button');
  big.id = 'cat-big';
  big.setAttribute('aria-label', 'Stop the cat');
  big.innerHTML = CAT;
  document.body.appendChild(big);

  var label = document.createElement('div');
  label.id = 'cat-label';
  label.textContent = 'OIIA OIIA';
  document.body.appendChild(label);

  for (var i = 0; i < 6; i++) {
    var f = document.createElement('div');
    f.className = 'cat-float';
    f.innerHTML = CAT;
    f.style.top = (8 + i * 14) + '%';
    f.style.animationDuration = (7 + Math.random() * 6) + 's';
    f.style.animationDelay = (-Math.random() * 10) + 's';
    f.style.opacity = '0.9';
    document.body.appendChild(f);
  }

  // ---- sound ----
  var ctx = null, master = null, loop = null, step = 0, audioEl = null;
  var NOTES = [392, 523, 440, 523, 392, 330, 392, 440];
  var VOWELS = [[500, 900], [300, 2200], [700, 1200]];
  var noiseBuf = null;

  function noise() {
    if (!noiseBuf) {
      noiseBuf = ctx.createBuffer(1, ctx.sampleRate, ctx.sampleRate);
      var d = noiseBuf.getChannelData(0);
      for (var i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
    }
    var n = ctx.createBufferSource();
    n.buffer = noiseBuf;
    return n;
  }

  function kick(t) {
    var o = ctx.createOscillator(), g = ctx.createGain();
    o.frequency.setValueAtTime(160, t);
    o.frequency.exponentialRampToValueAtTime(40, t + 0.12);
    g.gain.setValueAtTime(1.2, t);
    g.gain.exponentialRampToValueAtTime(0.0001, t + 0.2);
    o.connect(g); g.connect(master);
    o.start(t); o.stop(t + 0.22);
  }

  function snare(t) {
    var n = noise(), f = ctx.createBiquadFilter(), g = ctx.createGain();
    f.type = 'bandpass'; f.frequency.value = 1800; f.Q.value = 0.8;
    g.gain.setValueAtTime(0.7, t);
    g.gain.exponentialRampToValueAtTime(0.0001, t + 0.14);
    n.connect(f); f.connect(g); g.connect(master);
    n.start(t); n.stop(t + 0.15);
  }

  function hat(t, loud) {
    var n = noise(), f = ctx.createBiquadFilter(), g = ctx.createGain();
    f.type = 'highpass'; f.frequency.value = 7000;
    g.gain.setValueAtTime(loud ? 0.35 : 0.18, t);
    g.gain.exponentialRampToValueAtTime(0.0001, t + 0.05);
    n.connect(f); f.connect(g); g.connect(master);
    n.start(t); n.stop(t + 0.06);
  }

  function tick() {
    var t = ctx.currentTime;
    var f0 = NOTES[step % NOTES.length];
    var v = VOWELS[step % 3];
    var pos = step % 8;
    if (pos === 0 || pos === 4 || pos === 7) kick(t);
    if (pos === 2 || pos === 6) snare(t);
    hat(t, pos % 2 === 0);
    step++;
    var osc = ctx.createOscillator();
    osc.type = 'sawtooth';
    osc.frequency.value = f0;
    var bp = ctx.createBiquadFilter();
    bp.type = 'bandpass';
    bp.Q.value = 4;
    bp.frequency.setValueAtTime(v[0], t);
    bp.frequency.linearRampToValueAtTime(v[1], t + 0.15);
    var g = ctx.createGain();
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(1, t + 0.02);
    g.gain.exponentialRampToValueAtTime(0.0001, t + 0.18);
    osc.connect(bp); bp.connect(g); g.connect(master);
    osc.start(t); osc.stop(t + 0.2);
  }

  function startSynth() {
    var AC = window.AudioContext || window.webkitAudioContext;
    if (!AC) return;
    ctx = ctx || new AC();
    ctx.resume();
    master = ctx.createGain();
    master.gain.value = 0.18;
    master.connect(ctx.destination);
    step = 0;
    tick();
    loop = setInterval(tick, 190);
  }

  function startSound() {
    if (!CUSTOM_AUDIO_URL) { startSynth(); return; }
    audioEl = audioEl || new Audio(CUSTOM_AUDIO_URL);
    audioEl.loop = true;
    var fallback = function () {
      CUSTOM_AUDIO_URL = null;
      audioEl = null;
      if (on) startSynth();
    };
    audioEl.onerror = fallback;
    var pr = audioEl.play();
    if (pr && pr.catch) pr.catch(fallback);
  }

  function stopSound() {
    if (audioEl) { audioEl.pause(); audioEl.currentTime = 0; }
    if (loop) { clearInterval(loop); loop = null; }
    if (master) { master.disconnect(); master = null; }
  }

  // ---- clicks ----
  var clicks = 0, timer = null, on = false;

  function toggle(state) {
    on = state;
    document.body.classList.toggle('cat-on', on);
    if (on) startSound(); else stopSound();
  }

  tiny.addEventListener('click', function () {
    if (on) { toggle(false); return; }
    clicks++;
    clearTimeout(timer);
    timer = setTimeout(function () { clicks = 0; }, 1000);
    if (clicks >= 2) { clicks = 0; toggle(true); }
  });
  big.addEventListener('click', function () { toggle(false); });
})();
"""


@st.cache_data
def _loader_html():
    audio = _data_uri(["oiia.mp3"])
    image = _data_uri(["cat.png", "cat.jpg", "cat.jpeg", "cat.gif", "cat.webp"])
    js = JS.replace("__AUDIO__", json.dumps(audio)).replace("__IMAGE__", json.dumps(image))
    return (
        "<script>(function(){try{var p=window.parent;"
        "if(p.document.getElementById('cat-egg-script'))return;"
        "var s=p.document.createElement('script');s.id='cat-egg-script';"
        "s.textContent=" + json.dumps(js) + ";"
        "p.document.body.appendChild(s);}catch(e){}})();</script>"
    )


def add_cat():
    """Call once near the end of your app to add the cat."""
    components.html(_loader_html(), height=0)
