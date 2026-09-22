# Sitio web — Centro Escolar Católico "Fray Cosme Spessotto"

Rediseño completo, multipágina, en HTML5 + CSS3 + JavaScript vanilla (sin frameworks).
Pensado para editarse fácilmente en Visual Studio Code y publicarse en GitHub Pages
o cualquier hosting convencional.

## 1. Estructura del proyecto

```
/index.html                 Inicio
/nosotros.html               Acerca de Nosotros (resumen con enlaces)
/historia.html                Historia
/fundador.html                 Fundador (Beato Cosme Spessotto)
/identidad.html                 Identidad Institucional (Misión, Visión, Valores)
/modelo-educativo.html           Modelo Educativo Integral (acordeón)
/niveles-educativos.html          Recorrido educativo general
/parvularia.html                   Parvularia y Primer Grado
/educacion-basica.html               Educación Básica (1° a 9°)
/vida-estudiantil.html                 Banda, Cachiporras, Pastoral, Institucional
/eventos.html                            Eventos con filtros por categoría
/contacto.html                            Datos de contacto, mapa y formulario

/css/styles.css      Hoja de estilos principal (variables, componentes)
/css/responsive.css  Ajustes de cuadrícula/espaciado por punto de quiebre
/js/main.js          Menú móvil, acordeón, filtros, formulario, año automático, "volver arriba"
/js/carousel.js      Componente de carrusel reutilizable (flechas, puntos, swipe, teclado)
/js/gallery.js       Lightbox (galería ampliada) en JavaScript vanilla

/img/logo/            Escudo institucional
/img/inicio/            Fotografía del hero
/img/eventos/             Fotografías genéricas de eventos
/img/banda/, /cachiporras/, /pastorales/, /institucionales/,
/img/parvularia/, /basica/, /instalaciones/, /fundador/
```

**Todas las imágenes actuales son marcadores de posición** reutilizados del
proyecto original (indicados con el texto "reemplaza esta imagen" o similar).
Sustitúyelas por fotografías reales manteniendo el mismo nombre de archivo,
o agrega nuevas y actualiza la ruta en el HTML.

## 2. Cómo cambiar textos

Todo el texto vive directamente en cada archivo `.html`. Abre el archivo con
VS Code, busca el texto (Ctrl+F) y edítalo. Los textos que aún no tienen
información real están marcados así: `[Agregar información aquí]`.
Búscalos con Ctrl+Shift+F en todo el proyecto para encontrarlos todos.

Los datos institucionales reales ya incorporados son:
- Dirección: Km 60 Barrio Guadalupe, Distrito de San Luis La Herradura
- Teléfono: 2355-8959
- Correo: parroquialcosmespessotto@gmail.com
- Misión, Visión y el lema "Formar para construir un mundo fraterno"

## 3. Cómo cambiar fotografías

1. Copia tu fotografía dentro de la carpeta correspondiente en `/img/`.
2. Reemplaza el archivo existente (mismo nombre) **o** usa un nombre nuevo.
3. Si usaste un nombre nuevo, actualiza el atributo `src="img/..."` en el
   HTML correspondiente.
4. Escribe siempre un `alt="..."` descriptivo de la fotografía (accesibilidad y SEO).

## 4. Cómo agregar una fotografía a un carrusel

Busca el bloque `<div class="carousel" data-carousel>` en la página deseada
(por ejemplo `parvularia.html` o `educacion-basica.html`) y copia uno de los
`<div class="carousel-slide">` existentes, cambiando la imagen y el texto:

```html
<div class="carousel-slide">
  <figure><img src="img/parvularia/tu-foto.jpg" alt="Descripción de la foto" loading="lazy" data-lightbox></figure>
  <figcaption>Descripción breve</figcaption>
</div>
```

No es necesario tocar el JavaScript: `js/carousel.js` detecta automáticamente
cualquier `data-carousel` en la página.

## 5. Cómo agregar un nuevo evento

Abre `eventos.html` y copia una tarjeta `<article class="card event-card" ...>`
completa, cambiando:
- `data-category="..."` (debe coincidir con una de las categorías del filtro:
  `banda`, `cachiporras`, `pastoral`, `institucional`, `academico`, `cultural`, `deportivo`)
- la imagen, el título, la fecha y la descripción.

Los botones de filtro ya existentes detectarán automáticamente la nueva tarjeta.

## 6. Cómo agregar una nueva tarjeta al Modelo Educativo

Abre `modelo-educativo.html` y copia un bloque `<div class="accordion-item">`
completo (incluye el botón y el panel), asignando un `id` único al panel
(por ejemplo `modelo-panel-10`) y repitiéndolo en el atributo
`aria-controls` del botón correspondiente.

## 7. Cómo modificar los colores institucionales

Todos los colores del sitio están centralizados como variables CSS al inicio
de `css/styles.css`:

```css
:root{
  --color-primary: #1E4B8F;     /* azul institucional */
  --color-secondary: #7A1F2B;   /* vino franciscano */
  --color-accent: #F0A93A;      /* dorado */
  --color-background: #FBF9F5;
  --color-text: #1B2333;
}
```

Cambia estos valores y el color se actualizará automáticamente en todo el sitio.

## 8. Cómo actualizar teléfono, dirección y redes sociales

Estos datos aparecen en el encabezado, el pie de página y `contacto.html`.
Para no editarlos uno por uno si vuelves a generar el sitio con el script
`build_site.py`, edita las constantes al inicio del archivo (`TELEFONO`,
`DIRECCION`, `CORREO`, etc.) y vuelve a ejecutarlo con `python3 build_site.py`.
Si prefieres editar directamente el HTML, busca esos mismos datos con
Ctrl+Shift+F en todo el proyecto.

Para las redes sociales, busca los comentarios:
```html
<!-- Reemplazar por el enlace oficial de Facebook -->
```
en el pie de página y en `contacto.html`, y coloca el enlace real.

Para el botón flotante de WhatsApp, busca en cada archivo:
```html
<!-- Botón flotante de WhatsApp: reemplazar NUMERO_WHATSAPP por el número oficial -->
```
y sustituye `NUMERO_WHATSAPP` por el número completo con código de país
(ejemplo: `503XXXXXXXX`, sin signos ni espacios).

## 9. El formulario de contacto

El formulario de `contacto.html` valida los campos en el navegador
(nombre, correo, asunto, mensaje), pero **todavía no envía los mensajes a
ningún lugar** porque no tiene backend. Para conectarlo, abre `js/main.js`,
busca la función `initContactForm` y sigue las instrucciones que están
comentadas ahí mismo para usar Formspree, EmailJS o un backend propio.

## 10. Cómo publicar el sitio en GitHub Pages

1. Crea un repositorio nuevo en GitHub (por ejemplo `sitio-fray-cosme-spessotto`).
2. Sube todo el contenido de esta carpeta (todos los `.html`, más `css/`, `js/` e `img/`)
   a la raíz del repositorio.
3. Entra a **Settings → Pages** del repositorio.
4. En "Source", selecciona la rama `main` (o `master`) y la carpeta `/ (root)`.
5. Guarda los cambios. GitHub mostrará la URL pública en unos minutos
   (algo como `https://tuusuario.github.io/sitio-fray-cosme-spessotto/`).
6. `index.html` debe permanecer con ese nombre exacto: es la página que
   GitHub Pages carga por defecto.

## 11. Notas técnicas

- El sitio funciona sin frameworks: solo HTML5, CSS3 y JavaScript vanilla.
- Las fuentes (Fraunces + Karla) se cargan desde Google Fonts; si el sitio
  se aloja sin conexión a internet, descárgalas y sírvelas localmente.
- El contenido principal (textos, tarjetas, formulario) permanece visible y
  usable incluso si JavaScript está desactivado; solo se pierden las
  animaciones, el carrusel, el acordeón interactivo, el menú móvil y la
  validación del formulario.
- Los carruseles y galerías con `data-lightbox` amplían las fotos en un
  modal accesible (cierra con la X, con Escape, o navega con las flechas
  del teclado y deslizando en pantallas táctiles).
- `build_site.py` (en la carpeta raíz del proyecto entregado, fuera de esta
  carpeta del sitio) es el script que generó estas páginas a partir de
  plantillas compartidas. No es necesario para publicar el sitio, pero es
  útil si prefieres regenerar todas las páginas después de cambiar datos
  institucionales centralizados (como el teléfono o la dirección) en un
  solo lugar.
