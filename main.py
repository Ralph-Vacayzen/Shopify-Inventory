import streamlit as st
import pandas as pd

st.set_page_config(page_title='Shopify Inventory', page_icon='📋', layout="wide", initial_sidebar_state="auto", menu_items=None)


st.caption('VACAYZEN')
st.title('Shopify Inventory')
st.info('Combine Shopify inventory files into a single, concise spreadsheet.')

l, r = st.columns(2)
monthly_inventory_file = l.file_uploader('Monthly Inventory','CSV')
products_export_file   = r.file_uploader('Products Export',  'CSV')

if products_export_file and monthly_inventory_file:

    pe = pd.read_csv(products_export_file)
    mi = pd.read_csv(monthly_inventory_file)

    df = pd.merge(pe, mi, left_on='Title', right_on='product_title', how='left')
    df = df[df.Status == 'active']
    df = df[['Title','Status','Variant Inventory Qty','Cost per item','sum_last_total_inventory_value']]
    df = df.sort_values(by='Title')

    st.dataframe(df, hide_index=True, use_container_width=True)
    st.download_button('Download', df.to_csv(index=False), 'shopify_inventory.csv', 'CSV', type='primary', use_container_width=True)