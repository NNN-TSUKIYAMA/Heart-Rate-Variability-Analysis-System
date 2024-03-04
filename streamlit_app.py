import streamlit as st
import pandas as pd

st.title("CSV/Excel データの読み込みとプロント")

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

        # プロントの表示
        st.subheader("データに対する操作:")
        if st.button("基本的な統計情報を表示"):
            st.write("### 基本的な統計情報:")
            st.write(df.describe())

        # ここに他のプロントやデータに対する操作を追加することができます
else:
    st.info("ファイルがアップロードされていません。")
