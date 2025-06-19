import numpy as np
import pandas as pd

def behavior_gap(prices: pd.Series,
                 panic_drop: int = 20,
                 fomo_rally: int = 20,
                 trade_cost: float = 0.5):
    """Simula patrimônio de um investidor disciplinado vs. emocional.

    Disciplined: buy & hold desde o início.
    Emotional: vende quando cai X %, recompra quando sobe Y %, pagando custo de transação.

    Retorna dois vetores numpy (disciplinado, emocional).
    """
    pct_drop = panic_drop / 100
    pct_rally = fomo_rally / 100
    tc = trade_cost / 100

    # Disciplined: caminho de buy & hold normalizado
    disciplined = (prices / prices.iloc[0]).values

    invested = True
    units = 1.0 / prices.iloc[0]  # começar investido com 1.0 de capital
    cash = 0.0
    last_high = prices.iloc[0]
    last_buy = prices.iloc[0]

    emotional_vals = []

    for price in prices:
        if invested:
            # trigger panic sell
            if (price - last_high) / last_high <= -pct_drop:
                cash = units * price * (1 - tc)
                invested = False
            emotional_vals.append(units * price if invested else cash)
        else:
            # check FOMO rally to buy back
            if (price - last_buy) / last_buy >= pct_rally:
                units = cash * (1 - tc) / price
                invested = True
                last_high = price
            emotional_vals.append(units * price if invested else cash)

        # update highs/lows
        if price > last_high:
            last_high = price
        if invested:
            last_buy = price

    emotional = np.array(emotional_vals)
    return disciplined, emotional
