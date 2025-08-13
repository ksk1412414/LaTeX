import numpy as np
import itertools

# 実験データ
d_values = np.array([
    2.3372, 2.2400, 2.1127, 2.0778, 2.0248,
    1.5845, 1.4945, 1.4317, 1.3511, 1.2745,
    1.2212, 1.0125
])

# 1/d^2 を計算して正規化
inv_d2_exp = 1 / d_values**2
inv_d2_exp /= inv_d2_exp[0]

# (h,k,l)の候補を作成 (FCC選択則に従う)
max_index = 5
hkl_list = list(itertools.product(range(0, max_index+1), repeat=3))
hkl_list = [
    (h,k,l) for (h,k,l) in hkl_list 
    if (h, k, l) != (0,0,0) and
       ((h % 2 == k % 2 == l % 2))  # FCC選択則: 全部偶数 or 全部奇数
]

# h^2 + k^2 + l^2 を計算
hkl_sums = np.array([h**2 + k**2 + l**2 for h, k, l in hkl_list])

# 許容誤差設定（5%）
tolerance = 0.05

# 保存用リスト
results = []

# 出力
print("d値 (Å) | 格子定数 a (Å)")
print("-" * 30)

for i, exp_val in enumerate(inv_d2_exp):
    normalized_hkl_sums = hkl_sums / hkl_sums.min()
    idx = np.argmin(np.abs(normalized_hkl_sums - exp_val))
    diff = abs(normalized_hkl_sums[idx] - exp_val)
    
    if diff <= tolerance:
        hkl_sum = hkl_sums[idx]
        a = d_values[i] * np.sqrt(hkl_sum)  # 格子定数を計算
        print(f"{d_values[i]:7.4f} | {a:8.4f}")
        results.append((d_values[i], a))
    else:
        print(f"{d_values[i]:7.4f} |    -    ")

