pip install openpyxl
import streamlit as st
import pandas as pd

def main():
    st.title("Excelデータ読み込みアプリ")

    # ファイルアップロード
    uploaded_file = st.file_uploader("Excelファイルをアップロードしてください", type=['xlsx'])

    if uploaded_file is not None:
        try:
            # Excelファイルの読み込み
            df = pd.read_excel(uploaded_file, engine='openpyxl')
            # 読み込んだデータを表示
            st.write("Excelデータ:")
            st.write(df)
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    main()
