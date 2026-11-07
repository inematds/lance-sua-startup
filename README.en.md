# Launch your Startup — your product on 56 launch sites

[![Launch your Startup](guia/assets/banner-en.jpg)](https://inematds.github.io/lance-sua-startup/guia/en/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## What it is

Launch your Startup is a free kit for anyone who built an app, website or SaaS and wants it to show up on the internet.
It brings together 56 launch sites and directories (like Product Hunt, G2 and AI directories) that send visits and
links back to your site, the so-called *backlinks*, which help with Google. A script builds the plan in the right order
and keeps track of progress, and a ready-made prompt has your AI agent fill in the forms for you. What you need:
Python 3, Claude Code with the Chrome extension, and an email address just for sign-ups.

## 📖 How to use

Full guide (landing + step by step + table with filters): **https://inematds.github.io/lance-sua-startup/guia/en/**

## What's in the kit

| File | What it does |
|---|---|
| `sites/sites.json` · `sites/sites.csv` | the 56 sites: submission link, estimated strength, cost, badge, whether it needs you, tips |
| `lancar.py` | `lista` (filters), `checa` (brand sheet), `plano` (4 groups + tracker), `marca`, `status`, `confere` |
| `agente/PROMPT-LANCAMENTO.en.md` | the prompt to paste into the agent: interview → brand sheet → plan → submission, with 2 approval gates |
| `marca/marca.modelo.json` | brand sheet template (texts, logo, numbers with a source, budget, accepts badge) |
| `exemplo/` | ready-made sheet from a real INEMA project, to test the plan before filling in your own |
| `scripts/junta_sites.py` | merges the research in `sites/` and updates the table in the guides |

**Strength** is an estimate (high, medium, low) based on the site's size and reputation, not an official authority score.
Site prices and rules change: the `conferido_em` field says when each one was opened, and the agent checks again at submission time.

## The 4 groups in the plan

With a budget of 0 and no badges (the example sheet), the plan today comes out as: **A = 20 · B = 0 · C = 22 · D = 14**.

| Group | What goes in | Who does it |
|---|---|---|
| **A** | free, no badge, doesn't need you | the agent, from strongest to weakest |
| **B** | asks for a badge on your site, or is paid within budget | the agent, after your `yes <id>` |
| **C** | launches with a set date, communities, verification (Product Hunt, Hacker News…) | you |
| **D** | paid only and budget 0, or asks for a badge and you said no | nobody |

## The process, start to finish

| # | Step | Command | Who |
|---|---|---|---|
| 1 | Download the kit | `git clone https://github.com/inematds/lance-sua-startup && cd lance-sua-startup` | 🧠 you |
| 2 | See the sites and filters | `python3 lancar.py lista --agente --gratis` | ⚙️ script |
| 3 | Test with the example | `python3 lancar.py plano --marca exemplo/marca.json --saida exemplo/trabalho` | ⚙️ script |
| 4 | Prepare the sign-up email, logo and screenshots in `marca/` (e.g. `marca/logo-512.png`, `marca/captura-1.png`) | — | 🧠 you |
| 4b | Install Claude Code (paid Claude plan) and the Claude in Chrome extension; connect with `/chrome` | `curl -fsSL https://claude.ai/install.sh \| bash` | 🧠 you |
| 5 | Paste the prompt into the agent (in the kit folder) | contents of `agente/PROMPT-LANCAMENTO.en.md` | 🤖 agent |
| 6 | Interview and brand sheet until `ficha OK` | `python3 lancar.py checa` | 🤖 agent + 🧠 you |
| 7 | Gate 1 | you type `brand sheet approved` | 🧠 you |
| 8 | Plan in 4 groups + tracker | `python3 lancar.py plano` | 🤖 agent |
| 9 | Gate 2 | you type `plan approved` | 🧠 you |
| 10 | Submission site by site (group A) | `python3 lancar.py marca <id> enviado` | 🤖 agent |
| 11 | Group B: cost or badge, one by one | you type `yes <id>` or `no <id>` | 🧠 you |
| 12 | Group C: the launches that are yours | `python3 lancar.py status` | 🧠 you |
| 13 | In 1 to 2 weeks: which listings are live | `python3 lancar.py confere` | ⚙️ script |

## Agent rules

It never pays for anything (not even US$ 1) and never puts a badge on your site without your yes for that site. It only
uses texts and numbers from the brand sheet; a number without a source is rejected by `checa`. Captcha, phone, ID
document or a question the sheet doesn't answer: it marks the site as `sua-vez` (your turn) and moves on. It doesn't
post in communities with your personal account and doesn't submit twice.

## Updating the list

Edit a batch in `sites/pesquisa/` (or create `lote6.json` with the same fields) and run:

```bash
python3 scripts/junta_sites.py
```

## License

MIT. Made by [INEMA.CLUB](https://inema.club).
