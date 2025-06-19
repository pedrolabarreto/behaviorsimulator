import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def simulate_behavioral_triggers(init_capital, const_ret, mu, sigma, years, drawdown_thresh, up1, up2):
    periods = years * 12
    # monthly returns
    r_const = (1 + const_ret) ** (1/12) - 1
    r_vol = np.random.normal(mu/12, sigma/np.sqrt(12), size=periods)
    # cumulative pure strategies
    cum_const = np.ones(periods + 1)
    cum_vol = np.ones(periods + 1)
    # tracking variables
    peak_vol = 1.0
    up_level = 0
    down_count = 0
    # initial weights
    w_const, w_vol = 0.5, 0.5
    # portfolio values
    value = np.zeros(periods + 1)
    value[0] = init_capital

    for t in range(1, periods + 1):
        # update pure cumulative returns
        cum_const[t] = cum_const[t-1] * (1 + r_const)
        cum_vol[t] = cum_vol[t-1] * (1 + r_vol[t-1])
        # update peak for vol
        peak_vol = max(peak_vol, cum_vol[t])
        # check drawdown trigger (panic)
        drawdown = (cum_vol[t] - peak_vol) / peak_vol
        if drawdown <= -drawdown_thresh and down_count < 3:
            down_count += 1
            if down_count == 1:
                w_const, w_vol = 0.8, 0.2
            elif down_count == 2:
                w_const, w_vol = 0.9, 0.1
            else:
                w_const, w_vol = 1.0, 0.0
        # check up-switch (greed) only if no panic
        elif down_count == 0 and up_level < 2:
            perf_diff = cum_vol[t] - cum_const[t]
            if up_level == 0 and perf_diff >= up1:
                up_level = 1
                w_const, w_vol = 0.4, 0.6
            elif up_level == 1 and perf_diff >= up2:
                up_level = 2
                w_const, w_vol = 0.3, 0.7
        # update portfolio value
        portfolio_ret = w_const * (1 + r_const) + w_vol * (1 + r_vol[t-1])
        value[t] = value[t-1] * portfolio_ret

    return value

# Streamlit interface
st.title("Portfolio Behavior Simulator with Behavioral Triggers")

# Sidebar inputs
init_cap = st.sidebar.number_input("Capital Inicial", value=100_000)
years = st.sidebar.slider("Horizonte (anos)", 5, 40, 30)
const_ret = st.sidebar.number_input("Retorno Constante (% a.a.)", value=10.0) / 100
mu = st.sidebar.number_input("Retorno Volátil (% a.a.)", value=10.0) / 100
sigma = st.sidebar.number_input("Volatilidade Volátil (% a.a.)", value=15.0) / 100
drawdown_thresh = st.sidebar.slider("Drawdown para Pânico (% mensais)", 1, 50, 5) / 100
up1_bps = st.sidebar.number_input("Threshold Ganância Up-Switch 1 (bps)", value=400)
up2_bps = st.sidebar.number_input("Threshold Ganância Up-Switch 2 (bps)", value=200)
trials = st.sidebar.number_input("Simulações (Monte Carlo)", 1, 2000, 500)

# display expected returns
st.write(f"**Retorno Esperado (Constante):** {const_ret:.2%} a.a.")
st.write(f"**Retorno Esperado (Volátil):** {mu:.2%} a.a.")

if st.sidebar.button("Simular"):
    up1 = up1_bps / 10000
    up2 = up2_bps / 10000
    periods = years * 12
    all_vals = np.zeros((trials, periods + 1))
    for i in range(trials):
        all_vals[i] = simulate_behavioral_triggers(
            init_cap, const_ret, mu, sigma, years, drawdown_thresh, up1, up2
        )

    # statistics
    median_series = np.median(all_vals, axis=0)
    p10 = np.percentile(all_vals, 10, axis=0)
    p90 = np.percentile(all_vals, 90, axis=0)
    dates = pd.date_range(start="2025-01-01", periods=periods + 1, freq="M")

    # plot
    fig, ax = plt.subplots()
    ax.plot(dates, median_series, label="Mediana")
    ax.fill_between(dates, p10, p90, alpha=0.3, label="10%-90%")
    ax.set_title("Evolução do Portfólio (Mediana + Faixa 10%-90%)")
    ax.legend()
    ax.set_xlabel("Data")
    ax.set_ylabel("Valor do Portfólio")
    st.pyplot(fig)

    # results
    final_med = median_series[-1]
    st.write(f"**Valor Final Mediano:** R$ {final_med:,.2f}")
    ann_ret = (final_med / init_cap) ** (1/years) - 1
    behavior_gap = ann_ret - const_ret
    st.write(f"**Retorno Anualizado Mediano:** {ann_ret:.2%}")
    st.write(f"**Behavior Gap:** {behavior_gap:.2%}")
