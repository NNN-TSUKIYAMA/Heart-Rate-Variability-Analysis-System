import streamlit as st
import pandas as pd
import numpy as np
from scipy import interpolate, signal
import matplotlib.pyplot as plt

# Streamlitアプリの設定
st.title("心拍変動解析ツール")
st.sidebar.header("解析オプション")

# ファイルアップロード
uploaded_file = st.file_uploader("Excelファイルをアップロードしてください", type='xlsx')

# ファイルがアップロードされた場合
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    st.write("アップロードされたデータ:")
    st.write(df)

    # データの前処理
    timestamps = df["Time[s]"]
    rri = df["RRIa"]

    valid_indices = ~np.isnan(rri)
    valid_timestamps = timestamps[valid_indices]
    valid_rri = rri[valid_indices]

    new_timestamps = np.arange(valid_timestamps.iloc[0], valid_timestamps.iloc[-1], 0.5)
    interpolator = interpolate.interp1d(valid_timestamps, valid_rri, kind='cubic', fill_value="extrapolate")
    resampled_rri = interpolator(new_timestamps)

    detrended_rri = resampled_rri - np.mean(resampled_rri)

    # フィルタリングとFFT分析
    filtered_rri = signal.filtfilt(*signal.butter(4, 0.04 / (0.5 * 2.0), btype='high'), detrended_rri)
    filtered_rri = signal.filtfilt(*signal.butter(4, 0.6 / (0.5 * 2.0), btype='low'), filtered_rri)
    filtered_rri_hamming = filtered_rri * signal.hamming(len(filtered_rri))

    N = len(filtered_rri_hamming)
    freq = np.fft.fftfreq(N, d=1/2.0)
    F = np.fft.fft(filtered_rri_hamming)
    amp = np.abs(F/(N/2))

    # プロット
    st.subheader("解析結果")
    st.pyplot(plt.plot(new_timestamps, filtered_rri, label="Filtered RRI"))
    st.pyplot(plt.plot(new_timestamps, filtered_rri_hamming, label="Filtered RRI (Hamming Window)"))
    st.pyplot(plt.plot(freq[1:int(N/2)], amp[1:int(N/2)], label="FFT Power Spectrum"))
    
    # LF/HF比と補正値の計算
    lf_power = np.sum(amp[(freq >= 0.04) & (freq <= 0.15)])
    hf_power = np.sum(amp[(freq >= 0.15) & (freq <= 0.4)])
    lf_hf_ratio = lf_power / hf_power

    lf_correction = lf_power / (np.sum(amp[(freq >= 0.0033) & (freq <= 0.04)]) + np.sum(amp[(freq >= 0) & (freq <= 0.4)]))
    hf_correction = hf_power / (np.sum(amp[(freq >= 0.0033) & (freq <= 0.04)]) + np.sum(amp[(freq >= 0) & (freq <= 0.4)]))
    lf_hf_ratio_correction = lf_correction / hf_correction

    st.subheader("解析結果の指標")
    st.write(f"LF/HF比: {lf_hf_ratio}")
    st.write(f"LF補正値: {lf_correction}")
    st.write(f"HF補正値: {hf_correction}")
    st.write(f"LF/HF Ratio 補正値: {lf_hf_ratio_correction}")

# 他の操作やプロントを追加することもできます
