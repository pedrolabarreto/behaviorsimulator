import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- Função de simulação com triggers ---
def simulate_behavioral_allocation(init_capital, const_ret, mu, sigma, years, drawdown_thresh):
    periods = years * 12
    # monthly returns
    r_const = (1 + const_ret) ** (1/12) - 1
    r_vol = np.random.normal(mu/12, sigma/np.sqrt(12), size=periods)
    # cumulative pure strategies
    cum_const = np.ones(periods + 1)
    cum_vol = np.ones(periods + 1)
    # tracking
    peak_vol = 1.0
    up_level = 0
    down_count = 0
    # initial weights
    w_const, w_vol = 0.5, 0.5
    # portfolio value series
    value = np.zeros(periods + 1)
    value[0] = init_capital

    for t in range(1, periods + 1):
        # update pure cum returns
        cum_const[t] = cum_const[t-1] * (1 + r_const)
        cum_vol[t] = cum_vol[t-1] * (1 + r_vol[t-1])
        # update peak for vol
        peak_vol = max(peak_vol, cum_vol[t])
        # check drawdown trigger
        drawdown = (cum_vol[t] - peak_vol) / peak_vol
        if drawdown <= -drawdown_thresh and down_count < 3:
            down_count += 1
            if down_count == 1:
                w_const, w_vol = 0.8, 0.2
            elif down_count == 2:
                w_const, w_vol = 0.9, 0.1
            else:
                w_const, w_vol = 1.0, 0.0
            up_level = up_level  # no change
        # check up-switch only if no down-switch
        elif down_count == 0 and up_level < 2:
            perf_diff = cum_vol[t] - cum_const[t]
            if up_level == 0 and perf_diff >= 0.04:
                up_level = 1
                w_const, w_vol = 0.4, 0.6
            elif up_level == 1 and perf_diff >= 0.02:
                up_level = 2
                w_const, w_vol = 0.3, 0.7
        # portfolio growth
        portfolio_ret = w_const * (1 + r_const) + w_vol * (1 + r_vol[t-1])
        value[t] = value[t-1] * portfolio_ret

    return value

# --- Interface Streamlit ---
st.title("Portfolio Behavior Simulator with Allocation Triggers")

# Sidebar inputs
init_cap = st.sidebar.number_input("Capital Inicial", value=100_000)
years = st.sidebar.slider("Horizonte (anos)", 5, 40, 30)
const_ret = st.sidebar.number_input("Retorno Constante (% a.a.)", value=10.0) / 100
mu = st.sidebar.number_input("Retorno Volátil (% a.a.)", value=10.0) / 100
sigma = st.sidebar.number_input("Volatilidade Volátil (% a.a.)", value=15.0) / 100
drawdown_thresh = st.sidebar.slider("Drawdown para pânico (% mensais)", 1, 50, 5) / 100
trials = st.sidebar.number_input("Simulações (Monte Carlo)", 1, 2000, 500)

if st.sidebar.button("Simular"):
    periods = years * 12
    all_values = np.zeros((trials, periods + 1))

    for i in range(trials):
        all_values[i] = simulate_behavioral_allocation(
            init_cap, const_ret, mu, sigma, years, drawdown_thresh
        )

    # estatísticas por mês
    median_series = np.median(all_values, axis=0)
    p10 = np.percentile(all_values, 10, axis=0)
    p90 = np.percentile(all_values, 90, axis=0)
    dates = pd.date_range(start="2025-01-01", periods=periods + 1, freq="M")

    # Plot com matplotlib
    fig, ax = plt.subplots()
    ax.plot(dates, median_series, label="Mediana")
    ax.fill_between(dates, p10, p90, alpha=0.3, label="10%-90%")
    ax.set_title("Evolução do Portfólio (Mediana + Faixa 10%-90%)")
    ax.legend()
    ax.set_xlabel("Data")
    ax.set_ylabel("Valor do Portfólio")
    st.pyplot(fig)

    # valor final mediano
    st.write(f"**Valor Final Mediano:** R$ {median_series[-1]:,.2f}")
