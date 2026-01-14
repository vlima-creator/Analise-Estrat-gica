import math
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Mercado Livre Ads - Relatório Estratégico", layout="wide")

# =========================
# Performance flags
# =========================
pd.options.mode.copy_on_write = True

# =========================
# Helpers
# =========================

def to_number_series(s: pd.Series) -> pd.Series:
    """Converte coluna com R$, %, pt-br para float com vetorização."""
    if s is None:
        return s

    # já numérico
    if pd.api.types.is_numeric_dtype(s):
        return s.astype(float)

    x = s.astype(str).str.strip()

    # marca % antes de remover
    is_percent = x.str.contains("%", na=False)

    x = (
        x.str.replace("R$", "", regex=False)
         .str.replace("$", "", regex=False)
         .str.replace("%", "", regex=False)
         .str.replace("\u00a0", " ", regex=False)
         .str.replace(" ", "", regex=False)
         .str.replace(".", "", regex=False)   # milhar
         .str.replace(",", ".", regex=False)  # decimal
    )

    v = pd.to_numeric(x, errors="coerce")

    # se era percent, transforma em decimal
    v = v.where(~is_percent, v / 100.0)
    return v.astype(float)


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    return df


def find_col(df: pd.DataFrame, candidates):
    cols = {c.lower(): c for c in df.columns}
    for cand in candidates:
        if cand.lower() in cols:
            return cols[cand.lower()]
    for c in df.columns:
        cl = c.lower()
        for cand in candidates:
            if cand.lower() in cl:
                return c
    return None


def safe_div_series(a: pd.Series, b: pd.Series) -> pd.Series:
    b0 = b.replace(0, pd.NA)
    return a / b0


def fmt_money(v):
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return "-"
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def fmt_pct(v):
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return "-"
    return f"{v*100:.1f}%".replace(".", ",")


# =========================
# Fast readers (cached)
# =========================

@st.cache_data(show_spinner=False)
def read_excel_fast(file, sheet_name=None):
    # lê o mínimo possível e sem adivinhar tipos demais
    return pd.read_excel(file, sheet_name=sheet_name, engine="openpyxl")


@st.cache_data(show_spinner=False)
def read_csv_fast(file):
    return pd.read_csv(file)


def read_any(file):
    name = file.name.lower()
    if name.endswith(".csv"):
        return read_csv_fast(file)
    return read_excel_fast(file)


# =========================
# Analysis
# =========================

@st.cache_data(show_spinner=False)
def analyze_campaigns(df_camp: pd.DataFrame):
    df_camp = normalize_columns(df_camp)

    col_name = find_col(df_camp, ["Nome da Campanha", "Campanha", "Campaign", "Nome campanha", "Nome"])
    col_budget = find_col(df_camp, ["Orçamento", "Orçamento diário", "Orcamento diario", "Budget", "Orçamento médio diário"])
    col_acos_target = find_col(df_camp, ["ACOS Objetivo", "ACOS alvo", "ACOS Objetivo Atual", "ACOS objetivo"])
    col_spend = find_col(df_camp, ["Investimento", "Gasto", "Spend", "Custo"])
    col_revenue = find_col(df_camp, ["Receita", "Vendas", "Vendas por Product Ads", "Sales", "Faturamento"])
    col_loss_budget = find_col(df_camp, ["% Perda Orçamento", "Perda por Orçamento", "Loss budget", "Perda orçamento"])
    col_loss_rank = find_col(df_camp, ["% Perda Classificação", "Perda por Classificação", "Perda por rank", "Loss rank", "Classificação"])

    if col_name is None or col_spend is None or col_revenue is None:
        return None, {"error": "Campanhas: não achei colunas mínimas (Nome da Campanha, Investimento/Gasto, Receita/Vendas)."}

    # mantém só colunas necessárias, isso acelera MUITO
    keep = [c for c in [col_name, col_budget, col_acos_target, col_spend, col_revenue, col_loss_budget, col_loss_rank] if c]
    df = df_camp[keep].copy()

    # normaliza numéricas
    for c in [col_budget, col_acos_target, col_spend, col_revenue, col_loss_budget, col_loss_rank]:
        if c and c in df.columns:
            df[c] = to_number_series(df[c])

    df["Campanha"] = df[col_name].astype(str)
    df["Investimento"] = df[col_spend]
    df["Receita"] = df[col_revenue]

    df["ROAS"] = safe_div_series(df["Receita"], df["Investimento"])
    df["ACOS_real"] = safe_div_series(df["Investimento"], df["Receita"])

    df["Orçamento_atual"] = df[col_budget] if col_budget else pd.NA
    df["ACOS_objetivo"] = df[col_acos_target] if col_acos_target else pd.NA
    df["Perda_orc"] = df[col_loss_budget] if col_loss_budget else pd.NA
    df["Perda_rank"] = df[col_loss_rank] if col_loss_rank else pd.NA

    # Pareto
    df_sorted = df.sort_values("Receita", ascending=False).reset_index(drop=True)
    total_rev = df_sorted["Receita"].sum(skipna=True)
    total_inv = df_sorted["Investimento"].sum(skipna=True)

    if total_rev and not pd.isna(total_rev):
        df_sorted["rev_share"] = df_sorted["Receita"] / total_rev
        df_sorted["rev_cum"] = df_sorted["rev_share"].cumsum()
        df_sorted["Prioridade_Pareto"] = df_sorted["rev_cum"] <= 0.80
    else:
        df_sorted["Prioridade_Pareto"] = False

    # mediana para "receita relevante"
    med = df_sorted["Receita"].median(skipna=True)

    # Quadrantes (vetorizado)
    roas = df_sorted["ROAS"]
    perda_orc = df_sorted["Perda_orc"]
    perda_rank = df_sorted["Perda_rank"]
    receita = df_sorted["Receita"]
    acos_real = df_sorted["ACOS_real"]
    acos_obj = df_sorted["ACOS_objetivo"]

    escala_orc = (roas > 7) & (perda_orc > 0.40)
    receita_relevante = (receita >= med) | (df_sorted["Prioridade_Pareto"] == True)
    competitividade = receita_relevante & (perda_rank > 0.50)
    hemorragia = (roas < 3) | ((acos_real > (acos_obj * 1.35)) & (~pd.isna(acos_obj)))

    df_sorted["Quadrante"] = "ESTAVEL"
    df_sorted.loc[hemorragia, "Quadrante"] = "HEMORRAGIA"
    df_sorted.loc[competitividade, "Quadrante"] = "COMPETITIVIDADE"
    df_sorted.loc[escala_orc, "Quadrante"] = "ESCALA_ORCAMENTO"

    action_map = {
        "ESCALA_ORCAMENTO": "🟢 Aumentar Orçamento",
        "COMPETITIVIDADE": "🟡 Subir ACOS Alvo",
        "HEMORRAGIA": "🔴 Revisar/Pausar",
        "ESTAVEL": "🔵 Manter",
    }
    df_sorted["AÇÃO RECOMENDADA"] = df_sorted["Quadrante"].map(action_map)

    meta = {
        "total_receita": float(total_rev) if not pd.isna(total_rev) else 0.0,
        "total_invest": float(total_inv) if not pd.isna(total_inv) else 0.0,
        "roas_conta": float(total_rev / total_inv) if total_inv else float("nan"),
        "acos_conta": float(total_inv / total_rev) if total_rev else float("nan"),
        "gamechangers": df_sorted[df_sorted["Prioridade_Pareto"]].head(10).copy(),
    }
    return df_sorted, meta


@st.cache_data(show_spinner=False)
def analyze_ads(df_ads: pd.DataFrame):
    df_ads = normalize_columns(df_ads)

    col_title = find_col(df_ads, ["Título do anúncio", "Titulo", "Anúncio", "Anuncio", "Item", "Publicação", "Publicacao"])
    col_mlb = find_col(df_ads, ["MLB", "Item ID", "ID do item", "Item_id", "ID"])
    col_spend = find_col(df_ads, ["Investimento", "Gasto", "Spend", "Custo"])
    col_revenue = find_col(df_ads, ["Receita", "Vendas", "Sales", "Faturamento"])
    col_units = find_col(df_ads, ["Unidades", "Unidades vendidas", "Units"])
    col_acos = find_col(df_ads, ["ACOS", "ACOS real", "ACOS Real"])
    col_roas = find_col(df_ads, ["ROAS", "ROAS real", "ROAS Real"])

    if col_spend is None or col_revenue is None:
        return None, {"error": "Anúncios: não achei Investimento/Gasto e Receita/Vendas."}

    keep = [c for c in [col_title, col_mlb, col_spend, col_revenue, col_units, col_acos, col_roas] if c]
    df = df_ads[keep].copy()

    for c in [col_spend, col_revenue, col_units, col_acos, col_roas]:
        if c and c in df.columns:
            df[c] = to_number_series(df[c])

    df["Investimento"] = df[col_spend]
    df["Receita"] = df[col_revenue]

    df["ROAS"] = df[col_roas] if col_roas else safe_div_series(df["Receita"], df["Investimento"])
    df["ACOS_real"] = df[col_acos] if col_acos else safe_div_series(df["Investimento"], df["Receita"])

    # normaliza ACOS se vier como 15 ao invés de 0.15
    df.loc[df["ACOS_real"] > 2, "ACOS_real"] = df.loc[df["ACOS_real"] > 2, "ACOS_real"] / 100.0

    df["Anúncio"] = df[col_title].astype(str) if col_title else "Anúncio"
    df["MLB"] = df[col_mlb].astype(str) if col_mlb else "-"

    # Perfil (vetorizado)
    estrela = (df["ROAS"] >= 7) & (df["Receita"] > 0)
    sanguessuga = (df["Investimento"] > 0) & ((df["Receita"].isna()) | (df["Receita"] == 0))
    gastao = (df["ROAS"] < 3) & (df["Receita"] > 0)

    df["Perfil"] = "NEUTRO"
    df.loc[gastao, "Perfil"] = "GASTAO"
    df.loc[sanguessuga, "Perfil"] = "SANGUESSUGA"
    df.loc[estrela, "Perfil"] = "ESTRELA"

    df = df.sort_values("Investimento", ascending=False)

    meta = {
        "top_sanguessugas": df[df["Perfil"] == "SANGUESSUGA"].head(25),
        "top_gastoes": df[df["Perfil"] == "GASTAO"].head(25),
        "top_estrelas": df[df["Perfil"] == "ESTRELA"].sort_values("Receita", ascending=False).head(25),
    }
    return df, meta


def render_report(camp_df, camp_meta, ads_df, ads_meta, period_label):
    st.markdown("## Relatório Estratégico de Performance")
    st.caption(period_label)

    st.markdown("### 1. Diagnóstico Executivo")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Receita (Ads)", fmt_money(camp_meta["total_receita"]))
    c2.metric("Investimento", fmt_money(camp_meta["total_invest"]))
    c3.metric("ROAS da conta", "-" if math.isnan(camp_meta["roas_conta"]) else f"{camp_meta['roas_conta']:.2f}")
    c4.metric("ACOS da conta", fmt_pct(camp_meta["acos_conta"]))

    roas = camp_meta["roas_conta"]
    if not math.isnan(roas) and roas >= 7:
        veredito = "Estamos deixando dinheiro na mesa em minas limitadas e locomotivas. Escale com corte de sangria."
    elif not math.isnan(roas) and roas < 3:
        veredito = "Precisamos estancar sangria antes de qualquer escala. Corte e ajuste de funil."
    else:
        veredito = "Conta intermediária. Escale só onde o gargalo é verba ou rank, e corte detratores."

    st.write(f"- Veredito: {veredito}")

    st.markdown("### 2. Análise de Oportunidades (Matriz CPI)")
    game = camp_meta["gamechangers"]
    locomotivas = game[game["Quadrante"] == "COMPETITIVIDADE"].head(5)
    minas = game[game["Quadrante"] == "ESCALA_ORCAMENTO"].head(5)
    hemo = game[game["Quadrante"] == "HEMORRAGIA"].head(5)

    st.markdown("**As Locomotivas (Faturamento Alto + Problema de Rank)**")
    st.dataframe(locomotivas[["Campanha", "Receita", "Investimento", "ROAS", "Perda_rank", "AÇÃO RECOMENDADA"]] if len(locomotivas) else pd.DataFrame(),
                 use_container_width=True)

    st.markdown("**As Minas Limitadas (ROAS Alto + Falta de Verba)**")
    st.dataframe(minas[["Campanha", "Receita", "Investimento", "ROAS", "Perda_orc", "AÇÃO RECOMENDADA"]] if len(minas) else pd.DataFrame(),
                 use_container_width=True)

    if len(hemo):
        st.markdown("**Hemorragias (Detratoras)**")
        st.dataframe(hemo[["Campanha", "Receita", "Investimento", "ROAS", "ACOS_real", "AÇÃO RECOMENDADA"]],
                     use_container_width=True)

    st.markdown("### 3. Plano de Ação Tático (Próximos 7 Dias)")
    st.markdown("**Dia 1 (Destravar):**")
    if len(minas):
        for _, r in minas.iterrows():
            st.write(f"- 🟢 Aumente orçamento: {r['Campanha']}")
    else:
        st.write("- Aumente orçamento nas campanhas com ROAS alto que travam por verba.")

    st.markdown("**Dia 2 (Competir):**")
    if len(locomotivas):
        for _, r in locomotivas.iterrows():
            st.write(f"- 🟡 Suba ACOS objetivo: {r['Campanha']}")
    else:
        st.write("- Suba ACOS objetivo nas campanhas com receita forte perdendo rank.")

    st.markdown("**Dia 3 (Estancar):**")
    if len(hemo):
        for _, r in hemo.iterrows():
            st.write(f"- 🔴 Corte ou reduza: {r['Campanha']}")
    else:
        st.write("- Corte campanhas com ROAS < 3 sem tese clara.")

    st.markdown("**Dia 5 (Monitorar):**")
    st.write("- Monitore ROAS pós ajustes e se receita cresce mais rápido que investimento.")

    st.markdown("### 4. 📋 Painel de Controle Geral")
    painel = camp_df[["Campanha", "Orçamento_atual", "ACOS_objetivo", "ROAS", "Perda_orc", "Perda_rank", "AÇÃO RECOMENDADA"]].copy()
    painel = painel.rename(columns={
        "Campanha": "Nome da Campanha",
        "Orçamento_atual": "Orçamento Atual",
        "ACOS_objetivo": "ACOS Objetivo Atual",
        "ROAS": "ROAS Real (Calculado)",
        "Perda_orc": "% Perda Orçamento",
        "Perda_rank": "% Perda Classificação (Rank)",
    })
    st.dataframe(painel, use_container_width=True)

    if ads_df is not None:
        st.markdown("### Corte de Sangria em Produtos e Anúncios")
        a, b, c = st.columns(3)
        with a:
            st.markdown("**🔴 Sanguessugas**")
            st.dataframe(ads_meta["top_sanguessugas"][["MLB", "Anúncio", "Investimento", "Receita", "ROAS", "ACOS_real"]], use_container_width=True)
        with b:
            st.markdown("**🟡 Gastões**")
            st.dataframe(ads_meta["top_gastoes"][["MLB", "Anúncio", "Investimento", "Receita", "ROAS", "ACOS_real"]], use_container_width=True)
        with c:
            st.markdown("**🟢 Estrelas**")
            st.dataframe(ads_meta["top_estrelas"][["MLB", "Anúncio", "Investimento", "Receita", "ROAS", "ACOS_real"]], use_container_width=True)


# =========================
# UI
# =========================

st.title("Mercado Livre Ads, Relatório Estratégico Automatizado")

period_label = st.text_input("Rótulo do período", value="Últimos 15 dias")

camp_file = st.file_uploader("Relatório de Campanhas (Excel ou CSV)", type=["xlsx", "xls", "csv"])
ads_file = st.file_uploader("Relatório de Anúncios Patrocinados (Excel ou CSV)", type=["xlsx", "xls", "csv"])

if camp_file:
    with st.spinner("Lendo relatório de campanhas..."):
        df_camp_raw = read_any(camp_file)

    with st.spinner("Analisando campanhas..."):
        camp_df, camp_meta = analyze_campaigns(df_camp_raw)

    if camp_df is None:
        st.error(camp_meta["error"])
        st.stop()

    ads_df = None
    ads_meta = None

    if ads_file:
        with st.spinner("Lendo relatório de anúncios patrocinados..."):
            df_ads_raw = read_any(ads_file)

        with st.spinner("Analisando anúncios..."):
            ads_df, ads_meta = analyze_ads(df_ads_raw)

        if ads_df is None:
            st.warning(ads_meta["error"])
            ads_df = None
            ads_meta = None

    render_report(camp_df, camp_meta, ads_df, ads_meta, period_label)

else:
    st.info("Envie o Relatório de Campanhas para gerar o relatório.")
