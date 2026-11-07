# Lance sua Startup — tu producto en 59 sitios de lanzamiento

[![Lance sua Startup](guia/assets/banner-es.jpg)](https://inematds.github.io/lance-sua-startup/guia/es/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## Qué es

Lance sua Startup es un kit gratuito para quien creó una app, un sitio web o un SaaS y quiere que aparezca en internet.
Reúne 59 sitios de lanzamiento y directorios (como Product Hunt, G2 y directorios de IA), que traen visitas y enlaces
de vuelta a tu sitio, los llamados *backlinks*, que ayudan en Google. Un script arma el plan en el orden correcto y
guarda el avance, y un prompt listo hace que tu agente de IA llene los formularios por ti. Para usarlo: Python 3,
Claude Code con la extensión de Chrome y un correo solo para los registros.

## 📖 Guía de uso

Guía completa (landing + paso a paso + tabla con filtros): **https://inematds.github.io/lance-sua-startup/guia/es/**

## Qué trae el kit

| Archivo | Qué hace |
|---|---|
| `sites/sites.json` · `sites/sites.csv` | los 59 sitios: enlace de envío, fuerza estimada, costo, sello, si te necesita, consejos |
| `lancar.py` | `lista` (filtros), `checa` (ficha), `plano` (4 grupos + rastreador), `marca`, `status`, `confere` |
| `agente/PROMPT-LANCAMENTO.es.md` | el prompt para pegar en el agente: entrevista → ficha → plan → envío, con 2 puntos de aprobación |
| `marca/marca.modelo.json` | modelo de la ficha de la marca (textos, logo, números con fuente, presupuesto, acepta sello) |
| `exemplo/` | ficha lista de un proyecto real de INEMA, para probar el plan antes de llenar la tuya |
| `scripts/junta_sites.py` | junta la investigación de `sites/` y actualiza la tabla de las guías |

**Fuerza** es una estimación (alta, media, baja) por el tamaño y la reputación del sitio, no un número oficial de autoridad.
Los precios y las reglas de los sitios cambian: el campo `conferido_em` dice cuándo se abrió cada uno, y el agente
verifica en el momento del envío.

## Los 4 grupos del plan

Con presupuesto 0 y sin sello (la ficha de ejemplo), el plan hoy queda: **A = 22 · B = 0 · C = 23 · D = 14**.

| Grupo | Qué entra | Quién lo hace |
|---|---|---|
| **A** | gratis, sin sello, sin necesitarte | el agente, del más fuerte al más débil |
| **B** | pide sello en tu sitio, o es pago dentro del presupuesto | el agente, después de tu `sí <id>` |
| **C** | lanzamiento con día fijo, comunidad, verificación (Product Hunt, Hacker News…) | tú |
| **D** | solo pago y presupuesto 0, o pide sello y dijiste que no | nadie |

## El proceso, de principio a fin

| # | Paso | Comando | Quién |
|---|---|---|---|
| 1 | Descargar el kit | `git clone https://github.com/inematds/lance-sua-startup && cd lance-sua-startup` | 🧠 tú |
| 2 | Ver los sitios y filtros | `python3 lancar.py lista --agente --gratis` | ⚙️ script |
| 3 | Probar con el ejemplo | `python3 lancar.py plano --marca exemplo/marca.json --saida exemplo/trabalho` | ⚙️ script |
| 4 | Preparar correo de registro, logo y capturas en `marca/` (ej.: `marca/logo-512.png`, `marca/captura-1.png`) | — | 🧠 tú |
| 4b | Instalar Claude Code (plan pago de Claude) y la extensión Claude in Chrome; conectar con `/chrome` | `curl -fsSL https://claude.ai/install.sh \| bash` | 🧠 tú |
| 5 | Pegar el prompt en el agente (en la carpeta del kit) | contenido de `agente/PROMPT-LANCAMENTO.es.md` | 🤖 agente |
| 6 | Entrevista y ficha de la marca hasta `ficha OK` | `python3 lancar.py checa` | 🤖 agente + 🧠 tú |
| 7 | Punto de aprobación 1 | escribes `ficha aprobada` | 🧠 tú |
| 8 | Plan en 4 grupos + rastreador; busca si ya está listado | `python3 lancar.py plano` · `marca <id> ja-listado` | 🤖 agente |
| 9 | Punto de aprobación 2 | escribes `plan aprobado` | 🧠 tú |
| 10 | Envío sitio por sitio (grupo A), con comprobante | `python3 lancar.py marca <id> enviado --comprovante "..."` | 🤖 agente |
| 11 | Grupo B: costo o sello, uno por uno | escribes `sí <id>` o `no <id>` | 🧠 tú |
| 12 | Grupo C: el agente deja el texto en `trabalho/rascunhos/<id>.md`, tú lo publicas | `python3 lancar.py status` | 🤖 agente + 🧠 tú |
| 13 | En 1 a 2 semanas: qué listados están publicados | `python3 lancar.py confere` | ⚙️ script |

## Reglas del agente

Nunca paga nada (ni US$ 1) y nunca pone un sello en tu sitio sin tu sí para ese sitio. Solo usa textos y números de la
ficha; `checa` rechaza los números sin fuente. Captcha, teléfono, documento o una pregunta que la ficha no responde:
marca el sitio como `sua-vez` y sigue. No publica en comunidades con tu cuenta personal y no envía dos veces.

## Actualizar la lista

Edita un lote en `sites/pesquisa/` (o crea `lote6.json` con los mismos campos) y ejecuta:

```bash
python3 scripts/junta_sites.py
```

## Licencia

MIT. Hecho por [INEMA.CLUB](https://inema.club).
