import pandas as pd
import matplotlib.pyplot as plt

# Загрузка данных
df = pd.read_csv("clear_beats_rssi_reference.csv")

# Создаем гистограмму
plt.figure(figsize=(12, 6))
n, bins, patches = plt.hist(
    df['rssi_value'], 
    bins=20,
    edgecolor='black',
    color='skyblue',
    alpha=0.7
)

# Настройки графика
plt.title('Распределение значений RSSI', fontsize=14, pad=20)
plt.xlabel('Значение RSSI (dBm)', fontsize=12)
plt.ylabel('Количество измерений', fontsize=12)
plt.xticks(range(-106, -65, 2))  # Подписи с шагом 2 для читаемости
plt.grid(axis='y', linestyle='--', alpha=0.5)

# Добавляем подписи значений над столбцами
for i in range(len(n)):
    if n[i] > 0:
        plt.text(bins[i]+0.5, n[i]+0.1, 
                f'{int(n[i])}', 
                ha='center', 
                fontsize=10)

plt.tight_layout()
plt.show()