import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
plt.rcParams['font.family'] = 'Yu Gothic'
# --- 入力データ（例） ---
# ミラー指数と対応する面間隔 d (単位: nm)
miller_indices = [
    (1,1,1),
    (2,0,0),
    (2,2,0),
    (3,1,1),
    (4,0,0),
]

d_values = [
    2.3372,
    2.0248,
    1.4317,
    1.2212,
    1.0125,
]

# --- x: ミラー指数の二乗和, y: 1/d^2 を計算 ---
x = np.array([h**2 + k**2 + l**2 for h, k, l in miller_indices])
y = 1 / (np.array(d_values) ** 2)

# --- 線形フィッティング（y = m*x + b） ---
slope, intercept, r_value, p_value, std_err = linregress(x, y)

# --- 格子定数 a の計算 ---
a = 1 / np.sqrt(slope)

# --- 結果の出力 ---
print(f"回帰式: 1/d^2 = {slope:.4f} * (h^2 + k^2 + l^2) + {intercept:.4f}")
print(f"格子定数 a = {a:.5f} nm")
print(f"slope (full precision) = {slope:.15f}")


# --- プロット ---
plt.scatter(x, y, label="測定値")
plt.plot(x, slope * x + intercept, 'r--', label="フィッティング直線")
plt.xlabel("h² + k² + l²")
plt.ylabel("1 / d² (1/nm²)")
plt.title("1/d² vs. ミラー指数の二乗和")
plt.legend()
plt.grid(True)
plt.show()
# データを2列にまとめる
data = np.column_stack((x, y))

# .dat ファイルとして保存（タブ区切り、見やすい形式）
np.savetxt(r"C:\Users\KSK04\課題\物理学総合実験\物性\X線回折\plot_data.dat", data, fmt="%.6f", delimiter="\t", header="h2+k2+l2\t1/d^2 (1/nm^2)")
