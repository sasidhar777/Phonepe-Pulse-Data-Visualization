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


st.title("Guvi's Pulse Data analysis Analysis")

def question1():
    conn = st.experimental_connection('mysql', type='sql')
    st.subheader('Names of all videos and their corresponding channels')
    df = conn.query('select state, sum(transacion_count) "Transaction count" from aggregate_Transacion group by state', ttl=600)
    st.dataframe(df)

def question2():
    # Sample geographical data (latitude, longitude, and value)
    data = {
        'City': ['New York', 'San Francisco', 'Chicago'],
        'Lat': [40.7128, 37.7749, 41.8781],
        'Lon': [-74.0060, -122.4194, -87.6298],
        'Population': [8398748, 883305, 2716000]
    }

    # Create a DataFrame from the sample data
    df = pd.DataFrame(data)

    # Create a Streamlit app
    st.title('Geographical Visualization using Plotly')
    st.write('Sample geographical data visualization using Plotly')

    # Plot geographical data using Plotly and display in Streamlit
    fig = px.scatter_geo(df, lat='Lat', lon='Lon', size='Population', hover_name='City',
                        projection='albers usa', title='Population in US Cities')
    st.plotly_chart(fig)


def question3():
    # Sample geographical data (latitude, longitude, and value)
    data = {
        'City': ['andaman-&-nicobar-islands', 'andhra-pradesh', 'bihar'],
        'Lat': [10.2188344, 15.9240905, 25.6440845],
        'Lon': [92.5771329, 80.1863809, 85.906508],
        'Population': [8398748, 883305, 2716000]
    }

    # Create a DataFrame from the sample data
    df = pd.DataFrame(data)

    # Create a Streamlit app
    st.title('Geographical Visualization using Plotly')
    st.write('Sample geographical data visualization using Plotly')

    # Plot geographical data using Plotly and display in Streamlit
    fig = px.scatter_geo(df, lat='Lat', lon='Lon', size='Population', hover_name='City',
                         title='Population in US Cities')
    st.plotly_chart(fig)

def question4(dataframe1):
    conn = st.experimental_connection('mysql', type='sql')
    st.subheader('Names of all videos and their corresponding channels')
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
    fig = px.scatter_geo(df,  lat='Latitude', lon='Longitude', size='Transaction count', hover_name='state',
                         title='Population in US Cities')
    st.plotly_chart(fig)

def question5():
    conn = st.experimental_connection('mysql', type='sql')
    st.subheader('Names of all videos and their corresponding channels')
    df = conn.query('select Transacion_type , sum(Transacion_count) sum from aggregate_transacion group by Transacion_type having  Transacion_type <> "Others"', ttl=600)
    fig, ax = plt.subplots()
    ax.pie(df['sum'], labels=df['Transacion_type'], autopct='%1.1f%%', startangle=140)
    ax.axis('equal')  # Equal aspect ratio ensures that the pie is drawn as a circle.
    st.pyplot(fig)

def question5():
    conn = st.experimental_connection('mysql', type='sql')
    st.subheader('Names of all videos and their corresponding channels')
    df = conn.query('select Transacion_type , sum(Transacion_count) sum from aggregate_transacion group by Transacion_type having  Transacion_type <> "Others"', ttl=600)
    fig, ax = plt.subplots()
    ax.pie(df['sum'], labels=df['Transacion_type'], autopct='%1.1f%%', startangle=140)
    ax.axis('equal')  # Equal aspect ratio ensures that the pie is drawn as a circle.
    st.pyplot(fig)

def question6():
    conn = st.experimental_connection('mysql', type='sql')
    st.subheader('Names of all videos and their corresponding channels')
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

def question7():
    conn = st.experimental_connection('mysql', type='sql')
    st.subheader('Names of all videos and their corresponding channels')
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
        
    

def question8():
    conn = st.experimental_connection('mysql', type='sql')
    st.subheader('Names of all videos and their corresponding channels')
    df = conn.query('select quarter as "Max Transaction in Year", count(*) as count from (\
    select quarter from (\
    SELECT quarter, amt ,\
    max(amt) OVER( PARTITION BY year) AS max_amt from (\
    select year,quarter,sum(transacion_amount) amt from  aggregate_transacion group by year,quarter) sub ) sub1\
    where amt = max_amt) sub2 group by quarter ', ttl=600)
    df=df.set_index("Max Transaction in Year")
    st.dataframe(df)
'''
def question8():

    map_center = [20.5937, 78.9629]
    m = folium.Map(location=map_center, zoom_start=5)
    folium.Marker(location=map_center, popup="India").add_to(m)
    folium_static(m)'''

def question9(dataframe1):
    conn = st.experimental_connection('mysql', type='sql')
    st.subheader('Names of all videos and their corresponding channels')
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
                         title='Population in US Cities')
    fig.update_layout(
        
        geo_scope='asia'
    )
    st.plotly_chart(fig)



if __name__ == "__main__":
    options = ['Option 1', 'Option 2', 'Option 3', 'Option 4','Option 6', 'Option 7','Option 8','ALL']
    dataframe1 = pd.read_csv(r"C:\Users\AGM MSME PNB\OneDrive\Desktop\Sashidhar\Data scince\Projects\Phonepe Pulse Data Visualization\States_lat_long.csv")
    latitue_key_val = dict(zip(dataframe1['Name'], dataframe1['Latitude']))
    lonitude_key_val = dict(zip(dataframe1['Name'], dataframe1['Longitude']))
    selected_options = st.multiselect('Select options:', options)
    if 'Option 7' in  selected_options or 'ALL' in  selected_options :
        question7()
    '''
    if 'Option 1' in  selected_options or 'ALL' in  selected_options :
        question1()
    if 'Option 2' in  selected_options or 'ALL' in  selected_options :
        question2()  
    if 'Option 3' in  selected_options or 'ALL' in  selected_options :
        question3() 
    if 'Option 4' in  selected_options or 'ALL' in  selected_options :
        question4(dataframe1)
    
    question5()
    question6()'''