import time
start_time = time.time()

import pandas as pd
from census import Census
import us
from tqdm import tqdm
import re
import requests
import numpy
import csv
import os.path

api = '5baf306f06191f079d3fa727c38123f29e0e8993'
base_url = f'https://api.census.gov/data/2020/acs/acs5'

state_fips = pd.read_csv('https://gist.githubusercontent.com/dantonnoriega/bf1acd2290e15b91e6710b6fd3be0a53/raw/11d15233327c8080c9646c7e1f23052659db251d/us-state-ansi-fips.csv', dtype ={'st':'string'}, skipinitialspace = True)

def getCounties():
    "Function to return a dict of FIPS codes (keys) of U.S. counties (values)"
    d = {}
    r = requests.get("http://www2.census.gov/geo/docs/reference/codes/files/national_county.txt")
    reader = csv.reader(r.text.splitlines(), delimiter=',')    
    for line in reader:
        d[line[1] + line[2]] = line[3] 
    return d



def save_xls(dict_df, path):

    writer = pd.ExcelWriter(path)
    for key in dict_df.keys():
        dict_df[key].to_excel(writer, sheet_name=key)

    writer.save()


def getData(state):
	
	county_fips_codes = getCounties()
	from assets.codes import questions, products
	question = []
	codes = []
	for key, value in questions.items():
		question.append(key)
		codes.append(value)

	questions = {'questions' : question,
							 'codes' : codes
	}

	reg1 = re.compile(r'([^\s]+)')

	to_api = {
		'B':[],
		'S':[],
		'C':[],
		'D':[]
	}

	j = 0
	for code in questions.get('codes'):
		check = re.findall(reg1, str(code))
		for i in check:
			if i != '(' and i != ')' and i != '/' and i != '+' and i != ' ':
				product = str(i)[:1]
				to_api[product].append((j, i))
				j = j + 1

	from_api = {}

	api_data = pd.DataFrame()
	for key, value in to_api.items():
		product = products[key]
		variables = ','.join(list(zip(*value))[1])
		st_fips = state.fips
		url = f'{base_url}{product}?get={variables}&for=county:*&in=state:{st_fips}&key={api}'
		response = requests.get(url)
		urldata = response.json()
		cendata = pd.DataFrame.from_records(data = urldata[1:], columns = urldata[0])
		api_data = pd.concat([api_data, cendata], axis = 1)
		for k in urldata[1:]:
			ord_list_val = list(zip(list(zip(*value))[0], k[:-2]))
			try:
				from_api[k[-1]].extend(ord_list_val)
			except:
				from_api[k[-1]] = ord_list_val

	api_data = api_data.loc[:,~api_data.columns.duplicated()].copy()
	api_data = api_data.set_index('county')

	try:
			os.remove('assets/results/{}_result.xlsx'.format(state.abbr))
			print('deleted assets/results/{}_result.xlsx'.format(state.abbr))
	except OSError as e:
			print('creating file...')

	xlsx_dict = {}

	# tqdm(from_api.items(), desc = str(state)):

	for key, value in tqdm(from_api.items()):
		value.sort(key = lambda y: y[0])
		for j in range(0, len(questions.get('codes'))):
			code = questions.get('codes')[j]
			check = re.findall(reg1, code)
			for i in range(0, len(check)):
				if check[i] != '(' and check[i] != ')' and check[i] != '/' and check[i] != '+' and check[i] != ' ':
					check[i] = value.pop(0)[1]
			try:
				check = ''.join(check)
				x = eval(check)
			except:
				x = 'null'
			value.append((questions.get('questions')[j], x))
		value = pd.DataFrame.from_records(value, columns = ['question', 'value'])
		county_fips = pd.DataFrame({'question':'County FIPS Code',
																'value': key},			 
																index = [0])
		county_name = county_fips_codes.get(str(state.fips) + str(key))
		if county_name is not None:
			county_frame = pd.DataFrame({'question' : 'County Name',
													'value':county_name
													}, index = [0])
			value = pd.concat([county_fips, county_frame, value]).reset_index(drop = True)
		else:
			county_name = str(state.fips) + str(key)
			value = pd.concat([county_fips, value]).reset_index(drop = True)
		xlsx_dict[county_name[0:31]] = value
		
	save_xls(xlsx_dict, 'assets/results/{}_result.xlsx'.format(state.abbr))
	return

	
state = str(input('input state:	'))

if state == '*':
	start_time = time.time()
	state = us.states.STATES
	for i in state:
		getData(i)
		print('done with {} in {:.2f}s'.format(i.abbr, time.time() - start_time))
else:
	start_time = time.time()
	state = us.states.lookup(state)
	getData(state)	
	print('done with {} in {:.2f}s'.format(state.abbr, time.time() - start_time))





