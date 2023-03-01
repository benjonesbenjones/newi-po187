import pandas as pd
import requests
from bs4 import BeautifulSoup
from mechanize import *
import us
import io
from tqdm import tqdm

HEADER = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'}
URL = 'https://about.usps.com/who/legal/foia/documents/leased-facilities/'

# ----------------- POSTAL SERVICE CODES -----------------
# Adding USPS service codes to data. 'P' denotes zipcodes 
# that do not offer standard mail service.

# Import data
geo_df = pd.read_csv('assets/geo-data.csv')
mail_df = pd.read_csv('assets/zip-code-database.csv')

# Extract zipcodes and service codes from Postal Service data
service = [(str(d['ZipCode']), d['Classification']) for d in mail_df.to_dict(orient='records')]
service_df = pd.DataFrame().from_records(service, columns = ['zipcode', 'service'])

# Set type of dataframe to str and tr
geo_df = geo_df.astype(str)

# Merge dataframes to 
geo_df = pd.merge(geo_df, service_df, on='zipcode')
geo_df.to_csv('assets/nonstandard.csv', index = False)

states = us.states.STATES

def GetMailCSV(state, url, df_list):
    response = requests.get(url + state + '.csv', headers=HEADER)
    #if response.status_code == 200
    if response.ok:
        df_new = pd.read_csv( io.StringIO(response.text), header = [4] )
        df_list.append(df_new)
    else:
        print('aargh!')
    return df_list

df_list = []

# for state in tqdm(states):
#     state = state.abbr.lower()
#     GetMailCSV(state, URL, df_list)
# 
# po_df = pd.concat(df_list)
# po_df = po_df.rename(columns=po_df.iloc[0]).drop(po_df.index[0])
# po_df.to_csv('assets/mailrooms.csv', index = False)
pd.read_csv('assets/mailrooms.csv')