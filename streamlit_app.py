import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My parents new healthy diner')

streamlit.header('Breakfast Menu')
streamlit.text('๐ฅฃ omega 3 &  Blueberry oatmeal')
streamlit.text('๐ฅKale, Spinach and rocket smoothie')
streamlit.text('๐Hard-boiled free-range egg')
streamlit.text('๐ฅ๐ Avacado toast')
streamlit.header('๐๐ฅญ Build your own fruit smoothies')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" +fruit_choice)

#take the json version of response 
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
#output it the screen as table
streamlit.dataframe(fruityvice_normalized)

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)
add_my_fruit = streamlit.text_input('What fruit would you like to add?') 
streamlit.write('Thanks for adding ', add_my_fruit)
my_cur.execute("insert into fruit_load_list values('kiwi')")  
