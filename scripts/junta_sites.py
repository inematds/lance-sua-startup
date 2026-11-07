#!/usr/bin/env python3
"""Junta os lotes de pesquisa em sites/sites.json + sites/sites.csv e injeta a lista nos guias.

Uso: python3 scripts/junta_sites.py
- lê sites/pesquisa/lote*.json (ordem dos arquivos), cria o campo id (slug do nome)
- grava sites/sites.json e sites/sites.csv
- troca o bloco /*SITES*/.../*FIM*/ em guia/index.html, guia/en/index.html e guia/es/index.html
"""
import csv, glob, json, os, re, sys, unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAMPOS = ["id", "nome", "url", "url_envio", "categoria", "forca", "custo", "custo_obs", "selo",
          "precisa_de_voce", "precisa_de_voce_obs", "link_dofollow", "obs", "mercado", "conferido_em"]
VALORES = {"forca": {"alta", "media", "baixa"},
           "custo": {"gratis", "pago", "gratis-com-opcao-paga"},
           "categoria": {"avaliacoes", "lancamento", "diretorio-ia", "diretorio-saas", "comunidade",
                         "perfil-empresa", "dev"}}


def slug(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def main():
    sites, vistos, erros = [], set(), []
    for arq in sorted(glob.glob(os.path.join(RAIZ, "sites", "pesquisa", "lote*.json"))):
        for s in json.load(open(arq, encoding="utf-8")):
            s.setdefault("mercado", "global")
            s["id"] = slug(s["nome"])
            if s["id"] in vistos:
                erros.append(f"repetido: {s['nome']}")
                continue
            vistos.add(s["id"])
            for k, ok in VALORES.items():
                if s.get(k) not in ok:
                    erros.append(f"{s['nome']}: {k}={s.get(k)!r} fora de {sorted(ok)}")
            if not (s.get("url_envio") or "").startswith("http"):
                s["url_envio"] = s.get("url")
            sites.append({k: s.get(k) for k in CAMPOS})
    if erros:
        print("\n".join(erros))
        sys.exit(1)
    json.dump(sites, open(os.path.join(RAIZ, "sites", "sites.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    with open(os.path.join(RAIZ, "sites", "sites.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS)
        w.writeheader()
        w.writerows(sites)
    leve = [{k: s[k] for k in ("nome", "url", "url_envio", "categoria", "forca", "custo", "selo",
                                "precisa_de_voce", "mercado")} for s in sites]
    forca = {"alta": 0, "media": 1, "baixa": 2}
    leve.sort(key=lambda s: (forca[s["forca"]], s["nome"].lower()))
    bloco = "/*SITES*/" + json.dumps(leve, ensure_ascii=False) + "/*FIM*/"
    for g in ("guia/index.html", "guia/en/index.html", "guia/es/index.html"):
        p = os.path.join(RAIZ, g)
        if os.path.exists(p):
            h = open(p, encoding="utf-8").read()
            h2 = re.sub(r"/\*SITES\*/.*?/\*FIM\*/", lambda m: bloco, h, flags=re.S)
            open(p, "w", encoding="utf-8").write(h2)
            print(f"injetado em {g}")
    print(f"{len(sites)} sites gravados em sites/sites.json e sites/sites.csv")


if __name__ == "__main__":
    main()
