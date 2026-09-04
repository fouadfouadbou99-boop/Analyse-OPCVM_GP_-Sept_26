import numpy as np

def perf_ytd(current_vl, initial_vl):
    return current_vl / initial_vl - 1

def annualized_return(ytd_return, nb_days):
    return (1 + ytd_return) ** (365 / nb_days) - 1

def annualized_volatility(returns):
    return np.std(returns, ddof=1) * np.sqrt(52)

def tracking_error(fund_returns, benchmark_returns):
    active = fund_returns - benchmark_returns
    return np.std(active, ddof=1) * np.sqrt(52)

def beta(fund_returns, benchmark_returns):
    covariance = np.cov(fund_returns, benchmark_returns)[0,1]
    variance = np.var(benchmark_returns, ddof=1)
    return covariance / variance

def sharpe_ratio(annual_return, annual_vol, rf):
    return (annual_return - rf) / annual_vol

def treynor_ratio(annual_return, beta_value, rf):
    return (annual_return - rf) / beta_value

def information_ratio(
    annual_return_fund,
    annual_return_benchmark,
    tracking_error_ann
):
    return (
        annual_return_fund -
        annual_return_benchmark
    ) / tracking_error_ann
