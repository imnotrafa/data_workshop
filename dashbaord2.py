
import streamlit as st
import pandas as pd
import sqlite3
from sqlite3 import Error
import plotly.express as px



def initialized_dashboard():

    with st.expander("Dashboard"):
        input_text = st.text_input("")

        input_file = st.file_uploader(label="Upload file")

        button = st.button("submit")

        if button:
            create_table(data=input_file,table_name=input_text)
    
    with st.expander("Intial data"):
        initial_state()

    interactive_graph()

    pie_chart()


def connect_db():
    try:
        connection = sqlite3.connect("sql.db")
    except Error:
        st.write("Could not connect")
        return False 
    else:
        return connection

def create_table(data,table_name):

    df = pd.read_csv(data)

    number_rows = df.to_sql(table_name,connect_db())

    if number_rows > 0:
        st.write("Data has been inserted")


def initial_state():
    query = '''SELECT * FROM JOBS'''

    df = pd.read_sql_query(query,connect_db())
    
    show_data(df)

def show_data(data:pd.DataFrame):
    
    st.dataframe(data)



def create_slider(key):
  #Selecting max salary in dataset
  max_salary_query = '''SELECT MAX(salary_in_usd) FROM JOBS'''
  max_salary = pd.read_sql_query(max_salary_query,connect_db())

  #iloc --> locate values by their index in the dataframe
  max_salary = int(max_salary.iloc[0,0])
  
  #returns a slider object
  return st.slider("Salary Range:",0,max_salary,step=10000,key=key)


def interactive_graph():
  with st.expander("Interactive data"):
    salary_range = create_slider(1)

    st.write(''' # Sorted By salary and Location ''')
    range_query = f'''SELECT job_title,employee_residence,salary_in_usd 
    FROM JOBS WHERE salary_in_usd BETWEEN 0 AND {salary_range} ORDER BY salary_in_usd DESC'''

    new_dataframe = pd.read_sql_query(range_query,connect_db())

    show_data(new_dataframe)
    
    
    #GROUP BY job_title
   
 
""" Add this function to the initialized_dashbaord()"""
    

def pie_chart():
  with st.expander("Interactive Pie Chart"):
    salary_range2 = create_slider(2)
    
    select_box = st.selectbox("Choose",("job_title","comapny_location"),index=None,placeholder="Select")
    
    query = f'''SELECT * FROM JOBS WHERE salary_in_usd BETWEEN 0 AND {salary_range2}'''
    
    df = pd.read_sql_query(query,connect_db())
    
    #select only the 10 first rows
    df=df.head(n=10)
    
    #using plotly
       
         
    fig = px.pie(df,values="salary_in_usd",names=select_box)
    
    st.plotly_chart(fig)
  
    




    

initialized_dashboard()

