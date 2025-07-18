from typing import Union
import numpy as np
from pykalman import KalmanFilter


def kalman_filter(rssis: list[list[Union[float, int]]]):
    # Приведение данных
    timestamps = np.array([d[0] for d in rssis], dtype=float)
    values = np.array([d[1] for d in rssis], dtype=float)

    # Вычисляем dt (первый шаг — 0)
    dt = np.diff(timestamps)
    dt = np.concatenate([[0.0], dt])

    # Гиперпараметры
    q0 = 0.1   # базовый шум процесса
    R_const = 1.0   # шум измерения

    # Постоянная матрица перехода (без смещения)
    F = np.ones((len(values), 1, 1))      # каждый F_t = [[1]]
    # Шум процесса масштабируем по dt
    Q = np.array([[[q0 * d]] for d in dt])  # Q_t = q0 * dt_t

    # Наблюдение
    H = np.ones((len(values), 1, 1))         # каждый H_t = [[1]]
    R = np.full((len(values), 1, 1), R_const)

    # Создаём и запускаем фильтр
    kf = KalmanFilter(
        transition_matrices=F,
        observation_matrices=H,
        transition_covariance=Q,
        observation_covariance=R,
        initial_state_mean=values[0],
        initial_state_covariance=1.0
    )

    means, _ = kf.filter(values.reshape(-1, 1))
    filtered = means.flatten()

    return filtered.tolist()
