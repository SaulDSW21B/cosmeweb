/* ============================================================
   main.js — Centro Escolar Católico Fray Cosme Spessotto
   Funcionalidades generales del sitio:
   - Menú móvil (hamburguesa) y submenús desplegables
   - Año automático en el footer
   - Botón "Volver arriba"
   - Acordeón del Modelo Educativo Integral
   - Filtros de la página de Eventos
   - Validación del formulario de contacto
   - Animación de aparición al hacer scroll (reveal)
   ============================================================ */
(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    initMobileMenu();
    initDropdowns();
    initFooterYear();
    initBackToTop();
    initAccordion();
    initEventFilters();
    initContactForm();
    initScrollReveal();
  });

  /* ---------- Menú móvil ---------- */
  function initMobileMenu() {
    var toggle = document.getElementById('navToggle');
    var nav = document.getElementById('mainNav');
    var header = document.querySelector('.site-header');
    if (!toggle || !nav) return;

    // Update header height CSS variable dynamically
    function updateHeaderHeight() {
      if (header) {
        var h = header.offsetHeight;
        document.documentElement.style.setProperty('--header-h', h + 'px');
      }
    }

    // Initial calculation
    updateHeaderHeight();

    // Recalculate on resize and orientation change
    var resizeTimer;
    window.addEventListener('resize', function () {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(function () {
        updateHeaderHeight();
        if (window.innerWidth > 960 && nav.classList.contains('open')) {
          closeMenu();
        }
      }, 100);
    });

    // Also update on orientation change for mobile
    window.addEventListener('orientationchange', function () {
      setTimeout(updateHeaderHeight, 100);
    });

    function closeMenu() {
      nav.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
      document.body.classList.remove('menu-open');
      document.body.style.overflow = '';
    }

    function openMenu() {
      // Ensure header height is current before opening
      updateHeaderHeight();
      nav.classList.add('open');
      toggle.setAttribute('aria-expanded', 'true');
      document.body.classList.add('menu-open');
      document.body.style.overflow = 'hidden';
    }

    toggle.addEventListener('click', function () {
      var expanded = toggle.getAttribute('aria-expanded') === 'true';
      if (expanded) {
        closeMenu();
      } else {
        openMenu();
      }
    });

    // Cerrar el menú móvil al hacer clic en un enlace final (no en los que abren submenú)
    nav.querySelectorAll('.submenu a, .main-nav > ul > li > a:not(.has-submenu)').forEach(function (link) {
      link.addEventListener('click', function () {
        if (window.innerWidth <= 960) {
          closeMenu();
        }
      });
    });

    // Cerrar con tecla Escape
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('open')) {
        closeMenu();
        toggle.focus();
      }
    });
  }

  /* ---------- Submenús (escritorio: hover/click | móvil: clic para expandir) ---------- */
  function initDropdowns() {
    var items = document.querySelectorAll('.main-nav .nav-item.has-children');

    items.forEach(function (item) {
      var link = item.querySelector(':scope > a');
      if (!link) return;

      link.addEventListener('click', function (e) {
        var isMobile = window.innerWidth <= 960;
        if (isMobile) {
          e.preventDefault();
          var willOpen = !item.classList.contains('open');
          items.forEach(function (i) { if (i !== item) i.classList.remove('open'); });
          item.classList.toggle('open', willOpen);
          link.setAttribute('aria-expanded', String(willOpen));
        }
      });

      // Keyboard support for desktop
      link.addEventListener('keydown', function (e) {
        if (window.innerWidth > 960) {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            var willOpen = !item.classList.contains('open');
            items.forEach(function (i) { if (i !== item) i.classList.remove('open'); });
            item.classList.toggle('open', willOpen);
            link.setAttribute('aria-expanded', String(willOpen));
          }
          if (e.key === 'Escape') {
            item.classList.remove('open');
            link.setAttribute('aria-expanded', 'false');
          }
        }
      });
    });

    // Cerrar submenús de escritorio al hacer clic fuera
    document.addEventListener('click', function (e) {
      if (window.innerWidth > 960) {
        var isClickInside = e.target.closest('.nav-item.has-children');
        if (!isClickInside) {
          items.forEach(function (i) { i.classList.remove('open'); });
        }
      }
    });
  }

  /* ---------- Año automático ---------- */
  function initFooterYear() {
    var el = document.getElementById('anioActual');
    if (el) el.textContent = new Date().getFullYear();
  }

  /* ---------- Volver arriba ---------- */
  function initBackToTop() {
    var btn = document.getElementById('backToTop');
    if (!btn) return;
    window.addEventListener('scroll', function () {
      btn.classList.toggle('show', window.scrollY > 480);
    }, { passive: true });

    btn.addEventListener('click', function () {
      var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
    });
  }

  /* ---------- Acordeón (Modelo Educativo Integral) ---------- */
  function initAccordion() {
    var triggers = document.querySelectorAll('.accordion-trigger');
    triggers.forEach(function (trigger) {
      var panel = document.getElementById(trigger.getAttribute('aria-controls'));
      if (!panel) return;

      // Set initial ARIA state
      trigger.setAttribute('aria-expanded', 'false');

      trigger.addEventListener('click', function () {
        var expanded = trigger.getAttribute('aria-expanded') === 'true';
        trigger.setAttribute('aria-expanded', String(!expanded));
        if (!expanded) {
          panel.classList.add('is-open');
          panel.style.maxHeight = panel.scrollHeight + 'px';
        } else {
          panel.classList.remove('is-open');
          panel.style.maxHeight = 0;
        }
      });

      // Keyboard support
      trigger.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          trigger.click();
        }
      });
    });

    // Recalcular alturas si cambia el tamaño de ventana (texto reflow)
    var resizeTimer;
    window.addEventListener('resize', function () {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(function () {
        document.querySelectorAll('.accordion-trigger[aria-expanded="true"]').forEach(function (trigger) {
          var panel = document.getElementById(trigger.getAttribute('aria-controls'));
          if (panel && panel.classList.contains('is-open')) {
            panel.style.maxHeight = 'auto';
            var height = panel.scrollHeight;
            panel.style.maxHeight = height + 'px';
          }
        });
      }, 150);
    });
  }

  /* ---------- Filtros de eventos ---------- */
  function initEventFilters() {
    var bar = document.querySelector('.filter-bar');
    if (!bar) return;
    var buttons = bar.querySelectorAll('.filter-btn');
    var cards = document.querySelectorAll('.event-card');
    var empty = document.querySelector('.empty-state');

    buttons.forEach(function (btn) {
      btn.addEventListener('click', function () {
        buttons.forEach(function (b) { b.setAttribute('aria-pressed', 'false'); });
        btn.setAttribute('aria-pressed', 'true');
        var cat = btn.getAttribute('data-filter');
        var visibleCount = 0;

        cards.forEach(function (card) {
          var match = cat === 'todos' || card.getAttribute('data-category') === cat;
          card.hidden = !match;
          if (match) visibleCount++;
        });

        if (empty) empty.classList.toggle('show', visibleCount === 0);
      });
    });
  }

  /* ---------- Formulario de contacto ---------- */
  function initContactForm() {
    var form = document.getElementById('formContacto');
    if (!form) return;
    var status = document.getElementById('formStatus');

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var valid = true;

      var fields = [
        { id: 'nombre', check: function (v) { return v.trim().length >= 2; }, msg: 'Escribe tu nombre completo.' },
        { id: 'correo', check: function (v) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim()); }, msg: 'Escribe un correo electrónico válido.' },
        { id: 'asunto', check: function (v) { return v.trim().length >= 3; }, msg: 'Cuéntanos brevemente el asunto.' },
        { id: 'mensaje', check: function (v) { return v.trim().length >= 10; }, msg: 'Escribe un mensaje de al menos 10 caracteres.' }
      ];

      fields.forEach(function (f) {
        var input = document.getElementById(f.id);
        if (!input) return;
        var wrap = input.closest('.form-field');
        var errorEl = wrap.querySelector('.field-error');
        var ok = f.check(input.value);
        wrap.classList.toggle('invalid', !ok);
        if (errorEl) errorEl.textContent = ok ? '' : f.msg;
        if (!ok) valid = false;
      });

      // Teléfono es opcional, pero si se llena debe tener formato razonable
      var tel = document.getElementById('telefono');
      if (tel && tel.value.trim() && !/^[0-9+\s\-()]{7,15}$/.test(tel.value.trim())) {
        var telWrap = tel.closest('.form-field');
        telWrap.classList.add('invalid');
        telWrap.querySelector('.field-error').textContent = 'Escribe un número de teléfono válido.';
        valid = false;
      }

      if (!valid) {
        if (status) {
          status.textContent = 'Por favor corrige los campos marcados antes de enviar.';
          status.style.background = '#FBEAEA';
          status.style.color = '#7A1F2B';
          status.classList.add('show');
        }
        return;
      }

      /* ------------------------------------------------------------
         Este formulario aún NO tiene backend conectado.
         Para recibir los mensajes reales, conecta uno de estos servicios
         y reemplaza este bloque por el envío correspondiente:

         Opción A) Formspree:
           fetch('https://formspree.io/f/TU_ID', { method:'POST', body:new FormData(form), headers:{Accept:'application/json'} })

         Opción B) EmailJS:
           emailjs.sendForm('SERVICE_ID','TEMPLATE_ID', form)

         Opción C) Backend propio (Node, PHP, etc.):
           fetch('/api/contacto', { method:'POST', body: JSON.stringify(datos) })
      ------------------------------------------------------------ */

      if (status) {
        status.textContent = '¡Gracias! Tu mensaje quedó listo para enviarse. (Falta conectar el formulario a un servicio de envío real — ver comentario en js/main.js).';
        status.style.background = '#EAF3E9';
        status.style.color = '#285C33';
        status.classList.add('show');
      }
      form.reset();
    });
  }

  /* ---------- Animación de aparición al hacer scroll ---------- */
  function initScrollReveal() {
    var items = document.querySelectorAll('.reveal');
    if (!items.length) return;

    if (!('IntersectionObserver' in window) || window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      items.forEach(function (el) { el.classList.add('in-view'); });
      return;
    }

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in-view');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });

    items.forEach(function (el) { observer.observe(el); });
  }

  /* ---------- Utilidad ---------- */
  function debounce(fn, wait) {
    var t;
    return function () {
      clearTimeout(t);
      var args = arguments;
      t = setTimeout(function () { fn.apply(null, args); }, wait);
    };
  }
})();
