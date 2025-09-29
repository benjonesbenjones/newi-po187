# Import necessary libraries
import time
import warnings
import pandas as pd
from tqdm import tqdm
import us
import re
import requests
import numpy
import csv
import os.path
from assets.codes import questions, products, positions
warnings.simplefilter(action='ignore', category=FutureWarning)


# Define API key and base URL for the ACS API
api = '5baf306f06191f079d3fa727c38123f29e0e8993'
base_url = f'https://api.census.gov/data/2020/acs/acs5'

# Load a CSV file with state FIPS codes
state_fips = pd.read_csv('https://gist.githubusercontent.com/dantonnoriega/bf1acd2290e15b91e6710b6fd3be0a53/raw/11d15233327c8080c9646c7e1f23052659db251d/us-state-ansi-fips.csv', dtype ={'st':'string'}, skipinitialspace = True)
template_df = pd.read_csv(os.getcwd() + '/assets/Minnesota_MoVE.csv', skip_blank_lines=False)

# Define a function to return a dictionary of FIPS codes (keys) of U.S. counties (values)
def getCounties():
    d = {}
    # Send a request to get county FIPS codes from the US Census Bureau
    r = requests.get("http://www2.census.gov/geo/docs/reference/codes/files/national_county.txt")
    # Read the response as a CSV file and split the content into lines
    reader = csv.reader(r.text.splitlines(), delimiter=',')
    for line in reader:
        # Combine the state FIPS code and county FIPS code as the key, and the county name as the value
        d[line[1] + line[2]] = line[3]
    return d

def count_missing_values(xlsx_dict):
    missing_values_count = {}

    for county_name, value in xlsx_dict.items():
        for index, row in value.iterrows():
            question = row['question']
            data_value = row['value']

            if data_value == 'null':
                if question not in missing_values_count:
                    missing_values_count[question] = 1
                else:
                    missing_values_count[question] += 1

    return missing_values_count

# Define a function to save a dictionary of DataFrames as an Excel file with multiple sheets
def save_xls(dict_df, path, template_df, positions):
    writer = pd.ExcelWriter(path)
    
    for key in dict_df.keys():
        # Create a new DataFrame by copying the template
        formatted_df = template_df.copy()

        # Populate the formatted DataFrame with data from dict_df

        data = dict_df[key]['value'].values

        for position, value in zip(positions, data):
            formatted_df.at[position, 'Score'] = value
        
        # Remove all rows up to row 145 (inclusive)
        formatted_df = formatted_df.iloc[146:].reset_index(drop=True)

        # Write the formatted DataFrame to the Excel file
        formatted_df.to_excel(writer, sheet_name=key, index=False)

    writer.save()

def count_missing_data(df, missing_value='null'):
    """Count the number of missing data (default value is -666666666) and None values in the DataFrame."""
    missing_count = (df['value'] == missing_value).sum()
    none_count = df['value'].isnull().sum()
    return missing_count + none_count

# Main function to retrieve and process data from the U.S. Census Bureau's ACS for a specified state
def getData(state):
    # Get county FIPS codes for the specified state
    county_fips_codes = getCounties()
    # Import questions and product codes from the assets.codes module
    from assets.codes import questions, products

    # Initialize lists to store questions and codes
    question = []
    codes = []
    # Iterate through the questions dictionary and append the keys and values to the lists
    for key, value in questions.items():
        question.append(key)
        codes.append(value)

    # Create a new dictionary with the lists of questions and codes
    questions = {'questions': question,
                 'codes': codes}

    # Define a regular expression to extract non-space characters from the codes
    reg1 = re.compile(r'([^\s]+)')

    # Initialize a dictionary to store the code indices and the corresponding codes for each product
    to_api = {
        'B': [],
        'S': [],
        'C': [],
        'D': []
    }

    # Iterate through the codes list and extract the non-space characters using the regular expression
    # Group the extracted codes by their first character (B, S, C, or D) and store them in the to_api dictionary
    j = 0
    # Iterate through the codes list and extract the non-space characters using the regular expression
    for code in questions.get('codes'):
        check = re.findall(reg1, str(code))
        for i in check:
            if i != '(' and i != ')' and i != '/' and i != '+' and i != ' ':
                # Determine the product type (B, S, C, or D) by getting the first character of the code
                product = str(i)[:1]
                # Store the index counter and code as a tuple in the to_api dictionary under the corresponding product type
                to_api[product].append((j, i))
                # Increment the index counter
                j = j + 1

    # Initialize a dictionary to store the data fetched from the API
    from_api = {}

    # Initialize an empty DataFrame to store the API data
    api_data = pd.DataFrame()
    # Iterate through the to_api dictionary and fetch the data for each product type from the API
    for key, value in to_api.items():
        product = products[key]
        # Create a comma-separated string of the codes for the API request
        variables = ','.join(list(zip(*value))[1])
        # Get the state FIPS code
        st_fips = state.fips
        # Construct the API request URL
        url = f'{base_url}{product}?get={variables}&for=county:*&in=state:{st_fips}&key={api}'
        # Send the API request and parse the JSON response
        response = requests.get(url)
        urldata = response.json()
        # Create a DataFrame from the API response data and concatenate it with the existing api_data DataFrame
        cendata = pd.DataFrame.from_records(data=urldata[1:], columns=urldata[0])
        api_data = pd.concat([api_data, cendata], axis=1)
        # Update the from_api dictionary with the fetched data
        for k in urldata[1:]:
            ord_list_val = list(zip(list(zip(*value))[0], k[:-2]))
            try:
                from_api[k[-1]].extend(ord_list_val)
            except:
                from_api[k[-1]] = ord_list_val

    # Remove duplicate columns from the api_data DataFrame and set the index to the county FIPS code
    api_data = api_data.loc[:, ~api_data.columns.duplicated()].copy()
    api_data = api_data.set_index('county')

    # Try to delete the existing output file, if any, before saving the new results
    try:
        os.remove('assets/results/{}_result.xlsx'.format(state.abbr))
        print('deleted assets/results/{}_result.xlsx'.format(state.abbr))
    except OSError as e:
        print('creating file...')

    # Initialize a dictionary to store the output DataFrames for each county
    xlsx_dict = {}

    # Iterate through the from_api dictionary to process the data for each county
    for key, value in tqdm(from_api.items()):
        # Sort the value list by the index counter (first element of each tuple)
        value.sort(key=lambda y: y[0])
        # Iterate through the questions and codes lists and evaluate the corresponding expressions using the fetched data
        for j in range(0, len(questions.get('codes'))):
            code = questions.get('codes')[j]
            check = re.findall(reg1, code)
            for i in range(0, len(check)):
                if check[i] != '(' and check[i] != ')' and check[i] != '/' and check[i] != '+' and check[i] != ' ':
                    # Replace the non-space character in the check list with the corresponding value from the fetched data
                    check[i] = value.pop(0)[1]
            try:
                # Evaluate the modified check list as an arithmetic expression
                check = ''.join(check)
                x = eval(check)
            except:
                x = 'null'
            # Append the result of the evaluation (or 'null' if an error occurred) to the value list
            value.append((questions.get('questions')[j], x))
            my_list = [x[1] for x in value]
        # Convert the value list to a DataFrame with 'question' and 'value' columns
        value = pd.DataFrame.from_records(value, columns=['question', 'value'])
        # Add the county FIPS code as a new row in the value DataFrame
        county_fips = pd.DataFrame({'question': 'County FIPS Code',
                                    'value': key},
                                   index=[0])
        # Get the county name from the county_fips_codes dictionary
        county_name = county_fips_codes.get(str(state.fips) + str(key))
        if county_name == None:
            county_name = str(state.fips) + str(key)
        
        # Replace -666666666 and None values with 'null'
        value = value.applymap(lambda x: 'null' if (x is None or (isinstance(x, (int, float)) and x < 0)) else x)
      
        # Store the value DataFrame in the xlsx_dict dictionary with the county name as the key
        xlsx_dict[county_name[0:31]] = value

    # Initialize counters for counties with missing data
    counties_with_missing_data = 0
    total_missing_values = 0

    # Iterate through the xlsx_dict dictionary and count missing data for each county
    for county_name, county_df in xlsx_dict.items():
        missing_count = count_missing_data(county_df)

        if missing_count > 0:
            counties_with_missing_data += 1
            total_missing_values += missing_count

    # Calculate the percentage of counties with missing data
    percentage_of_counties_with_missing_data = (counties_with_missing_data / len(xlsx_dict)) * 100

    print('\n')
    print(f"Percentage of counties with missing data: {percentage_of_counties_with_missing_data:.2f}%")
    print(f"Total missing values (-666666666 and None): {total_missing_values}")

    missing_values_count = count_missing_values(xlsx_dict)
    sorted_missing_values = sorted(missing_values_count.items(), key=lambda x: x[1], reverse=True)

    print("Questions with the most missing values:")
    for question, count in sorted_missing_values:
        print(f"{question}: {count} missing values")

    # Save the xlsx_dict dictionary as an Excel file with multiple sheets
    save_xls(xlsx_dict, 'assets/results/{}_result.xlsx'.format(state.abbr), template_df, positions)
    return

# Prompt the user to enter a state abbreviation
# state = str(input('input state:   '))
state = 'MN'

# Process the data for the specified state or all states, depending on the user's input
if state == '*':
    start_time = time.time()
    state = us.states.STATES
    for i in state:
        getData(i)
        print('done with {} in {:.2f}s'.format(i.abbr, time.time() - start_time))
elif state == 'na':
    print('done!')
else:
    start_time = time.time()
    state = us.states.lookup(state)
    getData(state)
    print('done with {} in {:.2f}s'.format(state.abbr, time.time() - start_time))
