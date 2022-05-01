from datetime import datetime
from email.policy import default
from gc import callbacks
from subprocess import call
from tkinter import Button
from matplotlib.style import available
import streamlit as st
import pandas as pd
import datetime as dt

def fix_template():

    st.title('Lead Generation Application')
    st.header('Inputs')

    # date
    col1, col2 = st.columns(2)
    st.session_state['input_start_date'] = col1.date_input("Transaction effective start date", value = dt.datetime.now().replace(month=1, day=1), on_change = fix_template if not st.session_state.num_filter else update_filters)
    st.session_state['input_end_date'] = col2.date_input("Transaction effective end date", on_change = fix_template if not st.session_state.num_filter else update_filters)

    # pre-defines
    st.session_state['input_products'] = st.multiselect("Product", ["Fund", "Stock", "Offshore"], default='Fund', on_change = fix_template if not st.session_state.num_filter else update_filters)
    st.session_state['input_fund_categories'] = None
    if "Fund" in st.session_state['input_products'] or "All" in st.session_state['input_products']:
        st.session_state['input_fund_categories'] = st.multiselect('Fund Category', ["All", "Money market", "Equity", "Fixed Income"], default = "All", on_change = fix_template if not st.session_state.num_filter else update_filters)

    st.session_state.is_fix_template_called = True

# dynamic conditions

def dynamic_condition(i):
    '''
    Return new dynamic filters
    '''
    available_cols = [f'col_{i}' for i in range(1,11)]
    col1, col2, col3 = st.columns(3)
    col1.selectbox(f'condition_{i}', ['AND', 'OR'], key = f'input_condition_{i}', on_change = update_filters)
    col2.selectbox(f'feature_{i}', available_cols, key = f'input_feature_{i}', on_change = update_filters)
    col3.number_input(f'value_{i}', 0, key = f'input_value_{i}', on_change = update_filters)

def update_filters():
    '''
    load the fix tempalte and current filters
    '''

    st.session_state.is_fix_template_called = False
    if not st.session_state.is_fix_template_called:
        fix_template()

    for _ in range(st.session_state.num_filter):
        dynamic_condition(_)

    # st.session_state.is_submit_button_rendered = False
    # if not st.session_state.is_submit_button_rendered:
    #     submit = st.button('submit')

def add_filters():
    '''
    load the fix tempalte and current filters plus new filters
    '''
    
    st.session_state.is_fix_template_called = False
    if not st.session_state.is_fix_template_called:
        fix_template()

    st.session_state.num_filter += 1
    for _ in range(st.session_state.num_filter):
        dynamic_condition(_)

def remove_filter():

    st.session_state.is_fix_template_called = False
    if not st.session_state.is_fix_template_called:
        fix_template()

    st.session_state.num_filter -= 1
    for _ in range(st.session_state.num_filter):
        dynamic_condition(_)

    # delte state
    current_state = st.session_state.num_filter
    for key in ['condition', 'feature', 'value']:
        del st.session_state[f'{key}_{current_state}']

# Inital state

if 'num_filter' not in st.session_state:
    st.session_state.num_filter = 0

if 'is_fix_template_called' not in st.session_state:
    st.session_state.is_fix_template_called = False

if not st.session_state.is_fix_template_called:
    fix_template()

col1, col2, col3 = st.columns(3)
add_button = col1.button('add_filter', on_click = add_filters),
refresh_button = col2.button('refresh', on_click = update_filters),
remove_button = col3.button('remove_filter', on_click = remove_filter),
submit_button = st.button("submit", on_click=update_filters)

# submit
filter_values = {}
if submit_button:

    input_args = dict(st.session_state)
    sorted_dict = dict(sorted(input_args.items()))
    st.write(sorted_dict)
    
    
    # group of conditions
    # filter_values['dates'] = {'start_date' : start_date, 'end_date' : end_date}
    # filter_values['products'] = {'products' : products, 'sub_products_fund' : fund_categories}
    # filter_values['behavior'] = {'product_txn_amt' : product_txn_amt, 'product_aum_amt' : product_aum_amt}
    # st.write(filter_values)

#     predefined_conds = {
#     'dates' : f''' dt BETWEEN '{filter_values['dates']['start_date'].strftime("%Y%m%d")}' AND '{filter_values['dates']['end_date'].strftime("%Y%m%d")}' ''',
#     'products' : f'''\n AND products IN {filter_values['products']['products']}''',
#     'sub_product_fund' : f'''\n AND sub_products_fund IN {filter_values['products']['sub_products_fund']}''',
#     'product_txn_amt' : f'''\n AND product_txn_amt >= {product_txn_amt}''',
#     'product_aum_amt' : f'''\n AND product_aum_amt >= {product_aum_amt}''',
#     }

#     where_conds = ""
#     for cond in filter_values:
#         for element in filter_values[cond]:
#             if element is not None:
#                 where_conds += predefined_conds[cond]

#     query_tempalte = f'''
#     SELECT *
#     \n FROM table
#     \n WHERE {where_conds}
#     '''

#     st.write(filter_values)
#     st.write(f"Output query : {query_tempalte}")

