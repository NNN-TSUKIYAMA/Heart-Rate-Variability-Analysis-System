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
import pandas as pd
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
from scipy import signal

# Excelファイルからデータを読み込み
df = pd.read_excel(R"C:\Users\nonok\OneDrive\デスクトップ\卒論被験者データ\じゅんいち\じゅんいち珈琲ミント③.xlsx")
timestamps = df["Time[s]"]  # 心拍のタイムスタンプデータ
rri = df["RRIa"] # 心拍間隔データ



# NaN値を除外してデータを抽出
valid_indices = ~np.isnan(rri)
valid_timestamps = timestamps[valid_indices]
valid_rri = rri[valid_indices]


# リサンプリングのための新しいタイムスタンプを作成
new_timestamps = np.arange(valid_timestamps.iloc[0], valid_timestamps.iloc[-1], 0.5)

# スプライン3次補間関数を作成
interpolator = interpolate.interp1d(valid_timestamps, valid_rri, kind='cubic', fill_value="extrapolate")
resampled_rri = interpolator(new_timestamps)
print(new_timestamps,resampled_rri)

# 新しいデータフレームを作成
output_df = pd.DataFrame({'Time[s]': new_timestamps, 'RRI': resampled_rri})


# valid_rriの平均値を求める
mean_rri = np.mean(resampled_rri)

# 各valid_rriから平均値を引いた値を計算
detrended_rri = resampled_rri - mean_rri


#ハイパス
cutoff_freq = 0.04  # カットオフ周波数 [Hz]
sampling_rate = 2.0
b, a = signal.butter(4, cutoff_freq / (0.5 * sampling_rate), btype='high')
filtered_rri1 = signal.filtfilt(b, a, detrended_rri)

#ローパス
cutoff_freq = 0.6  # カットオフ周波数 [Hz]
sampling_rate = 2.0
b, a = signal.butter(4, cutoff_freq / (0.5 * sampling_rate), btype='low')
filtered_rri2 = signal.filtfilt(b, a, filtered_rri1)


#ハミングウィンドウ
window = signal.hamming(len(filtered_rri2))
filtered_rri_hamming = filtered_rri2 * window


#FFT分析
N = len(filtered_rri_hamming)
sampling_rate = 2.0
freq = np.fft.fftfreq(N, d=1/sampling_rate)
F = np.fft.fft(filtered_rri_hamming)
amp = np.abs(F/(N/2))

# グラフの表示
new_timestamps = new_timestamps[:len(filtered_rri2)]
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
ax1.plot(new_timestamps, filtered_rri2)
ax1.set_xlabel("Time")
ax1.set_ylabel("Filtered RRI")
ax1.set_title("Filtered RRI")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
ax1.plot(new_timestamps, filtered_rri_hamming)
ax1.set_xlabel("Time")
ax1.set_ylabel("Filtered RRI (Hamming Window)")
ax1.set_title("Filtered RRI with Hamming Window")

ax2.plot(freq[1:int(N/2)], amp[1:int(N/2)])
ax2.set_xlabel("Frequency [Hz]")
ax2.set_ylabel("Amplitude")
ax2.set_title("FFT Power Spectrum")

plt.tight_layout()
plt.show()

# LF帯域とHF帯域の周波数範囲を定義
lf_freq_range = (0.04, 0.15)  # LF帯域の周波数範囲 [Hz]
hf_freq_range = (0.15, 0.4)   # HF帯域の周波数範囲 [Hz]

# LF帯域とHF帯域のパワーを計算
lf_power = np.sum(amp[(freq >= lf_freq_range[0]) & (freq <= lf_freq_range[1])])
hf_power = np.sum(amp[(freq >= hf_freq_range[0]) & (freq <= hf_freq_range[1])])

# VLF帯域とトータルパワーの周波数範囲を定義
vlf_freq_range = (0.0033, 0.04)  # VLF帯域の周波数範囲 [Hz]
total_freq_range = (0, 0.4)      # トータルパワーの周波数範囲 [Hz]

# VLF帯域とトータルパワーのパワーを計算
vlf_power = np.sum(amp[(freq >= vlf_freq_range[0]) & (freq <= vlf_freq_range[1])])
total_power = np.sum(amp[(freq >= total_freq_range[0]) & (freq <= total_freq_range[1])])

print(vlf_power)
print(total_power)


# LF/HF比を計算
lf_hf_ratio = lf_power / hf_power

print(lf_power)
print( hf_power)
print( lf_hf_ratio)

# LF補正値とHF補正値を計算
lf_power = np.sum(amp[(freq >= 0.04) & (freq <= 0.15)])  # LF帯域の周波数範囲 [0.04, 0.15] Hz
hf_power = np.sum(amp[(freq >= 0.15) & (freq <= 0.4)])   # HF帯域の周波数範囲 [0.15, 0.4] Hz

lf_correction = lf_power / (vlf_power + total_power)
hf_correction = hf_power / (vlf_power + total_power)

# LF/HF補正値比を計算
lf_hf_ratio_correction = lf_correction / hf_correction

print("LF補正値:", lf_correction)
print("HF補正値:", hf_correction)
print("LF/HF Ratio 補正値:",lf_hf_ratio_correction)

