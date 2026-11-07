# Lance sua Startup — seu produto em 56 sites de lançamento

[![Lance sua Startup](guia/assets/banner.jpg)](https://inematds.github.io/lance-sua-startup/guia/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## O que é

Lance sua Startup é um kit gratuito para quem criou um app, site ou SaaS e quer que ele apareça na internet. Ele reúne
56 sites de lançamento e diretórios (como Product Hunt, G2 e diretórios de IA), que dão visitas e links de volta
para o seu site, os chamados *backlinks*, que ajudam no Google. Um script monta o plano na ordem certa e guarda o
andamento, e um prompt pronto faz o seu agente de IA preencher os formulários por você. Para usar: Python 3, o Claude
Code com a extensão do Chrome e um e-mail só para os cadastros.

## 📖 Guia de uso

Guia completo (landing + passo a passo + tabela com filtros): **https://inematds.github.io/lance-sua-startup/guia/**

## O que tem no kit

| Arquivo | O que faz |
|---|---|
| `sites/sites.json` · `sites/sites.csv` | os 56 sites: link de envio, força estimada, custo, selo, se precisa de você, dicas |
| `lancar.py` | `lista` (filtros), `checa` (ficha), `plano` (4 grupos + rastreador), `marca`, `status`, `confere` |
| `agente/PROMPT-LANCAMENTO.md` | o prompt para colar no agente: entrevista → ficha → plano → envio, com 2 portões de aprovação |
| `marca/marca.modelo.json` | modelo da ficha da marca (textos, logo, números com fonte, orçamento, aceita selo) |
| `exemplo/` | ficha pronta de um projeto real do INEMA, para testar o plano antes de preencher a sua |
| `scripts/junta_sites.py` | junta a pesquisa em `sites/` e atualiza a tabela dos guias |

**Força** é uma estimativa (alta, média, baixa) pelo tamanho e reputação do site, não um número oficial de autoridade.
Preços e regras dos sites mudam: o campo `conferido_em` diz quando cada um foi aberto, e o agente confere na hora do envio.

## Os 4 grupos do plano

Com orçamento 0 e sem selo (a ficha de exemplo), o plano hoje fica: **A = 20 · B = 0 · C = 22 · D = 14**.

| Grupo | O que entra | Quem faz |
|---|---|---|
| **A** | grátis, sem selo, sem precisar de você | o agente, do mais forte ao mais fraco |
| **B** | pede selo no seu site, ou é pago dentro do orçamento | o agente, depois do seu `sim <id>` |
| **C** | lançamento com dia marcado, comunidade, verificação (Product Hunt, Hacker News…) | você |
| **D** | só pago e orçamento 0, ou pede selo e você disse não | ninguém |

## O processo, do início ao fim

| # | Passo | Comando | Quem |
|---|---|---|---|
| 1 | Baixar o kit | `git clone https://github.com/inematds/lance-sua-startup && cd lance-sua-startup` | 🧠 você |
| 2 | Ver os sites e filtros | `python3 lancar.py lista --agente --gratis` | ⚙️ script |
| 3 | Testar com o exemplo | `python3 lancar.py plano --marca exemplo/marca.json --saida exemplo/trabalho` | ⚙️ script |
| 4 | Preparar e-mail de cadastro, logo e capturas em `marca/` (ex.: `marca/logo-512.png`, `marca/captura-1.png`) | — | 🧠 você |
| 4b | Instalar o Claude Code (plano pago do Claude) e a extensão Claude in Chrome; conectar com `/chrome` | `curl -fsSL https://claude.ai/install.sh \| bash` | 🧠 você |
| 5 | Colar o prompt no agente (na pasta do kit) | conteúdo de `agente/PROMPT-LANCAMENTO.md` | 🤖 agente |
| 6 | Entrevista e ficha da marca até `ficha OK` | `python3 lancar.py checa` | 🤖 agente + 🧠 você |
| 7 | Portão 1 | você escreve `ficha aprovada` | 🧠 você |
| 8 | Plano em 4 grupos + rastreador | `python3 lancar.py plano` | 🤖 agente |
| 9 | Portão 2 | você escreve `plano aprovado` | 🧠 você |
| 10 | Envio site por site (grupo A) | `python3 lancar.py marca <id> enviado` | 🤖 agente |
| 11 | Grupo B: custo ou selo, um por um | você escreve `sim <id>` ou `não <id>` | 🧠 você |
| 12 | Grupo C: lançamentos que são seus | `python3 lancar.py status` | 🧠 você |
| 13 | Em 1 a 2 semanas: quais listagens estão no ar | `python3 lancar.py confere` | ⚙️ script |

## Regras do agente

Nunca paga nada (nem US$ 1) e nunca põe selo no seu site sem o seu sim para aquele site. Só usa textos e números da
ficha; número sem fonte é recusado pelo `checa`. Captcha, telefone, documento ou pergunta que a ficha não responde:
ele marca o site como `sua-vez` e segue. Não posta em comunidade com a sua conta pessoal e não envia duas vezes.

## Atualizar a lista

Edite um lote em `sites/pesquisa/` (ou crie `lote6.json` com os mesmos campos) e rode:

```bash
python3 scripts/junta_sites.py
```

## Licença

MIT. Feito pelo [INEMA.CLUB](https://inema.club).
