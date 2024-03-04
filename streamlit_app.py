import streamlit as st
import pandas as pd
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
from scipy import signal

st.title("心拍変動解析") # タイトル
st.header("FFTr") # ヘッダー
uploaded_file = st.file_uploader("Excelファイルをアップロードしてください", type=['xlsx'])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    timestamps = df["Time[s]"]  # 心拍のタイムスタンプデータ
    rri = df["RRIa"] # 心拍間隔データ

