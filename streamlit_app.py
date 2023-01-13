import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My parents new healthy diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 omega 3 &  Blueberry oatmeal')
streamlit.text('🥗Kale, Spinach and rocket smoothie')
streamlit.text('🐔Hard-boiled free-range egg')
streamlit.text('🥑🍞 Avacado toast')
streamlit.header('🍌🥭 Build your own fruit smoothies')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page
streamlit.dataframe(fruits_to_show)

#create the repetable block (called a function)
def get_fruityvice_data(fruit_choice):
    from pandas.io.json import json_normalize
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

#new section to display fruityvice api response
streamlit.header('Fruityvice Fruit Advice!') 
try: 
    fruit_choice = streamlit.text_input('What fruit would you like information about?') 
    if not fruit_choice: 
        streamlit.error("Please select a fruit to get information.") 
    else: 
        back_from_function = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(fruityvice_normalized)
        
except URLError as e:
  streamlit.error()
  

streamlit.header("The Fruit Load List Contain:")
#snowflake related function
def get_fruit_load_list():
    with my_cur.cursor() as my_cur:
         my_cur.execute("select * from fruit_load_list")
         return my_cur.fetchall()
#Add a button to load the fruit 
if streamlit.button('Get Fruit Load List'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"]) 
   my_data_rows = get_fruit_load_list()
   streamlit.dataframe(my_data_rows)

#Allow the end user to add fruit to the list
def insert_snowflake_row(new_fruit):
    with my_cnx.cursor() as my_cur:
         my_cur.execute("insert into fruit_load_list values('"+ add_my_fruit +"')")
         return "Thanks for adding" + new_fruit

#Allow the end user add a fruit to the list
add_my_fruit = streamlit.text_input('What fruit would you like to add ?') 
if streamlit.button('Add a fruit to the list'): 
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"]) 
    my_cnx.close()
    back_from_function = insert_row_snowflake(add_my_fruit) 
    streamlit.text(back_from_function)

