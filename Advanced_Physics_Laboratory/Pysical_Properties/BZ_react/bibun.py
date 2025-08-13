import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# --- パラメータ設定 ---
epsilon = 0.01
a = 0.1

# --- モデル定義 ---
def fhn_model(state, t):
    x, z = state
    dxdt = (x - x**3 / 3 - z) / epsilon
    dzdt = a * x - z
    return [dxdt, dzdt]

# --- 解を計算 ---
x0, z0 = 2.0, 1.0
initial_state = [x0, z0]
t = np.linspace(0, 20, 10000)
solution = odeint(fhn_model, initial_state, t)
x, z = solution[:, 0], solution[:, 1]

# --- グリッド設定 ---
x_vals = np.linspace(-2.5, 2.5, 100)
z_vals = np.linspace(-2, 2, 100)
X, Z = np.meshgrid(x_vals, z_vals)
dX = (X - X**3 / 3 - Z) / epsilon
dZ = a * X - Z

# 正規化して矢印の長さを統一
norm = np.sqrt(dX**2 + dZ**2)
dX_unit = dX / (norm + 1e-8)
dZ_unit = dZ / (norm + 1e-8)

# 背景：スカラー場（元のベクトルの大きさ）だけ表示
magnitude = norm

# --- 描画 ---
plt.figure(figsize=(8, 6))

# スカラー場（ベクトルの大きさをカラーマップで表示）
pc = plt.pcolormesh(X, Z, magnitude, cmap='jet', shading='auto')
plt.colorbar(pc, label='Vector magnitude')

# ベクトル場（すべての矢印の長さを同じにする）
skip = 5
plt.quiver(
    X[::skip, ::skip], Z[::skip, ::skip],
    dX_unit[::skip, ::skip], dZ_unit[::skip, ::skip],
    color='black', scale=30, width=0.005
)

# ヌルクライン
x_null = np.linspace(-2.5, 2.5, 1000)
plt.plot(x_null, x_null - x_null**3 / 3, 'r--', linewidth=1.5, label='dx/dt = 0')
plt.plot(x_null, a * x_null, 'g-.', linewidth=1.5, label='dz/dt = 0')

# 軌道と初期点
plt.plot(x, z, 'k-', linewidth=2.0, label='Trajectory', zorder=3)
plt.plot(x0, z0, 'ro', label='Initial Point', zorder=3)

# 装飾
plt.xlabel('x')
plt.ylabel('z')
plt.title('FitzHugh–Nagumo Phase Plane (Uniform Arrows)')
plt.xlim(-2.5, 2.5)
plt.ylim(-2, 2)
plt.legend()
plt.tight_layout()
plt.show()
