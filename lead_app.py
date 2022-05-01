from datetime import datetime
from email.policy import default
import types
import click
import streamlit as st
import pandas as pd
import datetime as dt

st.title('Lead Generation Application')
st.header('Inputs')

# filters
filter_values = dict()

# date
col1, col2 = st.columns(2)
start_date = col1.date_input("Transaction effective start date", value = dt.datetime.now().replace(month=1, day=1))
end_date = col2.date_input("Transaction effective end date")
date_cond = f'''
effective_date BETWEEN {start_date} AND {end_date} 
AND dt BETWEEN '{start_date.strftime("%Y%m%d")}' AND '{end_date.strftime("%Y%m%d")}' 
'''

# products
products: list = st.multiselect("Product", ["Fund", "Stock", "Offshore"])
fund_categories = None
if "Fund" in products or "All" in products:
    fund_categories = st.multiselect('Fund Category', ["All", "Money market", "Equity", "Fixed Income"])

product_txn_amt = None
product_aum_amt = None
if st.checkbox("Behavior"):
    # behavior
    product_txn_amt = st.number_input('Minimum Transaction amount', 0)
    product_aum_amt = st.number_input('Minimum AUM amount', 0)
    
# submit
if st.button("Submit"):
    filter_values['dates'] = {'start_date' : start_date, 'end_date' : end_date}
    filter_values['products'] = {'products' : products, 'sub_products_fund' : fund_categories}
    filter_values['behavior'] = {'product_txn_amt' : product_txn_amt, 'product_aum_amt' : product_aum_amt}
    st.write(filter_values)