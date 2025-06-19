import streamlit as st
from modules.loaders import load_prices
from modules.simulations import behavior_gap
from modules.visuals import plot_paths

st.set_page_config(page_title="Behavior Gap", layout="wide")
st.title("Behavior Gap – Quanto o comportamento custa?")

ticker = st.selectbox("Índice/ativo:", ["SPY", "IVVB11", "BOVA11"])

st.sidebar.header("Parâmetros de (mau) comportamento")
panic = st.sidebar.slider("Vende após queda (%)", 5, 50, 20)
fomo  = st.sidebar.slider("Recompra após alta (%)", 5, 50, 20)
tcost = st.sidebar.number_input("Custo por operação (%)", 0.0, 2.0, 0.5)

prices = load_prices(ticker)
disciplined, emotional = behavior_gap(prices, panic, fomo, tcost)

st.pyplot(plot_paths(disciplined, emotional, prices.index), use_container_width=True)

gap_percent = emotional[-1] / disciplined[-1] - 1
st.metric("Behavior Gap", f"{gap_percent:.1%}")

diff = disciplined[-1] - emotional[-1]
st.markdown(f"Se você tivesse mantido disciplina, seu patrimônio seria **R$ {diff:,.0f}** maior.")
