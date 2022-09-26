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
xl = pd.read_excel('assets/Nevada MOVE Score Sheet.xlsx', None)
fips = pd.read_csv('assets/state_and_county_fips_master.csv')
nev_counties = dict.fromkeys(xl.keys())

# api paramters
api = '5baf306f06191f079d3fa727c38123f29e0e8993'
base_url = f'https://api.census.gov/data/2020/acs/acs5'


# correct xlsx sheets to county fips
nev_list = []
nev = {}
for key, value in nev_counties.items():
	if key == 'Carson City':
		nev_list.append(key)
	else:
		nev[key] = str(key) + ' County'
		nev_list.append(nev[key])
nev_counties = dict(zip(nev_list,list(nev_counties.values())))

# append fips values to nev counties dict
for key, value in nev_counties.items():
	if len(list(fips.loc[(fips['name'] == key) & (fips['state'] == 'NV')]['fips'].values)) != 0:
		nev_counties[key] = fips.loc[(fips['name'] == key) & (fips['state'] == 'NV')]['fips'].values[0]
		
	else:
		nev_counties[key] = None

nev = nev_counties
print(nev)

# create df from nev counties dict
df = pd.DataFrame(
    [{"county": key, "state_fips": str(value)[:2], "county_fips": str(value)[-3:]} for key, value in nev.items()])

for k,v in nev.items(): 
  if nev[k] is None:
  	print("failure!")
  	print(nev[k])

# ---------------------------------------------------------------------------------------------------------------------

# create df of question codes
questions = pd.DataFrame(data = questions, columns = list(questions.keys()), index = [0])

# append county fips to question code df, fill columns downwards
df = pd.concat([df, questions], axis = 1, copy = True)
df = df.fillna(method = 'ffill')

# compile question code regex
reg1 = re.compile(r'([^\s]+)')
reg2 = re.compile(r'(?=.*[A-Z])(?=.*[0-9])(?=.*_)[A-Z0-9_]+')

print(df)

# api fetch and processing function
def nv_data(value):
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
			code_nv = re.findall(reg1, value)
			for j in range(0, len(code_nv)):
				if code_nv[j] != '(' and code_nv[j] != ')' and code_nv[j] != '/' and code_nv[j] != '+' and code_nv[j] != ' ':
					product = products[str(code_nv[j])[:1]]
					variable = code_nv[j]
					url = f'{base_url}{product}?get={variable}&for=county:{county}&in=state:{state}&key={api}'
					response = requests.get(url)
					urldata = response.json()
					code_nv[j] = urldata[1][0]
					if code_nv[j] is None:
						code_nv[j] = 'null'
			code_nv = ''.join(code_nv)
			try:
				x = eval(code_nv)
			except:
				x = 'null'
			print('done in %.4ss' % (time.time() - data_time))
			return(x)

# iterate over rows and apply api call function	

county = 0
state = 0

i = 0
df1 = df.iloc[i:i+2]

for index, row in df1.iterrows():
	row = row.map(lambda x : nv_data(x))
	df1.at[index] = row


df1.to_csv('assets/nv_result.csv')


print('finished in %ss ' % (time.time() - start_time))
print('done at %f' % time.time())


