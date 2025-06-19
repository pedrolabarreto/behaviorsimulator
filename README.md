# Behavior Simulator

Aplicativo Streamlit que ilustra o *Behavior Gap* — a diferença de retorno entre
o investimento buy‑and‑hold e o retorno real obtido pelos investidores quando
deixam o comportamento guiar decisões (pânico, FOMO, overtrading).

## Executando localmente

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Estrutura de pastas

```
behaviorsimulator/
├── app.py
├── requirements.txt
├── modules/
│   ├── loaders.py
│   ├── simulations.py
│   └── visuals.py
└── data/
```

## Licença
MIT
