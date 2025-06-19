import numpy as np
import pandas as pd

def behavior_gap(prices: pd.Series,
                 panic_drop: int,
                 fomo_rally: int,
                 trade_cost: float):
    pct_drop = panic_drop / 100
    pct_rally = fomo_rally / 100
    tc = trade_cost / 100

    disciplined = (prices / prices.iloc[0]).values

    invested = True
    units = 1.0 / prices.iloc[0]
    cash = 0.0
    last_high = last_buy = prices.iloc[0]

    emotional_vals = []
    for p in prices:
        if invested and (p - last_high) / last_high <= -pct_drop:
            cash = units * p * (1 - tc)
            invested = False
        elif (not invested) and (p - last_buy) / last_buy >= pct_rally:
            units = cash * (1 - tc) / p
            invested = True
            last_high = p
        emotional_vals.append(units * p if invested else cash)

        if p > last_high:
            last_high = p
        if invested:
            last_buy = p
    emotional = np.array(emotional_vals)
    return disciplined, emotional
