(() => {
  const out = { vw: innerWidth, dpr: devicePixelRatio };

  // 1. traboccamento orizzontale
  out.docScrollW = document.documentElement.scrollWidth;
  out.overflowX = document.documentElement.scrollWidth - document.documentElement.clientWidth;
  const troppoLarghi = [];
  document.querySelectorAll('body *').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width === 0) return;
    if (r.right > innerWidth + 1.5 || r.left < -1.5) {
      const cs = getComputedStyle(el);
      if (cs.position === 'fixed' || cs.visibility === 'hidden' || cs.display === 'none') return;
      if (el.closest('.watermark, .drawer, .lightbox, svg')) return;
      troppoLarghi.push(el.tagName.toLowerCase() + '.' + (el.className.toString().split(' ')[0] || '') +
        ' L' + Math.round(r.left) + ' R' + Math.round(r.right));
    }
  });
  out.fuoriMisura = troppoLarghi.slice(0, 12);

  // 2. immagini
  const imgs = [...document.querySelectorAll('img')];
  out.imgTotali = imgs.length;
  out.imgRotte = imgs.filter(i => i.complete && i.naturalWidth === 0).map(i => i.getAttribute('src'));
  out.imgSenzaAlt = imgs.filter(i => !i.getAttribute('alt')).map(i => i.getAttribute('src'));

  // 3. collegamenti
  const links = [...document.querySelectorAll('a')];
  out.linkTotali = links.length;
  out.linkSenzaHref = links.filter(a => !a.getAttribute('href')).length;
  out.linkVuoti = links.filter(a => {
    const h = a.getAttribute('href');
    return h === '' || h === 'javascript:void(0)';
  }).length;
  out.hrefUnici = [...new Set(links.map(a => a.getAttribute('href')))].sort();

  // 4. ancore interne effettivamente presenti
  out.ancoreRotte = links
    .map(a => a.getAttribute('href') || '')
    .filter(h => h.includes('#'))
    .map(h => h.slice(h.indexOf('#') + 1))
    .filter(id => id && !document.getElementById(id));

  // 5. tipografia
  const p = document.querySelector('.why-item p') || document.querySelector('p');
  out.corpoPx = getComputedStyle(document.body).fontSize;
  out.paragrafoPx = p ? getComputedStyle(p).fontSize : null;
  out.h1Px = document.querySelector('h1') ? getComputedStyle(document.querySelector('h1')).fontSize : null;

  // 6. bersagli tattili
  const piccoli = [];
  document.querySelectorAll('a, button, summary, input').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) return;
    if (el.closest('.drawer, .lightbox, .footer-nav, .nav-desk, .skip')) return;
    if (r.height < 34) piccoli.push(el.tagName.toLowerCase() + '.' + (el.className.toString().split(' ')[0] || '(nessuna)') + ' h' + Math.round(r.height));
  });
  out.bersagliPiccoli = [...new Set(piccoli)].slice(0, 12);

  // 7. prezzi: non devono comparire da nessuna parte
  const testo = document.body.innerText;
  out.tracceDiPrezzo = (testo.match(/€|\beuro\b|\bprezzo\b|\bcosto\b|\blistino\b|\bacquist\w+|\bcarrello\b/gi) || []);

  return JSON.stringify(out, null, 1);
})()
