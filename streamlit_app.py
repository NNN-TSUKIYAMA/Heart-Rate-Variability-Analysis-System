import streamlit as st
import pandas as pd
import numpy as np

st.title("心拍変動解析") # タイトル
st.header("FFTr") # ヘッダー
uploaded_file = st.file_uploader("Excelファイルをアップロードしてください", type=['xlsx'])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    timestamps = df["Time[s]"]  # 心拍のタイムスタンプデータ
    rri = df["RRIa"] # 心拍間隔データ

# NaN値を除外してデータを抽出
valid_indices = ~np.isnan(rri)
valid_timestamps = timestamps[valid_indices]
valid_rri = rri[valid_indices]



