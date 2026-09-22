# -*- coding: utf-8 -*-
"""
Generador del sitio del Centro Escolar Católico Fray Cosme Spessotto.
Construye cada página HTML a partir de plantillas compartidas
(header, navegación, breadcrumbs, footer, botones flotantes)
para mantener coherencia y facilitar el mantenimiento.
"""
import os

OUT = "/home/claude/build/cosmeweb"

# ---------------------------------------------------------------
# DATOS INSTITUCIONALES REALES (proporcionados por el usuario)
# ---------------------------------------------------------------
NOMBRE = 'Centro Escolar Católico &quot;Fray Cosme Spessotto&quot;'
NOMBRE_CORTO = "Fray Cosme Spessotto"
DIRECCION = "Km 60 Barrio Guadalupe, Distrito de San Luis La Herradura"
TELEFONO = "2355-8959"
TELEFONO_HREF = "tel:+50323558959"
CORREO = "parroquialcosmespessotto@gmail.com"
LEMA = "Formar para construir un mundo fraterno"
MISION = ('Ofrecer una formación de calidad en las dimensiones espiritual, humana y académica, '
          'inspirada en valores evangélicos, marianos y franciscanos, para comprometerse a '
          '&ldquo;Reparar la viña del Señor&rdquo;.')
VISION = ('Ser una institución de sólido prestigio que desarrolla competencias académicas, '
          'científicas y espirituales, comprometida con la calidad educativa, la educación '
          'virtual y bilingüe, basada en principios y valores evangélicos según el espíritu franciscano.')
MAPS_EMBED_SRC = "https://www.google.com/maps?q=" + DIRECCION.replace(" ", "+").replace(",", "%2C") + "&output=embed"

# ---------------------------------------------------------------
# NAVEGACIÓN
# ---------------------------------------------------------------
NAV = [
    {"key": "inicio", "label": "Inicio", "href": "index.html"},
    {"key": "nosotros", "label": "Acerca de Nosotros", "href": "nosotros.html", "children": [
        ("Quiénes somos", "nosotros.html"),
        ("Historia de la institución", "historia.html"),
        ("Fundador", "fundador.html"),
        ("Identidad Institucional", "identidad.html"),
        ("Modelo Educativo Integral", "modelo-educativo.html"),
    ]},
    {"key": "niveles", "label": "Niveles Educativos", "href": "niveles-educativos.html", "children": [
        ("Visión general", "niveles-educativos.html"),
        ("Parvularia y Primer Grado", "parvularia.html"),
        ("Educación Básica", "educacion-basica.html"),
    ]},
    {"key": "vida", "label": "Vida Estudiantil", "href": "vida-estudiantil.html", "children": [
        ("Banda", "vida-estudiantil.html#banda"),
        ("Cachiporras", "vida-estudiantil.html#cachiporras"),
        ("Actividades pastorales", "vida-estudiantil.html#pastoral"),
        ("Actividades institucionales", "vida-estudiantil.html#institucional"),
        ("Galería y eventos", "eventos.html"),
    ]},
    {"key": "contacto", "label": "Contáctanos", "href": "contacto.html", "button": True},
]

PAGE_SECTION = {
    "index.html": "inicio",
    "nosotros.html": "nosotros",
    "historia.html": "nosotros",
    "fundador.html": "nosotros",
    "identidad.html": "nosotros",
    "modelo-educativo.html": "nosotros",
    "niveles-educativos.html": "niveles",
    "parvularia.html": "niveles",
    "educacion-basica.html": "niveles",
    "vida-estudiantil.html": "vida",
    "eventos.html": "vida",
    "contacto.html": "contacto",
}


def build_nav(current_file):
    active_key = PAGE_SECTION.get(current_file, "")
    items_html = []
    for item in NAV:
        is_active = item["key"] == active_key
        li_classes = "nav-item"
        if "children" in item:
            li_classes += " has-children"
        if is_active:
            li_classes += " active"

        if item.get("button"):
            items_html.append(
                '<li class="{cls}"><a href="{href}" class="btn-contacto">{label}</a></li>'.format(
                    cls=li_classes, href=item["href"], label=item["label"]))
            continue

        if "children" in item:
            sub_items = "".join(
                '<li><a href="{href}">{label}</a></li>'.format(href=h, label=l)
                for l, h in item["children"]
            )
            items_html.append(
                '<li class="{cls}">'
                '<a href="{href}" class="has-submenu">{label} <span class="caret" aria-hidden="true">&#9662;</span></a>'
                '<ul class="submenu">{subs}</ul>'
                '</li>'.format(cls=li_classes, href=item["href"], label=item["label"], subs=sub_items)
            )
        else:
            items_html.append(
                '<li class="{cls}"><a href="{href}"{aria}>{label}</a></li>'.format(
                    cls=li_classes, href=item["href"], label=item["label"],
                    aria=' aria-current="page"' if is_active else '')
            )
    return "".join(items_html)


def header_html(current_file):
    return '''<header class="site-header">
  <div class="header-bar">
    <a href="index.html" class="brand">
      <img src="img/logo/logo.png" alt="Escudo del {nombre}">
      <span class="brand-text"><strong>{nombre_corto}</strong><span>Centro Escolar Católico</span></span>
    </a>
    <button class="nav-toggle" id="navToggle" aria-label="Abrir menú de navegación" aria-expanded="false" aria-controls="mainNav">
      <span></span><span></span><span></span>
    </button>
    <nav class="main-nav" id="mainNav" aria-label="Navegación principal">
      <ul>
        {items}
      </ul>
    </nav>
  </div>
</header>
'''.format(nombre=NOMBRE, nombre_corto=NOMBRE_CORTO, items=build_nav(current_file))


def breadcrumbs_html(trail):
    """trail: list of (label, href_or_None). Last item has href None (página actual)."""
    parts = []
    for i, (label, href) in enumerate(trail):
        if href:
            parts.append('<a href="{href}">{label}</a>'.format(href=href, label=label))
        else:
            parts.append('<span aria-current="page">{label}</span>'.format(label=label))
        if i < len(trail) - 1:
            parts.append('<span class="sep" aria-hidden="true">/</span>')
    return '<nav class="breadcrumbs" aria-label="Ruta de navegación">{parts}</nav>'.format(parts="".join(parts))


def page_banner(title, desc, trail):
    return '''<section class="page-banner">
  <div class="wrap">
    {crumbs}
    <h1>{title}</h1>
    <p>{desc}</p>
  </div>
</section>
'''.format(crumbs=breadcrumbs_html(trail), title=title, desc=desc)


def footer_html():
    return '''<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-col footer-brand">
        <img src="img/logo/logo.png" alt="Escudo del {nombre}">
        <div>
          <strong>{nombre_corto}</strong>
          <p>&ldquo;{lema}&rdquo;</p>
        </div>
      </div>
      <div class="footer-col">
        <h4>Navegación</h4>
        <a href="nosotros.html">Acerca de Nosotros</a>
        <a href="modelo-educativo.html">Modelo Educativo Integral</a>
        <a href="vida-estudiantil.html">Vida Estudiantil</a>
        <a href="eventos.html">Eventos</a>
        <a href="contacto.html">Contáctanos</a>
      </div>
      <div class="footer-col">
        <h4>Niveles educativos</h4>
        <a href="parvularia.html">Parvularia</a>
        <a href="parvularia.html">Primer Grado</a>
        <a href="educacion-basica.html">Primer Ciclo (1&deg;&ndash;3&deg;)</a>
        <a href="educacion-basica.html">Segundo Ciclo (4&deg;&ndash;6&deg;)</a>
        <a href="educacion-basica.html">Tercer Ciclo (7&deg;&ndash;9&deg;)</a>
      </div>
      <div class="footer-col">
        <h4>Contacto</h4>
        <p>{direccion}</p>
        <a href="{tel_href}">{telefono}</a>
        <a href="mailto:{correo}">{correo}</a>
        <div class="footer-social">
          <!-- Reemplazar por el enlace oficial de Facebook del centro escolar -->
          <a href="#" aria-label="Facebook" target="_blank" rel="noopener">f</a>
          <!-- Agregar aquí otras redes sociales disponibles -->
        </div>
      </div>
    </div>
    <div class="footer-bottom">&copy; <span id="anioActual"></span> {nombre}. Todos los derechos reservados.</div>
  </div>
</footer>
'''.format(nombre=NOMBRE, nombre_corto=NOMBRE_CORTO, lema=LEMA, direccion=DIRECCION,
           tel_href=TELEFONO_HREF, telefono=TELEFONO, correo=CORREO)


FLOATERS = '''<!-- Botón flotante de WhatsApp: reemplazar NUMERO_WHATSAPP por el número oficial -->
<a class="whatsapp-float" href="https://wa.me/NUMERO_WHATSAPP" target="_blank" rel="noopener" aria-label="Escribir por WhatsApp">&#128172;</a>
<button class="back-to-top" id="backToTop" aria-label="Volver arriba">&#8593;</button>
'''


def head_html(title, description, canonical):
    return '''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="https://www.fraycosmespessotto.edu.sv/{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="img/inicio/hero-portada.jpg">
<meta property="og:locale" content="es_SV">
<link rel="icon" href="img/logo/logo.png" type="image/png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,500;0,600;1,500&family=Karla:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/styles.css">
<link rel="stylesheet" href="css/responsive.css">
<script>document.documentElement.classList.add('js');</script>
</head>
'''.format(title=title, description=description, canonical=canonical)


def page(filename, title, description, body):
    """Ensambla una página completa: head + header + body + footer + scripts."""
    html = head_html(title, description, filename)
    html += '<body>\n'
    html += '<a class="skip-link" href="#main">Saltar al contenido principal</a>\n'
    html += header_html(filename)
    html += '<main id="main">\n'
    html += body
    html += '</main>\n'
    html += footer_html()
    html += FLOATERS
    html += '<script src="js/carousel.js" defer></script>\n'
    html += '<script src="js/gallery.js" defer></script>\n'
    html += '<script src="js/main.js" defer></script>\n'
    html += '</body>\n</html>\n'
    with open(os.path.join(OUT, filename), "w", encoding="utf-8") as f:
        f.write(html)
    print("Generado:", filename)


def cta_block(title, sub, primary, secondary=None):
    sec = ''
    if secondary:
        sec = '<a href="{href}" class="btn btn-outline">{label}</a>'.format(href=secondary[1], label=secondary[0])
    return '''<section class="tint">
  <div class="wrap text-center">
    <div class="section-head center reveal">
      <h2>{title}</h2>
      <p class="lede">{sub}</p>
    </div>
    <div class="hero-actions" style="justify-content:center;">
      <a href="{phref}" class="btn btn-primary">{plabel}</a>
      {sec}
    </div>
  </div>
</section>
'''.format(title=title, sub=sub, phref=primary[1], plabel=primary[0], sec=sec)


def carousel_block(title_id, images_captions, per4=False):
    """images_captions: list of (src, caption)"""
    slides = ""
    for src, cap in images_captions:
        slides += '''<div class="carousel-slide">
          <figure><img src="{src}" alt="{cap}" loading="lazy" data-lightbox></figure>
          <figcaption>{cap}</figcaption>
        </div>
        '''.format(src=src, cap=cap)
    perattr = ' data-per-view-4="4"' if per4 else ''
    return '''<div class="carousel reveal" data-carousel{perattr} aria-roledescription="carrusel" aria-label="Galería de fotografías: {title_id}">
  <div class="carousel-viewport">
    <div class="carousel-track">
      {slides}
    </div>
  </div>
  <div class="carousel-controls">
    <button class="carousel-btn" data-prev type="button" aria-label="Fotografía anterior">&#8592;</button>
    <div class="carousel-dots"></div>
    <button class="carousel-btn" data-next type="button" aria-label="Fotografía siguiente">&#8594;</button>
  </div>
</div>
'''.format(title_id=title_id, slides=slides, perattr=perattr)


# =================================================================
# INDEX.HTML
# =================================================================
def gen_index():
    body = '''
<section class="hero">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <span class="eyebrow">{lema}</span>
      <h1>Formación católica de calidad, desde Parvularia hasta Noveno Grado</h1>
      <p>El {nombre} acompaña a las familias del Distrito de San Luis La Herradura en la formación espiritual, humana y académica de sus hijos, inspirados en los valores evangélicos, marianos y franciscanos.</p>
      <div class="hero-actions">
        <a href="nosotros.html" class="btn btn-primary">Conócenos</a>
        <a href="niveles-educativos.html" class="btn btn-outline">Niveles Educativos</a>
        <a href="contacto.html" class="btn btn-outline">Contáctanos</a>
      </div>
    </div>
    <div class="hero-media">
      <img src="img/inicio/hero-portada.jpg" alt="Estudiantes del Centro Escolar Católico Fray Cosme Spessotto" width="900" height="700">
      <div class="hero-floating">
        <span class="icon" aria-hidden="true">&#9993;</span>
        <div><strong>{correo}</strong><span>Escríbenos tus dudas</span></div>
      </div>
    </div>
  </div>
</section>

<section class="surface">
  <div class="wrap split-panel reveal">
    <div class="panel">
      <img src="img/inicio/hero-portada.jpg" alt="Comunidad educativa del centro escolar" loading="lazy">
      <div class="panel-body">
        <span class="eyebrow">Quiénes somos</span>
        <h2>Una comunidad educativa con identidad propia</h2>
        <p>Formamos personas íntegras a partir de nuestra misión, visión y del carisma franciscano que da identidad a la institución. Conoce nuestra historia, a nuestro fundador y el modelo educativo que guía cada etapa del aprendizaje.</p>
        <a href="nosotros.html" class="card-link">Conocer más</a>
      </div>
    </div>
    <div class="panel">
      <img src="img/institucionales/placeholder-1.jpg" alt="Actividad institucional del centro escolar" loading="lazy">
      <div class="panel-body">
        <span class="eyebrow">Nuestra propuesta</span>
        <h2>Modelo Educativo Integral</h2>
        <p>Formación académica, en valores, en fe y acompañamiento psicológico se entrelazan en cada nivel, junto con inglés e informática desde Parvularia hasta Noveno Grado.</p>
        <a href="modelo-educativo.html" class="card-link">Conocer más</a>
      </div>
    </div>
  </div>
</section>

<section class="tint">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Recorrido educativo</span>
      <h2>Dos áreas, un mismo acompañamiento</h2>
      <p class="lede">Parvularia y Primer Grado cuentan con un área propia e independiente, físicamente separada del área de Educación Básica.</p>
    </div>
    <div class="area-split reveal">
      <div class="area-card">
        <img src="img/parvularia/placeholder-1.jpg" alt="Área de Parvularia y Primer Grado" loading="lazy">
        <div class="area-body">
          <h3>Área de Parvularia y Primer Grado</h3>
          <p>Parvularia 4, 5, 6 años y Primer Grado, en un espacio propio pensado para los más pequeños.</p>
          <a href="parvularia.html" class="btn btn-ghost btn-sm">Conocer más</a>
        </div>
      </div>
      <div class="area-card">
        <img src="img/basica/placeholder-1.jpg" alt="Área de Educación Básica" loading="lazy">
        <div class="area-body">
          <h3>Área de Educación Básica</h3>
          <p>Primer, Segundo y Tercer Ciclo (1&deg; a 9&deg; grado), con instalaciones propias para esta etapa.</p>
          <a href="educacion-basica.html" class="btn btn-ghost btn-sm">Conocer más</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="surface">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Momentos que nos unen</span>
      <h2>Nuestra Vida Estudiantil</h2>
      <p class="lede">Banda, cachiporras, actividades pastorales, institucionales y mucho más: así celebramos y crecemos en comunidad.</p>
    </div>
    <div class="grid grid-3 reveal">
      <div class="card">
        <div class="card-media"><img src="img/banda/placeholder-1.jpg" alt="Banda estudiantil" loading="lazy"></div>
        <div class="card-body">
          <span class="tag">Banda</span>
          <h3>Banda de Paz</h3>
          <p>[Agregar descripción real de la Banda de Paz de la institución.]</p>
          <a href="vida-estudiantil.html#banda" class="card-link">Ver más</a>
        </div>
      </div>
      <div class="card">
        <div class="card-media"><img src="img/cachiporras/placeholder-1.jpg" alt="Cachiporras" loading="lazy"></div>
        <div class="card-body">
          <span class="tag tag-vino">Cachiporras</span>
          <h3>Escuadra de Cachiporras</h3>
          <p>[Agregar descripción real del grupo de cachiporras.]</p>
          <a href="vida-estudiantil.html#cachiporras" class="card-link">Ver más</a>
        </div>
      </div>
      <div class="card">
        <div class="card-media"><img src="img/pastorales/placeholder-1.jpg" alt="Actividad pastoral" loading="lazy"></div>
        <div class="card-body">
          <span class="tag tag-oro">Pastoral</span>
          <h3>Actividades pastorales</h3>
          <p>[Agregar descripción real de retiros, eucaristías y celebraciones.]</p>
          <a href="vida-estudiantil.html#pastoral" class="card-link">Ver más</a>
        </div>
      </div>
    </div>
    <div class="text-center" style="margin-top:36px;">
      <a href="eventos.html" class="btn btn-primary">Ver todos los eventos</a>
    </div>
  </div>
</section>
'''.format(lema=LEMA, nombre=NOMBRE, correo=CORREO)
    page("index.html",
         "Inicio | " + NOMBRE,
         "Educación católica de calidad desde Parvularia hasta Noveno Grado en el Distrito de San Luis La Herradura.",
         body)


# =================================================================
# NOSOTROS.HTML
# =================================================================
def gen_nosotros():
    body = page_banner("Acerca de Nosotros",
                        "Conoce la historia, el fundador, la identidad institucional y el modelo educativo del " + NOMBRE + ".",
                        [("Inicio", "index.html"), ("Acerca de Nosotros", None)])
    body += '''
<section class="surface">
  <div class="wrap">
    <div class="section-head reveal">
      <h2>Una institución con historia, fe y propósito</h2>
      <p class="lede">{mision}</p>
    </div>
    <div class="grid grid-4 reveal">
      <div class="card">
        <div class="card-media"><img src="img/institucionales/placeholder-1.jpg" alt="Historia de la institución" loading="lazy"></div>
        <div class="card-body">
          <h3>Historia</h3>
          <p>El camino recorrido por nuestra institución a lo largo de los años.</p>
          <a href="historia.html" class="card-link">Conocer más</a>
        </div>
      </div>
      <div class="card">
        <div class="card-media"><img src="img/fundador/placeholder-retrato.jpg" alt="Fundador de la institución" loading="lazy"></div>
        <div class="card-body">
          <h3>Fundador</h3>
          <p>El legado del Beato Cosme Spessotto, patrono de nuestra comunidad educativa.</p>
          <a href="fundador.html" class="card-link">Conocer más</a>
        </div>
      </div>
      <div class="card">
        <div class="card-media"><img src="img/institucionales/placeholder-2.jpg" alt="Identidad institucional" loading="lazy"></div>
        <div class="card-body">
          <h3>Identidad Institucional</h3>
          <p>Misión, visión, valores y principios que guían nuestro quehacer diario.</p>
          <a href="identidad.html" class="card-link">Conocer más</a>
        </div>
      </div>
      <div class="card">
        <div class="card-media"><img src="img/institucionales/placeholder-3.jpg" alt="Modelo Educativo Integral" loading="lazy"></div>
        <div class="card-body">
          <h3>Modelo Educativo Integral</h3>
          <p>Formación académica, humana, espiritual y psicológica en cada etapa.</p>
          <a href="modelo-educativo.html" class="card-link">Conocer más</a>
        </div>
      </div>
    </div>
  </div>
</section>
'''.format(mision=MISION)
    body += cta_block("&iquest;Quieres conocer m&aacute;s sobre nuestra instituci&oacute;n?",
                       "Escríbenos o visítanos; con gusto resolvemos tus dudas.",
                       ("Contáctanos", "contacto.html"),
                       ("Ver niveles educativos", "niveles-educativos.html"))
    page("nosotros.html", "Acerca de Nosotros | " + NOMBRE,
         "Historia, fundador, identidad institucional y modelo educativo del " + NOMBRE + ".", body)


# =================================================================
# HISTORIA.HTML
# =================================================================
def gen_historia():
    body = page_banner("Historia de la institución",
                        "El recorrido del " + NOMBRE + " a través de los años.",
                        [("Inicio", "index.html"), ("Acerca de Nosotros", "nosotros.html"), ("Historia", None)])
    body += '''
<section class="surface">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Nuestro camino</span>
      <h2>Línea del tiempo institucional</h2>
      <p class="lede">Aquí se documentan los acontecimientos más importantes en la historia del centro escolar. Sustituye cada marcador con fechas, hechos y fotografías reales.</p>
    </div>
    <div class="grid grid-3 reveal">
      <div class="card">
        <div class="card-media"><img src="img/institucionales/placeholder-1.jpg" alt="Fundación de la institución" loading="lazy"></div>
        <div class="card-body">
          <span class="tag">[Año]</span>
          <h3>[Agregar acontecimiento real]</h3>
          <p>[Agregar descripción real del hecho histórico.]</p>
        </div>
      </div>
      <div class="card">
        <div class="card-media"><img src="img/institucionales/placeholder-2.jpg" alt="Crecimiento de la institución" loading="lazy"></div>
        <div class="card-body">
          <span class="tag">[Año]</span>
          <h3>[Agregar acontecimiento real]</h3>
          <p>[Agregar descripción real del hecho histórico.]</p>
        </div>
      </div>
      <div class="card">
        <div class="card-media"><img src="img/institucionales/placeholder-3.jpg" alt="Actualidad de la institución" loading="lazy"></div>
        <div class="card-body">
          <span class="tag">[Año]</span>
          <h3>[Agregar acontecimiento real]</h3>
          <p>[Agregar descripción real del hecho histórico.]</p>
        </div>
      </div>
    </div>
    <p class="placeholder-note reveal">Esta sección utiliza marcadores de posición porque no se proporcionaron fechas ni hechos históricos reales. Para agregar más eventos, copia una de las tarjetas dentro de <code>&lt;div class="grid grid-3"&gt;</code> en <code>historia.html</code>.</p>
  </div>
</section>
'''
    body += cta_block("Conoce a nuestro fundador", "Descubre el legado que inspira nuestra labor educativa.",
                       ("Ver fundador", "fundador.html"), ("Volver a Nosotros", "nosotros.html"))
    page("historia.html", "Historia | " + NOMBRE,
         "Línea de tiempo con los acontecimientos históricos del " + NOMBRE + ".", body)


# =================================================================
# FUNDADOR.HTML
# =================================================================
def gen_fundador():
    body = page_banner("Fundador",
                        "Beato Cosme Spessotto, sacerdote franciscano y patrono de nuestra comunidad educativa.",
                        [("Inicio", "index.html"), ("Acerca de Nosotros", "nosotros.html"), ("Fundador", None)])
    body += '''
<section class="surface">
  <div class="wrap split-panel reveal">
    <div class="panel" style="grid-column: span 1;">
      <img src="img/fundador/placeholder-retrato.jpg" alt="Retrato del Beato Cosme Spessotto" loading="lazy" style="aspect-ratio:3/4;">
    </div>
    <div class="panel">
      <div class="panel-body">
        <span class="eyebrow">Patrono de la institución</span>
        <h2>Beato Cosme Spessotto, OFM</h2>
        <p>Nuestra institución lleva el nombre del Beato Cosme Spessotto, sacerdote franciscano nacido en Italia en 1923, quien llegó a El Salvador como misionero en 1950. Sirvió durante casi tres décadas como párroco de San Juan Nonualco, en el departamento de La Paz, donde fundó una escuela parroquial y acompañó a la comunidad con entrega y sencillez.</p>
        <p>Fue asesinado el 14 de junio de 1980 mientras oraba en su parroquia, en el contexto del conflicto que vivía El Salvador. La Iglesia Católica lo declaró beato el 22 de enero de 2022, reconociendo su martirio en defensa de la fe y de su comunidad.</p>
        <p class="placeholder-note">[Agregar aquí la relación específica entre el Beato Cosme Spessotto y la fundación de esta institución educativa, así como cualquier frase real que se desee destacar.]</p>
      </div>
    </div>
  </div>
</section>

<section class="tint">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Su legado</span>
      <h2>Un espíritu que sigue formando</h2>
    </div>
    <div class="grid grid-3 reveal">
      <div class="card">
        <div class="card-body">
          <span class="tag tag-oro">Servicio</span>
          <h3>Entrega humilde</h3>
          <p>Su cercanía con las familias más sencillas inspira nuestro trato cotidiano con cada estudiante.</p>
        </div>
      </div>
      <div class="card">
        <div class="card-body">
          <span class="tag tag-oro">Fe</span>
          <h3>Identidad franciscana</h3>
          <p>El carisma franciscano orienta la formación espiritual que ofrecemos desde Parvularia hasta Noveno Grado.</p>
        </div>
      </div>
      <div class="card">
        <div class="card-body">
          <span class="tag tag-oro">Comunidad</span>
          <h3>Compromiso local</h3>
          <p>Su vínculo con la comunidad de La Paz refleja la cercanía que buscamos con las familias del distrito.</p>
        </div>
      </div>
    </div>
  </div>
</section>
'''
    body += cta_block("Descubre nuestra identidad institucional", "Misión, visión y valores que heredan este mismo espíritu.",
                       ("Ver identidad institucional", "identidad.html"))
    page("fundador.html", "Fundador | " + NOMBRE,
         "Conoce al Beato Cosme Spessotto, patrono y fundador espiritual de la institución.", body)


# =================================================================
# IDENTIDAD.HTML
# =================================================================
def gen_identidad():
    body = page_banner("Identidad Institucional",
                        "Misión, visión, valores y principios del " + NOMBRE + ".",
                        [("Inicio", "index.html"), ("Acerca de Nosotros", "nosotros.html"), ("Identidad Institucional", None)])
    body += '''
<section class="surface">
  <div class="wrap grid grid-2 reveal">
    <div class="card">
      <div class="card-body">
        <span class="tag">Misión</span>
        <p style="color:var(--color-text); font-size:1.05rem;">{mision}</p>
      </div>
    </div>
    <div class="card">
      <div class="card-body">
        <span class="tag tag-vino">Visión</span>
        <p style="color:var(--color-text); font-size:1.05rem;">{vision}</p>
      </div>
    </div>
  </div>
</section>

<section class="tint">
  <div class="wrap">
    <div class="section-head center reveal">
      <span class="eyebrow">Lo que nos identifica</span>
      <h2>Nuestros valores</h2>
      <p class="lede">Estos valores pueden ampliarse con el tiempo; agrega nuevas tarjetas siguiendo la misma estructura.</p>
    </div>
    <div class="grid grid-4 reveal">
      <div class="card"><div class="card-body"><span style="font-size:1.8rem;">&#10084;</span><h3>Caridad</h3><p>Servicio y cercanía inspirados en el espíritu franciscano.</p></div></div>
      <div class="card"><div class="card-body"><span style="font-size:1.8rem;">&#9997;</span><h3>Excelencia académica</h3><p>Formación rigurosa en cada nivel educativo.</p></div></div>
      <div class="card"><div class="card-body"><span style="font-size:1.8rem;">&#128330;</span><h3>Fe cristiana</h3><p>Vida sacramental y formación religiosa constante.</p></div></div>
      <div class="card"><div class="card-body"><span style="font-size:1.8rem;">&#129309;</span><h3>Fraternidad</h3><p>&ldquo;{lema}&rdquo;, vivida en el trato diario.</p></div></div>
    </div>
    <p class="placeholder-note reveal">[Agregar o modificar los valores institucionales reales, así como la filosofía y los principios específicos de la institución.]</p>
  </div>
</section>

<section class="surface">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Espíritu franciscano</span>
      <h2>Filosofía institucional</h2>
    </div>
    <p class="reveal">[Agregar aquí la filosofía institucional completa: principios pedagógicos, enfoque católico y franciscano, y la forma en que se traduce en la vida diaria del centro escolar.]</p>
  </div>
</section>
'''.format(mision=MISION, vision=VISION, lema=LEMA)
    body += cta_block("Conoce el Modelo Educativo Integral", "Así llevamos esta identidad al aula, todos los días.",
                       ("Ver modelo educativo", "modelo-educativo.html"))
    page("identidad.html", "Identidad Institucional | " + NOMBRE,
         "Misión, visión y valores del " + NOMBRE + ".", body)


# =================================================================
# MODELO-EDUCATIVO.HTML (acordeón interactivo)
# =================================================================
MODELO_ITEMS = [
    ("&#128172;", "Inglés", "Desde Parvularia hasta Noveno Grado",
     "La institución imparte clases de inglés desde Parvularia hasta Noveno Grado, desarrollando progresivamente las competencias de comprensión y comunicación en este idioma."),
    ("&#128187;", "Informática", "Competencias tecnológicas",
     "Los estudiantes reciben formación en informática y competencias tecnológicas como parte de su preparación para los desafíos del mundo actual."),
    ("&#9995;", "Religión y formación en la fe", "Desde Parvularia hasta Noveno Grado",
     "La materia de Religión forma parte de la formación integral desde Parvularia hasta Noveno Grado, de acuerdo con la identidad católica de la institución."),
    ("&#128172;".replace("128172","129504"), "Apoyo Psicológico", "Acompañamiento a estudiantes",
     "La institución brinda acompañamiento y apoyo psicológico para los estudiantes desde Parvularia hasta Noveno Grado."),
    ("&#128218;", "Formación académica", "Excelencia en cada nivel",
     "[Agregar información específica sobre el enfoque académico, metodologías y logros de la institución.]"),
    ("&#128101;", "Formación humana", "Desarrollo de la persona",
     "[Agregar información específica sobre el acompañamiento en el desarrollo humano y social de los estudiantes.]"),
    ("&#127775;", "Formación en valores", "Vida cristiana cotidiana",
     "[Agregar información específica sobre cómo se trabajan los valores institucionales en el día a día.]"),
    ("&#127912;", "Desarrollo artístico y cultural", "Banda, cachiporras y más",
     "[Agregar información específica sobre las actividades artísticas y culturales, como la Banda de Paz y las Cachiporras.]"),
    ("&#9917;", "Actividad física y deportiva", "Educación física",
     "[Agregar información específica sobre la clase de educación física y las actividades deportivas disponibles.]"),
]


def gen_modelo_educativo():
    body = page_banner("Modelo Educativo Integral",
                        "Formación académica, humana, espiritual y psicológica en cada etapa del recorrido escolar.",
                        [("Inicio", "index.html"), ("Acerca de Nosotros", "nosotros.html"), ("Modelo Educativo Integral", None)])
    body += '''
<section class="surface">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Nuestra propuesta educativa</span>
      <h2>Una formación integral, área por área</h2>
      <p class="lede">El Modelo Educativo Integral articula la formación académica con la humana, la espiritual y el acompañamiento psicológico. Haz clic en cada área para conocer más.</p>
    </div>
    <div class="accordion-grid reveal">
'''
    for i, (icon, name, short, desc) in enumerate(MODELO_ITEMS):
        panel_id = "modelo-panel-{}".format(i + 1)
        body += '''      <div class="accordion-item">
        <h3 style="margin:0;">
        <button class="accordion-trigger" type="button" aria-expanded="false" aria-controls="{pid}">
          <span class="acc-icon" aria-hidden="true">{icon}</span>
          <span class="acc-title"><strong>{name}</strong><span>{short}</span></span>
          <span class="acc-toggle" aria-hidden="true">+</span>
        </button>
        </h3>
        <div class="accordion-panel" id="{pid}">
          <div class="accordion-panel-inner"><p>{desc}</p></div>
        </div>
      </div>
'''.format(pid=panel_id, icon=icon, name=name, short=short, desc=desc)
    body += '''    </div>
  </div>
</section>
'''
    body += cta_block("Conoce cómo acompañamos cada etapa educativa", "Descubre los niveles educativos, desde Parvularia hasta Noveno Grado.",
                       ("Ver niveles educativos", "niveles-educativos.html"), ("Contáctanos", "contacto.html"))
    page("modelo-educativo.html", "Modelo Educativo Integral | " + NOMBRE,
         "Áreas de formación del Modelo Educativo Integral: inglés, informática, religión, apoyo psicológico y más.", body)


# =================================================================
# NIVELES-EDUCATIVOS.HTML
# =================================================================
def gen_niveles_educativos():
    body = page_banner("Niveles Educativos",
                        "El recorrido educativo completo, desde Parvularia 4 años hasta Noveno Grado.",
                        [("Inicio", "index.html"), ("Niveles Educativos", None)])
    body += '''
<section class="surface">
  <div class="wrap">
    <div class="section-head center reveal">
      <span class="eyebrow">Un recorrido continuo</span>
      <h2>De Parvularia 4 a Noveno Grado</h2>
      <p class="lede">Cada etapa acompaña el crecimiento académico, humano y espiritual de los estudiantes.</p>
    </div>
    <div class="level-path reveal">
      <div class="level-stop"><h4>Parvularia 4, 5 y 6</h4><p>Primeros pasos en la formación integral.</p></div>
      <div class="level-stop"><h4>Primer Grado</h4><p>Inicio de la Educación Básica, en el área de Parvularia.</p></div>
      <div class="level-stop"><h4>Primer Ciclo</h4><p>1&deg;, 2&deg; y 3&deg; grado.</p></div>
      <div class="level-stop"><h4>Segundo Ciclo</h4><p>4&deg;, 5&deg; y 6&deg; grado.</p></div>
    </div>
    <div class="level-path reveal" style="margin-top:18px; grid-template-columns: repeat(1, 1fr); max-width:280px; margin-left:auto; margin-right:auto;">
      <div class="level-stop"><h4>Tercer Ciclo</h4><p>7&deg;, 8&deg; y 9&deg; grado.</p></div>
    </div>
  </div>
</section>

<section class="tint">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Dos áreas físicas</span>
      <h2>Espacios propios para cada etapa</h2>
      <p class="lede">Parvularia y Primer Grado cuentan con un área propia e independiente, físicamente separada del área de Educación Básica.</p>
    </div>
    <div class="area-split reveal">
      <div class="area-card">
        <img src="img/parvularia/placeholder-2.jpg" alt="Área de Parvularia y Primer Grado" loading="lazy">
        <div class="area-body">
          <h3>Parvularia y Primer Grado</h3>
          <p>Un espacio diseñado especialmente para los primeros años de formación.</p>
          <a href="parvularia.html" class="btn btn-ghost btn-sm">Conocer más</a>
        </div>
      </div>
      <div class="area-card">
        <img src="img/basica/placeholder-2.jpg" alt="Área de Educación Básica" loading="lazy">
        <div class="area-body">
          <h3>Educación Básica</h3>
          <p>Primer, Segundo y Tercer Ciclo, en instalaciones propias para esta etapa.</p>
          <a href="educacion-basica.html" class="btn btn-ghost btn-sm">Conocer más</a>
        </div>
      </div>
    </div>
  </div>
</section>
'''
    body += cta_block("Conoce cómo acompañamos cada etapa educativa", "Visita en detalle Parvularia o Educación Básica.",
                       ("Parvularia y Primer Grado", "parvularia.html"), ("Educación Básica", "educacion-basica.html"))
    page("niveles-educativos.html", "Niveles Educativos | " + NOMBRE,
         "Recorrido educativo desde Parvularia 4 años hasta Noveno Grado en el " + NOMBRE + ".", body)


# =================================================================
# PARVULARIA.HTML
# =================================================================
def gen_parvularia():
    body = page_banner("Parvularia y Primer Grado",
                        "Un área propia, pensada para los primeros años de formación.",
                        [("Inicio", "index.html"), ("Niveles Educativos", "niveles-educativos.html"), ("Parvularia", None)])
    body += '''
<section class="surface">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Área independiente</span>
      <h2>Un espacio propio para Parvularia y Primer Grado</h2>
      <p class="lede">Parvularia y Primer Grado disponen de un área propia, separada físicamente del área de Educación Básica, pensada para acompañar de cerca esta primera etapa.</p>
    </div>
    <div class="grid grid-4 reveal">
      <div class="card"><div class="card-body"><span class="tag">Nivel</span><h3>Parvularia 4</h3><p>Primer año del nivel de Parvularia.</p></div></div>
      <div class="card"><div class="card-body"><span class="tag">Nivel</span><h3>Parvularia 5</h3><p>Segundo año del nivel de Parvularia.</p></div></div>
      <div class="card"><div class="card-body"><span class="tag">Nivel</span><h3>Parvularia 6</h3><p>Tercer año del nivel de Parvularia.</p></div></div>
      <div class="card"><div class="card-body"><span class="tag tag-vino">Nivel</span><h3>Primer Grado</h3><p>Inicio de la Educación Básica, dentro de esta misma área.</p></div></div>
    </div>
  </div>
</section>

<section class="tint">
  <div class="wrap grid grid-2 reveal">
    <div class="card"><div class="card-body">
      <h3>Espacios educativos</h3>
      <p>[Agregar información real sobre las aulas, áreas de juego y espacios específicos del área de Parvularia y Primer Grado.]</p>
    </div></div>
    <div class="card"><div class="card-body">
      <h3>Metodología</h3>
      <p>[Agregar información real sobre la metodología utilizada en esta etapa: juego, estimulación temprana, desarrollo psicomotor, etc.]</p>
    </div></div>
  </div>
</section>

<section class="surface">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Galería</span>
      <h2>Momentos de Parvularia y Primer Grado</h2>
    </div>
''' + carousel_block("Parvularia", [
        ("img/parvularia/placeholder-1.jpg", "Actividades de Parvularia — sustituir por fotografía real"),
        ("img/parvularia/placeholder-2.jpg", "Espacios educativos — sustituir por fotografía real"),
        ("img/parvularia/placeholder-3.jpg", "Primer Grado — sustituir por fotografía real"),
        ("img/basica/placeholder-1.jpg", "Actividades — sustituir por fotografía real"),
    ]) + '''
  </div>
</section>
'''
    body += cta_block("Conoce el siguiente paso: Educación Básica", "Descubre cómo continúa el recorrido educativo desde Primer Ciclo.",
                       ("Ver Educación Básica", "educacion-basica.html"))
    page("parvularia.html", "Parvularia y Primer Grado | " + NOMBRE,
         "Área propia de Parvularia (4, 5 y 6 años) y Primer Grado en el " + NOMBRE + ".", body)


# =================================================================
# EDUCACION-BASICA.HTML
# =================================================================
def gen_educacion_basica():
    body = page_banner("Educación Básica",
                        "Primer, Segundo y Tercer Ciclo: de Primer a Noveno Grado.",
                        [("Inicio", "index.html"), ("Niveles Educativos", "niveles-educativos.html"), ("Educación Básica", None)])
    body += '''
<section class="surface">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Tres ciclos</span>
      <h2>De Primer a Noveno Grado</h2>
      <p class="lede">Primer Grado tiene una mención especial: funciona físicamente dentro del área destinada a Parvularia y Primer Grado.</p>
    </div>
    <div class="grid grid-3 reveal">
      <div class="card">
        <div class="card-media"><img src="img/basica/placeholder-1.jpg" alt="Primer Ciclo" loading="lazy"></div>
        <div class="card-body">
          <span class="tag">Primer Ciclo</span>
          <h3>1&deg;, 2&deg; y 3&deg; grado</h3>
          <p>Primer Grado se imparte físicamente en el área de Parvularia y Primer Grado.</p>
        </div>
      </div>
      <div class="card">
        <div class="card-media"><img src="img/basica/placeholder-2.jpg" alt="Segundo Ciclo" loading="lazy"></div>
        <div class="card-body">
          <span class="tag tag-vino">Segundo Ciclo</span>
          <h3>4&deg;, 5&deg; y 6&deg; grado</h3>
          <p>[Agregar información real sobre esta etapa: metodología, asignaturas destacadas, etc.]</p>
        </div>
      </div>
      <div class="card">
        <div class="card-media"><img src="img/basica/placeholder-3.jpg" alt="Tercer Ciclo" loading="lazy"></div>
        <div class="card-body">
          <span class="tag tag-oro">Tercer Ciclo</span>
          <h3>7&deg;, 8&deg; y 9&deg; grado</h3>
          <p>[Agregar información real sobre esta etapa: orientación vocacional, proyectos finales, etc.]</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="tint">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Instalaciones</span>
      <h2>Espacios para Educación Básica</h2>
    </div>
''' + carousel_block("Educación Básica", [
        ("img/instalaciones/placeholder-1.jpg", "Instalaciones de Educación Básica — sustituir por fotografía real"),
        ("img/instalaciones/placeholder-2.jpg", "Aulas — sustituir por fotografía real"),
        ("img/instalaciones/placeholder-3.jpg", "Espacios comunes — sustituir por fotografía real"),
        ("img/basica/placeholder-1.jpg", "Actividades académicas — sustituir por fotografía real"),
    ]) + '''
  </div>
</section>
'''
    body += cta_block("&iquest;Tienes dudas sobre el proceso educativo?", "Escríbenos y con gusto te orientamos.",
                       ("Contáctanos", "contacto.html"), ("Ver Parvularia", "parvularia.html"))
    page("educacion-basica.html", "Educación Básica | " + NOMBRE,
         "Primer, Segundo y Tercer Ciclo de Educación Básica (1° a 9° grado) en el " + NOMBRE + ".", body)


# =================================================================
# VIDA-ESTUDIANTIL.HTML
# =================================================================
def vida_section(anchor, eyebrow, title, desc, images, tag_class="tag"):
    slides = [(src, cap) for src, cap in images]
    return '''<section id="{anchor}" class="surface">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">{eyebrow}</span>
      <h2>{title}</h2>
      <p class="lede">{desc}</p>
    </div>
    <div class="grid grid-3 reveal" style="margin-bottom:36px;">
      <div class="card">
        <div class="card-media"><img src="{img1}" alt="{title}" loading="lazy"></div>
        <div class="card-body"><span class="{tagclass}">Vida estudiantil</span><h3>Fotografía destacada</h3><p>[Sustituir por fotografía real de {title}.]</p></div>
      </div>
    </div>
    {carousel}
    <div class="section-head reveal" style="margin-top:40px; margin-bottom:16px;">
      <h3>Galería</h3>
    </div>
    <div class="gallery-grid reveal">
      {gallery}
    </div>
  </div>
</section>
'''.format(anchor=anchor, eyebrow=eyebrow, title=title, desc=desc, img1=images[0][0],
           tagclass=tag_class, carousel=carousel_block(title, slides),
           gallery="".join('<button type="button"><img src="{src}" alt="{cap}" loading="lazy"></button>'.format(src=s, cap=c) for s, c in images))


def gen_vida_estudiantil():
    body = page_banner("Vida Estudiantil",
                        "Banda, cachiporras, actividades pastorales e institucionales: así celebramos en comunidad.",
                        [("Inicio", "index.html"), ("Vida Estudiantil", None)])
    body += vida_section(
        "banda", "Formación artística", "Banda", tag_class="tag",
        desc="[Agregar descripción real de la Banda de Paz de la institución: instrumentos, participación en actos cívicos, etc.]",
        images=[
            ("img/banda/placeholder-1.jpg", "Banda — sustituir por fotografía real"),
            ("img/banda/placeholder-2.jpg", "Banda — sustituir por fotografía real"),
            ("img/banda/placeholder-3.jpg", "Banda — sustituir por fotografía real"),
        ])
    body += vida_section(
        "cachiporras", "Formación artística", "Cachiporras", tag_class="tag tag-vino",
        desc="[Agregar descripción real del grupo de cachiporras: presentaciones, participación en desfiles, etc.]",
        images=[
            ("img/cachiporras/placeholder-1.jpg", "Cachiporras — sustituir por fotografía real"),
            ("img/cachiporras/placeholder-2.jpg", "Cachiporras — sustituir por fotografía real"),
            ("img/cachiporras/placeholder-3.jpg", "Cachiporras — sustituir por fotografía real"),
        ])
    body = body.replace('<section id="cachiporras" class="surface">', '<section id="cachiporras" class="tint">')
    body += vida_section(
        "pastoral", "Vida cristiana", "Actividades Pastorales", tag_class="tag tag-oro",
        desc="[Agregar descripción real de retiros, eucaristías, celebraciones y actividades pastorales del centro escolar.]",
        images=[
            ("img/pastorales/placeholder-1.jpg", "Actividad pastoral — sustituir por fotografía real"),
            ("img/pastorales/placeholder-2.jpg", "Actividad pastoral — sustituir por fotografía real"),
            ("img/pastorales/placeholder-3.jpg", "Actividad pastoral — sustituir por fotografía real"),
        ])
    body += vida_section(
        "institucional", "Comunidad escolar", "Actividades Institucionales", tag_class="tag",
        desc="[Agregar descripción real de actos cívicos, celebraciones, actividades académicas, culturales y recreativas.]",
        images=[
            ("img/institucionales/placeholder-1.jpg", "Actividad institucional — sustituir por fotografía real"),
            ("img/institucionales/placeholder-2.jpg", "Actividad institucional — sustituir por fotografía real"),
            ("img/institucionales/placeholder-3.jpg", "Actividad institucional — sustituir por fotografía real"),
        ])
    body = body.replace('<section id="institucional" class="surface">', '<section id="institucional" class="tint">', 1)
    body += cta_block("&iquest;Quieres ver todos nuestros eventos?", "Filtra por categoría y descubre cada actividad.",
                       ("Ver todos los eventos", "eventos.html"))
    page("vida-estudiantil.html", "Vida Estudiantil | " + NOMBRE,
         "Banda, cachiporras, actividades pastorales e institucionales del " + NOMBRE + ".", body)


# =================================================================
# EVENTOS.HTML
# =================================================================
EVENTOS = [
    ("banda", "Banda", "img/banda/placeholder-1.jpg", "Presentación de la Banda de Paz", "[Fecha]", "[Agregar descripción real del evento.]"),
    ("cachiporras", "Cachiporras", "img/cachiporras/placeholder-1.jpg", "Presentación de Cachiporras", "[Fecha]", "[Agregar descripción real del evento.]"),
    ("pastoral", "Pastoral", "img/pastorales/placeholder-1.jpg", "Retiro espiritual", "[Fecha]", "[Agregar descripción real del evento.]"),
    ("institucional", "Institucional", "img/institucionales/placeholder-1.jpg", "Acto cívico institucional", "[Fecha]", "[Agregar descripción real del evento.]"),
    ("academico", "Académico", "img/basica/placeholder-1.jpg", "Feria académica", "[Fecha]", "[Agregar descripción real del evento.]"),
    ("cultural", "Cultural", "img/institucionales/placeholder-2.jpg", "Celebración cultural", "[Fecha]", "[Agregar descripción real del evento.]"),
    ("deportivo", "Deportivo", "img/instalaciones/placeholder-1.jpg", "Jornada deportiva", "[Fecha]", "[Agregar descripción real del evento.]"),
    ("pastoral", "Pastoral", "img/pastorales/placeholder-2.jpg", "Eucaristía de acción de gracias", "[Fecha]", "[Agregar descripción real del evento.]"),
    ("institucional", "Institucional", "img/institucionales/placeholder-3.jpg", "Graduación", "[Fecha]", "[Agregar descripción real del evento.]"),
]

FILTER_CATS = [("todos", "Todos"), ("banda", "Banda"), ("cachiporras", "Cachiporras"),
               ("pastoral", "Pastoral"), ("institucional", "Institucional"),
               ("academico", "Académico"), ("cultural", "Cultural"), ("deportivo", "Deportivo")]

TAG_CLASS_BY_CAT = {"pastoral": "tag tag-oro", "cachiporras": "tag tag-vino"}


def gen_eventos():
    body = page_banner("Eventos",
                        "Explora nuestras actividades por categoría: banda, cachiporras, pastoral, institucional y más.",
                        [("Inicio", "index.html"), ("Vida Estudiantil", "vida-estudiantil.html"), ("Eventos", None)])
    filters = "".join(
        '<button class="filter-btn" type="button" data-filter="{key}" aria-pressed="{pressed}">{label}</button>'.format(
            key=k, label=l, pressed="true" if k == "todos" else "false") for k, l in FILTER_CATS)
    cards = ""
    for cat, label, img, title, fecha, desc in EVENTOS:
        tagclass = TAG_CLASS_BY_CAT.get(cat, "tag")
        cards += '''<article class="card event-card" data-category="{cat}">
        <div class="card-media"><img src="{img}" alt="{title}" loading="lazy"></div>
        <div class="card-body">
          <div class="card-meta"><span class="{tagclass}">{label}</span><span>{fecha}</span></div>
          <h3>{title}</h3>
          <p>{desc}</p>
          <a href="vida-estudiantil.html" class="card-link">Ver galería</a>
        </div>
      </article>
      '''.format(cat=cat, img=img, title=title, tagclass=tagclass, label=label, fecha=fecha, desc=desc)

    body += '''
<section class="surface">
  <div class="wrap">
    <div class="filter-bar reveal" role="group" aria-label="Filtrar eventos por categoría">
      {filters}
    </div>
    <div class="events-grid reveal">
      {cards}
    </div>
    <p class="empty-state">No hay eventos en esta categoría todavía. [Agregar nuevos eventos editando <code>eventos.html</code>.]</p>
  </div>
</section>
'''.format(filters=filters, cards=cards)
    body += cta_block("&iquest;Vives un momento que merece estar aquí?", "Cuéntanos sobre tu evento o actividad.",
                       ("Contáctanos", "contacto.html"))
    page("eventos.html", "Eventos | " + NOMBRE,
         "Calendario y galería de eventos del " + NOMBRE + ", filtrables por categoría.", body)


# =================================================================
# CONTACTO.HTML
# =================================================================
def gen_contacto():
    body = page_banner("Contáctanos",
                        "Escríbenos, llámanos o visítanos. Con gusto atenderemos tus dudas.",
                        [("Inicio", "index.html"), ("Contáctanos", None)])
    body += '''
<section class="surface">
  <div class="wrap contact-layout">
    <div class="info-card reveal">
      <h2>Información de contacto</h2>
      <div class="info-row">
        <span class="ic" aria-hidden="true">&#127963;</span>
        <div><strong>Institución</strong><span>{nombre}</span></div>
      </div>
      <div class="info-row">
        <span class="ic" aria-hidden="true">&#128205;</span>
        <div><strong>Dirección</strong><span>{direccion}</span></div>
      </div>
      <div class="info-row">
        <span class="ic" aria-hidden="true">&#128222;</span>
        <div><strong>Teléfono</strong><a href="{tel_href}">{telefono}</a></div>
      </div>
      <div class="info-row">
        <span class="ic" aria-hidden="true">&#9993;</span>
        <div><strong>Correo electrónico</strong><a href="mailto:{correo}">{correo}</a></div>
      </div>
      <div class="info-row">
        <span class="ic" aria-hidden="true">&#128337;</span>
        <div><strong>Horario</strong><span>[Agregar horario real]</span></div>
      </div>
      <div class="info-row">
        <span class="ic" aria-hidden="true">&#128247;</span>
        <div>
          <strong>Redes sociales</strong>
          <div class="social-row">
            <!-- Reemplazar por el enlace oficial de Facebook -->
            <a href="#" aria-label="Facebook" target="_blank" rel="noopener">f</a>
            <!-- Agregar aquí otras redes sociales disponibles -->
          </div>
        </div>
      </div>
      <div class="map-embed">
        <iframe src="{maps_src}" title="Ubicación del {nombre_corto}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
      </div>
    </div>

    <div class="form-card reveal">
      <h2>Envíanos un mensaje</h2>
      <p class="lede" style="margin-bottom:24px;">Completa el formulario y te responderemos a la brevedad.</p>
      <form id="formContacto" novalidate>
        <div class="form-grid">
          <div class="form-field">
            <label for="nombre">Nombre completo</label>
            <input type="text" id="nombre" name="nombre" required>
            <span class="field-error" role="alert"></span>
          </div>
          <div class="form-field">
            <label for="correo">Correo electrónico</label>
            <input type="email" id="correo" name="correo" required>
            <span class="field-error" role="alert"></span>
          </div>
          <div class="form-field">
            <label for="telefono">Teléfono (opcional)</label>
            <input type="tel" id="telefono" name="telefono">
            <span class="field-error" role="alert"></span>
          </div>
          <div class="form-field">
            <label for="asunto">Asunto</label>
            <input type="text" id="asunto" name="asunto" required>
            <span class="field-error" role="alert"></span>
          </div>
          <div class="form-field full">
            <label for="mensaje">Mensaje</label>
            <textarea id="mensaje" name="mensaje" required></textarea>
            <span class="field-error" role="alert"></span>
          </div>
        </div>
        <button type="submit" class="btn btn-primary">Enviar mensaje</button>
        <p class="form-status" id="formStatus" role="status"></p>
        <!-- Este formulario aún no envía datos a un backend real.
             Ver js/main.js para instrucciones de cómo conectar
             Formspree, EmailJS o un backend propio. -->
      </form>
    </div>
  </div>
</section>
'''.format(nombre=NOMBRE, nombre_corto=NOMBRE_CORTO, direccion=DIRECCION, tel_href=TELEFONO_HREF,
           telefono=TELEFONO, correo=CORREO, maps_src=MAPS_EMBED_SRC)
    page("contacto.html", "Contáctanos | " + NOMBRE,
         "Dirección, teléfono, correo y formulario de contacto del " + NOMBRE + ".", body)


# =================================================================
# EJECUCIÓN
# =================================================================
if __name__ == "__main__":
    gen_index()
    gen_nosotros()
    gen_historia()
    gen_fundador()
    gen_identidad()
    gen_modelo_educativo()
    gen_niveles_educativos()
    gen_parvularia()
    gen_educacion_basica()
    gen_vida_estudiantil()
    gen_eventos()
    gen_contacto()
    print("Sitio generado en", OUT)
