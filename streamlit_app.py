import streamlit as st
import pandas as pd

st.title("CSV/Excel データの読み込み")

# ファイルアップロード
uploaded_file = st.file_uploader("CSVまたはExcelファイルをアップロードしてください", type=['csv', 'xlsx'])

if uploaded_file is not None:
    # ファイルがアップロードされた場合
    file_ext = uploaded_file.name.split(".")[-1]

    try:
        if file_ext == 'csv':
            # CSVファイルの場合
            df = pd.read_csv(uploaded_file)
        elif file_ext in ['xls', 'xlsx']:
            # Excelファイルの場合
            df = pd.read_excel(uploaded_file)
        else:
            st.error("サポートされていないファイル形式です。CSVまたはExcelファイルをアップロードしてください。")
    except Exception as e:
        st.error(f"ファイルの読み込み中にエラーが発生しました: {e}")
    else:
        # データの表示
        st.write("読み込んだデータ:")
        st.write(df)
else:
    st.info("ファイルがアップロードされていません。")

# ここにデータに対する操作や可視化などを追加することができます
