import streamlit as st
import pandas as pd
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
from scipy import signal

st.title("心拍変動解析") # タイトル
st.header("FFTr") # ヘッダー
uploaded_file = st.file_uploader("Excelファイルをアップロードしてください", type=['xlsx'])
