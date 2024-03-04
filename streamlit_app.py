import streamlit as st
import pandas as pd

# Streamlitアプリのタイトルを設定
st.title("Excelデータの読み込み")

# ファイルアップロード
uploaded_file = st.file_uploader("Excelファイルをアップロードしてください", type=['xlsx', 'xls'])

# アップロードされたファイルがある場合
if uploaded_file is not None:
    try:
        # Excelファイルを読み込む
        df = pd.read_excel(uploaded_file)
        
        # 読み込んだデータを表示
        st.write("読み込んだデータ:")
        st.write(df)
        
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")

else:
    st.info("Excelファイルがアップロードされていません。")
