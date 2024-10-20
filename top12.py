import streamlit as st
import pandas as pd
import csv
import re
import datetime
import tempfile
import chardet

#Function adds a column time sec ,by converting column time to sec
def convert_time_to_sec(df,time):
    df['time sec'] = df['time'].apply(time_to_seconds)
    return df

# Function keeps the minimun time for a swimmer
def select_minimum_relay_rows(df):
    # Group by the second column and find the row with the minimum value in the third column
    result = df.loc[df.groupby(['eventnum' ,'swimmer1','swimmer2','swimmer3','swimmer4'])['time sec'].idxmin()]
    return result

def select_minimum_individual_rows(df):
    # Group by the second column and find the row with the minimum value in the third column
    result = df.loc[df.groupby(['eventnum' ,'swimmer'])['time sec'].idxmin()]
    return result

#Function merges 2 files into one output file
def merge_csv(file1, file2, output_file):
    with open(file1, 'rb') as f:
        result1 = chardet.detect(f.read())
    with open(file2, 'rb') as f:
        result2 = chardet.detect(f.read())

  
    # Read the CSV files
    df1 = pd.read_csv(file1, encoding=result1['encoding'])
    df2 = pd.read_csv(file2, encoding=result2['encoding'])

    # # Read the CSV files
    # df1 = pd.read_csv(file1)
    # df2 = pd.read_csv(file2)
    
    # Concatenate the DataFrames
    merged_df = pd.concat([df1, df2], ignore_index=True)    
    # Save the merged DataFrame to a new CSV file
    merged_df.to_csv(output_file, index=False)


# Function to extract the event number
def extract_event(input_string):
    # Regular expression to find the number after # and space
    match = re.search(r'#\s+(\d+)', input_string)

    if match:
        number = match.group(1)
        return number        
    else:
        print("No match found.")

# Function to convert time to seconds
def time_to_seconds(time_str):
    time = str(time_str)
    time.strip()
    time_split = time.split(':')
    if len(time_split) == 2:
        secs = round(float(time_split[0]) * 60 + float(time_split[1]), 2)
    else:
        secs = round(float(time_split[0]), 2)
    return secs


# Function to Remove the 'Y' suffix if it exists
def format_time(time_str):
    if time_str.endswith('Y'):
        time_str = time_str[:-1]
    return time_str

#process_pretop_csv('Relay',previousrelayfile,relayfile)
def process_pretop_csv(input_type,previousfile,input_file,output_file):    
    """
    Function to process individual or relay swim data from uploaded CSV file.
    """
   
    if input_type == 'Individual' :   
        intermediate_file = 'Individual_extracted_cols.csv'
        output_file = 'Individual_top.csv'
        header = ["meetname","eventnum", "time", "swimmer","school"]
        columns_to_extract = [5, 8, 10, 14, 15]  
    elif input_type == 'Relay': 
        intermediate_file = 'Relay_extracted_cols.csv'
        output_file = 'Relay_top.csv'
        header = ["meetname","eventnum", "time", "swimmer1","swimmer2","swimmer3","swimmer4","school"]
        columns_to_extract = [ 5, 9, 11,22, 23, 24, 25, 17]  

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(input_file.read())

    with open(temp_file.name, 'r', newline='') as input_csvfile:
               
        with open(intermediate_file, 'w', newline='') as output_csvfile:
            csv_writer = csv.writer(output_csvfile)
            csv_reader = csv.reader(input_csvfile)
            # Read and write the header row
            csv_writer.writerow(header)

            # Read and filter rows based on conditions
            filtered_rows = []
            for row in csv_reader:
                if input_type == 'Individual':
                    if "DQ" in row[11] or "NS" in row[10] or "DQ" in row[10]:
                        continue  # Skip rows with "DQ" in column 3 or "NS" in column 2
                    row[10] = format_time(row[10])  # Format the time in column 2
                    row[8] = extract_event(row[8])
                    if row[8] == "23" :
                        row[8] = "13"
                    elif row[8] == "24":
                        row[8] = "14"
                    elif row[8] == "17":
                        row[8] = "7"
                    elif row[8] == "18" :
                        row[8]= "8"        
                elif input_type == 'Relay':
                    if "DQ" in row[12] or "NS" in row[11]:
                        continue  # Skip rows with "DQ" in column 3 or "NS" in column 2
                    row[9] = extract_event(row[9])        
                filtered_rows.append(row)

            # Write the filtered and sorted rows to the output file
            for row in filtered_rows:
                selected_data = [row[i] for i in columns_to_extract]
            
                csv_writer.writerow(selected_data)
    df1 = pd.read_csv(intermediate_file)
    df2 = pd.read_csv(previousfile)
    
    # Concatenate the DataFrames
    merged_df = pd.concat([df1, df2], ignore_index=True)    

    # Select minimum time for a swimmer
    sec_converted_df = convert_time_to_sec(merged_df,'time')
    if input_type == 'Individual':
        result_df = select_minimum_individual_rows(sec_converted_df)
    elif input_type == 'Relay':
        result_df = select_minimum_relay_rows(sec_converted_df)
        
    sorted_df = result_df.sort_values(by=['eventnum','time sec'])

    # Group by the event column and keep only the first 12 rows for each group
    processed_df = sorted_df.groupby('eventnum').head(12)
    processed_df.to_csv(output_file, index=False)

def process_top_csv(input_type,input_file,output_file):    
    """
    Function to process individual or relay swim data from uploaded CSV file.
    """
    if input_type == 'Individual' :
        
        intermediate_file = 'Individual_extracted_cols.csv'
        output_file = 'Individual_top.csv'
        header = ["meetname","eventnum", "time", "swimmer","school"]
        columns_to_extract = [5, 8, 10, 14, 15]  
    elif input_type == 'Relay': 
         
        intermediate_file = 'Relay_extracted_cols.csv'
        output_file = 'Relay_top.csv'
        header = ["meetname","eventnum", "time", "swimmer1","swimmer2","swimmer3","swimmer4","school"]
        columns_to_extract = [ 5, 9, 11,22, 23, 24, 25, 17]  

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(input_file.read())

    with open(temp_file.name, 'r', newline='') as input_csvfile:
  
        with open(intermediate_file, 'w', newline='') as output_csvfile:
                    # Create CSV reader and writer objects
            csv_writer = csv.writer(output_csvfile)
            csv_reader = csv.reader(input_csvfile)
 
            # Read and write the header row
            csv_writer.writerow(header)
            # Read and filter rows based on conditions
            filtered_rows = []
            for row in csv_reader:
                if input_type == 'Individual':
                    if "DQ" in row[11] or "NS" in row[10] or "DQ" in row[10]:
                        continue  # Skip rows with "DQ" in column 3 or "NS" in column 2
                    row[10] = format_time(row[10])  # Format the time in column 2
                    row[8] = extract_event(row[8])
                    if row[8] == "23" :
                        row[8] = "13"
                    elif row[8] == "24":
                        row[8] = "14"
                    elif row[8] == "17":
                        row[8] = "7"
                    elif row[8] == "18" :
                        row[8]= "8"        
                elif input_type == 'Relay':
                    if "DQ" in row[12] or "NS" in row[11]:
                        continue  # Skip rows with "DQ" in column 3 or "NS" in column 2
                    row[9] = extract_event(row[9])        
                filtered_rows.append(row)

            # Write the filtered and sorted rows to the output file
            for row in filtered_rows:
                selected_data = [row[i] for i in columns_to_extract]
                csv_writer.writerow(selected_data)
    df = pd.read_csv(intermediate_file)
    # Select minimum time for a swimmer
    sec_converted_df = convert_time_to_sec(df,'time')

    if input_type == 'Individual':
        result_df = select_minimum_individual_rows(sec_converted_df)
    elif input_type == 'Relay':
        result_df = select_minimum_relay_rows(sec_converted_df)
        
    sorted_df = result_df.sort_values(by=['eventnum','time sec'])
    
    # Group by the event column and keep only the first 12 rows for each group
    processed_df = sorted_df.groupby('eventnum').head(12)
    processed_df.to_csv(output_file, index=False)

def app():
    """
    Streamlit app to upload multiple CSV files, call processing functions, 
    and potentially download generated files.
    """
    st.header("Top 12 Swimmers-Time ")
   
    previoustopfile = st.checkbox('Check the box if you have the previous top Individual and Relay files')
    if previoustopfile :
        required_files = ["Relay.csv", "Individual.csv", "PreviousRelay_top.csv","PreviousIndividual_top.csv"] 
    else:    
        required_files = ["Relay.csv", "Individual.csv"] 
       
    print(required_files)
    relay_output_file = 'Relay_top.csv'      
    indi_output_file = 'Individual_top.csv'
 
    uploaded_files = {}
    for file_name in required_files:
        uploaded_files[file_name] = st.file_uploader(f"Upload {file_name}", type="csv")
    if all(file is not None for file in uploaded_files.values()):
        # Check if all required files are uploaded
        for file_name, uploaded_file in uploaded_files.items():
            if uploaded_file.name != file_name:
                st.error(f"Incorrect filename: {uploaded_file.name}. Please upload {file_name}.")
                return
    if all(file is not None for file in uploaded_files.values()):
        # Check if all required files are uploaded
        for file_name, uploaded_file in uploaded_files.items():
            if uploaded_file.name != file_name:
                st.error(f"Incorrect filename: {uploaded_file.name}. Please upload {file_name}.")
                return
        m = st.markdown("""
        <style>
        div.stButton > button:first-child {
            background-color: #018749;
            color:#ffffff;
        }
        </style>""", unsafe_allow_html=True)

#        if st.button('Prepare Consolidated File'):

        if previoustopfile:
            for file_name, uploaded_file in uploaded_files.items():
                if file_name == "Relay.csv":
                    relay_file=uploaded_file
                elif file_name == "Individual.csv":
                    individual_file=uploaded_file
                if file_name == "PreviousRelay_top.csv":
                    relay_output_file = 'Relay_top.csv'      
                    process_pretop_csv('Relay',uploaded_file,relay_file,relay_output_file)
                elif file_name == "PreviousIndividual_top.csv":
                    indi_output_file = 'Individual_top.csv'
                    process_pretop_csv('Individual',uploaded_file,individual_file,indi_output_file)
        else:
            for file_name, uploaded_file in uploaded_files.items():
                if file_name == "Relay.csv":
                    relay_output_file = 'Relay_top.csv'      
                    process_top_csv('Relay',uploaded_file,relay_output_file)

                elif file_name == "Individual.csv":
                    indi_output_file = 'Individual_top.csv'
                    process_top_csv('Individual',uploaded_file,indi_output_file)   
        # Download functionality 
        st.success("Processing complete , click to download the file")                    

        with open(relay_output_file, 'r') as f:
            top_relay_data = f.read()
            st.download_button(
                label=":orange[Download Relay_top.csv]",
                data=top_relay_data,
                file_name="Relay_top.csv",
                mime="text/csv",
            )

        with open(indi_output_file, 'r') as f:
            top_indi_data = f.read()
            st.download_button(
                label=":orange[Download Individual_top.csv]",
                data=top_indi_data,
                file_name="Individual_top.csv",
                mime="text/csv",
            )
