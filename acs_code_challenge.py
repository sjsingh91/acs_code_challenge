import pandas as pd
import re
from urllib.parse import urlparse, parse_qs
import numpy as np


# Reading file from source location or S3 buckets

#file_path = 'uploads/inp_data.tsv'

class acs_code:
    
    def load_file(self,file_path):
        df_raw = pd.read_csv(file_path,sep = "\t")
        return df_raw


    def intermediate_df(self,file_path):
        df_int = self.load_file(file_path)
        df = df_int[['date_time','ip','event_list','referrer','product_list']]
        return df

    # Domain Name extraction

    def domain_name_extract(self,file_path):
        int_list = []
        df_dne = self.intermediate_df(file_path)
        for i in range(len(df_dne)):
            m = urlparse(df_dne['referrer'][i]).netloc
            int_list.append('.'.join(m.split('.')[1:]))
        df_dne['Search Engine Domain'] = int_list
        return df_dne

    # Ungrouping of Product List
    def prod_list_ungroup(self,file_path):
        df_prod_list_ungroup = self.domain_name_extract(file_path)

        df_prod_list_ungroup['product_list'] = df_prod_list_ungroup['product_list'].astype(str)
        df_prod_list_ungroup[['Category','Product Name','Number of Items','Total Revenue',
               'Merchandizing eVar']] = df_prod_list_ungroup['product_list'].str.split(';',expand=True)
        return df_prod_list_ungroup


        # Search Key word extraction

    def keyword_extract(self,file_path):
        keyword_list = []
        df_keyword_extract = self.prod_list_ungroup(file_path)
        for i in range(len(df_keyword_extract)):
            m = urlparse(df_keyword_extract['referrer'][i])
            keyword_dict = parse_qs(m.query)
            keys = keyword_dict.keys()
            if 'search' in (m.path):
                for i in keys:
                    if len(i)==1:
                        keyword_list.append(keyword_dict[i][0])
            else:
                keyword_list.append('')
        keyword_list = [i.lower() for i in keyword_list]
        df_keyword_extract['Search Keyword'] = keyword_list
        return df_keyword_extract

    # Filling search engine domain name and search keyword with first value
    def search_engine_filling(self,file_path):
        df_search_engine = self.keyword_extract(file_path)
        df_search_engine_filling = pd.DataFrame(columns=df_search_engine.columns)
        for i in df_search_engine.ip.unique():
            df_search_engine_int = df_search_engine[df_search_engine['ip']==i]
            df_search_engine_int['Search Engine Domain']= df_search_engine_int['Search Engine Domain'].groupby(df_search_engine_int['ip']).first()[0]
            df_search_engine_int['Search Keyword']= df_search_engine_int['Search Keyword'].groupby(df_search_engine_int['ip']).first()[0]
            df_search_engine_filling = pd.concat([df_search_engine_filling,df_search_engine_int])
        df_search_engine_filling = df_search_engine_filling.reset_index(drop=True)
        return df_search_engine_filling



    # final group by for results
    def final_group(self,file_path):
        df_intermediate_group = self.search_engine_filling(file_path)
        df_intermediate_group_int = df_intermediate_group[['Search Engine Domain','Search Keyword','Total Revenue']]
        df_intermediate_group_int['Total Revenue'] = df_intermediate_group_int['Total Revenue'].replace(r'', np.NaN)
        df_intermediate_group_int['Total Revenue'].fillna(value=0, inplace=True)
        df_intermediate_group_int['Total Revenue'] = df_intermediate_group_int['Total Revenue'].astype(int)
        df_final = df_intermediate_group_int.groupby(['Search Engine Domain', 'Search Keyword'],as_index=False).sum()
        df_final = df_final.sort_values(['Total Revenue'],ascending=False)
        df_final_no_indices = df_final.to_string(index=False)
        return df_final


# if __name__ == "__main__":
    
#     p1 = acs_code_challenge()
#     p2 = p1.final_group()
#     p2.to_csv('/Users/singhsaurabh/Downloads/op_data.tsv',sep = "\t", index = False)




