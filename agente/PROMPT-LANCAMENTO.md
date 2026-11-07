# Prompt de lançamento — cole no seu agente

Use com o **Claude Code** aberto na pasta deste kit e com a extensão **Claude in Chrome** ligada (o agente
controla o seu navegador). Serve também para outro agente que leia arquivos e controle o navegador.

Antes de colar:

1. Abra no navegador o **e-mail de cadastro** (uma caixa só para isso, ex.: `lancamento@suamarca.com`),
   já logado. É lá que chegam os links de confirmação.
2. Deixe os arquivos da marca (logo 512×512, 1 a 3 capturas de tela) dentro da pasta `marca/`.

Copie tudo o que está entre as linhas `---` e cole no agente.

---

Você vai lançar a minha startup em sites de lançamento e diretórios, usando o kit desta pasta.
Trabalhe em 4 fases e **não pule nenhum portão**.

**Fase 1 — Entrevista e ficha da marca.**
Copie `marca/marca.modelo.json` para `marca/marca.json` (se ainda não existir). Leia o meu site
(o endereço que eu te passar) e me entreviste, **uma pergunta por vez**, para preencher cada campo.
Regras da ficha:
- `tagline` até 60 caracteres; `descricao_curta` até 160; `descricao_longa` até 1000.
- Em `numeros`, só número real que eu confirmar, sempre com a `fonte`. Se eu não tiver número, a lista fica vazia.
  Nunca escreva "milhares de usuários", "líder de mercado" ou parecido sem fonte.
- Pergunte o `orcamento_usd` (padrão 0 = só grátis) e se `aceita_selo` (pôr um selo do diretório no meu site;
  padrão false).
- Escreva os textos no idioma de cada site (a maioria é em inglês): prepare `tagline`, `descricao_curta` e
  `descricao_longa` em inglês também, num bloco `"en": {...}` dentro da ficha.
Quando terminar, rode `python3 lancar.py checa` e corrija até dar `ficha OK`.
**Portão 1:** me mostre a ficha inteira e espere eu escrever `ficha aprovada`.

**Fase 2 — Plano.**
Rode `python3 lancar.py plano`. Leia `trabalho/plano.md` e me mostre um resumo: quantos sites em cada
grupo (A = você faz sozinho, B = pede meu sim, C = minha vez, D = fora do plano) e os 10 primeiros do grupo A.
**Portão 2:** espere eu escrever `plano aprovado`.

**Fase 3 — Envio, um site por vez, na ordem do grupo A.**
Para cada site:
1. Abra o `url_envio` do rastreador (`trabalho/rastreador.csv`).
2. Crie a conta com o `email_cadastro` (se o site pedir conta) e preencha o formulário **só com dados da ficha**.
   Envie logo, capturas e links quando o site pedir.
3. Se chegar e-mail de confirmação, abra a caixa de e-mail na outra aba e clique no link.
4. Atualize o rastreador:
   `python3 lancar.py marca <id> enviado --link "<endereço da listagem, se já existir>" --nota "<o que aconteceu>"`
   (use `aguardando-email` se falta confirmar, `recusado` se o site recusou).

**Pare e me chame** (marque `sua-vez` com o motivo e passe para o próximo site) quando aparecer:
- qualquer cobrança, plano pago, "boost", fila paga ou cartão — **mesmo que seja US$ 1**;
- pedido de selo, badge ou link de volta no meu site;
- captcha, verificação por telefone, documento, vídeo ou chamada;
- pergunta que a ficha não responde (não invente a resposta);
- termos de uso que peçam algo além de criar conta e listar o produto (ex.: exclusividade, cessão de direitos).

Nunca: pagar; mudar o meu site; postar em comunidade com a minha conta pessoal; enviar o mesmo produto duas
vezes no mesmo site; usar outro e-mail que não o `email_cadastro`.

**Fase 4 — Grupo B e relatório.**
Para cada site do grupo B, me mostre o custo ou o selo pedido e espere `sim <id>` ou `não <id>`. Faça só os `sim`.
No fim, rode `python3 lancar.py status` e me entregue:
- quantos sites foram enviados, quantos aguardam e-mail, quantos são minha vez (com o link de cada um);
- a lista do grupo C (Product Hunt, Hacker News e afins) com o que eu preciso fazer em cada um.

Daqui a 1 a 2 semanas, eu rodo `python3 lancar.py confere` para ver quais listagens já estão no ar.

---
