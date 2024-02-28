# Import convention
import streamlit as st
import pandas as pd
import sqlite3
from sqlite3 import Error

import plotly.express as px




#Main application function
def initialized_dashboard():
    st.header("Welcome to HACCS Data Workshop :sunglasses:",divider="orange")
    #Drop-Down where we can upload a file and create a table with it
    with st.expander("Upload a file to database"):
        table_name = st.text_input("Name of the table")
        file_upload = st.file_uploader("Upload a CSV file")
        
        button = st.button("Submit",type="primary")    
        if button:
            #Create create_db() to the database
            create_table(file=file_upload,table_name=table_name)
    #Drop down where we can Preview RAW Data
   

    #SHowcase our raw data
    initial_data()

    interactive_graph()

    interactive_pie_chart()



#Create the SQL database and Connection
def create_db():
    try:
        sqliteConnection = sqlite3.connect('sql.db')
    except Error:
        print("Connection to database not possible")
    else:
        return sqliteConnection
    

#Creates a table
def create_table(file,table_name):
    if not file or not table_name:
        st.write("Missing values")
    
    else:
        current_file = pd.read_csv(file)
        number_of_rows = current_file.to_sql(table_name,create_db())

        if number_of_rows >0:
            st.write("Table has been created")

        



#Shows raw data
def initial_data():
      
    #Create create_db() to the database
    with st.expander("Initial Data"):
        query1= '''SELECT * FROM JOBS'''
        df = pd.read_sql_query(query1,create_db())

        show_dataframe(df)

#Displays a dataframe as a table
def show_dataframe(df:pd.DataFrame):
    st.dataframe(df)
    



#interactive Pie chart
def interactive_pie_chart():
    with st.expander("Interactive pie chart"):
        salary_range2 = create_slider(2)
        
        select_box = st.selectbox("What would you like to see",("job_title","company_location"),index=None,placeholder="Select One from the following")
        
        #Salaries &  name = Country 

        # Salary &  name = Jobs    
        query = f'''SELECT * FROM JOBS WHERE salary_in_usd BETWEEN 0 AND {salary_range2}'''
        df = pd.read_sql_query(query,create_db())

        df = df.head(n=10)
        fig = px.pie(data_frame=df,values="salary_in_usd",names=select_box)

        st.plotly_chart(fig)
   
#interactive charts
def interactive_graph():
   with st.expander("Interactive data"):
    salary_range = create_slider(1)

    st.write(''' # Sorted By salary and Location ''')
    range_query = f'''SELECT job_title, employee_residence, salary_in_usd 
    FROM JOBS 
    WHERE salary_in_usd BETWEEN 0 AND {salary_range} 
    ORDER BY salary_in_usd ASC'''

    new_dataframe = pd.read_sql_query(range_query,create_db())

    show_dataframe(new_dataframe)


    
    st.write('''
    # Gruped By Job_title
    ''')
    # We want the job title only
    cleaned_query = f'''SELECT job_title, employee_residence, salary_in_usd 
    FROM JOBS 
    WHERE salary_in_usd BETWEEN 0 AND {salary_range}
    GROUP BY job_title
    ORDER BY salary_in_usd DESC, employee_residence'''

    cleaned_df = pd.read_sql_query(cleaned_query,create_db())


    show_dataframe(cleaned_df)

    return salary_range


#Creates a slider obeject
def create_slider(key):
     #Selecting max salary in dataset
    max_salary_query = '''SELECT MAX(salary_in_usd) FROM JOBS'''
    max_salary = pd.read_sql_query(max_salary_query,create_db())
    
    #iloc --> locate values by their index in the dataframe
    max_salary = int(max_salary.iloc[0,0])
    
    #returns a slider object
    return st.slider("Salary Range:",0,max_salary,step=10000,key=key)





initialized_dashboard()

