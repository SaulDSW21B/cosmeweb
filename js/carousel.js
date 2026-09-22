/* ============================================================
   carousel.js — Componente de carrusel reutilizable
   Uso: agrega data-carousel a un contenedor con la estructura:

   <div class="carousel" data-carousel>
     <div class="carousel-viewport">
       <div class="carousel-track">
         <div class="carousel-slide">...</div>
         ...
       </div>
     </div>
     <div class="carousel-controls">
       <button class="carousel-btn" data-prev aria-label="Anterior">&#8592;</button>
       <div class="carousel-dots"></div>
       <button class="carousel-btn" data-next aria-label="Siguiente">&#8594;</button>
     </div>
   </div>

   Soporta: flechas, puntos indicadores, teclado (flechas izq/der con foco),
   swipe táctil y arrastre con mouse. Los puntos y el número de slides
   visibles se recalculan según el ancho disponible.
   ============================================================ */
(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[data-carousel]').forEach(setupCarousel);
  });

  function setupCarousel(root) {
    var viewport = root.querySelector('.carousel-viewport');
    var track = root.querySelector('.carousel-track');
    var slides = Array.prototype.slice.call(root.querySelectorAll('.carousel-slide'));
    var prevBtn = root.querySelector('[data-prev]');
    var nextBtn = root.querySelector('[data-next]');
    var dotsWrap = root.querySelector('.carousel-dots');
    if (!track || !slides.length) return;

    var index = 0;
    var perView = getPerView();
    var maxIndex = Math.max(0, slides.length - perView);

    buildDots();
    update();

    // Debounced resize handler
    var resizeTimer;
    window.addEventListener('resize', function () {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(function () {
        perView = getPerView();
        maxIndex = Math.max(0, slides.length - perView);
        if (index > maxIndex) index = maxIndex;
        buildDots();
        update();
      }, 150);
    });

    if (prevBtn) prevBtn.addEventListener('click', function () { go(index - 1); });
    if (nextBtn) nextBtn.addEventListener('click', function () { go(index + 1); });

    // Navegación con teclado cuando el carrusel tiene el foco
    root.setAttribute('tabindex', '0');
    root.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { go(index + 1); }
      if (e.key === 'ArrowLeft') { go(index - 1); }
      if (e.key === 'Home') { e.preventDefault(); go(0); }
      if (e.key === 'End') { e.preventDefault(); go(maxIndex); }
    });

    // Soporte táctil / swipe
    var startX = 0, currentX = 0, dragging = false;
    viewport.addEventListener('touchstart', function (e) {
      startX = e.touches[0].clientX; dragging = true;
    }, { passive: true });
    viewport.addEventListener('touchmove', function (e) {
      if (!dragging) return;
      currentX = e.touches[0].clientX;
    }, { passive: true });
    viewport.addEventListener('touchend', function () {
      if (!dragging) return;
      var delta = currentX - startX;
      if (Math.abs(delta) > 40) { go(delta < 0 ? index + 1 : index - 1); }
      dragging = false; startX = 0; currentX = 0;
    });

    // Arrastre con mouse (desktop)
    var mouseDown = false, mouseStartX = 0;
    viewport.addEventListener('mousedown', function (e) { mouseDown = true; mouseStartX = e.clientX; });
    window.addEventListener('mouseup', function (e) {
      if (!mouseDown) return;
      var delta = e.clientX - mouseStartX;
      if (Math.abs(delta) > 50) { go(delta < 0 ? index + 1 : index - 1); }
      mouseDown = false;
    });

    function getPerView() {
      // Use viewport width for more accurate calculation
      var w = viewport ? viewport.clientWidth : (root.clientWidth || window.innerWidth);
      if (w >= 1180) return slides.some(function(s) { return s.classList.contains('wide-4'); }) ? 4 : 3;
      if (w >= 900) return 3;
      if (w >= 560) return 2;
      return 1;
    }

    function go(newIndex) {
      index = Math.min(Math.max(newIndex, 0), maxIndex);
      update();
    }

    function update() {
      var slideWidth = 100 / perView;
      slides.forEach(function (slide) { slide.style.flexBasis = slideWidth + '%'; });
      track.style.transform = 'translateX(-' + (index * slideWidth) + '%)';

      if (prevBtn) prevBtn.disabled = index === 0;
      if (nextBtn) nextBtn.disabled = index >= maxIndex;

      if (dotsWrap) {
        Array.prototype.forEach.call(dotsWrap.children, function (dot, i) {
          dot.setAttribute('aria-current', String(i === index));
        });
      }
    }

    function buildDots() {
      if (!dotsWrap) return;
      dotsWrap.innerHTML = '';
      var dotCount = maxIndex + 1;
      for (var i = 0; i < dotCount; i++) {
        var dot = document.createElement('button');
        dot.type = 'button';
        dot.setAttribute('aria-label', 'Ir a la imagen ' + (i + 1));
        dot.setAttribute('aria-current', String(i === index));
        (function (i) { dot.addEventListener('click', function () { go(i); }); })(i);
        dotsWrap.appendChild(dot);
      }
    }
  }

  function debounce(fn, wait) {
    var t;
    return function () {
      clearTimeout(t);
      var args = arguments;
      t = setTimeout(function () { fn.apply(null, args); }, wait);
    };
  }
})();
