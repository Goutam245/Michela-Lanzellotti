/* =========================================================================
   Michela Lanzellotti — comportamenti di pagina
   Nessuna libreria esterna. Tutto degrada con grazia se il JS non parte.
   ========================================================================= */
(function () {
  'use strict';

  var ridotto = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ------------------------------------------------------------ testata */
  var testata = document.querySelector('.site-header');
  if (testata) {
    var aggiornaTestata = function () {
      testata.classList.toggle('is-stuck', window.scrollY > 24);
    };
    aggiornaTestata();
    window.addEventListener('scroll', aggiornaTestata, { passive: true });
  }

  /* ------------------------------------------------------------ cassetto */
  var burger = document.getElementById('burger');
  var cassetto = document.getElementById('cassetto');

  if (burger && cassetto) {
    var voci = cassetto.querySelectorAll('nav a');
    Array.prototype.forEach.call(voci, function (a, i) {
      a.style.animationDelay = (90 + i * 55) + 'ms';
    });

    var chiudiCassetto = function () {
      cassetto.classList.remove('is-open');
      burger.setAttribute('aria-expanded', 'false');
      burger.setAttribute('aria-label', 'Apri il menu');
      document.body.classList.remove('is-locked');
    };

    var apriCassetto = function () {
      cassetto.classList.add('is-open');
      burger.setAttribute('aria-expanded', 'true');
      burger.setAttribute('aria-label', 'Chiudi il menu');
      document.body.classList.add('is-locked');
    };

    burger.addEventListener('click', function () {
      if (burger.getAttribute('aria-expanded') === 'true') { chiudiCassetto(); }
      else { apriCassetto(); }
    });

    Array.prototype.forEach.call(voci, function (a) {
      a.addEventListener('click', chiudiCassetto);
    });
    var ctaCassetto = cassetto.querySelector('.drawer-foot a');
    if (ctaCassetto) { ctaCassetto.addEventListener('click', chiudiCassetto); }

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && burger.getAttribute('aria-expanded') === 'true') {
        chiudiCassetto();
        burger.focus();
      }
    });

    // se si passa a schermo largo mentre il cassetto è aperto
    var largo = window.matchMedia('(min-width: 68em)');
    var onLargo = function (e) { if (e.matches) { chiudiCassetto(); } };
    if (largo.addEventListener) { largo.addEventListener('change', onLargo); }
    else if (largo.addListener) { largo.addListener(onLargo); }
  }

  /* ------------------------------------------------------------ comparse */
  var daRivelare = document.querySelectorAll('.reveal');

  var mostraTutto = function () {
    Array.prototype.forEach.call(daRivelare, function (el) { el.classList.add('is-in'); });
  };

  if (!('IntersectionObserver' in window) || ridotto) {
    mostraTutto();
  } else {
    var osservatore = new IntersectionObserver(function (voci) {
      voci.forEach(function (v) {
        if (v.isIntersecting) {
          v.target.classList.add('is-in');
          osservatore.unobserve(v.target);
        }
      });
      // margine fisso, non percentuale: su schermi molto alti una percentuale
      // creerebbe una fascia cieca in fondo alla finestra
    }, { rootMargin: '0px 0px -80px 0px', threshold: 0 });
    Array.prototype.forEach.call(daRivelare, function (el) { osservatore.observe(el); });

    // rete di sicurezza: se per qualsiasi motivo qualcosa resta nascosto,
    // dopo qualche secondo si mostra comunque. Il testo viene prima dell'effetto.
    window.setTimeout(function () {
      Array.prototype.forEach.call(daRivelare, function (el) {
        var r = el.getBoundingClientRect();
        if (r.top < window.innerHeight * 1.5) { el.classList.add('is-in'); }
      });
    }, 2500);
  }

  /* ------------------------------------------------------------ il rosone si accende */
  var palco = document.getElementById('stage-rosone');
  if (palco) {
    if (!('IntersectionObserver' in window) || ridotto) {
      palco.classList.add('is-lit');
    } else {
      var luce = new IntersectionObserver(function (voci) {
        voci.forEach(function (v) {
          if (v.isIntersecting) { v.target.classList.add('is-lit'); luce.unobserve(v.target); }
        });
      }, { threshold: 0.3 });
      luce.observe(palco);
    }
  }

  /* ------------------------------------------------------------ lente sulle foto */
  var lente = document.getElementById('lente');
  var scatti = Array.prototype.slice.call(document.querySelectorAll('.gal-item'));

  if (lente && scatti.length) {
    var lbImg = document.getElementById('lb-img');
    var lbCap = document.getElementById('lb-cap');
    var lbChiudi = document.getElementById('lb-close');
    var lbPrec = document.getElementById('lb-prev');
    var lbSucc = document.getElementById('lb-next');
    var indice = 0;
    var ultimoFocus = null;

    var mostra = function (i) {
      indice = (i + scatti.length) % scatti.length;
      var b = scatti[indice];
      var img = b.querySelector('img');
      var pieno = b.getAttribute('data-src') || img.getAttribute('src');
      // prima il webp, con ritorno al jpg se il browser non lo legge
      lbImg.onerror = function () {
        if (this.src.slice(-5) === '.webp') { this.src = this.src.replace(/\.webp$/, '.jpg'); }
      };
      lbImg.src = pieno.replace(/\.jpg$/, '.webp');
      lbImg.alt = img ? img.getAttribute('alt') : '';
      lbCap.textContent = b.getAttribute('data-cap') || '';
    };

    var apriLente = function (i) {
      ultimoFocus = document.activeElement;
      lente.hidden = false;
      mostra(i);
      requestAnimationFrame(function () { lente.classList.add('is-open'); });
      document.body.classList.add('is-locked');
      lbChiudi.focus();
    };

    var chiudiLente = function () {
      lente.classList.remove('is-open');
      document.body.classList.remove('is-locked');
      window.setTimeout(function () { lente.hidden = true; lbImg.src = ''; }, ridotto ? 0 : 400);
      if (ultimoFocus && ultimoFocus.focus) { ultimoFocus.focus(); }
    };

    scatti.forEach(function (b, i) {
      b.addEventListener('click', function () { apriLente(i); });
    });

    lbChiudi.addEventListener('click', chiudiLente);
    lbPrec.addEventListener('click', function () { mostra(indice - 1); });
    lbSucc.addEventListener('click', function () { mostra(indice + 1); });
    lente.addEventListener('click', function (e) {
      if (e.target === lente || e.target.tagName === 'FIGURE') { chiudiLente(); }
    });

    document.addEventListener('keydown', function (e) {
      if (lente.hidden) { return; }
      if (e.key === 'Escape') { chiudiLente(); }
      else if (e.key === 'ArrowLeft') { mostra(indice - 1); }
      else if (e.key === 'ArrowRight') { mostra(indice + 1); }
      else if (e.key === 'Tab') {
        // il fuoco resta dentro la lente
        var focalizzabili = [lbChiudi, lbPrec, lbSucc];
        var pos = focalizzabili.indexOf(document.activeElement);
        e.preventDefault();
        var passo = e.shiftKey ? -1 : 1;
        focalizzabili[(pos + passo + focalizzabili.length) % focalizzabili.length].focus();
      }
    });
  }

  /* ------------------------------------------------------------ il calendario del tuo abito */
  var modulo = document.getElementById('cal-form');

  if (modulo) {
    var campo = document.getElementById('cal-data');
    var esito = document.getElementById('cal-out');
    var avviso = document.getElementById('cal-msg');
    var wa = document.getElementById('cal-wa');
    var baseWa = wa.getAttribute('href').split('?')[0];

    var formato = new Intl.DateTimeFormat('it-IT', { day: 'numeric', month: 'long', year: 'numeric' });
    var fmt = function (d) {
      var s = formato.format(d);
      return s.charAt(0).toUpperCase() + s.slice(1);
    };

    var oggi = new Date();
    oggi.setHours(0, 0, 0, 0);

    // la data minima selezionabile è domani (calcolata in ora locale, non UTC)
    var iso = function (d) {
      return d.getFullYear() + '-' +
             ('0' + (d.getMonth() + 1)).slice(-2) + '-' +
             ('0' + d.getDate()).slice(-2);
    };
    campo.min = iso(new Date(oggi.getFullYear(), oggi.getMonth(), oggi.getDate() + 1));

    // la data di oggi si conosce senza chiedere nulla: il calendario parte già acceso
    var celleOggi = document.getElementById('cal-oggi');
    celleOggi.textContent = fmt(oggi);
    celleOggi.classList.remove('is-vuoto');

    // un mese esatto prima, con il giorno riportato all'ultimo del mese se non esiste
    var unMesePrima = function (d) {
      var g = d.getDate();
      var r = new Date(d.getFullYear(), d.getMonth() - 1, 1);
      var ultimo = new Date(r.getFullYear(), r.getMonth() + 1, 0).getDate();
      r.setDate(Math.min(g, ultimo));
      return r;
    };

    modulo.addEventListener('submit', function (e) {
      e.preventDefault();
      avviso.textContent = '';

      // riporta il calendario allo stato di attesa
      var svuota = function () {
        ['cal-consegna', 'cal-nozze'].forEach(function (id) {
          var el = document.getElementById(id);
          el.textContent = '—';
          el.classList.add('is-vuoto');
        });
        wa.hidden = true;
        esito.classList.remove('is-on');
      };

      var parti = (campo.value || '').split('-');
      if (parti.length !== 3) {
        avviso.textContent = 'Scegli la data del matrimonio.';
        svuota();
        campo.focus();
        return;
      }

      var nozze = new Date(+parti[0], +parti[1] - 1, +parti[2]);
      nozze.setHours(0, 0, 0, 0);

      if (isNaN(nozze.getTime())) {
        avviso.textContent = 'Questa data non esiste. Controllala e riprova.';
        svuota();
        return;
      }

      if (nozze <= oggi) {
        avviso.textContent = 'Scegli una data futura: il calendario parte da oggi.';
        svuota();
        campo.focus();
        return;
      }

      var consegna = unMesePrima(nozze);

      [['cal-consegna', consegna], ['cal-nozze', nozze]].forEach(function (coppia) {
        var el = document.getElementById(coppia[0]);
        el.textContent = fmt(coppia[1]);
        el.classList.remove('is-vuoto');
      });

      if (consegna <= oggi) {
        avviso.textContent = 'La consegna cadrebbe prima di oggi: scrivi subito a Michela e parlatene insieme.';
      }

      var testo = 'Ciao Michela, il mio matrimonio è il ' + formato.format(nozze) +
                  '. Vorrei parlarti del mio abito.';
      wa.setAttribute('href', baseWa + '?text=' + encodeURIComponent(testo));
      wa.hidden = false;
      esito.classList.add('is-on');
    });
  }

})();
