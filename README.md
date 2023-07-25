# Phonepe-Pulse-Data-Visualization
The problem statement is Visualizing the phone pay users and transactions related data by taking the Data from Phonepe pulse Github repository which contains a large amount of data related to various metrics and statistics. The goal is to extract this data and process it to obtain insights and information that can be visualized in a user-friendly manner using live geo visualization dashboard.

# Languages and technologies used:
Git
Github Cloning 
Python
Pandas
MySQL connection using mysql-connector-python library
Streamlit and Plotly

# Code Overview and approach:

1) Data extraction: Cloned the Github phone pay data using Git commands scripting to fetch the data from the Phonepe pulse Github repository and store it in Loacal desktop
2) Data transformation: Use a scripting language such as Python, along with
libraries such as Pandas, to manipulate and pre-process the data. This may
include cleaning the data, handling missing values, and transforming the data
into a format suitable for analysis and visualization.
3. Database insertion: Use the "mysql-connector-python" library in Python to
connect to a MySQL database and insert the transformed data using SQL
commands.
4. Dashboard creation: Use the Streamlit and Plotly libraries in Python to create
an interactive and visually appealing dashboard. Plotly's built-in geo map
functions can be used to display the data on a map and Streamlit can be used
to create a user-friendly interface with multiple dropdown options for users to
select different facts and figures to display.
5. Data retrieval: Use the "mysql-connector-python" library to connect to the
MySQL database and fetch the data into a Pandas dataframe. Use the data in
the dataframe to update the dashboard dynamically.
# Dataset Link:
https://github.com/PhonePe/pulse#readme
