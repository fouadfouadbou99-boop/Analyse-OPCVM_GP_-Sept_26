import numpy as np
from scipy.stats import norm

def historical_var(returns, confidence=0.95):
    return np.quantile(
        returns,
        1 - confidence
    )

def max_drawdown(vls):

    vls = np.array(vls)

    peaks = np.maximum.accumulate(vls)

    drawdowns = (vls - peaks) / peaks

    return drawdowns.min()
