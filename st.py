import streamlit as st
import pandas as pd

st.title('SP Atlas Query')

try:
    sheet_id = '1w9oUYI3lgYDVe4I22zaQY4fMhCHeEEySytZ_Pv4Glco'
    sheet_name = 'page1'
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

    df = pd.read_csv(url)

    df = df.drop(['Area "name" front', 'Area "name" back',
                 'SPOD SKU ID', 'Halle SKU', 'Big Oven SKU composition', 'Printforia', 'QTco', 'Casestry'], axis=1)

    df = df.rename(
        columns={
            'Valadio SKU ID': 'Valadio',
            'Monster SKU ID': 'Monster',
            'Dimona SKU composition': 'Dimona',
            'TSAS SKU composition': 'TSAS',
            'Dubow SKU composition': 'Dubow',
            'Shirtplatform Product': 'SP Product',
            'Shirtplatform color': 'SP Color',
            'Shirtplatform size': 'SP Size',
            'Moteefe product': 'MTF Product',
            'Moteefe color': 'MTF Color',
            'Moteefe size': 'MTF Size'})

    df = df.apply(lambda x: x.astype(str).str.lower())

    df['Print Logistic'] = df['Print Logistic'].apply(
        lambda x: x[:-2])

    df['OP Tiger'] = df['OP Tiger'].apply(
        lambda x: x[:-2])

    search = st.text_input('Search:').strip().lower()

    if ',' in search:
        search = search.replace(', ', ',')
        search = search.split(',')
        df = df.loc[(df['SP Product'] == search[0])
                    & (df['SP Color'] == search[1]) & (df['SP Size'] == search[2])]

        df = df.dropna(axis=1, how='all')

    else:
        df = df[df.isin([search]).any(axis=1)].dropna(axis=1, how='all')

    cols = ((df != 'nan') & (df != 'n')).any()
    df = df[cols[cols].index]

    if search:
        st.write(f'Input: {search}')
        st.write(f'\nNumber of results: {len(df)}\n')

        st.write(df)

except Exception as e:
    st.write(f'{e}')

