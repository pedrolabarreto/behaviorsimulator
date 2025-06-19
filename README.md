# Portfolio Behavior Simulator with Behavioral Allocation

Este projeto demonstra, via simulação numérica e Monte Carlo, como decisões de realocação baseadas em performance e drawdown afetam a evolução do patrimônio ao longo de décadas.

## Como usar

1. Clone este repositório:
   ```bash
   git clone https://github.com/SEU_USUARIO/portfolio_behavior_simulator.git
   cd portfolio_behavior_simulator
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Execute a aplicação:
   ```bash
   streamlit run streamlit_app.py
   ```

4. Acesse o link (`localhost:8501` por padrão).

## Lógica de Alocação

- **Inicial**: 50% constante / 50% volátil  
- **Up-switch 1**: +400 bps de outperformance da parte volátil → 40% constante / 60% volátil  
- **Up-switch 2**: +200 bps adicionais → 30% constante / 70% volátil  
- **Down-switch 1**: drawdown da parte volátil ≥ threshold → 80% constante / 20% volátil  
- **Down-switch 2**: segundo drawdown antes de up-switch → 90% constante / 10% volátil  
- **Down-switch 3**: terceiro drawdown → 100% constante  

## Inputs na sidebar

- Capital Inicial  
- Horizonte (anos)  
- Retorno Constante (% a.a.)  
- Retorno Volátil (% a.a.)  
- Volatilidade Volátil (% a.a.)  
- Drawdown (% para pânico)  
- Simulações (Monte Carlo)

## Deploy

Conecte ao repositório no Streamlit Cloud (https://share.streamlit.io).

