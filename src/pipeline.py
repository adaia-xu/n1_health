from extract import extracting_records
from transform import (
    records_to_dataframe,
    sorting_step_counts,
    add_day_for_column,
    daily_totals,
    completeness_report,
    confidence_growth,
)
from plots import plot_confidence_growth, plot_completeness_heatmap


def run_pipeline(xml_path):
    # extract
    healthrecords = extracting_records(xml_path)

    # transform
    df = records_to_dataframe(healthrecords)
    steps = sorting_step_counts(df)
    steps = add_day_for_column(steps)

    dailysteps = daily_totals(steps)
    dailysteps = dailysteps.iloc[:-1]  # drop partial final day

    report = completeness_report(dailysteps)
    growth = confidence_growth(dailysteps)

    # load / output
    dailysteps.to_csv("data/processed/daily_steps.csv", index=False)
    report.to_csv("data/processed/completeness_report.csv", index=False)

    plot_confidence_growth(growth)
    plot_completeness_heatmap(report)

    # summary printed to console
    days_with = report["has_data"].sum()
    print(f"Total records: {len(healthrecords)}")
    print(f"Days with data: {days_with} / {len(report)} ({days_with / len(report):.0%})")
    print("Saved: data/processed/daily_steps.csv, completeness_report.csv")
    print("Saved: confidence_growth.png, completeness_heatmap.png")


if __name__ == "__main__":
    run_pipeline("data/raw/export.xml")