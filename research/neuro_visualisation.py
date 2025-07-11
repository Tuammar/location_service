import pandas as pd
import matplotlib.pyplot as plt

# Загрузка данных
df = pd.read_csv("rssi_tralalelo.csv")

# Вычисление среднего и медианы
mean_rssi = df["rssi"].mean()
median_rssi = df["rssi"].median()

# Построение графика
plt.figure(figsize=(12, 6))

# Точки RSSI по оси времени (индекс)
plt.plot(df.index, df["rssi"], marker='o', linestyle='', color='blue', label='RSSI')

# Линии среднего и медианы
plt.axhline(mean_rssi, color='red', linestyle='--', label=f'Mean: {mean_rssi:.2f}')
plt.axhline(median_rssi, color='green', linestyle='-', label=f'Median: {median_rssi:.2f}')

# Оформление графика
plt.title("RSSI Over Time with Mean and Median")
plt.xlabel("Time (index)")
plt.ylabel("RSSI")
plt.legend()
plt.tight_layout()
plt.grid(True)

# Показ графика
plt.show()