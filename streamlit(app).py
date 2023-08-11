import streamlit as st 
from sqlalchemy.sql import text
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from PIL import Image


st.title("Guvi's Pulse Data analysis Analysis")
image = Image.open('guvi_image.jpg')
st.image(image, caption='Guvi Brand Amabassador')


def question1():
    conn = st.experimental_connection('mysql', type='sql')
    st.subheader('Sates and Transaction Count')
    df = conn.query('select state, sum(transacion_count) "Transaction count" from aggregate_Transacion group by state', ttl=600)
    st.dataframe(df)


def question2(dataframe1):
    conn = st.experimental_connection('mysql', type='sql')
    st.subheader('Geographical representation of states and Transaction Count')
    df = conn.query('select state, sum(transacion_count) "Transaction count" from aggregate_Transacion group by state', ttl=600)
    l1=[]
    l2=[]
    for i in df['state']:
        l1.append(latitue_key_val[i])
    for i in df['state']:
        l2.append(lonitude_key_val[i])
    df['Latitude'] = l1
    df['Longitude'] = l2
    #st.dataframe(df)
    fig = px.scatter_geo(df, lat='Latitude', lon='Longitude', size='Transaction count', hover_name='state',
                         title='Transaction count in Indian states')
    fig.update_layout(
        
        geo_scope='asia'
    )
    st.plotly_chart(fig)



def question3():
    conn = st.experimental_connection('mysql', type='sql')
    st.subheader('Graphical representation of Count based on transaction Type')
    df = conn.query('select Transacion_type , sum(Transacion_count) sum from aggregate_transacion group by Transacion_type having  Transacion_type <> "Others"', ttl=600)
    fig, ax = plt.subplots()
    ax.pie(df['sum'], labels=df['Transacion_type'], autopct='%1.1f%%', startangle=140)
    ax.axis('equal')  # Equal aspect ratio ensures that the pie is drawn as a circle.
    st.pyplot(fig)


def question4():
    conn = st.experimental_connection('mysql', type='sql')
    st.subheader('Year wise Transaction Count')
    df = conn.query('select year,sum(transacion_count) sum from aggregate_transacion group by year order by 2', ttl=600)
    fig, ax = plt.subplots()
    bars = ax.bar(df['year'], df['sum'])
    ax.bar(df['year'], df['sum'])
    plt.xticks(rotation=45)  # Rotate the category labels for better visibility
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height, str(height),
                ha='center', va='bottom')
    st.pyplot(fig)

def question5():
    conn = st.experimental_connection('mysql', type='sql')
    st.subheader('Predection of Year wise transacion count')
    user_input = st.text_input("Year whose transaction count to be predicted:")
    df = conn.query('select year,sum(transacion_count) sum from aggregate_transacion group by year', ttl=600)
    X=df['year']
    y=df['sum']
    model = LinearRegression()
    x_train,x_test,y_train,y_test=train_test_split(X,y,test_size=0.2)
    st.write(df)
    model.fit(X.values.reshape(-1, 1), y.values.reshape(-1, 1))
    if user_input.strip(): 
        original_array = np.array([int(user_input)])
        reshaped_array = original_array.reshape(-1, 1)
        y_pred = model.predict(reshaped_array)   
        st.write('transaction value predicted as on ' + user_input + ' is: ' + str(y_pred[0]/1000000000) + ' billions')
        st.write(y_pred)
        
    else:
        st.write("give year value in text box")
        
    

def question6():
    conn = st.experimental_connection('mysql', type='sql')
    st.subheader('Count of Quarters with Maximum transaction in Year')
    df = conn.query('select concat( "Q", quarter) as "Quarter Number for Max no of transactions", count(*) as count from (\
    select quarter from (\
    SELECT quarter, amt ,\
    max(amt) OVER( PARTITION BY year) AS max_amt from (\
    select year,quarter,sum(transacion_amount) amt from  aggregate_transacion group by year,quarter) sub ) sub1\
    where amt = max_amt) sub2 group by quarter ', ttl=600)
    df=df.set_index("Quarter Number for Max no of transactions")
    st.dataframe(df)

def question7():
    conn = st.experimental_connection('mysql', type='sql')
    st.subheader('States with Maximum users For a Year')
    df = conn.query('select "Maximum users For a Year",state, year , district , amount from (\
        select state, year, district , amount , max(amount) over (partition by Year) max_amount from top_trans) sub\
        where amount = max_amount \
        union all \
        select "Minimum users For a Year ",state, year , district , amount from ( \
        select state, year, district , amount , min(amount) over (partition by Year) max_amount from top_trans) sub \
        where amount = max_amount ', ttl=600)
    df=df.set_index("Maximum users For a Year")
    st.dataframe(df)

def question8():
    conn = st.experimental_connection('mysql', type='sql')
    st.subheader('States with increasing trend of transactions')
    df = conn.query('select state , t4 "Registerd Users" from (\
         select state,  total_count t0 , LEAD(total_count, 1)  over(partition by state) t1 , \
         LEAD(total_count, 2)  over(partition by state) t2 , LEAD(total_count, 3)  over(partition by state)t3, \
         LEAD(total_count, 4)  over(partition by state) t4 from (\
         select state,year, sum(registeredUsers) total_count from top_trans group by state , year) sub ) sub2\
         where  t0 < t1 and t1 <  t2 and t2 <  t3 and t3 <  t4  \
         order by t4 desc Limit  10', ttl=600)
    df=df.set_index("state")
    st.dataframe(df)

def question9():
    conn = st.experimental_connection('mysql', type='sql')
    st.subheader('States with Decreasing trend of transactions')
    df = conn.query('select state , t4 registerdUsers from ( \
         select state,  total_count t0 , LEAD(total_count, 1)  over(partition by state) t1 , \
         LEAD(total_count, 2)  over(partition by state) t2 , LEAD(total_count, 3)  over(partition by state)t3, \
         LEAD(total_count, 4)  over(partition by state) t4 from ( \
         select state,year, sum(registeredUsers) total_count from top_trans group by state , year) sub ) sub2 \
         where  t0 > t1 or t1 >  t2 or t2 >  t3 or t3 >  t4  \
         order by t4 desc Limit  10', ttl=600)
    df=df.set_index("state")
    st.dataframe(df)

def question10():
    conn = st.experimental_connection('mysql', type='sql')
    st.subheader('Top districts and states registered users list')
    year_input = st.text_input("Year  transaction count to be predicted:")
    if year_input.strip():
        quarter_input = st.text_input("quarter who transaction count to be predicted:")
    if year_input.strip() and quarter_input.strip() : 
        df = conn.query('select state , Year, Quarter, registeredUsers from top_users where ( year , quarter , registeredUsers ) in (\
                    select year,quarter , users from (\
                    select year, quarter, max(registeredUsers) users from top_users  \
                    group by year , quarter ) sub  where year =' + year_input + ' and quarter = '+ quarter_input + ')' 
                    , ttl=600)
        df=df.set_index("state")
        st.dataframe(df)





if __name__ == "__main__":
    options = ['Sates and Transaction Count', 
    'Geographical representation of states and Transaction Count', 
    'Graphical representation of Count based on transaction Type', 
    'Year wise Transaction Count',
    'Predection of Year wise transacion count', 
    'Count of Quarters with Maximum transaction in Year',
    'States with Maximum users For a Year',
    'States with increasing trend of transactions', 
    'States with Decreasing trend of transactions',
    'Top districts and states registered users list',
     'ALL']
    dataframe1 = pd.read_csv(r"C:\Users\AGM MSME PNB\OneDrive\Desktop\Sashidhar\Data scince\Projects\Phonepe Pulse Data Visualization\States_lat_long.csv")
    latitue_key_val = dict(zip(dataframe1['Name'], dataframe1['Latitude']))
    lonitude_key_val = dict(zip(dataframe1['Name'], dataframe1['Longitude']))
    selected_options = st.multiselect('Select options:', options)
    if 'States with Maximum users For a Year' in  selected_options or 'ALL' in  selected_options :
        question7()
    if 'Sates and Transaction Count' in  selected_options or 'ALL' in  selected_options :
        question1()
    if 'Geographical representation of states and Transaction Count' in  selected_options or 'ALL' in  selected_options :
        question2(dataframe1)  
    if 'Graphical representation of Count based on transaction Type' in  selected_options or 'ALL' in  selected_options :
        question3() 
    if 'Year wise Transaction Count' in  selected_options or 'ALL' in  selected_options :
        question4()
    if 'Predection of Year wise transacion count' in  selected_options or 'ALL' in  selected_options :
        question5()
    if 'Count of Quarters with Maximum transaction in Year' in  selected_options or 'ALL' in  selected_options :
        question6()
    if 'States with increasing trend of transactions' in  selected_options or 'ALL' in  selected_options :
        question8()
    if 'States with Decreasing trend of transactions' in  selected_options or 'ALL' in  selected_options :
        question9()
    if 'Top districts and states registered users list' in  selected_options or 'ALL' in  selected_options :
        question10()
   