#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd



# In[3]:

def save_csv(archive_name,zip_name,df):
    
    compression_opts = dict(method='zip', archive_name=archive_name)    
    df.to_csv(zip_name, index=False, compression=compression_opts)
    pass


# In[4]:
def get_edge_list(df):
    #get a complete edge list
    dt = df['similar_product'].str.split(' ', expand=True)
    dt.drop(dt.columns[[0, 1, 2, 4, 6, 8, 10]], axis=1, inplace=True)
    dt.rename(columns={3: 'product1', 5: 'product2', 7: 'product3', 9: 'product4', 11: 'product5'}, inplace=True)
    dt.replace(to_replace=[None], value='', inplace=True)

    dt_merged = dt.merge(df[['ASIN']], how='outer', left_index=True, right_index=True)

    dt_merged_1 = dt_merged[['ASIN', 'product1']].rename(columns={'product1': 'product'})
    dt_merged_2 = dt_merged[['ASIN', 'product2']].rename(columns={'product2': 'product'})
    dt_merged_3 = dt_merged[['ASIN', 'product3']].rename(columns={'product3': 'product'})
    dt_merged_4 = dt_merged[['ASIN', 'product4']].rename(columns={'product4': 'product'})
    dt_merged_5 = dt_merged[['ASIN', 'product5']].rename(columns={'product5': 'product'})

    edge_list = pd.concat([dt_merged_1, dt_merged_2, dt_merged_3, dt_merged_4, dt_merged_5]).reset_index()
    edge_list.drop(edge_list.columns[0], axis=1, inplace=True)
    edge_list.replace('', np.nan, inplace=True)
    edge_list.dropna(how='any', axis=0, inplace=True)
    edge_list.rename(columns={'ASIN': 'source', 'product': 'target'}, inplace=True)

    return edge_list

def get_attr(df, edge_list4):
    attr = df[['Id', 'ASIN', 'title', 'group', 'sales_rank', 'category', 'avg_rating']]
    source = edge_list4['source'].unique()
    target = edge_list4['target'].unique()
    all_products = pd.Series(np.concatenate((source, target))).unique()
    attr_select = attr[attr['ASIN'].isin(all_products)].reset_index()
    attr_select.drop(attr_select.columns[[0, 1]], axis=1, inplace=True)
    attr_select.rename(columns={'ASIN': 'Id','title':'label'}, inplace=True)
    return attr_select

def get_product_source_to_source(edge_list):
    source = edge_list['source'].tolist()
    target = edge_list['target'].tolist()
    product = list(set(source).intersection(set(target)))
    return product

def get_counter(product):
    counter = {}
    for key in product:
        counter[key]=counter.get(key, 0) + 1
    return counter

def get_degree_above_100_products(counter_target):
    product2 = []
    for k, v in counter_target.items():
        if v >= 100:
            product2.append(k)
    return product2

if __name__ == '__main__':

    df = pd.read_csv('amazon_meta_data.csv')

    edge_list = get_edge_list(df)
    # get full edge_list
    print('full edge list: \n', edge_list)

    product = get_product_source_to_source(edge_list)

    edge_list2 = edge_list[edge_list['target'].isin(product)]
    # We only have attributes with products in 'source' column,
    # so, we create a smaller edge list (edge_list2) that only contains source to source products

    target = edge_list2['target'].tolist()
    counter_target = get_counter(target)
    # sort_counter_target = sorted(counter_target.items(), key=lambda x: x[1], reverse=True)
    # sort counter to get some insights
    product2 = get_degree_above_100_products(counter_target)
    print('\n products degree above 100: \n', product2)

    edge_list3 = edge_list2[edge_list2['target'].isin(product2)]
    # get even smaller edge list that only includes target products degree above 100
    # It's degree 1 of nodes network

    product3 = edge_list3['source'].unique()
    # get all products that relate to product2

    edge_list4 = edge_list2[edge_list2['source'].isin(product3)]
    print('\n get edge list for a complete network with products that degree above 100: \n', edge_list4)

    attr = get_attr(df, edge_list4)
    print('\n selected products attributes: \n', attr)


    save_csv('edge_list_select.csv', 'amazon-product-edge-list.zip', edge_list4)
    save_csv('attr.csv', 'amazon-product-attributes.zip', attr)


