import streamlit as st

st.title("心拍変動解析") # タイトル
st.header("FFTr") # ヘッダー
uploaded_file = st.file_uploader("Excelファイルをアップロードしてください", type=['xlsx'])
