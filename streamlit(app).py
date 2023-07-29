import streamlit as st 
from sqlalchemy.sql import text
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.express as px


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
    fig = px.scatter_geo(df, lat='Latitude', lon='Longitude', size='Transaction count', hover_name='state',
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
if __name__ == "__main__":
    dataframe1 = pd.read_csv(r"C:\Users\AGM MSME PNB\OneDrive\Desktop\Sashidhar\Data scince\Projects\Phonepe Pulse Data Visualization\States_lat_long.csv")
    latitue_key_val = dict(zip(dataframe1['Name'], dataframe1['Latitude']))
    lonitude_key_val = dict(zip(dataframe1['Name'], dataframe1['Longitude']))

    question1()
    question2()  
    question3() 
    question4(dataframe1)
    question5()
    question6()