import streamlit as st
import pandas as pd
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb

st.set_page_config(layout='wide', page_title="SP Atlas", page_icon="🔍")
st.title('SP Atlas Query 🔍')
st.caption('''Returns results for any value in the SP Atlas spreadsheet like color, product name, sku, size or stock id. Ex: search for black.''')

def read_data():
        SHEET_ID = st.secrets["SHEET_ID"]
        SHEET_NAME = st.secrets["SHEET_NAME"]
        url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'
        df = pd.read_csv(url)
        return df

def custom_style(val):
    # color = "orange" if val == search else "grey"
    color = "orange" if search in val else "grey"
    return f"color: {color}"

try:
    df = read_data()

    df = df.drop(['Area "name" front', 'Area "name" back',
                'SPOD SKU ID', 'Halle SKU', 'Big Oven SKU composition', 'Printforia', 'QTco', 'Casestry', 'Unnamed: 30', 'Unnamed: 29', 
                'Unnamed: 28', 'Unnamed: 27', 'Whitelabel', 'Express Shipping'], axis=1)
    
    df = df.rename(
    columns={
        'Valadio SKU ID': 'Valadio', 
        'Monster SKU ID': 'Monster', 
        'Dimona SKU composition': 'Dimona', 
        'TSAS SKU composition': 'TSAS', 
        'Dubow SKU composition': 'Dubow', 
        'Shirtplatform Product': 'SP_Product',
        'Shirtplatform color': 'SP_Color', 
        'Shirtplatform size': 'SP_Size',
        'Moteefe product': 'MTF_Product', 
        'Moteefe color': 'MTF_Color', 
        'Moteefe size': 'MTF_Size',
        'Stock ID':'Stock_ID',
        'Print Logistic': 'Printlogistic',
        'OP Tiger':'Optiger'})

    df = df.apply(lambda x: x.astype(str))

    df['Printlogistic'] = df['Printlogistic'].apply(
        lambda x: x[:-2])

    df['Optiger'] = df['Optiger'].apply(
        lambda x: x[:-2])
    
    df['Stock_ID'] = df['Stock_ID'].apply(
    lambda x: x[:-2])

    search = st.text_input('Search', placeholder='Search', label_visibility="collapsed").strip()

    df = df.query(
        'SP_Product.str.contains(@search, case=False) | \
            SP_Color.str.contains(@search, case=False) | \
            SP_Size.str.contains(@search, case=False) | \
            MTF_Product.str.contains(@search, case=False) | \
            MTF_Color.str.contains(@search, case=False) | \
            MTF_Size.str.contains(@search, case=False) | \
            Stock_ID.str.contains(@search, case=False) | \
            Valadio.str.contains(@search, case=False) | \
            Monster.str.contains(@search, case=False) | \
            Dimona.str.contains(@search, case=False) | \
            TSAS.str.contains(@search, case=False) | \
            Dubow.str.contains(@search, case=False) | \
            Albumo.str.contains(@search, case=False) | \
            SwiftPOD.str.contains(@search, case=False) | \
            Polyconcept.str.contains(@search, case=False) | \
            Printlogistic.str.contains(@search, case=False) | \
            Optiger.str.contains(@search, case=False)'
            )
    df = df.replace(['n','nan'], 'x')

    df_styled = df.style.applymap(custom_style)

    if search and len(df) > 0:
        st.success(f'\nFound {len(df)} results for "{search}"\n')

        st.dataframe(df_styled, use_container_width=True)

        def to_excel(df):
            output = BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            df.to_excel(writer, index=False, sheet_name='Sheet1')
            workbook = writer.book
            worksheet = writer.sheets['Sheet1']
            format1 = workbook.add_format({'num_format': '0.00'})
            worksheet.set_column('A:A', None, format1)
            writer.save()
            processed_data = output.getvalue()
            return processed_data

        df_xlsx = to_excel(df)
        st.download_button(label='Download',
                        data=df_xlsx,
                        file_name='download_so_atlas.xlsx')
    elif search and len(df) == 0:
        st.error(f'\nFound {len(df)} results for "{search}"\n')

except Exception as e:
    st.error(f'{e}')

