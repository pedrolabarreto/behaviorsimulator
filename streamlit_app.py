import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- Funções de simulação ---
def simulate_constant(init_capital, rate, years):
    periods = years * 12
    monthly_return = (1 + rate) ** (1/12) - 1
    values = init_capital * (1 + monthly_return) ** np.arange(periods + 1)
    return values

def simulate_random(init_capital, mu, sigma, years):
    periods = years * 12
    shocks = np.random.normal(mu/12, sigma/np.sqrt(12), size=periods)
    values = [init_capital]
    for r in shocks:
        values.append(values[-1] * (1 + r))
    return np.array(values)

def simulate_behavioral(init_capital, mu, sigma, years, panic_drawdown):
    volatile = simulate_random(init_capital, mu, sigma, years)
    periods = years * 12
    for i in range(1, len(volatile)):
        peak = volatile[:i+1].max()
        drawdown = (volatile[i] - peak) / peak
        if drawdown <= -panic_drawdown:
            remaining_months = periods - i
            monthly_return = (1 + mu * 0.5) ** (1/12) - 1
            cons = volatile[i] * (1 + monthly_return) ** np.arange(remaining_months + 1)
            return np.concatenate([volatile[:i+1], cons[1:]])
    return volatile

# --- Interface Streamlit ---
st.title("Portfolio Behavior Simulator")

st.sidebar.header("Parâmetros")
init_cap = st.sidebar.number_input("Capital Inicial", value=100_000)
years = st.sidebar.slider("Horizonte (anos)", min_value=5, max_value=40, value=30)
strategy = st.sidebar.selectbox("Estratégia", ("Constante", "Volátil", "Comportamental"))

if strategy == "Constante":
    rate = st.sidebar.number_input("Retorno anual (%)", value=6.0) / 100
else:
    mu = st.sidebar.number_input("Retorno anual médio (%)", value=8.0) / 100
    sigma = st.sidebar.number_input("Volatilidade anual (%)", value=15.0) / 100
    if strategy == "Comportamental":
        panic = st.sidebar.slider("Limite de drawdown (%) para pânico", min_value=5, max_value=50, value=20) / 100

trials = st.sidebar.number_input("Simulações (Monte Carlo)", min_value=1, max_value=5000, value=1)

if st.sidebar.button("Simular"):
    if trials == 1:
        # Simulação única
        if strategy == "Constante":
            series = simulate_constant(init_cap, rate, years)
        elif strategy == "Volátil":
            series = simulate_random(init_cap, mu, sigma, years)
        else:
            series = simulate_behavioral(init_cap, mu, sigma, years, panic)
        df = pd.DataFrame({"Patrimônio": series})
        df.index = pd.date_range(start="2025-01-01", periods=len(df), freq="M")
        st.line_chart(df)
        st.write(f"**Valor Final:** R$ {df.Patrimônio.iloc[-1]:,.2f}")
        max_dd = (df.Patrimônio.cummax() - df.Patrimônio).max() / df.Patrimônio.cummax().max()
        st.write(f"**Máxima Queda (drawdown):** {max_dd:.2%}")
    else:
        # Monte Carlo
        results = {"Constante": [], "Volátil": [], "Comportamental": []}
        for _ in range(trials):
            results["Constante"].append(simulate_constant(init_cap, rate, years)[-1])
            results["Volátil"].append(simulate_random(init_cap, mu, sigma, years)[-1])
            results["Comportamental"].append(simulate_behavioral(init_cap, mu, sigma, years, panic)[-1])
        # Estatísticas
        stats = {}
        for key, vals in results.items():
            arr = np.array(vals)
            stats[key] = {
                "Média": np.mean(arr),
                "Mediana": np.median(arr),
                "10º Percentil": np.percentile(arr, 10),
                "90º Percentil": np.percentile(arr, 90)
            }
        stats_df = pd.DataFrame(stats).T
        stats_df = stats_df.applymap(lambda x: f"R$ {x:,.2f}")
        st.write("### Estatísticas (Valor Final em cada simulação)")
        st.table(stats_df)

        # Boxplot comparativo
        fig, ax = plt.subplots()
        ax.boxplot([results["Constante"], results["Volátil"], results["Comportamental"]],
                   labels=["Constante", "Volátil", "Comportamental"])
        ax.set_title("Distribuição do Valor Final - Estratégias")
        st.pyplot(fig)
