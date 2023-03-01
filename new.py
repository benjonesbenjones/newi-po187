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


wi = pd.read_excel('assets/results/WI_result.xlsx', sheet_name = None, index_col = 0)

cols = {i : 0 for i in list(wi['Winnebago County']['question'])}

for k, v in wi.items():
	nulls = list(v[v.isna().any(axis=1)]['question'])
	for i in nulls:
		cols[i] = cols[i] + 1


	# print( list(v[v.isna().any(axis=1)]['question']) )

cols = pd.Series(cols)
print(cols.iloc[cols.to_numpy().nonzero()])