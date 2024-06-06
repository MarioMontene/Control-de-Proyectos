import pandas as pd
import plotly.express as px
import streamlit as st 

from streamlit_dynamic_filters import DynamicFilters

# Configuraciones generales de la página
st.set_page_config(page_title="Log de Cambios W1 Ore Dashboard",
                   page_icon=":building_construction:",
                   layout="wide"
)

# Lectura de datos
datos = pd.read_excel(r'C:\000 WORKSPACE\700 SOPORTE\PYTHON\24.06.03 Change Log 5.xlsx')

# Cambio de fecha al formato correcto
datos['Date'] = pd.to_datetime(datos['Date']).dt.strftime('%m/%d/%Y')

# Filtraciones dinámicas
dynamic_filters = DynamicFilters(datos, filters=['Prime_Code', 'State', 'Document_Type'])
st.sidebar.header("Filtrar aquí:")

datos_selection = dynamic_filters.filter_df()

with st.sidebar:
   dynamic_filters.display_filters()
dynamic_filters.display_df()

#datos_selection = dynamic_filters.filter_df()

# Página Principal
st.title(":bar_chart: Change Log W1 Ore")
st.markdown("##")

# Top KPI's
total_sdc = int(datos_selection["Amount"].sum())
hh = round(datos_selection["HH"].mean(), 0)
man_rating = ":construction_worker:" * int(round(hh, 0))
average_hh_by_amount = round(datos_selection["HH"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Amount:")
    st.subheader(f"US $ {total_sdc:,}")
with middle_column:
    st.subheader("HH:")
    st.subheader(f"{hh} {man_rating}")
with left_column:
    st.subheader("HH Per Amount:")
    st.subheader(f"HH {average_hh_by_amount}")

st.markdown("---")

# Positive and Negative Number
def pos(col):  
  return col[col > 0].sum() 
  
def neg(col):  
  return col[col < 0].sum() 

d = datos.groupby(datos_selection['Document_Type'])
print(d['Amount'].agg([('negative_values', neg),
                       ('positive_values', pos)
                       ]))

# Amount by Nature of Change [BAR CHART]
amount_by_nature_of_change = datos_selection.groupby(by=["Nature_of_change"])[["Amount"]].sum().sort_values(by="Amount")
fig_natureofchange_amount = px.bar(
    amount_by_nature_of_change,
    x="Amount",
    y=amount_by_nature_of_change.index,
    orientation="h",
    title="<b>Amount by Nature of Change</b>",
    color_discrete_sequence=["#0083B8"] * len(amount_by_nature_of_change),
    template="plotly_white",
)
fig_natureofchange_amount.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
st.plotly_chart(fig_natureofchange_amount)

# Date by Amount

sales_by_hour = datos_selection.groupby(by=["Date"])[["Amount"]].sum()
fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Amount",
    title="<b>Date by Amount</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    template="plotly_white",
)
fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)
st.plotly_chart(fig_hourly_sales)



















