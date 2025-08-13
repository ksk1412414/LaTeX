import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# .xy ファイルの読み込み（カンマ区切りファイルの場合）
data = np.loadtxt('Al.xy')  # .xyファイル名を指定

# xとyに分ける
x = data[:, 0]
y = data[:, 1]

# ピーク検出：顕著さ（prominence）を指定
peaks, properties = find_peaks(y, prominence=110)  # 顕著さが120以上のピークを検出
# データを .dat ファイルに保存
np.savetxt(r'C:\Users\KSK04\課題\物理学総合実験\物性\X線回折\peak_data.dat', np.column_stack((x, y)), header='x y', comments='')

# ピーク位置を .dat ファイルに保存（必要に応じて）
np.savetxt(r'C:\Users\KSK04\課題\物理学総合実験\物性\X線回折\peak.dat', np.column_stack((x[peaks], y[peaks])), header='x_peak y_peak', comments='')

# 隣接ピークの距離が近すぎる場合、x座標が小さい方だけを残す
min_distance = 0.4  # ピーク間の最小距離（この値はデータに応じて調整が必要）

filtered_peaks = [peaks[0]]  # 最初のピークは必ず残す

for i in range(1, len(peaks)):
    if x[peaks[i]] - x[peaks[i-1]] >= min_distance:
        filtered_peaks.append(peaks[i])  # 前のピークと十分に離れている場合だけ追加

# フィルタリングされたピークの位置（フィルタ後）をコンソールに表示
print("Filtered peaks:")
for peak in filtered_peaks:
    print(f"{x[peak]}, {y[peak]}")  # フィルタ後のピークの x と y 座標を表示

# ブラッグの条件に基づいて d間隔を計算
wavelength = 1.5405  # 波長 (Cu Kα)
theta_2_filtered = x[filtered_peaks]  # フィルタ後の2θ

# θ (theta) は2θを半分にする
theta = theta_2_filtered / 2  # 度

# d間隔をブラッグの式から計算 (n=1)
d_spacing = wavelength / (2 * np.sin(np.deg2rad(theta)))  # ラジアンに変換してsin

# d間隔の結果を表示
print("\nFiltered peaksに対する d間隔:")
for i, d in enumerate(d_spacing):
    print(f"{d:.4f} ")

# データをプロット
plt.plot(x, y, label="Data")
plt.plot(x[filtered_peaks], y[filtered_peaks], 'rx', label="Filtered Peaks")  # フィルタ後のピーク位置に赤い×を表示

# 軸ラベルとタイトルを設定
plt.xlabel('2θ')
plt.ylabel('Intensity')
plt.title('Peak Detection (Filtered)')

# プロットを表示
plt.legend()
plt.show()
