import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Curva ABC, Diagnóstico e Ações", layout="wide")


# =========================
# Estilo premium aprimorado v3.1
# =========================
st.markdown(
    """
<style>
/* ===== RESET E BASE ===== */
* { font-variant-numeric: tabular-nums; }
.block-container {padding-top: 1rem; padding-bottom: 2rem; max-width: 1600px;}

/* Header transparente */
header[data-testid="stHeader"] {background: rgba(0,0,0,0);}

/* Esconde linhas separadoras */
hr {display: none !important;}

/* ===== SIDEBAR PREMIUM ===== */
section[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #1a1b2e 0%, #0f0f1a 100%);
  border-right: 1px solid rgba(139, 92, 246, 0.2);
}
section[data-testid="stSidebar"] .block-container {padding-top: 1rem;}
section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {
  letter-spacing: -0.3px;
  color: #e2e8f0;
}

/* ===== HEADER PRINCIPAL ===== */
.hero-header {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.15), rgba(139, 92, 246, 0.10));
  border: 1px solid rgba(139, 92, 246, 0.25);
  border-radius: 20px;
  padding: 24px 28px;
  margin: 0 0 1.5rem 0;
  position: relative;
  overflow: hidden;
}
.hero-header::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 200px;
  height: 200px;
  background: radial-gradient(circle, rgba(139, 92, 246, 0.2), transparent 70%);
  border-radius: 50%;
  transform: translate(30%, -30%);
}
.hero-title {
  font-size: 2rem;
  font-weight: 800;
  margin: 0;
  letter-spacing: -0.5px;
  background: linear-gradient(135deg, #fff, #c4b5fd);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.hero-subtitle {
  margin-top: 0.5rem;
  opacity: 0.85;
  font-size: 1rem;
  color: #a5b4fc;
}

/* ===== CARDS DE MÉTRICAS ===== */
.metric-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 1.5rem;
}
@media (max-width: 1200px) {
  .metric-grid { grid-template-columns: repeat(2, 1fr); }
}
.metric-card {
  background: linear-gradient(145deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: 16px;
  padding: 20px;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}
.metric-card:hover {
  border-color: rgba(139, 92, 246, 0.4);
  transform: translateY(-2px);
  box-shadow: 0 8px 32px rgba(139, 92, 246, 0.15);
}
.metric-card.purple { border-left: 4px solid #8b5cf6; }
.metric-card.blue { border-left: 4px solid #3b82f6; }
.metric-card.green { border-left: 4px solid #22c55e; }
.metric-card.amber { border-left: 4px solid #f59e0b; }
.metric-card.rose { border-left: 4px solid #f43f5e; }
.metric-card.cyan { border-left: 4px solid #06b6d4; }
.metric-card.orange { border-left: 4px solid #f97316; }
.metric-card.indigo { border-left: 4px solid #6366f1; }

.metric-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.4rem;
  margin-bottom: 12px;
}
.metric-icon.purple { background: rgba(139, 92, 246, 0.2); }
.metric-icon.blue { background: rgba(59, 130, 246, 0.2); }
.metric-icon.green { background: rgba(34, 197, 94, 0.2); }
.metric-icon.amber { background: rgba(245, 158, 11, 0.2); }
.metric-icon.rose { background: rgba(244, 63, 94, 0.2); }
.metric-icon.cyan { background: rgba(6, 182, 212, 0.2); }
.metric-icon.orange { background: rgba(249, 115, 22, 0.2); }
.metric-icon.indigo { background: rgba(99, 102, 241, 0.2); }

.metric-label {
  font-size: 0.85rem;
  opacity: 0.7;
  margin: 0 0 4px 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.metric-value {
  font-size: 1.75rem;
  font-weight: 800;
  margin: 0;
  letter-spacing: -0.5px;
}
.metric-value.purple { color: #a78bfa; }
.metric-value.blue { color: #60a5fa; }
.metric-value.green { color: #4ade80; }
.metric-value.amber { color: #fbbf24; }
.metric-value.rose { color: #fb7185; }
.metric-value.cyan { color: #22d3ee; }
.metric-value.orange { color: #fb923c; }
.metric-value.indigo { color: #818cf8; }

/* ===== PERIOD SELECTOR ===== */
.period-selector {
  background: linear-gradient(145deg, rgba(139, 92, 246, 0.15), rgba(99, 102, 241, 0.10));
  border: 1px solid rgba(139, 92, 246, 0.3);
  border-radius: 16px;
  padding: 16px 20px;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 16px;
}
.period-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #a5b4fc;
  display: flex;
  align-items: center;
  gap: 8px;
}

/* ===== LOGISTICA CARD ===== */
.logistics-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin: 1rem 0;
}
@media (max-width: 900px) {
  .logistics-grid { grid-template-columns: 1fr; }
}
.logistics-card {
  background: linear-gradient(145deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: 16px;
  padding: 20px;
  text-align: center;
}
.logistics-card.full { border-top: 4px solid #22c55e; }
.logistics-card.correios { border-top: 4px solid #3b82f6; }
.logistics-card.flex { border-top: 4px solid #f59e0b; }
.logistics-card.outros { border-top: 4px solid #6b7280; }

.logistics-icon {
  font-size: 2rem;
  margin-bottom: 8px;
}
.logistics-title {
  font-size: 0.85rem;
  opacity: 0.7;
  margin-bottom: 4px;
  text-transform: uppercase;
}
.logistics-value {
  font-size: 1.5rem;
  font-weight: 800;
}
.logistics-value.full { color: #4ade80; }
.logistics-value.correios { color: #60a5fa; }
.logistics-value.flex { color: #fbbf24; }
.logistics-value.outros { color: #9ca3af; }

.logistics-bar {
  height: 8px;
  background: rgba(255,255,255,0.1);
  border-radius: 4px;
  margin-top: 12px;
  overflow: hidden;
}
.logistics-bar-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.5s ease;
}
.logistics-bar-fill.full { background: linear-gradient(90deg, #22c55e, #4ade80); }
.logistics-bar-fill.correios { background: linear-gradient(90deg, #3b82f6, #60a5fa); }
.logistics-bar-fill.flex { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
.logistics-bar-fill.outros { background: linear-gradient(90deg, #6b7280, #9ca3af); }

/* ===== ADS CARD ===== */
.ads-container {
  background: linear-gradient(145deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: 16px;
  padding: 20px;
  margin: 1rem 0;
}
.ads-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}
.ads-icon {
  font-size: 1.5rem;
}
.ads-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #e2e8f0;
}
.ads-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}
.ads-metric {
  text-align: center;
  padding: 16px;
  background: rgba(255,255,255,0.03);
  border-radius: 12px;
}
.ads-metric.ads { border-left: 4px solid #f97316; }
.ads-metric.organic { border-left: 4px solid #22c55e; }
.ads-metric-value {
  font-size: 2rem;
  font-weight: 800;
}
.ads-metric-value.ads { color: #fb923c; }
.ads-metric-value.organic { color: #4ade80; }
.ads-metric-label {
  font-size: 0.85rem;
  opacity: 0.7;
  margin-top: 4px;
}
.ads-bar-container {
  margin-top: 16px;
}
.ads-bar-labels {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  opacity: 0.7;
  margin-bottom: 6px;
}
.ads-bar {
  height: 12px;
  background: rgba(255,255,255,0.1);
  border-radius: 6px;
  overflow: hidden;
  display: flex;
}
.ads-bar-ads {
  height: 100%;
  background: linear-gradient(90deg, #f97316, #fb923c);
  transition: width 0.5s ease;
}
.ads-bar-organic {
  height: 100%;
  background: linear-gradient(90deg, #22c55e, #4ade80);
  transition: width 0.5s ease;
}

/* ===== EXPORT CARDS ===== */
.export-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin: 1rem 0;
}
@media (max-width: 1000px) {
  .export-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 700px) {
  .export-grid { grid-template-columns: 1fr; }
}
.export-card {
  background: linear-gradient(145deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: 16px;
  padding: 20px;
  transition: all 0.3s ease;
}
.export-card:hover {
  border-color: rgba(139, 92, 246, 0.4);
  transform: translateY(-2px);
}
.export-card.defense { border-left: 4px solid #22c55e; }
.export-card.correction { border-left: 4px solid #f59e0b; }
.export-card.attack { border-left: 4px solid #3b82f6; }
.export-card.cleanup { border-left: 4px solid #f43f5e; }
.export-card.opportunity { border-left: 4px solid #8b5cf6; }
.export-card.combo { border-left: 4px solid #06b6d4; }

.export-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}
.export-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}
.export-icon.defense { background: rgba(34, 197, 94, 0.2); }
.export-icon.correction { background: rgba(245, 158, 11, 0.2); }
.export-icon.attack { background: rgba(59, 130, 246, 0.2); }
.export-icon.cleanup { background: rgba(244, 63, 94, 0.2); }
.export-icon.opportunity { background: rgba(139, 92, 246, 0.2); }
.export-icon.combo { background: rgba(6, 182, 212, 0.2); }

.export-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #e2e8f0;
}
.export-desc {
  font-size: 0.85rem;
  opacity: 0.6;
}
.export-stats {
  display: flex;
  gap: 20px;
}
.export-stat {
  flex: 1;
}
.export-stat-value {
  font-size: 1.25rem;
  font-weight: 700;
  color: #a5b4fc;
}
.export-stat-label {
  font-size: 0.75rem;
  opacity: 0.6;
  text-transform: uppercase;
}

/* ===== TACTICAL CARD ===== */
.tactical-card {
  background: linear-gradient(145deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 16px;
  transition: all 0.3s ease;
}
.tactical-card:hover {
  border-color: rgba(139, 92, 246, 0.3);
}
.tactical-card.defense { border-left: 4px solid #22c55e; }
.tactical-card.correction { border-left: 4px solid #f59e0b; }
.tactical-card.attack { border-left: 4px solid #3b82f6; }
.tactical-card.cleanup { border-left: 4px solid #f43f5e; }
.tactical-card.optimization { border-left: 4px solid #8b5cf6; }

.tactical-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}
.tactical-title {
  font-size: 1rem;
  font-weight: 700;
  color: #e2e8f0;
  margin: 0;
}
.tactical-mlb {
  font-size: 0.8rem;
  opacity: 0.6;
  font-family: monospace;
}
.tactical-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}
.tactical-badge.defense { background: rgba(34, 197, 94, 0.2); color: #4ade80; }
.tactical-badge.correction { background: rgba(245, 158, 11, 0.2); color: #fbbf24; }
.tactical-badge.attack { background: rgba(59, 130, 246, 0.2); color: #60a5fa; }
.tactical-badge.cleanup { background: rgba(244, 63, 94, 0.2); color: #fb7185; }
.tactical-badge.optimization { background: rgba(139, 92, 246, 0.2); color: #a78bfa; }

.tactical-metrics {
  display: flex;
  gap: 20px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}
.tactical-metric {
  min-width: 80px;
}
.tactical-metric-value {
  font-size: 1.1rem;
  font-weight: 700;
  color: #a5b4fc;
}
.tactical-metric-label {
  font-size: 0.7rem;
  opacity: 0.6;
  text-transform: uppercase;
}
.tactical-action {
  background: rgba(139, 92, 246, 0.1);
  border-radius: 8px;
  padding: 10px 14px;
  font-size: 0.9rem;
  color: #c4b5fd;
}

/* ===== FRONT CARDS ===== */
.front-card {
  background: linear-gradient(145deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 16px;
  transition: all 0.3s ease;
}
.front-card:hover {
  border-color: rgba(139, 92, 246, 0.3);
}
.front-card.defense { border-left: 4px solid #22c55e; }
.front-card.correction { border-left: 4px solid #f59e0b; }
.front-card.attack { border-left: 4px solid #3b82f6; }
.front-card.cleanup { border-left: 4px solid #f43f5e; }

.front-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}
.front-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.3rem;
}
.front-icon.defense { background: rgba(34, 197, 94, 0.2); }
.front-icon.correction { background: rgba(245, 158, 11, 0.2); }
.front-icon.attack { background: rgba(59, 130, 246, 0.2); }
.front-icon.cleanup { background: rgba(244, 63, 94, 0.2); }

.front-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #e2e8f0;
}
.front-desc {
  font-size: 0.85rem;
  opacity: 0.6;
}
.front-stats {
  display: flex;
  gap: 20px;
}
.front-stat {
  flex: 1;
  text-align: center;
  padding: 12px;
  background: rgba(255,255,255,0.03);
  border-radius: 10px;
}
.front-stat-value {
  font-size: 1.25rem;
  font-weight: 700;
  color: #a5b4fc;
}
.front-stat-label {
  font-size: 0.7rem;
  opacity: 0.6;
  text-transform: uppercase;
}

/* ===== REPORT SECTIONS ===== */
.report-section {
  background: linear-gradient(145deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 20px;
  padding: 24px;
  margin-bottom: 24px;
}
.report-header {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(255,255,255,0.08);
}
.report-icon {
  width: 52px;
  height: 52px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.6rem;
}
.report-icon.purple { background: rgba(139, 92, 246, 0.2); }
.report-icon.blue { background: rgba(59, 130, 246, 0.2); }
.report-icon.green { background: rgba(34, 197, 94, 0.2); }
.report-icon.amber { background: rgba(245, 158, 11, 0.2); }
.report-icon.rose { background: rgba(244, 63, 94, 0.2); }
.report-icon.cyan { background: rgba(6, 182, 212, 0.2); }

.report-title {
  font-size: 1.4rem;
  font-weight: 800;
  color: #e2e8f0;
  margin: 0;
}
.report-desc {
  font-size: 0.9rem;
  opacity: 0.6;
  margin-top: 2px;
}

/* ===== KPI HIGHLIGHT ===== */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin: 16px 0;
}
@media (max-width: 800px) {
  .kpi-grid { grid-template-columns: 1fr; }
}
.kpi-box {
  background: linear-gradient(145deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02));
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: 14px;
  padding: 20px;
  text-align: center;
}
.kpi-box.purple { border-top: 3px solid #8b5cf6; }
.kpi-box.blue { border-top: 3px solid #3b82f6; }
.kpi-box.green { border-top: 3px solid #22c55e; }
.kpi-box.amber { border-top: 3px solid #f59e0b; }
.kpi-box.rose { border-top: 3px solid #f43f5e; }

.kpi-value {
  font-size: 2rem;
  font-weight: 800;
  margin-bottom: 4px;
}
.kpi-value.purple { color: #a78bfa; }
.kpi-value.blue { color: #60a5fa; }
.kpi-value.green { color: #4ade80; }
.kpi-value.amber { color: #fbbf24; }
.kpi-value.rose { color: #fb7185; }

.kpi-label {
  font-size: 0.85rem;
  opacity: 0.7;
}

/* ===== INSIGHT CARD ===== */
.insight-card {
  background: linear-gradient(145deg, rgba(139, 92, 246, 0.1), rgba(99, 102, 241, 0.05));
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 14px;
  padding: 18px 20px;
  margin: 16px 0;
  display: flex;
  align-items: flex-start;
  gap: 14px;
}
.insight-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}
.insight-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: #c4b5fd;
  margin-bottom: 4px;
}
.insight-text {
  font-size: 0.9rem;
  opacity: 0.85;
  line-height: 1.5;
}

/* ===== FRONT SUMMARY ===== */
.front-summary {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin: 16px 0;
}
.front-pill {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: 30px;
  font-size: 0.9rem;
}
.front-pill-icon {
  font-size: 1rem;
}
.front-pill-count {
  font-weight: 700;
  color: #a5b4fc;
}
.front-pill-label {
  opacity: 0.7;
}

/* ===== SECTION HEADER ===== */
.section-box {
  background: linear-gradient(145deg, rgba(255,255,255,0.04), rgba(255,255,255,0.01));
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 20px;
}
.section-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}
.section-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}
.section-icon.purple { background: rgba(139, 92, 246, 0.2); }
.section-icon.blue { background: rgba(59, 130, 246, 0.2); }
.section-icon.green { background: rgba(34, 197, 94, 0.2); }
.section-icon.amber { background: rgba(245, 158, 11, 0.2); }
.section-icon.rose { background: rgba(244, 63, 94, 0.2); }
.section-icon.cyan { background: rgba(6, 182, 212, 0.2); }

.section-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #e2e8f0;
}
.section-desc {
  font-size: 0.85rem;
  opacity: 0.6;
}

/* ===== INPUTS ===== */
div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div {
  border-radius: 12px !important;
  border-color: rgba(255,255,255,0.15) !important;
}
div[data-baseweb="input"] > div:focus-within,
div[data-baseweb="select"] > div:focus-within {
  border-color: rgba(139, 92, 246, 0.5) !important;
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.15) !important;
}

/* ===== BOTÕES ===== */
div.stDownloadButton button, div.stButton button {
  border-radius: 12px !important;
  padding: 0.6rem 1rem !important;
  border: 1px solid rgba(139, 92, 246, 0.3) !important;
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.2), rgba(139, 92, 246, 0.1)) !important;
  transition: all 0.3s ease !important;
}
div.stDownloadButton button:hover, div.stButton button:hover {
  border-color: rgba(139, 92, 246, 0.5) !important;
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.3), rgba(139, 92, 246, 0.2)) !important;
  box-shadow: 0 4px 16px rgba(139, 92, 246, 0.2) !important;
  transform: translateY(-1px) !important;
}

/* ===== TABS ===== */
.stTabs [data-baseweb="tab-list"] {
  gap: 8px;
  background: rgba(255,255,255,0.03);
  padding: 8px;
  border-radius: 14px;
}
.stTabs [data-baseweb="tab"] {
  border-radius: 10px !important;
  padding: 10px 20px !important;
  font-weight: 600 !important;
}
.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.3), rgba(99, 102, 241, 0.2)) !important;
}

/* ===== EXPANDERS ===== */
.streamlit-expanderHeader {
  background: rgba(255,255,255,0.03) !important;
  border-radius: 12px !important;
}


/* ===== SIDEBAR PREMIUM v2 ===== */
.sidebar-section {
  background: linear-gradient(145deg, rgba(99, 102, 241, 0.12), rgba(139, 92, 246, 0.06));
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 16px;
  padding: 18px;
  margin-bottom: 16px;
}
.sidebar-section-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 14px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(139, 92, 246, 0.15);
}
.sidebar-section-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  background: rgba(139, 92, 246, 0.2);
}
.sidebar-section-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: #e2e8f0;
}
.sidebar-section-desc {
  font-size: 0.75rem;
  opacity: 0.6;
  margin-top: 2px;
}
.sidebar-stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  margin-top: 14px;
}
.sidebar-stat {
  background: rgba(255,255,255,0.04);
  border-radius: 10px;
  padding: 10px;
  text-align: center;
}
.sidebar-stat-value {
  font-size: 1.1rem;
  font-weight: 800;
  color: #a78bfa;
}
.sidebar-stat-label {
  font-size: 0.65rem;
  opacity: 0.6;
  text-transform: uppercase;
  margin-top: 2px;
}
.sidebar-tip {
  background: linear-gradient(145deg, rgba(34, 197, 94, 0.12), rgba(34, 197, 94, 0.04));
  border: 1px solid rgba(34, 197, 94, 0.2);
  border-radius: 10px;
  padding: 12px;
  margin-top: 12px;
  font-size: 0.8rem;
  color: #86efac;
  line-height: 1.4;
}
.sidebar-version {
  text-align: center;
  font-size: 0.75rem;
  opacity: 0.4;
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid rgba(255,255,255,0.08);
}

/* ===== FILTER BAR v2 ===== */
.filter-container {
  background: linear-gradient(145deg, rgba(99, 102, 241, 0.08), rgba(139, 92, 246, 0.04));
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 20px;
  padding: 24px;
  margin-bottom: 24px;
}
.filter-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}
.filter-header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}
.filter-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.3rem;
  background: rgba(139, 92, 246, 0.2);
}
.filter-main-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #e2e8f0;
}
.filter-subtitle {
  font-size: 0.8rem;
  opacity: 0.6;
}
.filter-count {
  background: rgba(139, 92, 246, 0.2);
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  color: #a78bfa;
}
.filter-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1.5fr 1fr;
  gap: 16px;
  align-items: end;
}
@media (max-width: 1000px) {
  .filter-grid { grid-template-columns: 1fr 1fr; }
}
.filter-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.filter-label {
  font-size: 0.8rem;
  font-weight: 600;
  color: #a5b4fc;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* ===== FRONT BUTTONS ===== */
.front-buttons {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 16px;
}
.front-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  border-radius: 12px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 2px solid transparent;
}
.front-btn.defense {
  background: rgba(34, 197, 94, 0.15);
  color: #4ade80;
  border-color: rgba(34, 197, 94, 0.3);
}
.front-btn.correction {
  background: rgba(245, 158, 11, 0.15);
  color: #fbbf24;
  border-color: rgba(245, 158, 11, 0.3);
}
.front-btn.attack {
  background: rgba(59, 130, 246, 0.15);
  color: #60a5fa;
  border-color: rgba(59, 130, 246, 0.3);
}
.front-btn.cleanup {
  background: rgba(244, 63, 94, 0.15);
  color: #fb7185;
  border-color: rgba(244, 63, 94, 0.3);
}
.front-btn.optimization {
  background: rgba(139, 92, 246, 0.15);
  color: #a78bfa;
  border-color: rgba(139, 92, 246, 0.3);
}
.front-btn-count {
  background: rgba(255,255,255,0.15);
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 0.8rem;
}


/* ===== SIDEBAR CARD ===== */
.sidebar-card {
  background: linear-gradient(145deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02));
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: 16px;
  padding: 16px;
  margin: 0.5rem 0 1rem 0;
}
.sidebar-title {
  font-size: 0.9rem;
  font-weight: 700;
  margin-bottom: 12px;
  color: #a5b4fc;
}

/* ===== FILTER BAR ===== */
.filter-bar {
  background: linear-gradient(145deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 20px;
}
.filter-title {
  font-size: 0.9rem;
  font-weight: 700;
  color: #a5b4fc;
  margin-bottom: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
}

/* ===== PROGRESS BAR ===== */
.progress-container {
  background: rgba(255,255,255,0.1);
  border-radius: 10px;
  height: 8px;
  overflow: hidden;
  margin: 8px 0;
}
.progress-bar {
  height: 100%;
  border-radius: 10px;
  transition: width 0.5s ease;
}
.progress-bar.green { background: linear-gradient(90deg, #22c55e, #4ade80); }
.progress-bar.amber { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
.progress-bar.rose { background: linear-gradient(90deg, #f43f5e, #fb7185); }

</style>
    """,
    unsafe_allow_html=True,
)

# Header principal
st.markdown(
    """
<div class="hero-header">
  <div class="hero-title">📊 Curva ABC, Diagnóstico e Ações</div>
  <div class="hero-subtitle">Análise inteligente para decisões rápidas por frente e prioridade</div>
</div>
    """,
    unsafe_allow_html=True,
)


# =========================
# Helpers visuais
# =========================
def render_metric_card(label: str, value: str, icon: str = "📈", color: str = "purple"):
    st.markdown(
        f"""
<div class='metric-card {color}'>
  <div class='metric-icon {color}'>{icon}</div>
  <p class='metric-label'>{label}</p>
  <p class='metric-value {color}'>{value}</p>
</div>
        """,
        unsafe_allow_html=True,
    )

def render_metric_grid(metrics: list):
    """Renderiza grid de métricas. metrics = [(label, value, icon, color), ...]"""
    html = '<div class="metric-grid">'
    for label, value, icon, color in metrics:
        html += f"""
<div class='metric-card {color}'>
  <div class='metric-icon {color}'>{icon}</div>
  <p class='metric-label'>{label}</p>
  <p class='metric-value {color}'>{value}</p>
</div>
        """
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

def render_logistics_section(full_pct: float, correios_pct: float, flex_pct: float, outros_pct: float, period: str):
    """Renderiza seção de logística com todas as formas de entrega"""
    html = f"""
<div class="section-box">
  <div class="section-header">
    <div class="section-icon cyan">🚚</div>
    <div>
      <div class="section-title">Logística - Período {period}</div>
      <div class="section-desc">Distribuição por forma de entrega</div>
    </div>
  </div>
  <div class="logistics-grid">
    <div class="logistics-card full">
      <div class="logistics-icon">📦</div>
      <div class="logistics-title">Full</div>
      <div class="logistics-value full">{full_pct:.1f}%</div>
      <div class="logistics-bar">
        <div class="logistics-bar-fill full" style="width: {full_pct}%"></div>
      </div>
    </div>
    <div class="logistics-card correios">
      <div class="logistics-icon">📮</div>
      <div class="logistics-title">Correios / Pontos</div>
      <div class="logistics-value correios">{correios_pct:.1f}%</div>
      <div class="logistics-bar">
        <div class="logistics-bar-fill correios" style="width: {correios_pct}%"></div>
      </div>
    </div>
    <div class="logistics-card flex">
      <div class="logistics-icon">🚴</div>
      <div class="logistics-title">Flex</div>
      <div class="logistics-value flex">{flex_pct:.1f}%</div>
      <div class="logistics-bar">
        <div class="logistics-bar-fill flex" style="width: {flex_pct}%"></div>
      </div>
    </div>
  </div>
</div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_ads_section(ads_pct: float, organic_pct: float, ads_qty: int, organic_qty: int, period: str):
    """Renderiza seção de vendas por publicidade"""
    html = f"""
<div class="ads-container">
  <div class="ads-header">
    <div class="ads-icon">📢</div>
    <div class="ads-title">Vendas por Publicidade - Período {period}</div>
  </div>
  <div class="ads-grid">
    <div class="ads-metric ads">
      <div class="ads-metric-value ads">{ads_pct:.1f}%</div>
      <div class="ads-metric-label">Via Publicidade ({ads_qty:,} vendas)</div>
    </div>
    <div class="ads-metric organic">
      <div class="ads-metric-value organic">{organic_pct:.1f}%</div>
      <div class="ads-metric-label">Orgânicas ({organic_qty:,} vendas)</div>
    </div>
  </div>
  <div class="ads-bar-container">
    <div class="ads-bar-labels">
      <span>📢 Ads</span>
      <span>🌱 Orgânico</span>
    </div>
    <div class="ads-bar">
      <div class="ads-bar-ads" style="width: {ads_pct}%"></div>
      <div class="ads-bar-organic" style="width: {organic_pct}%"></div>
    </div>
  </div>
</div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_export_card(icon: str, title: str, desc: str, itens: int, fat: float, card_type: str):
    """Renderiza card de exportação com estatísticas"""
    return f"""
<div class='export-card {card_type}'>
  <div class='export-header'>
    <div class='export-icon {card_type}'>{icon}</div>
    <div>
      <div class='export-title'>{title}</div>
      <div class='export-desc'>{desc}</div>
    </div>
  </div>
  <div class='export-stats'>
    <div class='export-stat'>
      <div class='export-stat-value'>{br_int(itens)}</div>
      <div class='export-stat-label'>Itens</div>
    </div>
    <div class='export-stat'>
      <div class='export-stat-value'>{br_money(fat)}</div>
      <div class='export-stat-label'>Faturamento</div>
    </div>
  </div>
</div>
    """

def render_tactical_card(row: dict, frente: str):
    """Renderiza card tático para um produto"""
    frente_map = {
        "DEFESA": "defense",
        "CORREÇÃO": "correction",
        "ATAQUE": "attack",
        "LIMPEZA": "cleanup",
        "OTIMIZAÇÃO": "optimization"
    }
    card_class = frente_map.get(frente, "optimization")
    
    return f"""
<div class='tactical-card {card_class}'>
  <div class='tactical-header'>
    <div>
      <p class='tactical-title'>{row.get('Título', '-')[:60]}...</p>
      <p class='tactical-mlb'>{row.get('MLB', '-')}</p>
    </div>
    <span class='tactical-badge {card_class}'>{frente}</span>
  </div>
  <div class='tactical-metrics'>
    <div class='tactical-metric'>
      <div class='tactical-metric-value'>{row.get('Curva 0-30', '-')}</div>
      <div class='tactical-metric-label'>Curva Atual</div>
    </div>
    <div class='tactical-metric'>
      <div class='tactical-metric-value'>{row.get('Curva 31-60', '-')}</div>
      <div class='tactical-metric-label'>Curva Anterior</div>
    </div>
    <div class='tactical-metric'>
      <div class='tactical-metric-value'>{br_money(float(row.get('Fat. 0-30', 0))) if row.get('Fat. 0-30') else '-'}</div>
      <div class='tactical-metric-label'>Fat. Atual</div>
    </div>
    <div class='tactical-metric'>
      <div class='tactical-metric-value'>{br_int(row.get('Qntd 0-30', 0))}</div>
      <div class='tactical-metric-label'>Qtd. Atual</div>
    </div>
  </div>
  <div class='tactical-action'>💡 {row.get('Ação sugerida', 'Sem ação definida')}</div>
</div>
    """

def render_front_summary(fronts: list):
    """Renderiza resumo das frentes. fronts = [(icon, count, label), ...]"""
    html = '<div class="front-summary">'
    for icon, count, label in fronts:
        html += f"""
<div class='front-pill'>
  <span class='front-pill-icon'>{icon}</span>
  <span class='front-pill-count'>{count}</span>
  <span class='front-pill-label'>{label}</span>
</div>
        """
    html += '</div>'
    return html

def render_report_section(icon: str, title: str, desc: str, color: str):
    """Renderiza header de seção do relatório"""
    return f"""
<div class='report-section'>
  <div class='report-header'>
    <div class='report-icon {color}'>{icon}</div>
    <div>
      <div class='report-title'>{title}</div>
      <div class='report-desc'>{desc}</div>
    </div>
  </div>
    """

def render_kpi_highlight(kpis: list):
    """Renderiza KPIs destacados. kpis = [(value, label, color), ...]"""
    html = '<div class="kpi-grid">'
    for value, label, color in kpis:
        html += f"""
<div class='kpi-box {color}'>
  <div class='kpi-value {color}'>{value}</div>
  <div class='kpi-label'>{label}</div>
</div>
        """
    html += '</div>'
    return html

def render_insight_card(icon: str, title: str, text: str):
    """Renderiza card de insight"""
    return f"""
<div class='insight-card'>
  <div class='insight-icon'>{icon}</div>
  <div>
    <div class='insight-title'>{title}</div>
    <div class='insight-text'>{text}</div>
  </div>
</div>
    """

def section_header(title: str, desc: str, icon: str = "📊", color: str = "purple"):
    """Renderiza header de seção"""
    st.markdown(
        f"""
<div class='section-box'>
  <div class='section-header'>
    <div class='section-icon {color}'>{icon}</div>
    <div>
      <div class='section-title'>{title}</div>
      <div class='section-desc'>{desc}</div>
    </div>
  </div>
        """,
        unsafe_allow_html=True,
    )

def section_footer():
    st.markdown("</div>", unsafe_allow_html=True)

def render_front_card(icon: str, title: str, desc: str, itens: int, fat: float, card_type: str, filename: str, df_seg: pd.DataFrame):
    """Renderiza card de frente com download"""
    st.markdown(
        f"""
<div class='front-card {card_type}'>
  <div class='front-header'>
    <div class='front-icon {card_type}'>{icon}</div>
    <div>
      <div class='front-title'>{title}</div>
      <div class='front-desc'>{desc}</div>
    </div>
  </div>
  <div class='front-stats'>
    <div class='front-stat'>
      <div class='front-stat-value'>{br_int(itens)}</div>
      <div class='front-stat-label'>Itens</div>
    </div>
    <div class='front-stat'>
      <div class='front-stat-value'>{br_money(fat)}</div>
      <div class='front-stat-label'>Faturamento</div>
    </div>
    <div class='front-stat'>
      <div class='front-stat-value'>0</div>
      <div class='front-stat-label'>Em andamento</div>
    </div>
  </div>
</div>
        """,
        unsafe_allow_html=True,
    )
    st.download_button(
        f"📥 Baixar {title}",
        data=to_csv_bytes(df_seg),
        file_name=filename,
        mime="text/csv",
        key=f"dl_{title}_{filename}",
    )

# =========================
# Helpers de formatação
# =========================
def br_money(x: float) -> str:
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "-"
    return f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def br_int(x) -> str:
    try:
        return f"{int(x):,}".replace(",", ".")
    except Exception:
        return "-"

def safe_div(a, b):
    try:
        if b and b != 0:
            return a / b
    except Exception:
        pass
    return np.nan

def pct(x, decimals=1) -> str:
    try:
        if x is None or (isinstance(x, float) and np.isnan(x)):
            return "-"
        return f"{round(float(x) * 100, decimals)}%"
    except Exception:
        return "-"

def to_csv_bytes(dataframe: pd.DataFrame) -> bytes:
    csv = dataframe.to_csv(index=False, sep=";", encoding="utf-8-sig")
    return csv.encode("utf-8-sig")

def ensure_cols(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    """Garante que todas as colunas existam antes do recorte (evita KeyError)."""
    out = df.copy()
    for c in cols:
        if c not in out.columns:
            out[c] = np.nan
    return out[cols].copy()

rank = {"-": 0, "C": 1, "B": 2, "A": 3}

periods = [
    ("0-30", "Curva 0-30", "Qntd 0-30", "Fat. 0-30"),
    ("31-60", "Curva 31-60", "Qntd 31-60", "Fat. 31-60"),
    ("61-90", "Curva 61-90", "Qntd 61-90", "Fat. 61-90"),
    ("91-120", "Curva 91-120", "Qntd 91-120", "Fat. 91-120"),
]

QTY_COLS = ["Qntd 0-30", "Qntd 31-60", "Qntd 61-90", "Qntd 91-120"]
FAT_COLS = ["Fat. 0-30", "Fat. 31-60", "Fat. 61-90", "Fat. 91-120"]
CURVE_COLS = ["Curva 0-30", "Curva 31-60", "Curva 61-90", "Curva 91-120"]

# =========================
# Loaders
# =========================
@st.cache_data
def _transform_ml_raw(file) -> tuple:
    """Converte o relatorio bruto de vendas do Mercado Livre (120 dias) na estrutura 'Export'.
    Retorna: (df_export, df_logistics, df_ads)
    """

    def _seek0(f):
        try:
            f.seek(0)
        except Exception:
            pass

    def _pick_col(cols, target: str) -> str:
        if target in cols:
            return target
        for c in cols:
            sc = str(c).strip()
            if sc.startswith(target + "."):
                return c
        t = target.lower()
        for c in cols:
            if t in str(c).lower():
                return c
        raise KeyError(f"Coluna '{target}' não encontrada")

    def _try_pick_col(cols, target: str):
        try:
            return _pick_col(cols, target)
        except KeyError:
            return None

    _seek0(file)
    preview = pd.read_excel(file, sheet_name=0, header=None, nrows=80)

    header_row = None
    for i in range(min(60, len(preview))):
        row = preview.iloc[i].astype(str).str.lower()
        if row.str.contains('data da venda', na=False).any() or row.str.contains('# de anúncio', na=False).any() or row.str.contains('de anúncio', na=False).any():
            header_row = i
            break
    if header_row is None:
        header_row = 0

    _seek0(file)
    df = pd.read_excel(file, sheet_name=0, header=header_row)
    df.columns = [str(c).strip() for c in df.columns]

    col_data = _pick_col(df.columns, 'Data da venda')
    col_unid = _pick_col(df.columns, 'Unidades')

    try:
        col_rec = _pick_col(df.columns, 'Receita por produtos (BRL)')
    except Exception:
        col_rec = _pick_col(df.columns, 'Receita por produtos')

    col_mlb = _pick_col(df.columns, '# de anúncio')
    col_sku = _try_pick_col(df.columns, 'SKU')
    col_tit = _pick_col(df.columns, 'Título do anúncio')
    col_log = _pick_col(df.columns, 'Forma de entrega')
    
    # Nova coluna: Venda por publicidade (nome correto do ML)
    col_ads = None
    ads_variations = [
        'Venda por publicidade',  # Nome correto do ML
        'Venda por Publicidade',
        'Vendas por Publicidade',
        'Vendas por publicidade', 
        'vendas por publicidade',
        'venda por publicidade',
        'Publicidade',
        'publicidade',
    ]
    for var in ads_variations:
        col_ads = _try_pick_col(df.columns, var)
        if col_ads is not None:
            break
    
    # Se ainda não encontrou, busca parcial por "publicidade"
    if col_ads is None:
        for c in df.columns:
            c_lower = str(c).lower().strip()
            if 'publicidade' in c_lower:
                col_ads = c
                break

    use_cols = [col_data, col_unid, col_rec, col_mlb, col_tit, col_log]
    if col_sku is not None:
        use_cols.insert(4, col_sku)
    if col_ads is not None:
        use_cols.append(col_ads)

    base = df[use_cols].copy()

    # Renomear colunas
    if col_sku is None and col_ads is None:
        base.columns = ['data', 'unidades', 'receita', 'mlb', 'titulo', 'logistica']
        base['sku'] = ''
        base['ads'] = ''
    elif col_sku is None and col_ads is not None:
        base.columns = ['data', 'unidades', 'receita', 'mlb', 'titulo', 'logistica', 'ads']
        base['sku'] = ''
    elif col_sku is not None and col_ads is None:
        base.columns = ['data', 'unidades', 'receita', 'mlb', 'sku', 'titulo', 'logistica']
        base['ads'] = ''
    else:
        base.columns = ['data', 'unidades', 'receita', 'mlb', 'sku', 'titulo', 'logistica', 'ads']

    base['mlb'] = base['mlb'].astype(str).str.strip()
    base['sku'] = base['sku'].astype(str).str.strip()
    base['titulo'] = base['titulo'].astype(str).str.strip()
    base['logistica'] = base['logistica'].astype(str).str.strip()
    base['ads'] = base['ads'].astype(str).str.strip().str.lower()

    empty_mlb = base['mlb'].isin(['', 'nan', 'none', 'None', 'NaN'])
    if empty_mlb.any():
        base.loc[empty_mlb, 'mlb'] = base.loc[empty_mlb, 'sku']

    base['_data_raw'] = base['data'].astype(str)
    base['data'] = pd.to_datetime(base['_data_raw'], errors='coerce', dayfirst=True)

    if base['data'].notna().sum() == 0:
        s = base['_data_raw'].astype(str)
        for fmt in ('%d/%m/%Y %H:%M:%S', '%d/%m/%Y %H:%M', '%d/%m/%Y'):
            tmp = pd.to_datetime(s, errors='coerce', format=fmt)
            if tmp.notna().sum() > 0:
                base['data'] = tmp
                break

    if base['data'].notna().sum() == 0:
        month_map = {
            'janeiro': '01', 'fevereiro': '02', 'março': '03', 'marco': '03',
            'abril': '04', 'maio': '05', 'junho': '06', 'julho': '07',
            'agosto': '08', 'setembro': '09', 'outubro': '10',
            'novembro': '11', 'dezembro': '12',
        }
        s = base['_data_raw'].astype(str).str.lower()
        s = s.str.replace('hs.', '', regex=False).str.replace('hs', '', regex=False)
        for name, num in month_map.items():
            s = s.str.replace(rf'\b{name}\b', num, regex=True)
        s = s.str.replace(r'\s*de\s*', '/', regex=True)
        s = s.str.replace(r'\s+', ' ', regex=True).str.strip()
        tmp = pd.to_datetime(s, errors='coerce', dayfirst=True)
        if tmp.notna().sum() > 0:
            base['data'] = tmp

    base = base.drop(columns=['_data_raw'], errors='ignore')
    base = base.dropna(subset=['data'])
    base = base[~base['mlb'].isin(['', 'nan', 'none', 'None', 'NaN'])].copy()

    base['unidades'] = pd.to_numeric(base['unidades'], errors='coerce').fillna(0).astype(int)

    rec = base['receita']
    if rec.dtype == object:
        rec = (rec.astype(str)
                 .str.replace('\u00a0', '', regex=False)
                 .str.replace('.', '', regex=False)
                 .str.replace(',', '.', regex=False))
    base['receita'] = pd.to_numeric(rec, errors='coerce').fillna(0.0)

    if base.empty:
        cols = ['MLB','Título'] + [f'Qntd {p}' for p in ['0-30','31-60','61-90','91-120']] + [f'Fat. {p}' for p in ['0-30','31-60','61-90','91-120']] + [f'Curva {p}' for p in ['0-30','31-60','61-90','91-120']]
        empty_df = pd.DataFrame(columns=cols)
        empty_log = pd.DataFrame(columns=['periodo', 'full_pct', 'correios_pct', 'flex_pct', 'outros_pct', 'full_qty', 'correios_qty', 'flex_qty', 'outros_qty'])
        empty_ads = pd.DataFrame(columns=['periodo', 'ads_pct', 'organic_pct', 'ads_qty', 'organic_qty'])
        return empty_df, empty_log, empty_ads

    ref = base['data'].max()
    base['dias'] = (ref - base['data']).dt.days

    def bucket(d):
        if d <= 30:
            return '0-30'
        if d <= 60:
            return '31-60'
        if d <= 90:
            return '61-90'
        if d <= 120:
            return '91-120'
        return None

    base['periodo'] = base['dias'].apply(bucket)
    base = base.dropna(subset=['periodo'])

    # Classificar logística
    log_lower = base['logistica'].str.lower()
    base['is_full'] = log_lower.str.contains('full', na=False)
    base['is_correios'] = log_lower.str.contains('correios', na=False) | log_lower.str.contains('pontos', na=False) | log_lower.str.contains('ponto de envio', na=False)
    base['is_flex'] = log_lower.str.contains('flex', na=False)
    base['is_outros'] = ~(base['is_full'] | base['is_correios'] | base['is_flex'])
    
    # Classificar vendas por publicidade: "Sim" = venda via Ads, Vazio/outros = Orgânica
    # Normaliza valores e verifica se é "sim" ou variações
    ads_lower = base['ads'].astype(str).str.strip().str.lower()
    base['is_ads'] = ads_lower.isin(['sim', 's', 'yes', 'y', '1', 'true', 'si'])
    
    # Debug: contar quantos Ads foram encontrados
    ads_count = base['is_ads'].sum()
    total_count = len(base)
    # st.write(f"DEBUG: {ads_count} vendas via Ads de {total_count} total")

    # Agregar por período para logística
    logistics_data = []
    ads_data = []
    
    for periodo in ['0-30', '31-60', '61-90', '91-120']:
        periodo_df = base[base['periodo'] == periodo]
        total_qty = int(periodo_df['unidades'].sum())
        
        if total_qty > 0:
            full_qty = int(periodo_df[periodo_df['is_full']]['unidades'].sum())
            correios_qty = int(periodo_df[periodo_df['is_correios']]['unidades'].sum())
            flex_qty = int(periodo_df[periodo_df['is_flex']]['unidades'].sum())
            outros_qty = int(periodo_df[periodo_df['is_outros']]['unidades'].sum())
            
            logistics_data.append({
                'periodo': periodo,
                'full_pct': (full_qty / total_qty) * 100,
                'correios_pct': (correios_qty / total_qty) * 100,
                'flex_pct': (flex_qty / total_qty) * 100,
                'outros_pct': (outros_qty / total_qty) * 100,
                'full_qty': full_qty,
                'correios_qty': correios_qty,
                'flex_qty': flex_qty,
                'outros_qty': outros_qty,
                'total_qty': total_qty
            })
            
            # Vendas por publicidade
            ads_qty = int(periodo_df[periodo_df['is_ads']]['unidades'].sum())
            organic_qty = total_qty - ads_qty
            
            ads_data.append({
                'periodo': periodo,
                'ads_pct': (ads_qty / total_qty) * 100,
                'organic_pct': (organic_qty / total_qty) * 100,
                'ads_qty': ads_qty,
                'organic_qty': organic_qty,
                'total_qty': total_qty
            })
        else:
            logistics_data.append({
                'periodo': periodo,
                'full_pct': 0, 'correios_pct': 0, 'flex_pct': 0, 'outros_pct': 0,
                'full_qty': 0, 'correios_qty': 0, 'flex_qty': 0, 'outros_qty': 0, 'total_qty': 0
            })
            ads_data.append({
                'periodo': periodo,
                'ads_pct': 0, 'organic_pct': 0, 'ads_qty': 0, 'organic_qty': 0, 'total_qty': 0
            })

    df_logistics = pd.DataFrame(logistics_data)
    df_ads = pd.DataFrame(ads_data)

    # Agregação para export
    agg_total = base.groupby(['mlb','titulo','periodo'], as_index=False).agg(
        unidades=('unidades','sum'),
        receita=('receita','sum'),
    )

    agg_full = base[base['is_full']].groupby(['mlb','titulo','periodo'], as_index=False).agg(
        unidades_full=('unidades','sum'),
        receita_full=('receita','sum'),
    )

    agg = agg_total.merge(agg_full, on=['mlb','titulo','periodo'], how='left')
    agg['unidades_full'] = agg['unidades_full'].fillna(0).astype(int)
    agg['receita_full'] = agg['receita_full'].fillna(0.0)

    out_q = agg.pivot_table(index=['mlb','titulo'], columns='periodo', values='unidades', aggfunc='sum', fill_value=0)
    out_f = agg.pivot_table(index=['mlb','titulo'], columns='periodo', values='receita', aggfunc='sum', fill_value=0.0)
    out_qf = agg.pivot_table(index=['mlb','titulo'], columns='periodo', values='unidades_full', aggfunc='sum', fill_value=0)
    out_ff = agg.pivot_table(index=['mlb','titulo'], columns='periodo', values='receita_full', aggfunc='sum', fill_value=0.0)

    out = out_q.reset_index().rename(columns={'mlb':'MLB','titulo':'Título'})

    for p in ['0-30','31-60','61-90','91-120']:
        out[f'Qntd {p}'] = out_q[p].values if p in out_q.columns else 0
        out[f'Fat. {p}'] = out_f[p].values if p in out_f.columns else 0.0

        q_full = out_qf[p].values if p in out_qf.columns else 0
        f_full = out_ff[p].values if p in out_ff.columns else 0.0

        q_tot = out[f'Qntd {p}'].replace(0, np.nan)
        f_tot = out[f'Fat. {p}'].replace(0, np.nan)

        out[f'Share Full Qtd {p}'] = (q_full / q_tot).fillna(0.0)
        out[f'Share Full Fat {p}'] = (f_full / f_tot).fillna(0.0)
        out[f'Logística dom {p}'] = np.where(out[f'Share Full Qtd {p}'] >= 0.5, 'FULL', 'NÃO FULL')

    def curva_abc(fat_series: pd.Series) -> pd.Series:
        fat = fat_series.fillna(0.0)
        total = float(fat.sum())
        if total <= 0:
            return pd.Series(['-'] * len(fat), index=fat.index)
        order = fat.sort_values(ascending=False)
        cum = order.cumsum() / total
        curve = pd.Series(index=order.index, dtype=object)
        curve.loc[cum <= 0.80] = 'A'
        curve.loc[(cum > 0.80) & (cum <= 0.95)] = 'B'
        curve.loc[cum > 0.95] = 'C'
        curve.loc[order == 0] = '-'
        return curve.reindex(fat.index).fillna('-')

    for p in ['0-30','31-60','61-90','91-120']:
        out[f'Curva {p}'] = curva_abc(out[f'Fat. {p}'])

    return out, df_logistics, df_ads


@st.cache_data
def load_main(file) -> tuple:
    """Aceita planilha pronta (aba Export) OU relatorio bruto do ML.
    Retorna: (df_main, df_logistics, df_ads)
    """
    if hasattr(file, 'seek'):
        file.seek(0)

    df_logistics = pd.DataFrame()
    df_ads = pd.DataFrame()

    try:
        xls = pd.ExcelFile(file)
        sheet_names = [str(s) for s in getattr(xls, 'sheet_names', [])]
    except Exception:
        if hasattr(file, 'seek'):
            file.seek(0)
        df, df_logistics, df_ads = _transform_ml_raw(file)
    else:
        if 'Export' in sheet_names:
            if hasattr(file, 'seek'):
                file.seek(0)
            df = pd.read_excel(file, sheet_name='Export')
        else:
            if hasattr(file, 'seek'):
                file.seek(0)
            df, df_logistics, df_ads = _transform_ml_raw(file)

    for col in QTY_COLS:
        if col not in df.columns:
            df[col] = 0
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

    for col in FAT_COLS:
        if col not in df.columns:
            df[col] = 0.0
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)

    for col in CURVE_COLS:
        if col not in df.columns:
            df[col] = '-'
        df[col] = df[col].fillna('-').astype(str).str.strip()

    if 'MLB' not in df.columns:
        df['MLB'] = ''
    if 'Título' not in df.columns:
        if 'Titulo' in df.columns:
            df['Título'] = df['Titulo']
        else:
            df['Título'] = ''

    df['MLB'] = df['MLB'].astype(str).str.strip()
    df['Título'] = df['Título'].astype(str).str.strip()

    return df, df_logistics, df_ads


# =========================
# Sidebar Premium v2
# =========================
with st.sidebar:
    # Logo e título
    st.markdown(
        """
<div style="text-align: center; padding: 10px 0 20px 0;">
  <div style="font-size: 2rem; margin-bottom: 4px;">📊</div>
  <div style="font-size: 1.1rem; font-weight: 800; background: linear-gradient(135deg, #fff, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Curva ABC</div>
  <div style="font-size: 0.75rem; opacity: 0.5;">Diagnóstico & Ações</div>
</div>
        """,
        unsafe_allow_html=True,
    )

    # Seção de Upload
    st.markdown(
        """
<div class='sidebar-section'>
  <div class='sidebar-section-header'>
    <div class='sidebar-section-icon'>📁</div>
    <div>
      <div class='sidebar-section-title'>Upload de Dados</div>
      <div class='sidebar-section-desc'>Relatórios do Mercado Livre</div>
    </div>
  </div>
</div>
        """,
        unsafe_allow_html=True,
    )
    
    main_file = st.file_uploader("📈 Relatório de Vendas (120 dias)", type=["xlsx", "xls"], key="main_file", help="Arquivo exportado do Mercado Livre com dados de vendas dos últimos 120 dias")
    enrich_file = st.file_uploader("📋 Enriquecimento (opcional)", type=["xlsx", "xls", "csv"], key="enrich_file", help="Arquivo adicional com dados de custo, margem, etc.")

    st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)

    # Seção de Filtros
    st.markdown(
        """
<div class='sidebar-section'>
  <div class='sidebar-section-header'>
    <div class='sidebar-section-icon'>🎯</div>
    <div>
      <div class='sidebar-section-title'>Filtros Globais</div>
      <div class='sidebar-section-desc'>Selecione as curvas para análise</div>
    </div>
  </div>
</div>
        """,
        unsafe_allow_html=True,
    )

    curve_filter = st.multiselect(
        "Curvas 0-30",
        options=["A", "B", "C", "-"],
        default=["A", "B", "C", "-"],
        help="A = Top 80% faturamento | B = Próximos 15% | C = Últimos 5% | - = Sem vendas"
    )
    
    # Dica
    st.markdown(
        """
<div class='sidebar-tip'>
  💡 <strong>Dica:</strong> Use as curvas para focar sua análise. Curva A são seus produtos estrela!
</div>
        """,
        unsafe_allow_html=True,
    )
    
    # Versão
    st.markdown(
        """
<div class='sidebar-version'>
  Dashboard v3.1 • Manus AI
</div>
        """,
        unsafe_allow_html=True,
    )

if main_file is None:
    st.info("👆 Faça upload do relatório de vendas do Mercado Livre (120 dias) para começar.")
    st.stop()

# =========================
# Carregar dados
# =========================
df, df_logistics, df_ads = load_main(main_file)

if df.empty:
    st.warning("Nenhum dado válido encontrado no arquivo.")
    st.stop()

# Enriquecimento opcional
if enrich_file is not None:
    if hasattr(enrich_file, 'seek'):
        enrich_file.seek(0)
    try:
        if enrich_file.name.endswith('.csv'):
            enrich = pd.read_csv(enrich_file, sep=None, engine='python')
        else:
            enrich = pd.read_excel(enrich_file)
        enrich.columns = [str(c).strip() for c in enrich.columns]
        if 'MLB' in enrich.columns:
            enrich['MLB'] = enrich['MLB'].astype(str).str.strip()
            df = df.merge(enrich, on='MLB', how='left', suffixes=('', '_enrich'))
    except Exception as e:
        st.warning(f"Erro ao carregar enriquecimento: {e}")

# Filtrar por curva
df_f = df[df["Curva 0-30"].isin(curve_filter)].copy()

if df_f.empty:
    st.warning("Nenhum produto corresponde aos filtros selecionados.")
    st.stop()

# =========================
# Cálculos auxiliares
# =========================
df_f["Fat total"] = df_f[FAT_COLS].sum(axis=1)
df_f["Qtd total"] = df_f[QTY_COLS].sum(axis=1)
df_f["TM total"] = df_f.apply(lambda r: safe_div(r["Fat total"], r["Qtd total"]), axis=1)

kpi_rows = []
for p, cc, qq, ff in periods:
    fat = float(df_f[ff].sum())
    qty = int(df_f[qq].sum())
    tm = safe_div(fat, qty)
    kpi_rows.append({"Período": p, "Qtd": qty, "Faturamento": fat, "Ticket médio": tm})
kpi_df = pd.DataFrame(kpi_rows)

# =========================
# Segmentações
# =========================
anchors = df_f[
    (df_f["Curva 0-30"] == "A") &
    (df_f["Curva 31-60"].isin(["A", "B"])) &
    (df_f["Curva 61-90"].isin(["A", "B"]))
].sort_values("Fat total", ascending=False).copy()

inactivate = df_f[
    (df_f["Qntd 0-30"] == 0) &
    (df_f["Qntd 31-60"] == 0) &
    (df_f["Qntd 61-90"] == 0)
].sort_values("Fat total", ascending=False).copy()

revitalize = df_f[
    (df_f["Curva 31-60"].isin(["A", "B"])) &
    (df_f["Curva 0-30"].isin(["C", "-"]))
].sort_values("Fat total", ascending=False).copy()

rise_to_A = df_f[
    (df_f["Curva 31-60"].isin(["B", "C"])) &
    (df_f["Curva 0-30"] == "A")
].sort_values("Fat total", ascending=False).copy()

opp_50_60 = df_f[
    (df_f["Curva 0-30"] == "B") &
    (df_f["Qntd 0-30"] >= df_f["Qntd 31-60"] * 1.1)
].sort_values("Fat total", ascending=False).copy()

dead_stock_combo = df_f[
    (df_f["Curva 0-30"] == "-") &
    (df_f["Fat total"] > 0)
].sort_values("TM total", ascending=False).copy()

drop_alert = df_f[
    (df_f["Curva 31-60"].isin(["A", "B"])) &
    (df_f["Curva 0-30"].isin(["C", "-"]))
].copy()

if len(drop_alert) > 0:
    drop_alert["Fat anterior ref"] = drop_alert[["Fat. 31-60", "Fat. 61-90"]].max(axis=1)
    drop_alert["Perda estimada"] = drop_alert["Fat anterior ref"] - drop_alert["Fat. 0-30"]
    drop_alert = drop_alert.sort_values("Perda estimada", ascending=False)

# =========================
# Plano tático
# =========================
plan = df_f.copy()

def suggest_action(row):
    c0, c1 = row["Curva 0-30"], row["Curva 31-60"]
    if c0 == "A" and c1 in ["A", "B"]:
        return "Manter estoque e conversão"
    if c0 == "A" and c1 in ["C", "-"]:
        return "Subiu rápido – validar se é sazonal"
    if c0 == "B" and c1 == "A":
        return "Caiu de A para B – investigar"
    if c0 == "B" and c1 in ["B", "C"]:
        return "Estável ou subindo – monitorar"
    if c0 == "C":
        return "Avaliar promoção ou combo"
    if c0 == "-":
        return "Sem giro – considerar liquidar"
    return "-"

plan["Ação sugerida"] = plan.apply(suggest_action, axis=1)

actions = pd.DataFrame(index=plan.index)
actions["15d"] = "-"
actions["30d"] = "-"

actions.loc[anchors.index, "15d"] = "Verificar estoque e buybox"
actions.loc[anchors.index, "30d"] = "Manter posição e monitorar concorrência"

actions.loc[drop_alert.index, "15d"] = "Revisar preço e anúncio"
actions.loc[drop_alert.index, "30d"] = "Testar promoção ou ads"

actions.loc[revitalize.index, "15d"] = "Checar estoque e reativar"
actions.loc[revitalize.index, "30d"] = "Monitorar recuperação"

actions.loc[rise_to_A.index, "15d"] = "Garantir estoque"
actions.loc[rise_to_A.index, "30d"] = "Escalar se margem ok"

actions.loc[opp_50_60.index, "15d"] = "Testar ads ou destaque"
actions.loc[opp_50_60.index, "30d"] = "Avaliar promoção para A"

actions.loc[dead_stock_combo.index, "15d"] = "Montar combo ou kit"
actions.loc[dead_stock_combo.index, "30d"] = "Liquidar se não girar"

actions.loc[inactivate.index, "15d"] = "Pausar anúncio"
actions.loc[inactivate.index, "30d"] = "Remover do catálogo"

plan["Plano 15 dias"] = actions.iloc[:, 0] if actions.shape[1] >= 1 else "-"
plan["Plano 30 dias"] = actions.iloc[:, 2] if actions.shape[1] >= 3 else "-"

def frente_bucket(idx):
    if idx in anchors.index:
        return "DEFESA"
    if idx in drop_alert.index:
        return "CORREÇÃO"
    if idx in revitalize.index:
        return "CORREÇÃO"
    if idx in rise_to_A.index or idx in opp_50_60.index:
        return "ATAQUE"
    if idx in dead_stock_combo.index or idx in inactivate.index:
        return "LIMPEZA"
    return "OTIMIZAÇÃO"

plan["Frente"] = [frente_bucket(i) for i in plan.index]

# =========================
# Diagnóstico macro
# =========================
dist_0_30 = df_f["Curva 0-30"].value_counts().reindex(["A", "B", "C", "-"]).fillna(0).astype(int)
dist_0_30_df = pd.DataFrame({"Curva": dist_0_30.index, "Anúncios": dist_0_30.values})

fat_0_30_total = float(df_f["Fat. 0-30"].sum())
fat_0_30_A = float(df_f.loc[df_f["Curva 0-30"] == "A", "Fat. 0-30"].sum())
conc_A_0_30 = safe_div(fat_0_30_A, fat_0_30_total)

tm_0_30 = float(kpi_df.loc[kpi_df["Período"] == "0-30", "Ticket médio"].iloc[0])
tm_31_60 = float(kpi_df.loc[kpi_df["Período"] == "31-60", "Ticket médio"].iloc[0])
tm_61_90 = float(kpi_df.loc[kpi_df["Período"] == "61-90", "Ticket médio"].iloc[0])

def tm_direction(a, b, c):
    if np.isnan(a) or np.isnan(b) or np.isnan(c):
        return "Sem dados suficientes para leitura do ticket médio."
    if a < b < c:
        return "📈 Ticket médio subindo. Ajuda margem, mas pode cair volume se preço esticar."
    if a > b > c:
        return "📉 Ticket médio caindo. Pode ser mix mais barato ou promoções."
    if b < a and c > b:
        return "🔄 Ticket caiu e depois recuperou."
    if b > a and c < b:
        return "⚡ Ticket subiu e depois caiu."
    return "📊 Ticket oscilando. Vale cruzar com mix e concorrência."

tm_reading = tm_direction(tm_0_30, tm_31_60, tm_61_90)

# =========================
# KPIs topo
# =========================
total_ads = len(df_f)
tt_fat = float(df_f[FAT_COLS].sum().sum())
tt_qty = int(df_f[QTY_COLS].sum().sum())

# Renderiza métricas principais
render_metric_grid([
    ("Total de Anúncios", br_int(total_ads), "📦", "purple"),
    ("Faturamento Total", br_money(tt_fat), "💰", "green"),
    ("Quantidade Total", br_int(tt_qty), "📊", "blue"),
    ("Ticket Médio", br_money(safe_div(tt_fat, tt_qty) if tt_qty else 0.0), "🎯", "amber"),
])

st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(
    ["📊 Dashboard", "📥 Listas e Exportação", "📋 Plano Tático", "📈 Relatório Estratégico"]
)

# =========================
# TAB 1: Dashboard
# =========================
with tab1:
    # Seletor de período
    st.markdown(
        """
<div class="period-selector">
  <div class="period-label">📅 Selecione o Período para Análise</div>
</div>
        """,
        unsafe_allow_html=True,
    )
    
    selected_period = st.selectbox(
        "Período",
        options=["0-30", "31-60", "61-90", "91-120"],
        index=0,
        label_visibility="collapsed"
    )
    
    # Mapear colunas baseado no período selecionado
    period_map = {
        "0-30": ("Curva 0-30", "Qntd 0-30", "Fat. 0-30"),
        "31-60": ("Curva 31-60", "Qntd 31-60", "Fat. 31-60"),
        "61-90": ("Curva 61-90", "Qntd 61-90", "Fat. 61-90"),
        "91-120": ("Curva 91-120", "Qntd 91-120", "Fat. 91-120"),
    }
    
    curve_col, qty_col, fat_col = period_map[selected_period]
    
    # Métricas do período selecionado
    period_fat = float(df_f[fat_col].sum())
    period_qty = int(df_f[qty_col].sum())
    period_tm = safe_div(period_fat, period_qty)
    
    # Distribuição de curvas do período
    dist_period = df_f[curve_col].value_counts().reindex(["A", "B", "C", "-"]).fillna(0).astype(int)
    dist_period_df = pd.DataFrame({"Curva": dist_period.index, "Anúncios": dist_period.values})
    
    # Métricas do período
    render_metric_grid([
        (f"Faturamento {selected_period}", br_money(period_fat), "💰", "green"),
        (f"Quantidade {selected_period}", br_int(period_qty), "📦", "blue"),
        (f"Ticket Médio {selected_period}", br_money(period_tm), "🎯", "amber"),
        (f"Curva A ({selected_period})", br_int(dist_period.get("A", 0)), "⭐", "purple"),
    ])

    left, right = st.columns([1.2, 1])

    with left:
        section_header("Resumo por Período", "Visão consolidada das 4 janelas de tempo", "📅", "purple")
        show = kpi_df.copy()
        show["Qtd"] = show["Qtd"].map(br_int)
        show["Faturamento"] = show["Faturamento"].map(br_money)
        show["Ticket médio"] = show["Ticket médio"].apply(lambda x: br_money(x) if pd.notna(x) else "-")
        
        # Destacar período selecionado
        st.dataframe(show, use_container_width=True, hide_index=True, height=220)
        section_footer()

    with right:
        section_header(f"Distribuição de Curvas ({selected_period})", f"Período selecionado: {selected_period} dias", "🎯", "blue")
        colors_map = {"A": "#22c55e", "B": "#3b82f6", "C": "#f59e0b", "-": "#6b7280"}
        fig = px.bar(
            dist_period_df, 
            x="Curva", 
            y="Anúncios",
            color="Curva",
            color_discrete_map=colors_map
        )
        fig.update_layout(
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=20, b=20),
            font=dict(color='#9ca3af')
        )
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)
        section_footer()

    # Seção de Logística com todas as formas de entrega
    if not df_logistics.empty:
        log_row = df_logistics[df_logistics['periodo'] == selected_period]
        if not log_row.empty:
            log_row = log_row.iloc[0]
            render_logistics_section(
                full_pct=log_row['full_pct'],
                correios_pct=log_row['correios_pct'],
                flex_pct=log_row['flex_pct'],
                outros_pct=log_row['outros_pct'],
                period=selected_period
            )
    else:
        # Fallback para cálculo antigo se não tiver dados de logística
        if all(c in df_f.columns for c in [f"Share Full Qtd {selected_period}", f"Share Full Fat {selected_period}"]):
            section_header(f"Logística no Período {selected_period}", "Distribuição FULL vs NÃO FULL", "🚚", "cyan")
            qtd_total = float(df_f[qty_col].sum())
            fat_total = float(df_f[fat_col].sum())
            share_full_qtd = (
                (df_f[qty_col] * df_f[f"Share Full Qtd {selected_period}"]).sum() / qtd_total
                if qtd_total > 0 else 0.0
            )
            share_full_fat = (
                (df_f[fat_col] * df_f[f"Share Full Fat {selected_period}"]).sum() / fat_total
                if fat_total > 0 else 0.0
            )
            dom = "FULL" if share_full_qtd >= 0.5 else "NÃO FULL"
            
            render_metric_grid([
                ("FULL por Quantidade", pct(share_full_qtd, 1), "📦", "cyan"),
                ("FULL por Faturamento", pct(share_full_fat, 1), "💵", "green"),
                ("Logística Dominante", dom, "🏆", "purple" if dom == "FULL" else "amber"),
            ])
            section_footer()

    # Seção de Vendas por Publicidade
    if not df_ads.empty:
        ads_row = df_ads[df_ads['periodo'] == selected_period]
        if not ads_row.empty:
            ads_row = ads_row.iloc[0]
            render_ads_section(
                ads_pct=ads_row['ads_pct'],
                organic_pct=ads_row['organic_pct'],
                ads_qty=int(ads_row['ads_qty']),
                organic_qty=int(ads_row['organic_qty']),
                period=selected_period
            )

    section_header("Faturamento por Curva e Período", "Comparativo entre as janelas de tempo", "📊", "green")
    rev_rows = []
    for p, cc, qq, ff in periods:
        grp = df_f.groupby(cc)[ff].sum()
        for curva in ["A", "B", "C", "-"]:
            rev_rows.append({"Período": p, "Curva": curva, "Faturamento": float(grp.get(curva, 0.0))})
    rev_df = pd.DataFrame(rev_rows)
    fig2 = px.bar(
        rev_df, 
        x="Período", 
        y="Faturamento", 
        color="Curva", 
        barmode="group",
        color_discrete_map=colors_map
    )
    fig2.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=20, b=20),
        font=dict(color='#9ca3af'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig2, use_container_width=True)
    section_footer()

    section_header("Evolução do Ticket Médio", "Tendência ao longo dos períodos", "📈", "amber")
    tm_df = kpi_df.copy()
    tm_df["Ticket médio"] = tm_df["Ticket médio"].fillna(0.0)
    fig3 = px.line(
        tm_df, 
        x="Período", 
        y="Ticket médio", 
        markers=True
    )
    fig3.update_traces(line_color='#f59e0b', marker_color='#fbbf24', line_width=3, marker_size=10)
    fig3.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=20, b=20),
        font=dict(color='#9ca3af')
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.info(tm_reading)
    section_footer()

    st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)
    
    section_header("Ações por Frente", "Visão estratégica das prioridades", "🎯", "rose")
    
    def _front_agg(df_seg: pd.DataFrame):
        if df_seg is None or len(df_seg) == 0:
            return 0, 0.0
        fat_col_agg = "Fat. 0-30" if "Fat. 0-30" in df_seg.columns else ("Fat total" if "Fat total" in df_seg.columns else None)
        fat = float(df_seg[fat_col_agg].sum()) if fat_col_agg else 0.0
        return int(len(df_seg)), fat

    crescimento = pd.concat([ensure_cols(rise_to_A, plan.columns), ensure_cols(opp_50_60, plan.columns)], ignore_index=True)
    crescimento = crescimento.drop_duplicates(subset=[c for c in ["MLB", "SKU", "# de anúncio", "Título"] if c in crescimento.columns])

    col1, col2 = st.columns(2)
    
    with col1:
        itens, fat = _front_agg(anchors)
        render_front_card("🛡️", "Defesa - Âncoras", "Proteja estoque e conversão", itens, fat, "defense", "ancoras.csv", anchors)
        
        itens, fat = _front_agg(drop_alert)
        render_front_card("⚠️", "Correção - Fuga de Receita", "Produtos que caíram", itens, fat, "correction", "fuga_de_receita.csv", drop_alert)

    with col2:
        itens, fat = _front_agg(crescimento)
        render_front_card("🚀", "Ataque - Crescimento", "Produtos em ascensão", itens, fat, "attack", "crescimento.csv", crescimento)
        
        itens, fat = _front_agg(inactivate)
        render_front_card("🧹", "Limpeza - Parados", "Produtos para cortar ou liquidar", itens, fat, "cleanup", "parados_inativar.csv", inactivate)

    section_footer()

# =========================
# TAB 2: Listas e Exportação (MELHORADA)
# =========================
with tab2:
    st.markdown(render_report_section("📥", "Central de Exportação", "Baixe listas segmentadas para ação imediata", "blue"), unsafe_allow_html=True)
    
    # Dica
    st.markdown(
        """
<div class='insight-card'>
  <div class='insight-icon'>💡</div>
  <div class='insight-title'>Dica de Uso</div>
  <div class='insight-text'>Baixe a lista, preencha custo/margem/ads nela, junte tudo num único arquivo de enriquecimento e suba no upload opcional da sidebar para análises mais completas.</div>
</div>
        """,
        unsafe_allow_html=True
    )

    extra_cols = []
    for c in [
        "custo_unitario", "margem_percentual", "investimento_ads",
        "tacos_0_30", "roas_0_30",
        "lucro_bruto_estimado_0_30", "lucro_pos_ads_0_30", "margem_pos_ads_%_0_30",
        "risco_lucro"
    ]:
        if c in df_f.columns:
            extra_cols.append(c)

    def enrich_df(base_df: pd.DataFrame) -> pd.DataFrame:
        if not extra_cols:
            return base_df.copy()
        return base_df.merge(
            df_f[["MLB"] + extra_cols].drop_duplicates("MLB"),
            on="MLB",
            how="left"
        )

    anchors_export = enrich_df(anchors.copy())
    inactivate_export = enrich_df(inactivate.copy())
    revitalize_export = enrich_df(revitalize.copy())
    opp_export = enrich_df(opp_50_60.copy())
    drop_export = enrich_df(drop_alert.copy())
    combo_export = enrich_df(dead_stock_combo.copy())

    anchors_cols = ["MLB","Título","Fat total","Qtd total","TM total","Curva 0-30","Curva 31-60","Curva 61-90","Curva 91-120"] + extra_cols
    inactivate_cols = ["MLB","Título","Fat total","Qtd total","Curva 0-30","Qntd 0-30","Qntd 31-60","Qntd 61-90"] + extra_cols
    revitalize_cols = ["MLB","Título","Fat total","Qtd total","Curva 31-60","Curva 0-30","Qntd 31-60","Qntd 0-30"] + extra_cols
    opp_cols = ["MLB","Título","Fat total","Curva 0-30","Qntd 0-30","Curva 31-60","Qntd 31-60"] + extra_cols
    drop_cols = ["MLB","Título","Curva 31-60","Curva 61-90","Curva 0-30","Fat anterior ref","Fat. 0-30","Perda estimada"] + extra_cols
    combo_cols = ["MLB","Título","TM histórico","Fat. 31-60","Fat. 61-90","Fat. 91-120","Fat. 0-30"] + extra_cols

    anchors_export = ensure_cols(anchors_export, anchors_cols)
    inactivate_export = ensure_cols(inactivate_export, inactivate_cols)
    revitalize_export = ensure_cols(revitalize_export, revitalize_cols)
    opp_export = ensure_cols(opp_export, opp_cols)
    drop_export = ensure_cols(drop_export, drop_cols)
    combo_export = ensure_cols(combo_export, combo_cols)

    # Calcular faturamentos
    def get_fat(df_exp):
        if "Fat total" in df_exp.columns:
            return float(df_exp["Fat total"].sum())
        elif "Fat. 0-30" in df_exp.columns:
            return float(df_exp["Fat. 0-30"].sum())
        return 0.0

    # Grid de cards de exportação
    st.markdown('<div class="export-grid">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(render_export_card("🛡️", "Âncoras", "Produtos estáveis em curva A", len(anchors_export), get_fat(anchors_export), "defense"), unsafe_allow_html=True)
        st.download_button("📥 Baixar CSV", data=to_csv_bytes(anchors_export), file_name="ancoras.csv", mime="text/csv", key="exp_anc", use_container_width=True)
    
    with col2:
        st.markdown(render_export_card("⚠️", "Fuga de Receita", "Produtos que caíram de curva", len(drop_export), get_fat(drop_export), "correction"), unsafe_allow_html=True)
        st.download_button("📥 Baixar CSV", data=to_csv_bytes(drop_export), file_name="fuga_receita.csv", mime="text/csv", key="exp_drop", use_container_width=True)
    
    with col3:
        st.markdown(render_export_card("🚀", "Crescimento", "Produtos em ascensão", len(opp_export), get_fat(opp_export), "attack"), unsafe_allow_html=True)
        st.download_button("📥 Baixar CSV", data=to_csv_bytes(opp_export), file_name="crescimento.csv", mime="text/csv", key="exp_opp", use_container_width=True)

    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.markdown(render_export_card("🧹", "Inativar", "Produtos sem giro", len(inactivate_export), get_fat(inactivate_export), "cleanup"), unsafe_allow_html=True)
        st.download_button("📥 Baixar CSV", data=to_csv_bytes(inactivate_export), file_name="inativar.csv", mime="text/csv", key="exp_ina", use_container_width=True)
    
    with col5:
        st.markdown(render_export_card("🔄", "Revitalizar", "Produtos para recuperar", len(revitalize_export), get_fat(revitalize_export), "opportunity"), unsafe_allow_html=True)
        st.download_button("📥 Baixar CSV", data=to_csv_bytes(revitalize_export), file_name="revitalizar.csv", mime="text/csv", key="exp_rev", use_container_width=True)
    
    with col6:
        st.markdown(render_export_card("🎁", "Combos/Liquidação", "Produtos para kits", len(combo_export), get_fat(combo_export), "combo"), unsafe_allow_html=True)
        st.download_button("📥 Baixar CSV", data=to_csv_bytes(combo_export), file_name="combos.csv", mime="text/csv", key="exp_combo", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Preview expandido
    st.markdown('<div style="height:1.5rem"></div>', unsafe_allow_html=True)
    
    with st.expander("👀 Prévia: Fuga de Receita (Top 20 por perda estimada)", expanded=False):
        show = drop_export.head(20).copy()
        show["Fat anterior ref"] = show["Fat anterior ref"].apply(lambda x: br_money(float(x)) if pd.notna(x) else "-")
        show["Fat. 0-30"] = show["Fat. 0-30"].apply(lambda x: br_money(float(x)) if pd.notna(x) else "-")
        show["Perda estimada"] = show["Perda estimada"].apply(lambda x: br_money(float(x)) if pd.notna(x) else "-")
        if "tacos_0_30" in show.columns:
            show["tacos_0_30"] = show["tacos_0_30"].apply(lambda x: f"{round(float(x)*100,2)}%" if pd.notna(x) else "-")
        if "lucro_pos_ads_0_30" in show.columns:
            show["lucro_pos_ads_0_30"] = show["lucro_pos_ads_0_30"].apply(lambda x: br_money(float(x)) if pd.notna(x) else "-")
        st.dataframe(show, use_container_width=True, hide_index=True, height=450)

    with st.expander("🛡️ Prévia: Âncoras (Top 20 por faturamento)", expanded=False):
        show = anchors_export.head(20).copy()
        show["Fat total"] = show["Fat total"].apply(lambda x: br_money(float(x)) if pd.notna(x) else "-")
        show["TM total"] = show["TM total"].apply(lambda x: br_money(float(x)) if pd.notna(x) else "-")
        st.dataframe(show, use_container_width=True, hide_index=True, height=450)

    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# TAB 3: Plano Tático (MELHORADA v2)
# =========================
with tab3:
    st.markdown(render_report_section("📋", "Plano Tático por Produto", "Ações detalhadas para 15 e 30 dias", "purple"), unsafe_allow_html=True)

    # Contagem de frentes para exibir nos botões
    fronts = sorted(plan["Frente"].unique().tolist())
    all_front_counts = plan["Frente"].value_counts()
    
    # Container de filtros premium
    st.markdown(f"""
<div class="filter-container">
  <div class="filter-header">
    <div class="filter-header-left">
      <div class="filter-icon">🎯</div>
      <div>
        <div class="filter-main-title">Central de Filtros</div>
        <div class="filter-subtitle">Refine sua análise por frente, faturamento e busca</div>
      </div>
    </div>
    <div class="filter-count">{len(plan)} produtos</div>
  </div>
</div>
    """, unsafe_allow_html=True)
    
    # Seleção de frentes com botões visuais
    st.markdown("**🎪 Selecione as Frentes:**")
    
    # Criar botões de frente com contagem
    front_cols = st.columns(5)
    front_icons = {"DEFESA": "🛡️", "CORREÇÃO": "⚠️", "ATAQUE": "🚀", "LIMPEZA": "🧹", "OTIMIZAÇÃO": "⚙️"}
    front_colors = {"DEFESA": "defense", "CORREÇÃO": "correction", "ATAQUE": "attack", "LIMPEZA": "cleanup", "OTIMIZAÇÃO": "optimization"}
    
    front_filter = []
    for i, frente in enumerate(["DEFESA", "CORREÇÃO", "ATAQUE", "LIMPEZA", "OTIMIZAÇÃO"]):
        with front_cols[i]:
            count = int(all_front_counts.get(frente, 0))
            if st.checkbox(f"{front_icons.get(frente, '📌')} {frente.title()} ({count})", value=True, key=f"front_{frente}"):
                front_filter.append(frente)
    
    st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)
    
    # Linha de filtros adicionais
    col1, col2, col3 = st.columns([1.5, 2, 1])
    
    with col1:
        st.markdown("**💰 Faturamento Mínimo:**")
        min_fat = st.number_input(
            "Fat. mínimo",
            min_value=0.0,
            value=0.0,
            step=100.0,
            label_visibility="collapsed",
            format="%.2f"
        )
    
    with col2:
        st.markdown("**🔍 Buscar Produto:**")
        text_search = st.text_input(
            "Buscar",
            value="",
            label_visibility="collapsed",
            placeholder="Digite MLB ou nome do produto..."
        )
    
    with col3:
        st.markdown("**👁️ Visualização:**")
        view_mode = st.selectbox(
            "Modo",
            ["Cards", "Tabela"],
            label_visibility="collapsed"
        )

    # Aplicar filtros
    view = plan[plan["Frente"].isin(front_filter)].copy() if front_filter else plan.copy()
    view = view[view["Fat total"] >= float(min_fat)].copy()

    if text_search:
        text_search = text_search.strip().lower()
        view = view[
            view["MLB"].astype(str).str.lower().str.contains(text_search) |
            view["Título"].astype(str).str.lower().str.contains(text_search)
        ].copy()

    # Resumo das frentes filtradas
    front_counts = view["Frente"].value_counts()
    
    st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
    
    # Métricas resumidas
    res_cols = st.columns(4)
    with res_cols[0]:
        st.metric("📦 Produtos Filtrados", f"{len(view):,}")
    with res_cols[1]:
        st.metric("💰 Fat. Total", br_money(view["Fat total"].sum()))
    with res_cols[2]:
        st.metric("📈 Qtd. Total", f"{int(view['Qtd total'].sum()):,}")
    with res_cols[3]:
        avg_tm = view["TM total"].mean() if len(view) > 0 else 0
        st.metric("💵 TM Médio", br_money(avg_tm))
    
    st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)

    cols = [
        "MLB", "Título", "Frente",
        "Curva 31-60", "Curva 0-30",
        "Qntd 31-60", "Qntd 0-30",
        "Fat. 0-30", "Fat total", "TM total",
        "Ação sugerida", "Plano 15 dias", "Plano 30 dias",
        "tacos_0_30", "roas_0_30", "lucro_pos_ads_0_30", "risco_lucro"
    ]

    view_show = ensure_cols(view.sort_values("Fat total", ascending=False), cols)

    # Botão de download
    st.download_button(
        "📥 Baixar CSV do Plano Filtrado",
        data=to_csv_bytes(view_show),
        file_name="plano_tatico.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)

    if view_mode == "Cards":
        # Visualização em cards
        for idx, row in view_show.head(20).iterrows():
            st.markdown(render_tactical_card(row.to_dict(), row.get("Frente", "OTIMIZAÇÃO")), unsafe_allow_html=True)
        
        if len(view_show) > 20:
            st.info(f"Mostrando 20 de {len(view_show)} produtos. Use os filtros para refinar ou baixe o CSV completo.")
    else:
        # Visualização em tabela
        show = view_show.copy()
        show["Fat. 0-30"] = show["Fat. 0-30"].apply(lambda x: br_money(float(x)) if pd.notna(x) else "-")
        show["Fat total"] = show["Fat total"].apply(lambda x: br_money(float(x)) if pd.notna(x) else "-")
        show["TM total"] = show["TM total"].apply(lambda x: br_money(float(x)) if pd.notna(x) else "-")
        show["tacos_0_30"] = show["tacos_0_30"].apply(lambda x: f"{round(float(x)*100,2)}%" if pd.notna(x) else "-")
        show["roas_0_30"] = show["roas_0_30"].apply(lambda x: round(float(x), 2) if pd.notna(x) else "-")
        show["lucro_pos_ads_0_30"] = show["lucro_pos_ads_0_30"].apply(lambda x: br_money(float(x)) if pd.notna(x) else "-")

        st.dataframe(show, use_container_width=True, hide_index=True, height=600)

    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# TAB 4: Relatório Estratégico (MELHORADA)
# =========================
with tab4:
    # Seção 1: Diagnóstico Macro
    st.markdown(render_report_section("🔍", "Diagnóstico Macro", "Visão geral da saúde do catálogo", "purple"), unsafe_allow_html=True)
    
    # KPIs destacados
    st.markdown(
        render_kpi_highlight([
            (br_int(total_ads), "Total de Anúncios", "purple"),
            (f"{round(float(conc_A_0_30 or 0.0) * 100, 1)}%", "Concentração Curva A", "green"),
            (br_money(tm_0_30), "Ticket Médio Atual", "amber"),
        ]),
        unsafe_allow_html=True
    )
    
    # Insight do ticket médio
    st.markdown(render_insight_card("📊", "Análise do Ticket Médio", tm_reading), unsafe_allow_html=True)
    
    # Distribuição de curvas
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Distribuição de Curvas (0-30)")
        st.dataframe(dist_0_30_df, use_container_width=True, hide_index=True, height=180)
    
    with col2:
        st.markdown("#### Evolução por Período")
        show_kpi = kpi_df.copy()
        show_kpi["Qtd"] = show_kpi["Qtd"].map(br_int)
        show_kpi["Faturamento"] = show_kpi["Faturamento"].map(br_money)
        show_kpi["Ticket médio"] = show_kpi["Ticket médio"].apply(lambda x: br_money(x) if pd.notna(x) else "-")
        st.dataframe(show_kpi, use_container_width=True, hide_index=True, height=180)

    st.markdown("</div>", unsafe_allow_html=True)

    # Seção 2: Segmentação
    st.markdown(render_report_section("📦", "Segmentação de Produtos", "Análise por categoria estratégica", "blue"), unsafe_allow_html=True)
    
    # Resumo das frentes
    front_counts_all = plan["Frente"].value_counts()
    st.markdown(
        render_front_summary([
            ("🛡️", int(front_counts_all.get("DEFESA", 0)), "Defesa"),
            ("⚠️", int(front_counts_all.get("CORREÇÃO", 0)), "Correção"),
            ("🚀", int(front_counts_all.get("ATAQUE", 0)), "Ataque"),
            ("🧹", int(front_counts_all.get("LIMPEZA", 0)), "Limpeza"),
            ("⚙️", int(front_counts_all.get("OTIMIZAÇÃO", 0)), "Otimização"),
        ]),
        unsafe_allow_html=True
    )

    # Âncoras
    st.markdown("#### 🛡️ Produtos Âncora (Top 5)")
    top5_anchors = anchors.head(5).copy()
    fat_sum_top5 = float(top5_anchors["Fat total"].sum()) if len(top5_anchors) else 0.0
    
    st.markdown(
        render_kpi_highlight([
            (br_int(len(anchors)), "Total de Âncoras", "green"),
            (br_money(fat_sum_top5), "Fat. Top 5", "blue"),
            (f"{round(len(anchors)/max(total_ads,1)*100, 1)}%", "% do Catálogo", "purple"),
        ]),
        unsafe_allow_html=True
    )

    anchor_cols = ["MLB","Título","Fat total","Qtd total","TM total"]
    show = ensure_cols(top5_anchors, anchor_cols)
    show["Fat total"] = show["Fat total"].apply(lambda x: br_money(float(x)) if pd.notna(x) else "-")
    show["Qtd total"] = show["Qtd total"].map(br_int)
    show["TM total"] = show["TM total"].apply(lambda x: br_money(float(x)) if pd.notna(x) else "-")
    st.dataframe(show, use_container_width=True, hide_index=True, height=220)

    # Fuga de receita
    st.markdown("#### ⚠️ Alerta de Fuga de Receita (Top 10)")
    loss_total = float(drop_alert["Perda estimada"].sum()) if len(drop_alert) else 0.0
    
    st.markdown(
        render_kpi_highlight([
            (br_int(len(drop_alert)), "Produtos em Fuga", "rose"),
            (br_money(loss_total), "Perda Estimada", "amber"),
            (f"{round(len(drop_alert)/max(total_ads,1)*100, 1)}%", "% do Catálogo", "purple"),
        ]),
        unsafe_allow_html=True
    )

    if len(drop_alert) > 0:
        st.markdown(
            render_insight_card("⚠️", "Atenção Imediata", 
                f"Você tem {len(drop_alert)} produtos que caíram de curva, representando uma perda estimada de {br_money(loss_total)}. Priorize a correção destes itens."),
            unsafe_allow_html=True
        )

    drop_cols_show = ["MLB","Título","Curva 31-60","Curva 0-30","Perda estimada"]
    show = ensure_cols(drop_alert.head(10), drop_cols_show)
    show["Perda estimada"] = show["Perda estimada"].apply(lambda x: br_money(float(x)) if pd.notna(x) else "-")
    st.dataframe(show, use_container_width=True, hide_index=True, height=350)

    st.markdown("</div>", unsafe_allow_html=True)

    # Seção 3: Plano Operacional
    st.markdown(render_report_section("📋", "Plano Operacional", "Distribuição de ações por frente", "green"), unsafe_allow_html=True)

    front_order = ["LIMPEZA", "CORREÇÃO", "ATAQUE", "DEFESA", "OTIMIZAÇÃO"]
    
    # Download do plano completo
    op_cols = ["Frente","MLB","Título","Curva 0-30","Fat. 0-30","Ação sugerida","Plano 15 dias","Plano 30 dias"]
    op = ensure_cols(plan, op_cols).copy()
    op = op.sort_values(["Frente", "Fat. 0-30"], ascending=[True, False])

    st.download_button(
        "📥 Baixar Plano Operacional Completo",
        data=to_csv_bytes(op),
        file_name="plano_operacional_completo.csv",
        mime="text/csv",
        use_container_width=True
    )

    # Tabelas por frente
    for fr in front_order:
        subset = op[op["Frente"] == fr].head(10).copy()
        if len(subset) == 0:
            continue
        
        icon = {"LIMPEZA": "🧹", "CORREÇÃO": "⚠️", "ATAQUE": "🚀", "DEFESA": "🛡️", "OTIMIZAÇÃO": "⚙️"}.get(fr, "📦")
        
        with st.expander(f"{icon} {fr} ({len(op[op['Frente'] == fr])} itens)", expanded=False):
            subset["Fat. 0-30"] = subset["Fat. 0-30"].apply(lambda x: br_money(float(x)) if pd.notna(x) else "-")
            st.dataframe(subset, use_container_width=True, hide_index=True, height=350)

    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown('<div style="height:2rem"></div>', unsafe_allow_html=True)
st.markdown(
    """
    <div style="text-align: center; opacity: 0.5; font-size: 0.85rem; padding: 20px 0;">
        📊 Curva ABC Dashboard v3.1 | Análise inteligente para decisões rápidas
    </div>
    """,
    unsafe_allow_html=True
)
