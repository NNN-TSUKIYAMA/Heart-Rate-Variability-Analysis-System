import streamlit as st
import pandas as pd

def main():
    st.title("Excelデータ読み込みアプリ")

    # ファイルアップロード
    uploaded_file = st.file_uploader("Excelファイルをアップロードしてください", type=['xlsx'])
