import pytest
from acs_code_challenge import acs_code

file_path = 'uploads/inp_data.tsv'


def test_load_file():
	acs_code_test = acs_code()
	assert len(acs_code_test.load_file(file_path)) == 21

def test_intermediate_df():
	acs_code_test = acs_code()
	df_int_test = acs_code_test.intermediate_df(file_path)
	assert  list(df_int_test.columns) == ['date_time','ip','event_list','referrer','product_list']

def test_domain_name_extract():
	acs_code_test = acs_code()
	df_dne_test = acs_code_test.domain_name_extract(file_path)
	assert len(df_dne_test['Search Engine Domain'].unique())==4

def test_prod_list_ungroup():
	acs_code_test = acs_code()
	df_prod_list_ungroup_test = acs_code_test.prod_list_ungroup(file_path)
	assert df_prod_list_ungroup_test['Category'].unique().all() in ['nan', 'Electronics']

def test_keyword_extract():
	acs_code_test = acs_code()
	df_keyword_extract_test = acs_code_test.keyword_extract(file_path)
	assert ['ipod'] in df_keyword_extract_test['Search Keyword'].unique()

def test_search_engine_filling():
	acs_code_test = acs_code()
	df_search_engine_filling_test = acs_code_test.search_engine_filling(file_path)
	assert len(df_search_engine_filling_test[df_search_engine_filling_test['Search Keyword']=='ipod']) == 15

def test_final_group():
	acs_code_test = acs_code()
	df_final_test = acs_code_test.final_group(file_path)
	assert df_final_test['Total Revenue'].sum()==730
# def test_reversed():
#     assert list(reversed([1, 2, 3, 4])) == [4, 3, 2, 1]

# def test_some_primes():
#     assert 37 in {
#         num
#         for num in range(1, 50)
#         if num != 1 and not any([num % div == 0 for div in range(2, num)])
#     }
