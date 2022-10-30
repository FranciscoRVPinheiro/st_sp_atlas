import streamlit as st
import pandas as pd

# uploaded_file = st.file_uploader("Drag and drop a CSV file")
# if uploaded_file is not None:

#     dataframe = pd.read_csv(uploaded_file)
#     st.write(dataframe)


# try:
#   st.title('Dimona - SP file parser')  

#   uploaded_file = st.file_uploader("Only accepts CSV files")

#   if uploaded_file is not None:

#     df = pd.read_csv(uploaded_file)

#     df.drop(df.columns[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
#             18, 19, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]], axis=1, inplace=True)

#     li = []
#     for fid, remote_id in zip(df["OrderId"], df["RemoteId"]):
#         new_results = fid[2:], remote_id
#         if new_results not in li:
#             li.append(new_results)
#         # print(new_results[0], new_results[1])

#     list_df = pd.DataFrame(li)

#     st.write(list_df)

# except Exception as e:
#   st.write(f'\n{e}')

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

    # search = input('\nAny value: ').strip().lower()
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

