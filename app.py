import streamlit as st
import pandas as pd
import numpy as np
from modules.loaders import load_prices
from modules.simulations import behavior_gap
from modules.visuals import plot_paths

st.set_page_config(page_title="Behavior Gap", layout="wide")

st.title("Behavior Gap – Quanto o seu comportamento custa?")

ticker = st.selectbox("Escolha o ativo/índice:", ["SPY", "IVVB11", "BOVA11"])

st.sidebar.header("Parâmetros de comportamento")
panic_drop = st.sidebar.slider("Vende após queda (%)", 5, 50, 20)
fomo_rally = st.sidebar.slider("Recompra após alta (%)", 5, 50, 20)
trade_cost = st.sidebar.number_input("Custo por operação (%)", 0.0, 2.0, 0.5)

prices = load_prices(ticker)
disciplined, emotional = behavior_gap(prices, panic_drop, fomo_rally, trade_cost)

fig = plot_paths(disciplined, emotional, prices.index)
st.pyplot(fig, use_container_width=True)

gap = emotional[-1] / disciplined[-1] - 1
st.metric("Behavior Gap", f"{gap:.1%}")

diff = disciplined[-1] - emotional[-1]
st.markdown(f"Se você tivesse mantido disciplina, seu patrimônio seria **R$ {diff:,.0f}** maior hoje.")
