#importing XML parser and naming ET
import xml.etree.ElementTree as ET

def extracting_records(xml_path):
    treedata = ET.parse(xml_path) #reads XML file into memory as tree structure
    
    #gets root of structure, the outermost tag for records
    dataroot = treedata.getroot() 

    #apple health export format is "Record"
    #matching list of elements gets returned
    healthrecords = dataroot.findall("Record")

    return healthrecords 


#only run this code if file is directly executed
if __name__== "__main__":

    #loading records and printing how many are found
    healthrecords = extracting_records("data/raw/export.xml")
    print(f"Total records found: {len(healthrecords)}")

    #importing two functions from transform.py
    from transform import records_to_dataframe, sorting_step_counts, add_day_for_column, daily_totals

    #converts list into of health records into pandas dataframe
    df = records_to_dataframe(healthrecords)

    #filtering dataframe
    steps = sorting_step_counts(df)
    print(steps.head()) #previewing data
    print(f"\nTotal step records:{len(steps)}")
    
    steps = add_day_for_column(steps)
    print(steps.head())

    #collapsing individual step segments into one total per calendar day
    dailysteps = daily_totals(steps)
    dailysteps = dailysteps.iloc[:-1] #last day of export is not a full day
    print(dailysteps.head())

    print(f"\nTotal days with data: {len(dailysteps)}")

    #build a full calendar(with missing days) and flag which ones have data
    from transform import completeness_report
    report = completeness_report(dailysteps)

    #true counts as 1, so sum will give total days with data
    days_with = report["has_data"].sum()
    print(f"\nDays with data: {days_with} / {len(report)} ({days_with / len(report):.0%})")
    print(report[~report["has_data"]].head(10))  # first 10 missing days

    #pull out just the missing days and checks if weekdays show up more than others
    missing = report[~report["has_data"]].copy()
    print(missing["day"].dt.day_name().value_counts())

    #compute running mean + standard error as data accumulates
    from transform import confidence_growth
    growth = confidence_growth(dailysteps)
    print(growth.tail())

    #generate + save confidence-growth chart as a png file
    from plots import plot_confidence_growth
    plot_confidence_growth(growth)
    print("Saved to chart to data/processed/confidence_growth.png")

    from plots import plot_completeness_heatmap

    plot_completeness_heatmap(report)
    print("Saved heatmap to data/processed/completeness_heatmap.png")