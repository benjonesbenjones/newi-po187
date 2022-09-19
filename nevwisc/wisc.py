import time
start_time = time.time()

import pandas as pd
from census import Census
from us import states
from assets.codes import questions, products
import re
import requests
import numpy

# read data from local storage
xl = pd.read_excel('assets/Wisconsin MOVE Score Sheets.xlsx', None)
fips = pd.read_csv('assets/state_and_county_fips_master.csv')
wisc_counties = dict.fromkeys(xl.keys())

# api paramters
api = '5baf306f06191f079d3fa727c38123f29e0e8993'
base_url = f'https://api.census.gov/data/2020/acs/acs5'


# correct xlsx sheets to county fips
wisc_list = []
wisc = {}
for key, value in wisc_counties.items():
	wisc[key] = str(key) + ' County'
	wisc_list.append(wisc[key])
wisc_counties = dict(zip(wisc_list,list(wisc_counties.values())))

# fix spelling
wisc_counties['Oneida County'] = wisc_counties.pop('Onieda County')

# append fips values to wisc counties dict
for key, value in wisc_counties.items():
	if len(list(fips.loc[(fips['name'] == key) & (fips['state'] == 'WI')]['fips'].values)) != 0:
		wisc_counties[key] = fips.loc[(fips['name'] == key) & (fips['state'] == 'WI')]['fips'].values[0]
		
	else:
		wisc_counties[key] = None

wisc = wisc_counties

# create df from wisc counties dict
df = pd.DataFrame(
    [{"county": key, "state_fips": str(value)[:2], "county_fips": str(value)[-3:]} for key, value in wisc.items()])

for k,v in wisc.items(): 
  if wisc[k] is None:
  	print("failure!")
  	print(wisc[k])

# ---------------------------------------------------------------------------------------------------------------------

# create df of question codes
questions = pd.DataFrame(data = questions, columns = list(questions.keys()), index = [0])

# append county fips to question code df, fill columns downwards
df = pd.concat([df, questions], axis = 1, copy = True)
df = df.fillna(method = 'ffill')

# compile question code regex
reg1 = re.compile(r'([^\s]+)')
reg2 = re.compile(r'(?=.*[A-Z])(?=.*[0-9])(?=.*_)[A-Z0-9_]+')


# api fetch and processing function
def wi_data(value):
		check = re.findall(reg2, value)
		if len(check) == 0:
			if len(value) == 2:
				global state 
				state = value
			elif len(value) == 3:
				global county 
				county = value
			return value
		else:
			data_time = time.time()
			code_wi = re.findall(reg1, value)
			for j in range(0, len(code_wi)):
				if code_wi[j] != '(' and code_wi[j] != ')' and code_wi[j] != '/' and code_wi[j] != '+' and code_wi[j] != ' ':
					product = products[str(code_wi[j])[:1]]
					variable = code_wi[j]
					url = f'{base_url}{product}?get={variable}&for=county:{county}&in=state:{state}&key={api}'
					response = requests.get(url)
					urldata = response.json()
					code_wi[j] = urldata[1][0]
					if code_wi[j] is None:
						code_wi[j] = 'null'
			code_wi = ''.join(code_wi)
			try:
				x = eval(code_wi)
			except:
				x = 'null'
			print('done in %.4ss' % (time.time() - data_time))
			return(x)

# iterate over rows and apply api call function	

county = 0
state = 0

for index, row in df.iterrows():
	row = row.map(lambda x : wi_data(x))
	df.at[index] = row
print(df)

df.to_csv('assets/result.csv')


print('finished in %ss ' % (time.time() - start_time))
print('done at %f' % time.time())


