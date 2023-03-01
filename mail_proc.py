import pandas as pd
import requests
from bs4 import BeautifulSoup
from mechanize import *
import us
import io
from tqdm import tqdm
from geopy import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import plotly.express as px

locator = Nominatim(user_agent='Ben Jones')

mailrooms = pd.read_csv('assets/mailrooms.csv')
zipcodes = pd.read_csv('assets/nonstandard.csv')

mailrooms = mailrooms.loc[mailrooms['Unit Name'] == 'MAIN OFFICE']
print(len(mailrooms))

def addresser(street, city, state, zipcode):
    return str(street) + ', ' + str(city) + ', ' + str(state) + ', ' + str(zipcode)
 
map = {
    'Property Address' : 'street',
    'City' : 'city',
    'ST' : 'state',
    'ZIP Code' : 'postalcode'
}

mailrooms['country'] = 'USA'
mailrooms = mailrooms.rename(columns=map)

mailroom_list = mailrooms[['street', 'city', 'state', 'country', 'postalcode']].to_dict(orient='records')

sub_mailroom_list = mailroom_list[1:15]

geocode = RateLimiter(locator.geocode, min_delay_seconds=1)

geo_list = []
for i in sub_mailroom_list:
    location = geocode(i, geometry='geojson')
    if location:
        geo_list.append(location)

print(type(geo_list[0]))


# mailrooms['address'] = mailrooms['address'].apply(geocode)

# mailroom_dict = {i['Street'] : i['address'] for i in mailrooms.to_dict(orient='records')}
# print(mailroom_dict)



# print(mailrooms)