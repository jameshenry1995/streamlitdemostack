import pandas as pd # loading pandas
import numpy as np # loading numpy
import altair as alt # loading altair
import streamlit as st # loading streamlit
alt.renderers.enable('altair_viewer') # enabling renderer for Altair

# ----- Setting the DashBoard Parameters -----

st.set_page_config(page_title = 'expense dashboard',
                   page_icon = ':bar_chrt:',
                   layout = 'wide'
                   )



# ----- Loading Data -----
df = pd.read_csv('customer_shopping_data.csv') # loading the customer shopping data .csv file obtained from kaggle




# ----- Descriptive Analysis -----

print(df.columns) # printing the column names

#print(df.shape) # printing the dimensions of the data

#print(df.head()) # printing the first few rows of the dataset1


groupby_columns = ['gender', 'category', 'payment_method', 'shopping_mall']
color_columns = ['quantity', 'price']
colorise_operations = ['sum','mean']

# -----------SIDEBAR-----------
st.sidebar.header('Plot and Table Selectors')
groupby_column = st.sidebar.selectbox('Select Column from the Data:', options = groupby_columns)
color_column = st.sidebar.selectbox('Numeric Column to Aggregate:', options = color_columns)
colorise_operation = st.sidebar.selectbox('Operation to Display on the Colour Scale:', options = colorise_operations)
#groupby_column = 'gender'



#df_grouped = df.groupby(groupby_column).size().to_frame('count').reset_index() # grouping by payment type and counting
df_grouped = df.groupby(groupby_column).agg({
    'customer_id': ['count'],
    color_column: colorise_operations
}).round(0).reset_index() # grouping by payment type and counting



df_grouped.columns = [groupby_column, 'count', 'sum', 'mean']


df_grouped['percentage'] = (df_grouped['count'] / df_grouped['count'].sum()).apply(lambda x: f'{x:.2%}')


#print(df_grouped)



# -----------Main Page-----------
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

col1, col2 = st.columns([0.35,0.65])




grouped_chart = alt.Chart(df_grouped).mark_bar().encode(
    x = 'count',
    y = groupby_column,
    color = alt.Color(field = colorise_operation,
                      type = "quantitative",
                      legend = alt.Legend(title= ''.join([colorise_operation, ' of the ', color_column, ' Column'])),
                      scale = alt.Scale(scheme = alt.SchemeParams(name = 'turbo',
                                                                  extent = [0.5, 1]))
                      ),
    tooltip = [alt.Tooltip(groupby_column,
                           title = 'Variable'),
               alt.Tooltip('count',
                           format = ',',
                           title = 'Nb. of Obs.'),
               alt.Tooltip('percentage',
                           title = 'Percentage')]
).properties(
    height = 500,
    width = 1000
)

col1.write(df_grouped)



col2.altair_chart(grouped_chart, use_container_width=True)



#grouped_chart.show()