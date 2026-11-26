#!/usr/bin/env python3
"""Auditoria dos dados SINISA (E2) - G02.

Le as planilhas municipais de indicadores de agua (ano t e t+1) definidas em
AUDITORIA (abaixo), pareia os municipios pelo codigo IBGE e gera as tabelas
usadas em `docs/dicionario-de-dados.md`. 

  reports/tables/cobertura-recortes.csv          pares validos por recorte
  reports/tables/cobertura-nordeste-uf.csv       cobertura por UF do recorte
  reports/tables/perfil-preditores-nordeste-ref2023.csv  perfil de cada indicador
  reports/tables/hashes-dados-brutos.csv         SHA-256 dos arquivos lidos

Uso (a partir da pasta do grupo; requer pandas e openpyxl):
    python -m src.data.auditoria_sinisa
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]

# Parametros da auditoria (E2). Caminhos relativos a pasta do grupo.
AUDITORIA = {
    "dados": {
        "raw": "data/raw/",
        # SINISA, modulo Agua, pasta "Agua - Base Municipal" de cada ZIP oficial
        "arquivo_t": "SINISA_AGUA_Indicadores_Base Municipal_2023.xlsx",
        "abas_t": ["Atendimento", "Estruturais e Operacionais", "Qualidade",
                   "Administrativo e Financeiro"],
        "arquivo_t1": "SINISA_AGUA_Indicadores_Base Municipal_2024_Retificação.xlsx",
        "abas_t1": ["Indicadores de Gestão"],
        "chave": "cod_IBGE",
        "alvo": "IAG2013",
        "faixa_alvo": [0, 100],
        "recorte_macrorregiao": "Nordeste",
        "subgrupos": {
            "ride_petrolina_juazeiro": "RAIDE do Polo Petrolina/PE e Juazeiro/BA",
            "ufs_pe_ba": ["PE", "BA"],
        },
        "max_ausentes_preditor": 0.20,
    },
    "saidas": {"tabelas": "reports/tables/"},
}
RE_INDICADOR = re.compile(r"^(IAG|IFA)\d{4}$")
CONTEXTO = {"Macrorregião", "Município", "UF", "Capital", "RM/RIDE"}


def sha256(caminho: Path) -> str:
    h = hashlib.sha256()
    with caminho.open("rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest().upper()


def ler_aba(caminho: Path, aba: str) -> tuple[pd.DataFrame, dict[str, str], dict[str, str]]:
    """Le uma aba no layout SINISA: linhas de titulo, nome, unidade e codigo."""
    bruto = pd.read_excel(caminho, sheet_name=aba, header=None, dtype=object)
    linha_cod = None
    for i in range(min(25, len(bruto))):
        valores = bruto.iloc[i].astype(str).str.strip()
        if valores.str.match(RE_INDICADOR.pattern).sum() >= 3:
            linha_cod = i
            break
    if linha_cod is None:
        raise ValueError(f"linha de codigos nao encontrada em {caminho.name}/{aba}")

    codigos = [str(c).strip() for c in bruto.iloc[linha_cod]]
    # 2023: nome, unidade, codigo; 2024: nome, (unidade), codigo -> procura o nome acima
    nomes_linha = next(
        i for i in range(linha_cod - 1, -1, -1)
        if str(bruto.iloc[i, 0]).strip().lower().startswith("codigo do ibge")
    )
    nomes = [str(c).strip() for c in bruto.iloc[nomes_linha]]
    unidades = (
        [str(c).strip() for c in bruto.iloc[linha_cod - 1]]
        if linha_cod - 1 > nomes_linha else ["" for _ in codigos]
    )

    codigos[0] = "cod_IBGE"
    for j, nome in enumerate(nomes[:10]):
        compacto = nome.replace(" ", "")
        if nome.startswith("Macrorregi"):
            codigos[j] = "Macrorregião"
        elif nome.startswith("Munic"):
            codigos[j] = "Município"
        elif nome in ("UF", "Capital"):
            codigos[j] = nome
        elif compacto == "RM/RIDE":
            codigos[j] = "RM/RIDE"

    df = bruto.iloc[linha_cod + 1 :].copy()
    df.columns = codigos
    df = df.loc[:, ~pd.Index(df.columns).duplicated()]
    df = df[pd.to_numeric(df["cod_IBGE"], errors="coerce").notna()].copy()
    df["cod_IBGE"] = pd.to_numeric(df["cod_IBGE"]).astype("int64")
    return df, dict(zip(codigos, nomes)), dict(zip(codigos, unidades))


def ler_planilha(caminho: Path, abas: list[str]) -> tuple[pd.DataFrame, dict, dict, dict]:
    base, nomes, unidades, origem = None, {}, {}, {}
    for aba in abas:
        df, n, u = ler_aba(caminho, aba)
        for c in df.columns:
            if RE_INDICADOR.match(c) and c not in origem:
                origem[c] = aba
        nomes.update(n)
        unidades.update(u)
        if base is None:
            base = df
        else:
            novas = [c for c in df.columns if c not in base.columns]
            base = base.merge(df[["cod_IBGE"] + novas], on="cod_IBGE", how="outer")
    return base, nomes, unidades, origem


def resumo(nome: str, d: pd.DataFrame, n_candidatos: int) -> dict:
    return {
        "recorte": nome,
        "pares_validos": len(d),
        "alvo_t1_media": round(d["alvo_t1"].mean(), 2),
        "alvo_t1_desvio": round(d["alvo_t1"].std(), 2),
        "alvo_t1_min": round(d["alvo_t1"].min(), 2),
        "alvo_t1_max": round(d["alvo_t1"].max(), 2),
        "variacao_abs_media_t_t1": round((d["alvo_t1"] - d["alvo_t"]).abs().mean(), 2),
        "preditores_candidatos": n_candidatos,
        "linhas_por_preditor": round(len(d) / max(n_candidatos, 1), 1),
    }


def main() -> None:
    cfg = AUDITORIA
    dados = cfg["dados"]
    raw = RAIZ / dados["raw"]
    saida = RAIZ / cfg["saidas"]["tabelas"]
    saida.mkdir(parents=True, exist_ok=True)
    alvo, chave = dados["alvo"], dados["chave"]
    lo, hi = dados["faixa_alvo"]
    limite = float(dados["max_ausentes_preditor"])

    arq_t, arq_t1 = raw / dados["arquivo_t"], raw / dados["arquivo_t1"]
    for arq in (arq_t, arq_t1):
        if not arq.is_file():
            raise SystemExit(f"arquivo bruto ausente: {arq} (ver docs/dicionario-de-dados.md)")

    pd.DataFrame(
        [{"arquivo": a.name, "sha256": sha256(a)} for a in (arq_t, arq_t1)]
    ).to_csv(saida / "hashes-dados-brutos.csv", index=False)

    t, nomes, unidades, origem = ler_planilha(arq_t, dados["abas_t"])
    t1, _, _, _ = ler_planilha(arq_t1, dados["abas_t1"])

    indicadores = [c for c in t.columns if RE_INDICADOR.match(c)]
    X = t[[chave] + sorted(CONTEXTO & set(t.columns)) + indicadores].copy()
    textos = {c: X[c].notna() & pd.to_numeric(X[c], errors="coerce").isna() for c in indicadores}
    for c in indicadores:
        X[c] = pd.to_numeric(X[c], errors="coerce")

    pares = X.merge(
        t1[[chave, alvo]].rename(columns={alvo: "alvo_t1"}), on=chave, how="inner"
    )
    pares["alvo_t"] = pares[alvo]
    pares["alvo_t1"] = pd.to_numeric(pares["alvo_t1"], errors="coerce")
    validos = pares[pares["alvo_t"].between(lo, hi) & pares["alvo_t1"].between(lo, hi)]

    def candidatos(d: pd.DataFrame) -> list[str]:
        ausente = d[indicadores].isna().mean()
        return [c for c in indicadores if c != alvo and ausente[c] <= limite]

    sub = dados["subgrupos"]
    recortes = {
        "Brasil": validos,
        dados["recorte_macrorregiao"]: validos[validos["Macrorregião"] == dados["recorte_macrorregiao"]],
        "PE+BA": validos[validos["UF"].isin(sub["ufs_pe_ba"])],
        "PE": validos[validos["UF"] == "PE"],
        "BA": validos[validos["UF"] == "BA"],
        "RIDE Petrolina-Juazeiro": validos[validos["RM/RIDE"] == sub["ride_petrolina_juazeiro"]],
    }
    pd.DataFrame(
        [resumo(n, d, len(candidatos(d))) for n, d in recortes.items()]
    ).to_csv(saida / "cobertura-recortes.csv", index=False)

    regiao = dados["recorte_macrorregiao"]
    ne = recortes[regiao]
    no_arquivo = t[t["Macrorregião"] == regiao].groupby("UF").size().rename("municipios_no_arquivo_t")
    cob = pd.concat([no_arquivo, ne.groupby("UF").size().rename("pares_validos")], axis=1).fillna(0)
    cob = cob.astype(int)
    cob["cobertura_pct"] = (100 * cob["pares_validos"] / cob["municipios_no_arquivo_t"]).round(1)
    cob.reset_index(names="UF").to_csv(saida / f"cobertura-{regiao.lower()}-uf.csv", index=False)

    linhas = []
    sel = set(candidatos(ne))
    ids = X[chave].isin(ne[chave])
    for c in indicadores:
        v = ne[c]
        linhas.append({
            "aba": origem.get(c, ""),
            "codigo": c,
            "variavel": " ".join(str(nomes.get(c, "")).split()),
            "unidade": unidades.get(c, ""),
            "pares": len(ne),
            "ausente_ou_nao_calculado_pct": round(100 * v.isna().mean(), 2),
            "texto_nao_calculado": int(textos[c][ids].sum()),
            "minimo": v.min(),
            "mediana": v.median(),
            "maximo": v.max(),
            "valores_distintos": v.nunique(),
            "uso": "alvo (t) / baseline" if c == alvo else ("candidato" if c in sel else "excluido (>20% ausente)"),
        })
    pd.DataFrame(linhas).to_csv(saida / f"perfil-preditores-{regiao.lower()}-ref2023.csv", index=False)

    print(pd.read_csv(saida / "cobertura-recortes.csv").to_string(index=False))
    print(cob.to_string())
    print(f"candidatos ({regiao}): {len(sel)} -> {sorted(sel)}")
    print("excluidos:", sorted(set(indicadores) - sel - {alvo}))


if __name__ == "__main__":
    main()
