# CLAUDE.md — lance-sua-startup

Kit para listar uma startup em 56 sites de lançamento e diretórios. Repo `inematds/lance-sua-startup`, autor dos commits
`inematds <inematds@gmail.com>`. Guia em `guia/` (PT) + `guia/en/` + `guia/es/`, publicado no GitHub Pages via Actions.

- Dados: `sites/pesquisa/lote*.json` é a fonte; `python3 scripts/junta_sites.py` gera `sites/sites.json`/`.csv` e
  injeta a tabela nos 3 guias. Não editar `sites/sites.json` à mão.
- `lancar.py` aceita só os status em PT (`enviado`, `sua-vez`…) e os campos da ficha em PT; os prompts EN/ES mantêm
  esses nomes.
- Nunca enviar formulário a site real nos testes: é ação externa. Testar com `exemplo/marca.json` e `--saida` temporária.
- Projeto INEMA sem citação de fonte externa.

## Self-learning

Quando o Nei corrigir algo ou você pegar um erro seu: antes de continuar, escreva a lição numa linha no TOPO da seção
Lessons abaixo.

## Lessons
