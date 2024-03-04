from io import BytesIO
import pandas as pd
import streamlit as st

def df_to_xlsx(df):
    byte_xlsx = BytesIO()
    writer_xlsx = pd.ExcelWriter(byte_xlsx, engine="xlsxwriter")
    df.to_excel(writer_xlsx, index=False, sheet_name="Sheet1")
    ##-----必要に応じてexcelのフォーマット等を設定-----##
    workbook = writer_xlsx.book
    worksheet = writer_xlsx.sheets["Sheet1"]
    format1 = workbook.add_format({"num_format": "0.00"})
    worksheet.set_column("A:A", None, format1)
    writer_xlsx.save()
    ##---------------------------------------------##
    workbook = writer_xlsx.book
    out_xlsx = byte_xlsx.getvalue()
    return out_xlsx


df_test = pd.read_excel("test.xlsx")
xlsx_test = df_to_xlsx(df_test)

st.download_button(label="Download", data=xlsx_test, file_name="_test.xlsx")
