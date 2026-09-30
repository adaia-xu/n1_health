#import each stage's funcs from their own module
#seperating the extract/transform/plot instead of placing in one giant file

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
    # extract --> parsing the raw Apple Health XML into list of record elements
    healthrecords = extracting_records(xml_path)

    # transform: turn raw records into clean --> analysis ready table
    df = records_to_dataframe(healthrecords) #list of dictionaires
    steps = sorting_step_counts(df) #keeping only step-count records
    steps = add_day_for_column(steps)

    dailysteps = daily_totals(steps) #collapse many per day records into one
    
    # drop partial final day (since it was recorded for barely an hour)
    # this prevents skewing of data
    dailysteps = dailysteps.iloc[:-1]  

    report = completeness_report(dailysteps) #full calender build
    growth = confidence_growth(dailysteps) #running mean + standard error over time

    # writing clean outputs to disk
    dailysteps.to_csv("data/processed/daily_steps.csv", index=False)
    report.to_csv("data/processed/completeness_report.csv", index=False)

    #generating + saving the two visualizations
    plot_confidence_growth(growth)
    plot_completeness_heatmap(report)

    # human readable summary printed to console
    days_with = report["has_data"].sum()
    print(f"Total records: {len(healthrecords)}")
    print(f"Days with data: {days_with} / {len(report)} ({days_with / len(report):.0%})")
    print("Saved: data/processed/daily_steps.csv, completeness_report.csv")
    print("Saved: confidence_growth.png, completeness_heatmap.png")


#run this block if file is executed directly
if __name__ == "__main__":
    run_pipeline("data/raw/export.xml")