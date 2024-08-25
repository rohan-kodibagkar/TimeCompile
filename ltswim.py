import streamlit as st
import pandas as pd
from datetime import datetime
import re

import tempfile
import csv
from pandas.core.api import to_numeric

def add_column(file1, file2, column1_index, column2_index, output_file):
  """Adds a column from file2 to file1 based on matching values in column1, retaining the original column name.

  Args:
    file1: Path to the first CSV file.
    file2: Path to the second CSV file.
    column1_index: Index of the column to match in both files.
    column2_index: Index of the column to add from file2 to file1.
    output_file: Path to the output CSV file.
  """

  df1 = pd.read_csv(file1)
  df2 = pd.read_csv(file2)

  # Extract the column name from file2
  column2_name = df2.columns[column2_index]

  # Rename columns for merging
  df1.rename(columns={df1.columns[column1_index]: 'match_column'}, inplace=True)
  df2.rename(columns={df2.columns[column1_index]: 'match_column'}, inplace=True)

  # Merge the two DataFrames based on the matching column
  merged_df = pd.merge(df1, df2[['match_column', column2_name]], on='match_column', how='left')

  # Save the merged DataFrame to a new CSV file
  merged_df.to_csv(output_file, index=False)

def process_csv(input_type,input_file):
#def individual(input_file,output_file):
    """
    Function to process individual swim data from uploaded CSV file.
    """

    # Read uploaded CSV content into a pandas dataframe
#    df = pd.read_csv(uploaded_file)
    if input_type == 'Individual':
        header = ["meet","eventnum", "time","dq", "swimmer","school", "grade","split1", "split2","split3", "split4", "split5","split6", "split7", "split8","split9", "split10"]
        columns_to_extract = [5, 8, 10, 11, 14, 15, 16, 31, 32, 33, 34, 35, 36, 37, 38, 47, 48]  # Change these indices to match the columns you want
        school_index=15
        output_file = "LT_individual_new.csv"
        
    elif input_type == 'Relay': 
        header = ["meet","eventnum", "finaltime", "dq","school","swimmer1", "swimmer2", "swimmer3","swimmer4", "split1", "split2","split3", "split4", "split5","split6", "split7", "split8"]
        columns_to_extract = [5, 9, 11, 14, 17, 22, 23, 24, 25, 31, 33, 35, 37, 39, 41, 43, 45]  # Change these indices to match the columns you want
        school_index=17
        output_file = "LT_relays_new.csv"
    
    meetname_index = 5
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(input_file.read())

    # Open the input CSV file for reading
    with open(temp_file.name, 'r', newline='') as input_csvfile:
        # Open the output CSV file for writing
 
        with open(output_file, 'w', newline='') as output_csvfile:
            csv_reader = csv.reader(input_csvfile)
            csv_writer = csv.writer(output_csvfile)
            csv_writer.writerow(header)    
            for row in csv_reader:
                school_value = row[school_index].strip()
                meetname = row[meetname_index]
                if school_value in [None, '', 'NULL', 'null', 'NaN', 'nan']:
                    row[school_index] = 'FRLE'
                selected_data = [row[i] for i in columns_to_extract]
                csv_writer.writerow(selected_data)

    with open(output_file, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)


    df = pd.DataFrame(data, columns=data[0])
        
#    st.write(f"Data prep complete for {input_type} file")
    return df,meetname

  
def main():
    """
    Streamlit app to upload multiple CSV files, call processing functions, 
    and potentially download generated files.
    """

    st.header("LTHS Swim Time Compile ")
    st.sidebar.image("./LTswimteam.jpg", use_column_width=True)
    #st.sidebar.image("/content/drive/MyDrive/Projects/Python/LTSwim v4/LTswimteam.jpg", use_column_width=True)
    st.sidebar.caption("This app creates consolidated list of the swimmers and their meet times")
    st.sidebar.caption("You will need to upload Relays and Individual files.Template file is optional")
    
    st.sidebar.write(":rainbow[Designed and Developed by Rohan Kodibagkar]")
    
    templetefileyes = st.checkbox('Check the box if you have the template file')
    print(templetefileyes)
    if templetefileyes :
        required_files = ["LT_relays.csv", "LT_individual.csv", "Template.csv"] 
    else:    
        required_files = ["LT_relays.csv", "LT_individual.csv"] 
       
    css = '''
        <style>
            [data-testid='stFileUploader'] {
                width: max-content;
            }
            [data-testid='stFileUploader'] section {
                padding: 0;
                float: left;
            }
            [data-testid='stFileUploader'] section > input + div {
                display: none;
            }
            [data-testid='stFileUploader'] section + div {
                float: right;
                padding-top: 0;
            }

        </style> 
        '''

    st.markdown(css, unsafe_allow_html=True)  
    print(required_files)
    uploaded_files = {}
#    required_files = ["LT_relays.csv", "LT_individual.csv", "Template.csv"]

    for file_name in required_files:
        uploaded_files[file_name] = st.file_uploader(f"Upload {file_name}", type="csv")

    if all(file is not None for file in uploaded_files.values()):
        # Check if all required files are uploaded
        for file_name, uploaded_file in uploaded_files.items():
            if uploaded_file.name != file_name:
                st.error(f"Incorrect filename: {uploaded_file.name}. Please upload {file_name}.")
                return
        
        eventsplitsfile='./eventsSplits.csv'

        # Process uploaded files
        for file_name, uploaded_file in uploaded_files.items():
            if file_name == "LT_relays.csv":
                # Call relay processing function with uploaded file content
                relaydf,meetname=process_csv('Relay',uploaded_file)
                #st.write(relaydf)
            elif file_name == "LT_individual.csv":
                # Call individual processing function with uploaded file content                
                #fileout = individual(uploaded_file,output_file='LT_individual_new.csv')
                inddf,meetname=process_csv('Individual',uploaded_file)
                #st.write(inddf)
            elif file_name == "Template.csv":
                # with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                #     temp_file.write(uploaded_file.read())
                templatefile=uploaded_file

                # Open the input CSV file for reading
                #templatefile = pd.read_csv(temp_file.name)
        eventsplits = pd.read_csv(eventsplitsfile)
                
                #st.write(eventsplits)
                
    #    st.success("Files uploaded successfully")        
        m = st.markdown("""
        <style>
        div.stButton > button:first-child {
            background-color: #018749;
            color:#ffffff;
        }
        </style>""", unsafe_allow_html=True)

        if st.button('Prepare Consolidated File'):
            
            SCHOOL='FRLE'
            # print("Hello")
            # print(SCHOOL)

            swimmers = {}
            events = set()
            inddf['time'] = inddf['time'].str.replace('Y','')
            inddf['event'] = inddf['eventnum'].str.split().str[2]
            inddf['concatTimes'] = ''
            inddf['gender']=''
        
            for ind, row in inddf[inddf['school']==SCHOOL].iterrows():

                swimmers_tuplist = list(swimmers)
                perf=''
                gender= eventsplits[eventsplits['eventNo']==int(row['event'])]['gender'].to_string(index=False)
                swimmers_tuplist.append((row['swimmer'],gender))
                swimmers=set(swimmers_tuplist)

                abbr= eventsplits[eventsplits['eventNo']==int(row['event'])]['eventAbbr'].to_string(index=False)
                #st.write(int(row['event']))
                reps= int(eventsplits[eventsplits['eventNo']==int(row['event'])]['noOfSplits'].iloc[0])
                #st.write(reps)
                perf=abbr+' '+str(row['dq'])+' '
                for i in range(reps):
                    splitnum = 'split'+str(i+1)
                    perf = perf+str(row[splitnum])+' '
                perf=perf+' '+str(inddf.at[ind,'time'])
                inddf.loc[ind,'concatTimes']=perf.replace('nan','')
                inddf.loc[ind, 'gender']=gender

            #st.write(inddf)

            individuals = pd.DataFrame(list(swimmers), columns=['swimmer','gender'])
            individuals['SwimTime'] =''

            for ind1, row1 in individuals.iterrows():
                indtime=''
                for ind2,row2 in inddf[inddf['swimmer']==row1['swimmer']].iterrows():
                    indtime = indtime+str(row2['concatTimes'])+'\n'
                individuals.loc[ind1,'SwimTime'] = indtime

            #st.write(individuals)

            relaydf = relaydf[relaydf['school']==SCHOOL]
            relaydf['event'] = relaydf['eventnum'].str.split().str[2]

            for ind, row in relaydf.iterrows():
                events.add(str(row['event']))

            my_dict = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}

            eventsdf = pd.DataFrame(list(events), columns=['event'])
            for ind1,row1 in eventsdf.iterrows():
                gender= eventsplits[eventsplits['eventNo']==int(row1['event'])]['gender'].to_string(index=False)
                eventcode = eventsplits[eventsplits['eventNo']==int(row1['event'])]['eventAbbr'].to_string(index=False)
                eventsdf.at[ind1,'gender']= gender
                tt=''
                i=0
                for ind2,row2 in relaydf[relaydf['event']==row1['event']].iterrows():
                    tt = tt+' '+my_dict[i]+' '+row2['finaltime']
                    i=i+1
                eventsdf.at[ind1,'eventcode']= eventcode+' '+tt

            #st.write(eventsdf)

            OUTFILE='LTProcessed.csv'

            def extract_string_before_number(string):
                for i, char in enumerate(string):
                    if char.isdigit():
                        return string[:i]
                return string

            def extract_date_dd_mm(string):
                date_pattern = r'\d{2}-\w{3}-\d{2}'
                match = re.search(date_pattern, string)

                if match:
                    date_str = match.group()
                    try:
                        date_obj = datetime.strptime(date_str, '%d-%b-%y')
                        #return f"{date_obj.day:02d}/{date_obj.month:02d}"
                        return f"{date_obj.month:02d}/{date_obj.day:02d}"
                    except ValueError:
                        return None
                else:
                    return None

            
            def processinddf(gender,start_row):

                new_df = individuals.loc[individuals['gender']==gender, ['swimmer','SwimTime']]
                #values = new_df.values.tolist()
        
                numrows = new_df.shape[0]            
                new_df =new_df.sort_values(by=['swimmer'])
                #set_with_dataframe(worksheet, new_df,start_row,1,include_column_header=False)
                new_df.to_csv(OUTFILE,mode='a',index=False,header=False)
                return numrows
            
            def processrelaydf(gender,inmode):
                allevents=''
                new_df = eventsdf.loc[eventsdf['gender']==gender, ['eventcode']]
                
                for ind,row in new_df.iterrows():
                    allevents = allevents+row['eventcode']+'\n'
                #st.write(allevents)

                data = {'Column1': [gender], 'Column2': [allevents]}
                df = pd.DataFrame(data)
                numrows = df.shape[0]
                #set_with_dataframe(worksheet, df,start_row,1,include_column_header=False)
                df.to_csv(OUTFILE,mode=inmode,index=False,header=False)
                return numrows

            num_rows = 1
            num_rows=processrelaydf('Girls','w')
            num_rows=processinddf('Girls','a')

            num_rows=processrelaydf('Boys','a')
            num_rows=processinddf('Boys','a')

            meetnamenew=extract_string_before_number(meetname)
            meetdate=extract_date_dd_mm(meetname)
            meetnamedate=meetnamenew + " "  + meetdate

            header=['Swimmer Name',meetnamedate]
            finaldf = pd.read_csv(OUTFILE,header=None)
            finaldf.columns = header
            finaldf.to_csv(OUTFILE, index=False)
            
            if templetefileyes:

            # Example usage
                file1 = templatefile
                file2 = OUTFILE
                column1_index = 0
                column2_index = 1
                output_file = "merged_file.csv"
                MERGEDFILE = output_file
                add_column(file1, file2, column1_index, column2_index, output_file)
            else:
                MERGEDFILE = OUTFILE

            with open(MERGEDFILE, 'r') as f:
                processed_data = f.read()

            # Download functionality 
          
            st.success("Processing complete , click to download the file")                    
            # Download functionality using st.download_button()
            st.download_button(
                label=":orange[Download LTprocessed.csv]",
                data=processed_data,
                file_name="LTprocessed.csv",
                mime="text/csv",
            )


if __name__ == "__main__":
    main()


