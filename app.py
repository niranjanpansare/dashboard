import streamlit as st 
from PIL import Image
import pandas as pd 
import numpy as np
import os 
import matplotlib.pyplot as plt
import plotly.express as px
import time
import seaborn as sns


#page setting 

st.set_page_config(page_title="Dashboard", page_icon="ðŸ ", layout="wide")
st.header("Dashboard")
 
df = pd.read_csv('tips.csv')
revenue = df['total_bill'].sum()
day = df.groupby('day')
sum_based_on_day =  df.groupby('day', as_index=False).sum()
#28.97,20.65
todays_sell = day.first()['total_bill'][0];
yesterdays_sell = day.first()['total_bill'][1];

data_types = df.dtypes
cat_cols = tuple(data_types[data_types == 'object'].index)

value_counts = df['time'].value_counts().index[0]
total = df['time'].value_counts().sum()
dinner_value = df['time'].value_counts()[0]
percentage_dinner = (dinner_value *100 )/total;
 
value_counts_day = df['day'].value_counts().index[0]
#st.dataframe(data=value_counts,width=2000,height=500)

with open('mycss.css') as f:
    st.markdown(f'<style>{f.read()}<style>',unsafe_allow_html=True)

    a1,a2,a3 = st.columns(3)
    a1.metric("Today's Revenue","$ "+ str(todays_sell) , "$ "+str(todays_sell - yesterdays_sell) )
    a2.metric("Most Prefered Time",value_counts)
    a3.metric("Prefered Day ",value_counts_day)


with st.expander(label='Sales and Distribution',expanded=True):
    t1,t2,t3 = st.tabs(["Total sell by Day", "Day wise Bill", "complete View"])
    fig = px.line(sum_based_on_day,x ='day', y="total_bill", color="day", text="total_bill")
    fig.update_traces(textposition="bottom right")
    t1.plotly_chart(fig)
    
    fig = px.bar(df,x="day", y="total_bill")
    t2.plotly_chart(fig)
    data_types = df.dtypes
    cat_cols = tuple(data_types[data_types == 'object'].index)
    path = t3.multiselect('select Feature',
                                    (cat_cols))
    fig = px.sunburst(data_frame=df,path=path)
    t3.plotly_chart(fig)

with st.expander(label='Average Total Bill', expanded=True):
    c1, c2, c3 = st.columns(3)
    with c1:
        group_cols = st.multiselect('select the features',cat_cols,cat_cols[0])
        features_to_groupby = group_cols
        n_features = len(features_to_groupby)
        
    with c2:
        stack_option = st.radio('Stacked',('Yes','No'))
        if stack_option == 'Yes':
            stacked = True
        else:
            stacked = False
            

    feature = ['total_bill']
    select_cols = feature+features_to_groupby
    avg_total_bill = df[select_cols].groupby(features_to_groupby).mean()
    if n_features >1:
        for i in range(n_features-1):
            avg_total_bill = avg_total_bill.unstack()
            
    avg_total_bill.fillna(0,inplace=True)
    
    # visual
    fig = px.bar(df,x="day", y="total_bill")
    t2.plotly_chart(fig)

    fig, ax = plt.subplots()
    avg_total_bill.plot(kind='bar',ax=ax,stacked=stacked)
    ax.legend(loc='center left',bbox_to_anchor=(1.0,0.5))
    ax.set_ylabel('Avg Total Bill')
    c2.pyplot(fig)

    with c3:
        c3.dataframe(avg_total_bill)
  
with st.expander(label='Male & Female Distributions', expanded=False):      
     value_counts = df['gender'].value_counts()
     col1, col2  = st.tabs(["Total Distribution", "Distribution Count"])
     with col1:
          fig = px.pie(value_counts, values=value_counts, names=['Male','Female'])
          col1.plotly_chart(fig)
     with col2:
        col2.dataframe(value_counts)

with st.expander(label='Tip', expanded=False): 
    fig = px.pie(df, values='tip', names='day')
    st.plotly_chart(fig)
   
 