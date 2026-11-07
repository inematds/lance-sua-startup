# Prompt de lanzamiento — pégalo en tu agente

Úsalo con **Claude Code** abierto en la carpeta de este kit y con la extensión **Claude in Chrome** activada (el agente
controla tu navegador). También sirve para otro agente que lea archivos y controle el navegador.

Antes de pegarlo:

1. Abre en el navegador el **correo de registro** (una casilla solo para esto, ej.: `lancamento@suamarca.com`),
   con la sesión iniciada. Ahí llegan los enlaces de confirmación.
2. Deja los archivos de la marca (logo 512×512, 1 a 3 capturas de pantalla) dentro de la carpeta `marca/`.

Copia todo lo que está entre las líneas `---` y pégalo en el agente.

---

Vas a lanzar mi startup en sitios de lanzamiento y directorios, usando el kit de esta carpeta.
Trabaja en 4 fases y **no te saltes ningún punto de aprobación**.

**Antes que nada — revisa tus herramientas.** Fíjate si puedes abrir sitios, llenar formularios y leer mi
casilla de correo de registro. Si algo no está disponible, dime exactamente qué y sigue con lo que se pueda
hacer. Nunca digas que enviaste, abriste o confirmaste algo que no lograste hacer.

**Fase 1 — Entrevista y ficha de la marca.**
Copia `marca/marca.modelo.json` a `marca/marca.json` (si todavía no existe). Lee mi sitio
(la dirección que te pase) y entrevístame, **una pregunta a la vez**, para llenar cada campo.
Pide también: logo cuadrado y logo horizontal (con el nombre), 3 a 5 capturas de pantalla, el tono de voz, los colores,
la fecha de lanzamiento y un correo público de contacto.
Reglas de la ficha:
- Pon `"idioma": "es"` en la ficha (así el plan da prioridad a los sitios de América Latina).
- `tagline` hasta 60 caracteres; `descricao_curta` hasta 160; `descricao_longa` hasta 1000.
- En `numeros`, solo números reales que yo confirme, siempre con la `fonte`. Si no tengo números, la lista queda vacía.
  Nunca escribas "miles de usuarios", "líder del mercado" o algo parecido sin fuente.
- Pregunta el `orcamento_usd` (por defecto 0 = solo gratis) y si `aceita_selo` (poner un sello del directorio en mi
  sitio; por defecto false).
- Escribe los textos en el idioma de cada sitio (la mayoría está en inglés): prepara `tagline`, `descricao_curta` y
  `descricao_longa` también en inglés, en un bloque `"en": {...}` dentro de la ficha. Además, puedes agregar un bloque
  `"es": {...}` con `tagline`, `descricao_curta` y `descricao_longa` en español para los sitios en español.
Cuando termines, ejecuta `python3 lancar.py checa` y corrige hasta que dé `ficha OK`.
**Punto de aprobación 1:** muéstrame la ficha completa y espera a que escriba `ficha aprobada`.

**Fase 2 — Plan.**
Ejecuta `python3 lancar.py plano`. Después, para cada sitio de los grupos A y B, busca si mi producto ya está listado
(el buscador del propio sitio o `site:<dominio> <nombre del producto>`); si lo está, márcalo
`python3 lancar.py marca <id> ja-listado --link "<dirección>"`. Lee `trabalho/plano.md` y muéstrame un resumen: cuántos sitios hay en cada
grupo (A = lo haces tú solo, B = pide mi sí, C = mi turno, D = fuera del plan) y los 10 primeros del grupo A.
**Punto de aprobación 2:** espera a que escriba `plan aprobado`.

**Fase 3 — Envío, un sitio a la vez, en el orden del grupo A.**
Para cada sitio:
1. Abre el `url_envio` del rastreador (`trabalho/rastreador.csv`).
2. Crea la cuenta con el `email_cadastro` (si el sitio pide cuenta) y llena el formulario **solo con datos de la ficha**.
   Envía logo, capturas y enlaces cuando el sitio los pida.
3. Si llega un correo de confirmación, abre la casilla de correo en la otra pestaña y haz clic en el enlace.
4. Actualiza el rastreador:
   `python3 lancar.py marca <id> enviado --link "<dirección del listado, si ya existe>" --comprovante "<asunto del correo de confirmación, número de pedido o nombre de la captura>" --nota "<qué pasó>"`
   (usa `aguardando-email` si falta confirmar, `recusado` si el sitio lo rechazó).
   Solo cuéntalo como **publicado** después de abrir la página publicada y ver el enlace a mi sitio.

**Detente y llámame** (marca `sua-vez` con el motivo y pasa al siguiente sitio) cuando aparezca:
- cualquier cobro, plan pago, "boost", fila paga o tarjeta — **aunque sea US$ 1**;
- pedido de sello, badge o enlace de vuelta en mi sitio;
- captcha, verificación por teléfono, documento, video o llamada;
- una pregunta que la ficha no responde (no inventes la respuesta);
- términos de uso que pidan algo más que crear una cuenta y listar el producto (ej.: exclusividad, cesión de derechos).

Nunca: pagar; cambiar mi sitio; publicar en comunidades con mi cuenta personal; enviar el mismo producto dos
veces al mismo sitio; usar otro correo que no sea el `email_cadastro`.

**Fase 4 — Grupo B e informe.**
Para cada sitio del grupo B, muéstrame el costo o el sello pedido y espera `sí <id>` o `no <id>`. Haz solo los `sí`.
Al final, ejecuta `python3 lancar.py status` y entrégame:
- cuántos sitios se enviaron, cuántos esperan correo, cuántos son mi turno (con el enlace de cada uno);
- la lista del grupo C (Product Hunt, Hacker News y similares) con lo que tengo que hacer en cada uno.

Para cada sitio del grupo C, deja listo lo que voy a publicar en `trabalho/rascunhos/<id>.md`: título, texto de la
publicación (ej.: el "Show HN" o el primer comentario de Product Hunt), enlaces y respuestas cortas a las preguntas
probables. Usa solo la ficha. Yo lo publico con mi cuenta.

Dentro de 1 a 2 semanas, ejecuto `python3 lancar.py confere` para ver qué listados ya están publicados.

---
