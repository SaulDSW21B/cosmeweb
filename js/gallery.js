/* ============================================================
   gallery.js — Lightbox ligero en JavaScript vanilla
   Cualquier <img> con el atributo data-lightbox (o dentro de un
   .gallery-grid button / .carousel-slide) abre una vista ampliada.
   Controles: cerrar (X / Escape), anterior, siguiente, swipe táctil.
   ============================================================ */
(function () {
  'use strict';

  var lightbox, imgEl, captionEl, closeBtn, prevBtn, nextBtn;
  var items = [];
  var current = 0;
  var lastFocused = null;

  document.addEventListener('DOMContentLoaded', function () {
    buildLightbox();
    collectItems();
    bindTriggers();
  });

  function buildLightbox() {
    lightbox = document.createElement('div');
    lightbox.className = 'lightbox';
    lightbox.setAttribute('role', 'dialog');
    lightbox.setAttribute('aria-modal', 'true');
    lightbox.setAttribute('aria-label', 'Galería de fotografías ampliada');
    lightbox.innerHTML =
      '<button class="lightbox-close" aria-label="Cerrar galería">&times;</button>' +
      '<button class="lightbox-prev" aria-label="Foto anterior">&#8592;</button>' +
      '<figure class="lightbox-figure">' +
        '<img alt="">' +
        '<figcaption></figcaption>' +
      '</figure>' +
      '<button class="lightbox-next" aria-label="Foto siguiente">&#8594;</button>';
    document.body.appendChild(lightbox);

    imgEl = lightbox.querySelector('img');
    captionEl = lightbox.querySelector('figcaption');
    closeBtn = lightbox.querySelector('.lightbox-close');
    prevBtn = lightbox.querySelector('.lightbox-prev');
    nextBtn = lightbox.querySelector('.lightbox-next');

    closeBtn.addEventListener('click', close);
    prevBtn.addEventListener('click', function () { show(current - 1); });
    nextBtn.addEventListener('click', function () { show(current + 1); });

    lightbox.addEventListener('click', function (e) {
      if (e.target === lightbox) close();
    });

    document.addEventListener('keydown', function (e) {
      if (!lightbox.classList.contains('open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowRight') show(current + 1);
      if (e.key === 'ArrowLeft') show(current - 1);
      if (e.key === 'Tab') trapFocus(e);
    });

    // Swipe táctil dentro del lightbox
    var startX = 0;
    lightbox.addEventListener('touchstart', function (e) { startX = e.touches[0].clientX; }, { passive: true });
    lightbox.addEventListener('touchend', function (e) {
      var delta = e.changedTouches[0].clientX - startX;
      if (Math.abs(delta) > 40) show(current + (delta < 0 ? 1 : -1));
    });
  }

  function trapFocus(e) {
    var focusableElements = lightbox.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
    var firstElement = focusableElements[0];
    var lastElement = focusableElements[focusableElements.length - 1];
    if (e.shiftKey && document.activeElement === firstElement) {
      e.preventDefault();
      lastElement.focus();
    } else if (!e.shiftKey && document.activeElement === lastElement) {
      e.preventDefault();
      firstElement.focus();
    }
  }

  function collectItems() {
    var nodes = document.querySelectorAll(
      '.gallery-grid button img, [data-lightbox], .carousel-slide img[data-lightbox], .carousel-slide figure img'
    );
    items = Array.prototype.map.call(nodes, function (img) {
      return { src: img.currentSrc || img.src, caption: img.alt || '' };
    });
  }

  function bindTriggers() {
    var galleryButtons = document.querySelectorAll('.gallery-grid button');
    galleryButtons.forEach(function (btn, i) {
      btn.setAttribute('tabindex', '0');
      btn.setAttribute('role', 'button');
      btn.setAttribute('aria-label', 'Ver imagen ampliada ' + (i + 1));
      btn.addEventListener('click', function () { open(i); });
      btn.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          open(i);
        }
      });
    });

    // Fotos dentro de carruseles también abren el lightbox al hacer clic
    var carouselImgs = document.querySelectorAll('.carousel-slide img');
    var offset = galleryButtons.length;
    carouselImgs.forEach(function (img, i) {
      img.style.cursor = 'zoom-in';
      img.addEventListener('click', function () { open(offset + i); });
      img.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          open(offset + i);
        }
      });
    });
  }

  function open(i) {
    if (!items.length) return;
    lastFocused = document.activeElement;
    lightbox.classList.add('open');
    document.body.style.overflow = 'hidden';
    show(i);
    closeBtn.focus();
  }

  function show(i) {
    if (!items.length) return;
    current = (i + items.length) % items.length;
    var item = items[current];
    imgEl.src = item.src;
    imgEl.alt = item.caption;
    captionEl.textContent = item.caption;
  }

  function close() {
    lightbox.classList.remove('open');
    document.body.style.overflow = '';
    imgEl.src = '';
    if (lastFocused) lastFocused.focus();
  }
})();
