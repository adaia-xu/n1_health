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