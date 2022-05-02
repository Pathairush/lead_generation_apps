from datetime import datetime
from email.policy import default
from gc import callbacks
from subprocess import call
from tkinter import Button
from matplotlib.style import available
import streamlit as st
import pandas as pd
import datetime as dt
import pandasql as ps

@st.cache
def load_data():
    data = pd.read_csv('Data/fake_data.csv')
    return data

data = load_data()
available_cols = data.columns

def fix_template():

    # header
    st.title('Lead Generation Application')
    st.header('Sample data')
    st.write(data.head(10))

    # Conditions 
    st.header('Inputs')

    # partitioned date condition
    last_eom_date = dt.datetime.now().replace(day=1) - dt.timedelta(days=1)
    st.session_state['input_as_of_date'] = st.date_input('As of date',  value = last_eom_date, on_change = fix_template if not st.session_state.num_filter else update_filters)

    # mandatory conditions
    input_products_choices = ["Fund", "Stock", "Offshore"]
    st.session_state['input_products'] = st.multiselect("Product", input_products_choices, on_change = fix_template if not st.session_state.num_filter else update_filters)
    st.session_state['input_fund_categories'] = None
    if "Fund" in st.session_state['input_products']:
        input_fund_category_choices = ["Money market", "Equity", "Fixed Income"]
        st.session_state['input_fund_categories'] = st.multiselect('Fund Category', input_fund_category_choices, on_change = fix_template if not st.session_state.num_filter else update_filters)

    # remember that the fix tempalte has been called.
    st.session_state.is_fix_template_called = True

# dynamic conditions

def dynamic_condition(i):
    '''
    Return a new dynamic filter
    '''
    i += 1
    col1, col2, col3, col4 = st.columns(4)
    col1.selectbox(f'condition_{i}', ['AND', 'OR'], key = f'input{i}_condition', on_change = update_filters)
    col2.selectbox(f'feature_{i}', available_cols, key = f'input{i}_feature', on_change = update_filters)
    col3.selectbox(f'sign_{i}', ['>', '<', "=", '>=', '<=', 'IN'], key = f'input{i}_sign', on_change = update_filters)
    col4.text_input(f'value_{i}', 0, key = f'input{i}_value', on_change = update_filters)

def update_filters():
    '''
    Load fix_template() and populate current filters
    '''

    st.session_state.is_fix_template_called = False
    if not st.session_state.is_fix_template_called:
        fix_template()

    for _ in range(st.session_state.num_filter):
        dynamic_condition(_)

def add_filters():
    '''
    Load fix_template() and populate a new filter
    '''
    
    st.session_state.is_fix_template_called = False
    if not st.session_state.is_fix_template_called:
        fix_template()

    st.session_state.num_filter += 1 # increase the number of filter
    for _ in range(st.session_state.num_filter):
        dynamic_condition(_)

def remove_filter():

    st.session_state.is_fix_template_called = False
    if not st.session_state.is_fix_template_called:
        fix_template()

    st.session_state.num_filter -= 1 # reduce the number of filter
    for _ in range(st.session_state.num_filter):
        dynamic_condition(_)

    # delete the latest filter fomr sessionstate 
    delete_state_number = st.session_state.num_filter + 1
    for key in ['condition', 'feature', 'value', 'sign']:
        del st.session_state[f'input{delete_state_number}_{key}']

# Inital state
if 'num_filter' not in st.session_state:
    st.session_state.num_filter = 0

if 'is_fix_template_called' not in st.session_state:
    st.session_state.is_fix_template_called = False

if not st.session_state.is_fix_template_called:
    fix_template()

# Buttons
col1, col2, col3 = st.columns(3)
add_button = col1.button('add_filter', on_click = add_filters),
refresh_button = col2.button('refresh', on_click = update_filters),
remove_button = col3.button('remove_filter', on_click = remove_filter),
lead_button = st.button("Generate Lead!", on_click=update_filters)

# Generate lead
if lead_button:

    # convert input params to dict
    input_args = dict(st.session_state)
    input_dict = dict(sorted(input_args.items()))
    # st.write(input_dict)

    # process mandatory conditions
    predefined_conds = {
    'input_as_of_date' : f''' dt = '{input_dict['input_as_of_date'].strftime("%Y%m%d")}' ''',
    'input_products' : f'''\n AND products IN {input_dict['input_products']}''',
    'input_fund_categories' : f'''\n AND sub_products_fund IN {input_dict['input_fund_categories']}'''
    }
    
    # process dynamic conditions
    dynamic_conds = []
    for i in range(1, input_dict['num_filter'] + 1):
        dynamic_conds.append(
            " ".join([input_dict[f'input{i}_condition'], input_dict[f'input{i}_feature'], input_dict[f'input{i}_sign'], input_dict[f'input{i}_value']])
        )

    # consoldiate conditions
    where_conds = ""
    for cond in input_dict:
        if cond in predefined_conds and input_dict[cond]:
            where_conds += predefined_conds[cond]
    for cond in dynamic_conds:
        where_conds += cond

    query_tempalte = f'''
    \n SELECT *
    \n FROM data
    \n WHERE {where_conds}
    '''
    # st.write(f"Output query : {query_tempalte}")

    # Output result
    st.header('Output')
    st.write(ps.sqldf(query_tempalte, locals()))