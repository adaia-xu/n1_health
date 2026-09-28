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
    
    dailysteps = daily_totals(steps)
    print(dailysteps.head())

    print(f"\nTotal days with data: {len(dailysteps)}")
   

