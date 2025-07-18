import numpy as np
from scipy.optimize import minimize


def location_calculator(beacons, ranges):
    """
    Compute (x, y) coordinates given beacon positions and measured ranges.
    Поддерживает «достоверные» измерения (<= 1.5 м) и «шумные» (только нижняя граница).
    Снаружи интерфейс (beacons, ranges) и тип результата ‑ такой же,
    как у исходной версии на нормальных уравнениях.

    Parameters
    ----------
    beacons : array‑like, shape (n, 2)
        Координаты маяков (x_i, y_i).
    ranges : array‑like, length n
        Измеренные расстояния d_i до каждого маяка.

    Returns
    -------
    tuple
        Оценённые (x, y) координаты.
    """
    # ------------------------------------------------------------
    # 1. Настройки: порог доверия и грубая сетка
    trust_radius = 1.5      # м — измерения ниже порога считаем точными
    grid_step    = 0.10     # м — шаг перебора
    pad          = 1.0      # м — запас вокруг облака маяков
    # ------------------------------------------------------------

    P = np.asarray(beacons, dtype=float)
    d = np.asarray(ranges,  dtype=float)

    reliable = d <= trust_radius          # булев массив точных измерений
    noisy    = ~reliable

    # 2. Грубый перебор: ищем точки, удовлетворяющие всем ограничениям
    #    • для reliable: |p - b_i| ≈ d_i
    #    • для noisy:    |p - b_i| >= d_i
    min_xy = P.min(axis=0) - pad
    max_xy = P.max(axis=0) + pad

    xs = np.arange(min_xy[0], max_xy[0] + grid_step, grid_step)
    ys = np.arange(min_xy[1], max_xy[1] + grid_step, grid_step)

    good_pts = []
    for x in xs:
        for y in ys:
            p = np.array([x, y])
            dist = np.linalg.norm(p - P, axis=1)

            cond_reliable = np.all(np.abs(dist[reliable] - d[reliable]) <= grid_step)
            cond_noisy    = np.all(dist[noisy] >= d[noisy] - 1e-6)

            if cond_reliable and cond_noisy:
                good_pts.append(p)

    # Стартовая точка оптимизации
    p0 = np.mean(good_pts, axis=0) if good_pts else P.mean(axis=0)

    # 3. Функция ошибки: для reliable — квадрат отклонения,
    #                   для noisy    — штраф, если ближе, чем d_i
    def loss(p):
        dist = np.linalg.norm(p - P, axis=1)
        err_rel = (dist[reliable] - d[reliable]) ** 2
        err_noi = np.maximum(0.0, d[noisy] - dist[noisy]) ** 2
        return err_rel.sum() + err_noi.sum()

    res = minimize(loss, p0, method="L-BFGS-B")
    return tuple(res.x)
