from src.data_loader import open_refinitiv_session, get_metric
from src.data_processing import consolidate_refinitiv_data, calculate_derived_metrics
from src.utils import format_dates
from src.summary import create_multi_metric_forecast_summary
from src.monte_carlo import simulate
from src.tsr import compute_tsr
from src.goals import find_equal_p
import pandas as pd
from config.historical import base, n_simulations
from builtins import float, print, any,list


def main():
    open_refinitiv_session()

    poa_input = "CY2025"
    companies = ['CRDA.L']
    metrics = {
        "Revenue": "TR.RevenueEstValue",
        "EBITDA": "TR.EBITDAEstValue",
        "EV/EBITDA": "TR.F.EVToEBITDA",
        "DPS": "TR.DPSEstValue",
        "Shares Outstanding": "TR.NumberOfSharesOutstanding",
        "Price": "TR.PriceClose"
    }

    data_frames = [get_metric(code, f"{metric} {poa_input}", companies, poa_input) for metric, code in metrics.items()]
    panel = consolidate_refinitiv_data(pd.concat(data_frames), ["Ticker", "Broker Name", "Estimate Date"])
    panel = calculate_derived_metrics(panel, poa_input)
    panel = format_dates(panel)

    panel.to_csv("outputs/consolidated_panel.csv", index=False)

    summary_df = create_multi_metric_forecast_summary(panel, list(metrics.keys()), "outputs/summary.xlsx")

    # Monte Carlo and TSR Calculation
    company_input = summary_df["Summary"].set_index("Statistic").T.to_dict()
    simulated_df = simulate(company_input, 10000)
    simulated_df = compute_tsr(simulated_df, base, 2)
    goal_seek_results = find_equal_p(simulated_df, base, 2, [0.8, 0.5, 0.2])

    print(goal_seek_results.round(6))
    goal_seek_results.to_csv("outputs/goal_seek.csv")

if __name__ == "__main__":
    main()
