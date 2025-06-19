# Behavior Gap App

Pequeno aplicativo Streamlit para demonstrar, de forma interativa, o impacto dos vieses comportamentais
(pânico, FOMO, excesso de confiança) na construção de patrimônio de longo prazo.

## Como rodar localmente

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Ou simplesmente faça o deploy no **Streamlit Community Cloud** apontando para `app.py`.

## Estrutura

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
