#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import re
import gzip

#########################################################################################
# input file data source: http://snap.stanford.edu/data/amazon-meta.html                #
# data_preparation.py average running time: 1 hr 15 min, RAM allocate: 1.5 G. intel i7  #
# To speed up the process, try Running Python script on GPU by using package next line: #
# from numba import jit, cuda                                                           #
#                                                                                       #
# output file is csv object that will be used in DataFrame_preparation.py               #
#########################################################################################


# In[2]:


def remove_discontinued_products(txt):
    text = re.sub(r'((.*(\n|\r|\r\n)){2}).*discontinued\sproduct','',txt)
    return text


# In[3]:

def print_txt_ex(txt):
    print("Dataset example: \n")
    print(txt[0:2153], '\n')
    pass    

# In[4]:

def get_id(txt):
    ID = re.findall(r'Id:\s+(\d+)',txt)
    print("ID top 5:", ID[0:5])
    print("ID shape:", np.shape(ID),"\n")
    return ID

# In[5]:

def get_asin(txt):
    ASIN = re.findall(r'ASIN:\s+([a-zA-Z0-9]+)',txt)
    print("ASIN top 5:", ASIN[0:5])
    print("ASIN shape:", np.shape(ASIN),'\n')
    return ASIN


# In[6]:

def get_title(txt):
    title = re.findall(r'title:(.+)',txt.replace('\r',''))
    print("title top 5:", title[0:5])
    print("title shape:", np.shape(title),"\n")
    return title


# In[7]:

def get_group(txt):
    group = re.findall(r'\s\sgroup:\s(\w+)', txt)
    print("group top 5:", group[0:5])
    print("group shape:", np.shape(group),"\n")
    return group


# In[8]:

def get_rank(txt):
    rank = re.findall(r'salesrank:\s(.*)', txt.replace('\r',''))
    print("salesrank top 5:", rank[0:5])
    print("salesrank shape:", np.shape(rank),"\n")
    return rank


# In[9]:

def get_ctg(txt):
    ctg = re.findall(r'categories:.+(\d+)', txt)
    print("categories top 5:", ctg[0:5])
    print("categories shape:", np.shape(ctg),"\n")
    return ctg

# In[10]:

def get_rating(txt):
    rating = re.findall(r'avg rating:(.+)', txt.replace('\r',''))
    print("avg ratings top 5:", rating[0:5])
    print("avg ratings shape:", np.shape(rating),"\n")
    return rating


# In[11]:

def get_sim(txt):
    sim = re.findall(r'similar:.+',txt.replace('\r',''))
    print("similar products top 5:", sim[0:5])
    print("similar products shape:", np.shape(sim),"\n")
    return sim


# In[12]:
if __name__ == "__main__":
    
    with gzip.open('amazon-meta.txt.gz', 'rb') as f:
        txt = f.read().decode("utf-8")
        
    print_txt_ex(txt)
        
    text = remove_discontinued_products(txt)

    ID = get_id(text)
    ASIN = get_asin(text)
    title = get_title(text)
    group = get_group(text)
    rank = get_rank(text)
    ctg = get_ctg(text)
    rating = get_rating(text)
    sim = get_sim(text)
    
    data_dic = {'Id':ID,'ASIN':ASIN,'title':title,'group':group,'sales_rank':rank,\
                'category':ctg,'avg_rating':rating,'similar_product':sim}
        
    df = pd.DataFrame(data_dic)
    print(df.head())

    compression_opts = dict(method='zip', archive_name='amazon_meta_data.csv')
    
    df.to_csv('amazon-meta-csv.zip', index=False, compression=compression_opts)





