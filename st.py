import streamlit as st
import pandas as pd
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb

st.set_page_config(layout='wide', page_title="SP Atlas", page_icon="🔍")
st.title('SP Atlas Query 🔍')
st.caption('''Returns results for any value in the SP Atlas spreadsheet like color, product name, sku or size. The query will only bring columns that have values in them. Ex: search for black.''')

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True


if check_password():
    try:
        SHEET_ID = st.secrets["SHEET_ID"]
        SHEET_NAME = st.secrets["SHEET_NAME"]
        url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'

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
                'Moteefe size': 'MTF Size',
                'Express Shipping': 'Exp ship'})

        df = df.apply(lambda x: x.astype(str).str.lower())

        df['Print Logistic'] = df['Print Logistic'].apply(
            lambda x: x[:-2])

        df['OP Tiger'] = df['OP Tiger'].apply(
            lambda x: x[:-2])

        df['Stock ID'] = df['Stock ID'].apply(
            lambda x: x[:-2])

        search = st.text_input('Search:', placeholder='Search:', label_visibility="collapsed").strip().lower()

        df = df[df.isin([search]).any(axis=1)].dropna(axis=1, how='all')

        cols = ((df != 'nan') & (df != 'n')).any()
        df = df[cols[cols].index]

        if search and len(df) > 0:
            st.success(f'\nFound {len(df)} results for "{search}"\n')

            st.dataframe(df, use_container_width=True)

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

