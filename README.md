# Portfolio Behavior Simulator with Behavioral Allocation and Behavior Gap

Este projeto demonstra, via simulação numérica e Monte Carlo, como decisões de realocação baseadas em performance e drawdown afetam a evolução do patrimônio, incorporando o conceito de *behavior gap*.

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
   - Capital Inicial  
   - Horizonte (anos)  
   - Retorno Esperado (Constant % a.a.)  
   - Retorno Esperado (Volátil % a.a.)  
   - Volatilidade (% a.a.)  
   - Drawdown (% mensais)  
   - Simulações (Monte Carlo)

5. A aplicação mostra:
   - **Retorno Esperado** das partes constante e volátil.  
   - Mediana e banda 10%-90% do valor do portfólio.  
   - **Behavior Gap**: diferença entre retorno anualizado mediano e retorno constante.

## Deploy

Conecte ao Streamlit Cloud: https://share.streamlit.io  

