import pandas as pd

def records_to_dataframe(healthrecords): #using apple health records as parameter

    #converting appple XML records into clean pandas Dataframe
    rows = [] #initializing empty list 

    for r in healthrecords: #r is a temporary variable
        rows.append(r.attrib) #adds XML dictionalry of attributes to end of rows list

    df = pd.DataFrame(rows) #convirintg list into dictionaires, each key becomes column name

    return df

def sorting_step_counts(df): 

    #filters DataFrame to only keep rows where type matches the Apple Health
    #step count identifier, making an independent copy of this data
    steps = df[df["type"]=="HKQuantityTypeIdentifierStepCount"].copy()

    #convert values to numeric, dates to real datetime objects

    #converts "column" from text into numbers
    steps["value"]=pd.to_numeric(steps["value"], errors = "coerce")
    
    #converts startDate column into proper datetime objects to be filtered by time
    steps["startDate"]=pd.to_datetime(steps["startDate"])
    
    #converts endDate column from text strings into proper datetime objects
    steps["endDate"]=pd.to_datetime(steps["endDate"])

    return steps[["startDate", "endDate", "value", "sourceName"]]

#grouping and creating sample series with date, time and timezone

def add_day_for_column(steps):

    #making copy of existing objects and assigning it back to variable
    steps = steps.copy()

    #extracts y-m-d and stores into column day
    steps["day"]=steps["startDate"].dt.date
    return steps

def daily_totals(steps):

    #steps.groupby groups all rows with same day value
    dailysteps = steps.groupby("day")["value"].sum().reset_index()
    dailysteps.columns=["day","total_steps"] #renaming columnns to be more clear
    return dailysteps

#checking for how complete the calendar is
def completeness_report(daily):
    #convering day column in the og data into standardized datetime objects
    daysHealth = pd.to_datetime(daily["day"])

    #finding earliest and latest dates in data
    full_range = pd.date_range(daysHealth.min(), daysHealth.max(), freq = "D")

    #building a baseline timeline with no gaps in the calendar
    stepsReport = pd.DataFrame({"day":full_range})

    #merging the blank calendar with original daily data
    #when we use how = 'left', every single day is kept from complete calendar
    reportHealth = stepsReport.merge(
        daily.assign(day=daysHealth), on="day", how="left"  
    )

    #creating a true/false column
    #flags days with values as true
    reportHealth["has_data"] = reportHealth["total_steps"].notna()
    return reportHealth

#copying the daily totals table
def confidence_growth(daily):
    d = daily.copy()
    d["day"] = pd.to_datetime(d["day"]) #ensures day is a real datetime type
    d = d.sort_values("day").reset_index(drop=True) #rows are sorted chronologically

    exp = d["total_steps"].expanding() #helps look at all rows from start up (including initial row)
    d["running_mean"] = exp.mean() #calculating mean of total_steps using every day
    d["running_se"] = exp.std() / exp.count() ** 0.5 #using Standard deviation formula
    return d #returning table with two new columns: running_mean and running_se