# Launch prompt — paste it into your agent

Use it with **Claude Code** open in this kit's folder and the **Claude in Chrome** extension turned on (the agent
controls your browser). It also works with any other agent that can read files and control the browser.

Before pasting:

1. Open the **sign-up email** in your browser (an inbox just for this, e.g. `launch@yourbrand.com`),
   already logged in. That's where the confirmation links arrive.
2. Put the brand files (512×512 logo, 1 to 3 screenshots) inside the `marca/` folder.

Copy everything between the `---` lines and paste it into the agent.

---

You are going to launch my startup on launch sites and directories, using the kit in this folder.
Work in 4 phases and **don't skip any gate**.

**First of all — check your tools.** See whether you can open websites, fill in forms and read my
sign-up email inbox. If something isn't available, tell me exactly what and carry on with what you can
do. Never say you submitted, opened or confirmed something you weren't able to do.

**Phase 1 — Interview and brand sheet.**
Copy `marca/marca.modelo.json` to `marca/marca.json` (if it doesn't exist yet). Set `"idioma": "en"` in the sheet.
Read my website (the address I give you) and interview me, **one question at a time**, to fill in each field.
Also ask for: a square logo and a horizontal logo (with the name), 3 to 5 screenshots, the tone of voice, the colors,
the launch date and a public contact email.
Brand sheet rules:
- `tagline` up to 60 characters; `descricao_curta` up to 160; `descricao_longa` up to 1000.
- Write the main fields (`tagline`, `descricao_curta`, `descricao_longa`, `categoria`, `tags`, `preco_detalhe`)
  in English, since the product is for a global market. Also fill in the `"en": {...}` block inside the sheet with
  `tagline`, `descricao_curta` and `descricao_longa` in English (most sites are in English; the block stays in the sheet).
- In `numeros`, only real numbers that I confirm, always with the `fonte`. If I have no number, the list stays empty.
  Never write "thousands of users", "market leader" or anything similar without a source.
- Ask for the `orcamento_usd` (default 0 = free only) and whether I `aceita_selo` (put a directory badge on my site;
  default false).
When you're done, run `python3 lancar.py checa` and fix it until it says `ficha OK`.
**Gate 1:** show me the whole sheet and wait for me to type `brand sheet approved`.

**Phase 2 — Plan.**
Run `python3 lancar.py plano`. Then, for each site in groups A and B, check whether my product is already listed
(the site's own search or `site:<domain> <product name>`); if it is, mark it
`python3 lancar.py marca <id> ja-listado --link "<address>"`. Read `trabalho/plano.md` and show me a summary: how many sites in each
group (A = you do it alone, B = asks for my yes, C = my turn, D = out of the plan) and the first 10 in group A.
**Gate 2:** wait for me to type `plan approved`.

**Phase 3 — Submission, one site at a time, in group A order.**
For each site:
1. Open the `url_envio` from the tracker (`trabalho/rastreador.csv`).
2. Create the account with the `email_cadastro` (if the site asks for an account) and fill in the form **only with data from the sheet**.
   Upload the logo, screenshots and links when the site asks for them.
3. If a confirmation email arrives, open the inbox in the other tab and click the link.
4. Update the tracker:
   `python3 lancar.py marca <id> enviado --link "<listing address, if it already exists>" --comprovante "<subject of the confirmation email, order number or screenshot name>" --nota "<what happened>"`
   (use `aguardando-email` if confirmation is still pending, `recusado` if the site rejected it).
   Only count it as **live** after opening the published page and seeing the link to my site.

**Stop and call me** (mark it `sua-vez` with the reason and move on to the next site) when any of these shows up:
- any charge, paid plan, "boost", paid queue or credit card — **even if it's US$ 1**;
- a request for a badge or a backlink on my site;
- captcha, phone verification, ID document, video or call;
- a question the sheet doesn't answer (don't make up the answer);
- terms of use that ask for anything beyond creating an account and listing the product (e.g. exclusivity, assignment of rights).

Never: pay; change my site; post in communities with my personal account; submit the same product twice
on the same site; use any email other than the `email_cadastro`.

**Phase 4 — Group B and report.**
For each site in group B, show me the cost or the badge requested and wait for `yes <id>` or `no <id>`. Only do the `yes` ones.
At the end, run `python3 lancar.py status` and give me:
- how many sites were submitted, how many are waiting for email, how many are my turn (with the link to each one);
- the group C list (Product Hunt, Hacker News and the like) with what I need to do on each one.

For each site in group C, get ready what I'll post in `trabalho/rascunhos/<id>.md`: title, post
text (e.g. the "Show HN" or the first comment on Product Hunt), links and short answers to the likely
questions. Use only the brand sheet. I'll post it with my own account.

In 1 to 2 weeks, I'll run `python3 lancar.py confere` to see which listings are already live.

---
