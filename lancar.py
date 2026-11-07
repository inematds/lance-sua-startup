#!/usr/bin/env python3
"""lancar.py — organiza o lançamento da sua startup em 50+ sites.

Comandos:
  lista     mostra os sites (com filtros)
  checa     confere a ficha da marca (marca/marca.json)
  plano     monta o plano e o rastreador a partir da ficha
  marca     atualiza um site no rastreador (status, link da listagem)
  status    resumo do andamento
  confere   abre cada listagem marcada como enviada e procura o seu domínio

Só usa a biblioteca padrão do Python 3. Nada aqui envia formulário: quem envia é o agente,
seguindo agente/PROMPT-LANCAMENTO.md, com o seu sim.
"""
import argparse, csv, datetime, json, os, re, sys, urllib.request, urllib.parse

RAIZ = os.path.dirname(os.path.abspath(__file__))
SITES = os.path.join(RAIZ, "sites", "sites.json")
FORCA = {"alta": 0, "media": 1, "baixa": 2}
STATUS = ["pendente", "enviado", "aguardando-email", "no-ar", "recusado", "pulado", "sua-vez"]
CAMPOS_CSV = ["id", "nome", "grupo", "forca", "custo", "url_envio", "status", "link_listagem", "data", "nota"]
GRUPOS = {
    "A": "Agente faz (grátis, sem você)",
    "B": "Pede o seu sim (selo ou pago)",
    "C": "Sua vez (precisa de você)",
    "D": "Fora do plano (pago sem orçamento ou selo recusado)",
}


def carrega_sites():
    with open(SITES, encoding="utf-8") as f:
        return json.load(f)


def ordena(sites, idioma="pt"):
    pref = {"pt": "br", "es": "latam"}.get(idioma)
    return sorted(sites, key=lambda s: (FORCA.get(s.get("forca"), 3),
                                        0 if s.get("mercado") == pref else 1,
                                        s["nome"].lower()))


def filtra(sites, a):
    out = []
    for s in sites:
        if a.gratis and s.get("custo") == "pago":
            continue
        if a.sem_selo and s.get("selo") is True:
            continue
        if a.precisa_de_voce and not s.get("precisa_de_voce"):
            continue
        if a.agente and (s.get("precisa_de_voce") or s.get("selo") is True or s.get("custo") == "pago"):
            continue
        if a.mercado and s.get("mercado", "global") != a.mercado:
            continue
        if a.categoria and s.get("categoria") != a.categoria:
            continue
        out.append(s)
    return out


def sim_nao(v):
    return {True: "sim", False: "não", None: "?"}[v]


def cmd_lista(a):
    sites = ordena(filtra(carrega_sites(), a))
    if a.json:
        print(json.dumps(sites, ensure_ascii=False, indent=1))
        return 0
    print(f"{'#':>3}  {'site':<26} {'força':<6} {'custo':<22} {'selo':<4} {'você?':<5} mercado")
    for i, s in enumerate(sites, 1):
        print(f"{i:>3}  {s['nome'][:26]:<26} {s.get('forca',''):<6} {s.get('custo',''):<22} "
              f"{sim_nao(s.get('selo')):<4} {sim_nao(s.get('precisa_de_voce')):<5} {s.get('mercado','global')}")
    print(f"\n{len(sites)} sites")
    return 0


# ---------- ficha da marca ----------
OBRIG = ["nome", "url", "email_cadastro", "tagline", "descricao_curta", "descricao_longa",
         "categoria", "tags", "preco", "fundador_nome", "pais", "logo_quadrado"]
LIMITES = {"tagline": 60, "descricao_curta": 160, "descricao_longa": 1000}


def le_marca(caminho):
    if not os.path.exists(caminho):
        sys.exit(f"ficha não encontrada: {caminho}\n"
                 "Copie marca/marca.modelo.json para marca/marca.json e preencha (ou deixe o agente fazer), "
                 "ou teste com --marca exemplo/marca.json")
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


def checa_marca(m, base):
    erros, avisos = [], []
    for k in OBRIG:
        v = m.get(k)
        if v in (None, "", []):
            erros.append(f"falta '{k}'")
    for k, n in LIMITES.items():
        v = m.get(k) or ""
        if len(v) > n:
            erros.append(f"'{k}' tem {len(v)} caracteres (máx. {n})")
    for lang in ("en", "es"):
        bloco = m.get(lang) or {}
        for k, n in LIMITES.items():
            if len(bloco.get(k) or "") > n:
                erros.append(f"'{lang}.{k}' tem {len(bloco[k])} caracteres (máx. {n})")
    if not m.get("en"):
        avisos.append("sem bloco 'en' — a maioria dos sites é em inglês")
    if m.get("url") and not str(m["url"]).startswith("https://"):
        erros.append("'url' precisa começar com https://")
    if m.get("email_cadastro") and "@" not in m["email_cadastro"]:
        erros.append("'email_cadastro' não parece e-mail")
    texto = json.dumps(m, ensure_ascii=False)
    if re.search(r"TODO|<preencher>|\{\{|lorem", texto, re.I):
        erros.append("ainda há campo de modelo sem preencher (TODO/<preencher>)")
    for i, n in enumerate(m.get("numeros") or [], 1):
        if not (n.get("fonte") or "").strip():
            erros.append(f"número {i} ('{n.get('numero','')}') sem fonte — só números reais entram")
    for k in ("logo_quadrado", "logo_horizontal"):
        p = m.get(k)
        if p and not p.startswith("http") and not os.path.exists(os.path.join(base, p)):
            erros.append(f"arquivo de '{k}' não encontrado: {p}")
    for p in m.get("capturas") or []:
        if not p.startswith("http") and not os.path.exists(os.path.join(base, p)):
            avisos.append(f"captura não encontrada: {p}")
    if not m.get("capturas"):
        avisos.append("sem capturas de tela — vários sites pedem 1 a 3")
    if "orcamento_usd" not in m:
        avisos.append("sem 'orcamento_usd' — vou assumir 0 (só grátis)")
    if "aceita_selo" not in m:
        avisos.append("sem 'aceita_selo' — vou assumir false (sites com selo saem do plano)")
    return erros, avisos


def cmd_checa(a):
    m = le_marca(a.marca)
    erros, avisos = checa_marca(m, os.path.dirname(os.path.abspath(a.marca)))
    for e in erros:
        print("ERRO  ", e)
    for w in avisos:
        print("aviso ", w)
    print("ficha OK" if not erros else f"{len(erros)} erro(s): corrija antes do plano")
    return 1 if erros else 0


# ---------- plano ----------
def grupo_de(s, orc, aceita_selo):
    pago = s.get("custo") == "pago"
    if pago and orc <= 0:
        return "D"
    if s.get("selo") is True and not aceita_selo:
        return "D"
    if s.get("precisa_de_voce"):
        return "C"
    if pago or s.get("selo") is True:
        return "B"
    return "A"


def cmd_plano(a):
    m = le_marca(a.marca)
    erros, _ = checa_marca(m, os.path.dirname(os.path.abspath(a.marca)))
    if erros and not a.forcar:
        print("A ficha tem erros. Rode `python3 lancar.py checa` e corrija (ou use --forcar).")
        return 1
    orc = float(m.get("orcamento_usd") or 0)
    aceita = bool(m.get("aceita_selo"))
    sites = ordena(carrega_sites(), m.get("idioma", "pt"))
    os.makedirs(a.saida, exist_ok=True)
    linhas = {g: [] for g in GRUPOS}
    for s in sites:
        linhas[grupo_de(s, orc, aceita)].append(s)

    md = [f"# Plano de lançamento — {m.get('nome','')}", "",
          f"Gerado em {datetime.date.today().isoformat()} · orçamento US$ {orc:g} · "
          f"aceita selo: {'sim' if aceita else 'não'}", "",
          "Ordem: força do site (alta → baixa), grátis antes de pago. "
          "O agente só começa depois do seu **aprovado** neste plano.", ""]
    for g, titulo in GRUPOS.items():
        md += [f"## {g}. {titulo} — {len(linhas[g])}", ""]
        if not linhas[g]:
            md += ["(nenhum)", ""]
            continue
        md += ["| # | site | força | custo | selo | observação |", "|---|---|---|---|---|---|"]
        for i, s in enumerate(linhas[g], 1):
            obs = (s.get("precisa_de_voce_obs") if g == "C" else s.get("custo_obs") if g in "BD" else s.get("obs")) or ""
            md.append(f"| {i} | [{s['nome']}]({s.get('url_envio') or s.get('url')}) | {s.get('forca','')} | "
                      f"{s.get('custo','')} | {sim_nao(s.get('selo'))} | {obs.replace('|','/')} |")
        md.append("")
    md += ["## Regras que o agente segue", "",
           "1. Nunca paga nada, nem 'só US$ 1', sem o seu sim para aquele site.",
           "2. Nunca põe selo/link no seu site sem o seu sim para aquele site.",
           "3. Só usa textos e números da ficha (`marca/marca.json`). Nada inventado.",
           "4. Captcha, telefone, documento ou pergunta que a ficha não responde: para e te chama.",
           "5. Depois de cada site, atualiza o rastreador (`python3 lancar.py marca ...`).", ""]
    plano = os.path.join(a.saida, "plano.md")
    open(plano, "w", encoding="utf-8").write("\n".join(md))

    rast = os.path.join(a.saida, "rastreador.csv")
    antigo = {}
    if os.path.exists(rast):
        with open(rast, encoding="utf-8") as f:
            antigo = {r["id"]: r for r in csv.DictReader(f)}
    with open(rast, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS_CSV)
        w.writeheader()
        for g in GRUPOS:
            for s in linhas[g]:
                r = antigo.get(s["id"], {})
                status = r.get("status") or ("sua-vez" if g == "C" else "pulado" if g == "D" else "pendente")
                w.writerow({"id": s["id"], "nome": s["nome"], "grupo": g, "forca": s.get("forca", ""),
                            "custo": s.get("custo", ""), "url_envio": s.get("url_envio") or s.get("url"),
                            "status": status, "link_listagem": r.get("link_listagem", ""),
                            "data": r.get("data", ""), "nota": r.get("nota", "")})
    tot = {g: len(v) for g, v in linhas.items()}
    print(f"plano: {plano}\nrastreador: {rast}")
    print(" · ".join(f"{g}={n}" for g, n in tot.items()), f"· total {sum(tot.values())}")
    return 0


# ---------- rastreador ----------
def le_rast(caminho):
    if not os.path.exists(caminho):
        sys.exit(f"rastreador não existe: {caminho} (rode `plano` antes)")
    with open(caminho, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def grava_rast(caminho, linhas):
    with open(caminho, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS_CSV)
        w.writeheader()
        w.writerows(linhas)


def cmd_marca(a):
    caminho = os.path.join(a.saida, "rastreador.csv")
    linhas = le_rast(caminho)
    if a.status not in STATUS:
        sys.exit(f"status inválido: {a.status} (use: {', '.join(STATUS)})")
    for r in linhas:
        if r["id"] == a.id:
            r["status"] = a.status
            if a.link:
                r["link_listagem"] = a.link
            if a.nota:
                r["nota"] = a.nota
            r["data"] = datetime.date.today().isoformat()
            grava_rast(caminho, linhas)
            print(f"{r['nome']}: {a.status}")
            return 0
    sys.exit(f"id não encontrado no rastreador: {a.id}")


def cmd_status(a):
    linhas = le_rast(os.path.join(a.saida, "rastreador.csv"))
    cont = {}
    for r in linhas:
        cont[r["status"]] = cont.get(r["status"], 0) + 1
    print(" · ".join(f"{k}: {cont.get(k,0)}" for k in STATUS), f"· total {len(linhas)}")
    for r in linhas:
        if r["status"] in ("sua-vez", "aguardando-email"):
            print(f"  [{r['status']}] {r['nome']} — {r['url_envio']}")
    return 0


def baixa(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (lance-sua-startup)"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(2_000_000).decode("utf-8", "replace")


def cmd_confere(a):
    m = le_marca(a.marca)
    dominio = urllib.parse.urlparse(m["url"]).netloc.replace("www.", "")
    caminho = os.path.join(a.saida, "rastreador.csv")
    linhas = le_rast(caminho)
    mudou = 0
    for r in linhas:
        if r["status"] not in ("enviado", "aguardando-email", "no-ar") or not r["link_listagem"]:
            continue
        try:
            html = baixa(r["link_listagem"])
            achou = dominio in html
            print(f"{'OK ' if achou else '-- '} {r['nome']}: {'link para ' + dominio + ' encontrado' if achou else 'seu domínio ainda não aparece'}")
            if achou and r["status"] != "no-ar":
                r["status"], r["data"] = "no-ar", datetime.date.today().isoformat()
                mudou += 1
        except Exception as e:
            print(f"?? {r['nome']}: não abriu ({type(e).__name__})")
    if mudou:
        grava_rast(caminho, linhas)
    print(f"{mudou} listagem(ns) confirmada(s) no ar")
    return 0


def main():
    p = argparse.ArgumentParser(description="Lance sua startup em 50+ sites — plano e rastreador.")
    sub = p.add_subparsers(dest="cmd", required=True)
    l = sub.add_parser("lista", help="mostra os sites")
    l.add_argument("--gratis", action="store_true", help="tira os só-pagos")
    l.add_argument("--sem-selo", action="store_true", help="tira os que exigem selo")
    l.add_argument("--precisa-de-voce", action="store_true", help="só os que exigem você")
    l.add_argument("--agente", action="store_true", help="grátis, sem selo e sem precisar de você (grupo A)")
    l.add_argument("--mercado", choices=["global", "br", "latam"])
    l.add_argument("--categoria")
    l.add_argument("--json", action="store_true")
    for nome, ajuda in (("checa", "confere a ficha"), ("plano", "gera plano + rastreador"),
                        ("confere", "procura seu domínio nas listagens")):
        s = sub.add_parser(nome, help=ajuda)
        s.add_argument("--marca", default="marca/marca.json")
        s.add_argument("--saida", default="trabalho")
        if nome == "plano":
            s.add_argument("--forcar", action="store_true", help="gera mesmo com erro na ficha")
    mk = sub.add_parser("marca", help="atualiza um site no rastreador")
    mk.add_argument("id")
    mk.add_argument("status")
    mk.add_argument("--link")
    mk.add_argument("--nota")
    mk.add_argument("--saida", default="trabalho")
    st = sub.add_parser("status", help="resumo do andamento")
    st.add_argument("--saida", default="trabalho")
    a = p.parse_args()
    return {"lista": cmd_lista, "checa": cmd_checa, "plano": cmd_plano, "marca": cmd_marca,
            "status": cmd_status, "confere": cmd_confere}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
