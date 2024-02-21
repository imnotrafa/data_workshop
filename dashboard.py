# Import convention
import streamlit as st
import pandas as pd
import sqlite3
from sqlite3 import Error







#Create the SQL database & Also Connects to it
def create_db():
    try:
        sqliteConnection = sqlite3.connect('sql.db')
    except Error:
        print("Connection to database not possible")
    else:
        return sqliteConnection
    



def create_table(file,table_name):
    if not file or not table_name:
        st.write("Missing values")
    
    else:
        current_file = pd.read_csv(file)
        current_file.to_sql(table_name,con=connection)



#Create connection to the database
connection = create_db()
cursor = connection.cursor()


query1= '''SELECT * FROM JOBS'''
df = pd.read_sql_query(query1,con=connection)





#displays a dataframe
def show_dataframe(df:pd.DataFrame):
    st.dataframe(df)
    

#interactive chart
def interactive_graph():
    #Selecting max salary in dataset
    max_salary_query = '''SELECT MAX(salary_in_usd) FROM JOBS'''
    max_salary = pd.read_sql_query(max_salary_query,connection)
    
    #iloc --> locate values by their index in the dataframe
    max_salary = int(max_salary.iloc[0,0])
    
    #Creates a Salary Slider
    salary_range = st.slider("Salart Range:",0,max_salary,step=10000)

    st.write(''' # Sorted By salary and Location ''')
    range_query = f'''SELECT job_title, employee_residence, salary_in_usd 
    FROM JOBS 
    WHERE salary_in_usd BETWEEN 0 AND {salary_range} 
    ORDER BY salary_in_usd DESC, employee_residence'''

    new_dataframe = pd.read_sql_query(range_query,connection)

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

    cleaned_df = pd.read_sql_query(cleaned_query,connection)


    show_dataframe(cleaned_df)


    




#Main application function
def initialized_dashboard():
    st.header("""    
    # Welcome To HACCS SQL & Python Workshop
    """)
    #Drop-Down where we can upload a file and create a table with it
    with st.expander("Upload a file to database"):
        table_name = st.text_input("Name of the table")
        file_upload = st.file_uploader("Upload a CSV file")
        
        button = st.button("Submit",type="primary")    
    if button:
        #Create connection to the database
        create_table(file=file_upload,table_name=table_name)
    #Drop down where we can Preview RAW Data
    with st.expander("Data Preview"):
        show_dataframe(df)

    with st.expander("Interactive Graph"):
        st.write("Drop in your salary range")
        interactive_graph()






initialized_dashboard()