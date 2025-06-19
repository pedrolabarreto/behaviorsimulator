# Portfolio Behavior Simulator with Behavioral Triggers

Este projeto demonstra, via simulação numérica e Monte Carlo, como decisões de realocação baseadas em performance (ganância) e drawdown (pânico) afetam a evolução do patrimônio ao longo de décadas.

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

4. Na sidebar, defina:
   - **Capital Inicial**  
   - **Horizonte (anos)**  
   - **Retorno Constante (% a.a.)**  
   - **Retorno Volátil (% a.a.)**  
   - **Volatilidade Volátil (% a.a.)**  
   - **Drawdown para Pânico (% mensais)**  
   - **Threshold Ganância Up-Switch 1 (bps)**  
   - **Threshold Ganância Up-Switch 2 (bps)**  
   - **Simulações (Monte Carlo)**  

5. A aplicação mostra:
   - **Retorno Esperado** da parte constante e volátil  
   - **Evolução Mediana** e **Faixa 10-90%** do portfólio  
   - **Valor Final Mediano**, **Retorno Anualizado Mediano** e **Behavior Gap**  

## Deploy

Conecte ao Streamlit Cloud: https://share.streamlit.io  
