import streamlit

streamlit.title('My parents new healthy diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 omega 3 &  Blueberry oatmeal')
streamlit.text('🥗Kale, Spinach and rocket smoothie')
streamlit.text('🐔Hard-boiled free-range egg')
streamlit.text('🥑🍞 Avacado toast')
streamlit.header('🍌🥭 Build your own fruit smoothies')
import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page
streamlit.dataframe(fruits_to_show)

#New Section to display api responses
streamlit.header("Fruityvice Fruit Advice!")
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

# take the jason file of response and normalize it 
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
#output it as in the screen 
streamlit.dataframe(fruityvice_normalized)

import snowflake.connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_row = my_cur.fetchone()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_row)


