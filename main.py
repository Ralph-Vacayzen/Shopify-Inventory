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

    pe['Option1 Value'] = pe['Option1 Value'].str.replace('-',' ').str.upper()
    pe['Option2 Value'] = pe['Option2 Value'].str.replace('-',' ').str.upper()

    def build_product_variant_title(row):
        if not pd.isna(row['Option1 Value']) and not pd.isna(row['Option2 Value']):
            return f"{row['Option1 Value']} / {row['Option2 Value']}"
        elif not pd.isna(row['Option1 Value']) and pd.isna(row['Option2 Value']):
            return row['Option1 Value']
        elif pd.isna(row['Option1 Value']) and not pd.isna(row['Option2 Value']):
            return row['Option2 Value']

        return

    pe['product_variant_title'] = pe.apply(build_product_variant_title, axis=1)
    mi['product_variant_title'] = mi['product_variant_title'].str.upper()

    df = pd.merge(pe, mi, left_on=['Title','product_variant_title'], right_on=['product_title','product_variant_title'], how='left')
    df = df[df.Status == 'active']
    df = df[['Title','product_variant_title','Status','Variant Inventory Qty','ending_quantity','Cost per item']]
    df = df.sort_values(by='Title')

    def get_quantity(row):
        if pd.isna(row['ending_quantity']):
            return row['Variant Inventory Qty']
        return row['ending_quantity']

    df['Quantity'] = df.apply(get_quantity, axis=1)

    df = df[['Title','product_variant_title','Status','Quantity','Cost per item']]

    df['Total'] = df['Quantity'].astype(int) * df['Cost per item'].astype(float)
    df.columns  = ['Asset','Variant','Status','Quantity','Cost_Per_Item','Total']

    st.dataframe(df, hide_index=True, use_container_width=True)
    st.download_button('Download', df.to_csv(index=False), 'shopify_inventory.csv', 'CSV', type='primary', use_container_width=True)