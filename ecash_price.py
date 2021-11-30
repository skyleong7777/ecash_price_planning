# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 16:29:57 2021

@author: skyleong
"""

#----import package----
import streamlit as st
import pandas as pd
#import numpy as np
from PIL import Image
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

pd.options.display.float_format='{:.2f}'.format

st.set_option('deprecation.showPyplotGlobalUse', False)

st.set_page_config(page_title="ecash price planning", page_icon=":star:", layout="wide")
st.set_option('deprecation.showPyplotGlobalUse', False)


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

#---- layout of title----
col1,col2,col3=st.columns(3)
with col2:
    st.markdown('## :star: Ecash price planning')
    image=Image.open('planning.jpg')
    st.image(image)


# ----upload ecash file and slot rating file----
upload_ecash=st.file_uploader('Please upload a Ecash dataset for analysis:(in CSV format)',type='csv')
upload_sr=st.file_uploader('Please upload a slot rating dataset for analysis:(in CSV format)',type='csv')
@st.cache
def file():
    if upload_ecash is not None:
        df_ecash = pd.read_csv(upload_ecash,parse_dates=['GamingDt'])
        return df_ecash
@st.cache
def file1():
    if upload_sr is not None:
        df_sr = pd.read_csv(upload_sr,parse_dates=['GamingDt'])
        return df_sr

df_ecash=file()
df_sr=file1()    


# ----Date Range----
if upload_ecash is not None:
    st.write('Ecash transaction from :',df_ecash['GamingDt'].min(), df_ecash['GamingDt'].max())
    
# ----total number transaction of ecash ----

if upload_ecash is not None:
    tol_ecash_count=df_ecash.TranCode.value_counts()
    tol_ecash_count=pd.DataFrame(tol_ecash_count)
    tol_ecash_count=tol_ecash_count.reset_index()
    tol_ecash_count=tol_ecash_count.rename(columns={'index':'TranCode','TranCode':'Total_records'})
    trancode_dict={'CSHWDPR':'Point_Reuqest','CSHSTLPR':'Point_Settle','CSHWDCR':'Promo_Request','CSHSTLCR':'Promo_Settle','CSHDEPCR':'ECash_Deposite'}
    tol_ecash_count['TranType']=tol_ecash_count['TranCode'].map(trancode_dict)
    tol_ecash_count=tol_ecash_count[['TranCode','TranType','Total_records']]
    if st.checkbox('Total number transaction of ecash'):
            st.write(tol_ecash_count)  


#----to view the top 10 amount of point/promo/deposte (ecash)----                    
if upload_ecash is not None:    
    value_counts_plt_wd=df_ecash.loc[df_ecash.TranCode=='CSHWDPR'][['TranCode','AuthAward','RedeemPts']].value_counts().sort_values(ascending=False).head(5)
    value_counts_plt_wd=value_counts_plt_wd.reset_index()
    value_counts_plt_wd=value_counts_plt_wd.rename(columns={0:'number_of_point_download'})
    value_counts_plt_wd=value_counts_plt_wd.drop(['TranCode'],axis=1)
    value_counts_promo_wd=df_ecash.loc[df_ecash.TranCode=='CSHWDCR'][['TranCode','AuthAward']].value_counts().sort_values(ascending=False).head(5)
    value_counts_promo_wd=value_counts_promo_wd.reset_index()
    value_counts_promo_wd=value_counts_promo_wd.rename(columns={0:'number_of_Promo_download'})
    value_counts_promo_wd=value_counts_promo_wd.drop(['TranCode'],axis=1)
    value_counts_dep_wd=df_ecash.loc[df_ecash.TranCode=='CSHDEPCR'][['TranCode','AwardUsed']].value_counts().sort_values(ascending=False).head(5)
    value_counts_dep_wd=value_counts_dep_wd.reset_index()
    value_counts_dep_wd=value_counts_dep_wd.rename(columns={0:'number_of_point_Deposite'})
    value_counts_dep_wd=value_counts_dep_wd.drop(['TranCode'],axis=1)
    if st.checkbox('Top 5 of ecash $ of Point-Promo_Deposite'):
        col4,col5,col6=st.columns(3)   
        col4.write(value_counts_plt_wd) 
        col5.write(value_counts_promo_wd)
        col6.write(value_counts_dep_wd)
        if st.checkbox('Download Top 5 records as CSV'):
            st.download_button(label='Download the transaction of Top 5 point as csv', data=value_counts_plt_wd.to_csv(), mime='text/csv')
            st.download_button(label='Download the transaction of Top 5 promo as csv', data=value_counts_promo_wd.to_csv(), mime='text/csv')
            st.download_button(label='Download the transaction of Top 5 Deposite as csv', data=value_counts_dep_wd.to_csv(), mime='text/csv')

# total player to download ecash per day
if upload_ecash is not None:
    group_dt=df_ecash.groupby(by=['GamingDt'])['Acct'].count()
    group_dt1=pd.DataFrame(group_dt).reset_index()
    group_dt2=group_dt1.rename(columns={'Acct':'Number of player to download eCash'})
    group_dt3=group_dt2.set_index('GamingDt')    
    if st.checkbox('Total player to download ecash per day'):
        st.bar_chart(group_dt3)
        if st.checkbox('Download the record of player to download eCash by daily'):
            st.download_button(label='Download the record of player to download eCash by daily', data=group_dt3.to_csv(), mime='text/csv')
            
            
# The average amount of eCash (point)    
if upload_ecash is not None:    
    all_plt_count=df_ecash.loc[df_ecash.TranCode=='CSHWDPR'][['AuthAward','RedeemPts']].value_counts().sort_values(ascending=False).reset_index()
    all_plt_count_mean=all_plt_count['AuthAward'].mean()
    all_plt_count_without_5=all_plt_count[5:]
    mean_all_plt_count_without_5=all_plt_count_without_5['AuthAward'].mean()
    if st.checkbox('"Average amount of ecash_point with other amount$" and "total of average ecash amount$"'):
        st.write('Average amount of ecash_point with other amount "except the popular amount$',mean_all_plt_count_without_5)
        st.write('Total amount of average ecash amount$',all_plt_count_mean)
    

# the total records of ecash download by daily

if upload_ecash is not None: 
    # to get the top 10 amout of ecash without gaming date
    value_counts_plt_wd_10=df_ecash.loc[df_ecash.TranCode=='CSHWDPR'][['AuthAward','RedeemPts']].value_counts().sort_values(ascending=False).head(10)
    value_counts_plt_wd_10=value_counts_plt_wd_10.reset_index()
    #to calculate the mean of ecash amount(point) and exclude the top 5
    all_plt_count=df_ecash.loc[df_ecash.TranCode=='CSHWDPR'][['AuthAward','RedeemPts']].value_counts().sort_values(ascending=False).reset_index()
    all_plt_count_without_5=all_plt_count[5:]
    mean_all_plt_count_without_5=all_plt_count_without_5['AuthAward'].mean()
    # to get all records of ecash amount with gaming date
    plt_mean_wd=df_ecash.loc[df_ecash.TranCode=='CSHWDPR'][['GamingDt','AuthAward','RedeemPts']]
    plt_mean_wd['total_mean']=mean_all_plt_count_without_5
    plt_mean_wd['total_mean']=plt_mean_wd['AuthAward'].apply(lambda x: x if x in value_counts_plt_wd_10['AuthAward'].values else mean_all_plt_count_without_5 )
    mean_auth_award = px.histogram(data_frame=plt_mean_wd,x='GamingDt',color='total_mean',opacity=0.8,title='Daily records with average amount')
    tol_auth_award = px.histogram(data_frame=plt_mean_wd,x='GamingDt',color='AuthAward',opacity=0.8,title='Daily records with different amount')
    if st.checkbox('The total records of ecash download by daily'):
       col7,col8=st.columns(2)  
       col7.plotly_chart(mean_auth_award)
       col8.plotly_chart(tol_auth_award)

# the max & min date of slot rating
if upload_sr is not None:
    st.write('Slot transaction from :',df_sr['GamingDt'].min(), df_sr['GamingDt'].max())
      
    
# Grop by acct for all slot rating
if upload_sr is not None:
    df_sr1=df_sr.groupby('Acct')[['total_plays', 'total_bets', 'total_theorWin', 'total_CasinoWin']].sum().reset_index()
    df_sr1['Acct']=df_sr1['Acct'].astype('object')
    df_ecash['Acct']=df_ecash['Acct'].astype('object')
    e_plt=df_ecash[df_ecash['TranCode']=='CSHSTLPR']
    e_plt2=e_plt.groupby('Acct')[['AwardUsed']].sum().reset_index()
    sr_plt=pd.merge(left=df_sr1,right=e_plt2,on='Acct', how='outer')
    if st.checkbox('The statistics performance of slot rating and ecash_point'):
        st.write(sr_plt.describe())
    if st.checkbox('The correlation of slot rating and ecash_point'):
        col9,col10=st.columns(2) 
        fig2, ax=plt.subplots()
        sns.heatmap(sr_plt.corr(),ax=ax)
        col10.write(fig2)
        col9.write(sr_plt.corr())
        
