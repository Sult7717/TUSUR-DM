import os
import random
import networkx as nx
import matplotlib.pyplot as plt

# ================ Лабораторная работа 1 ================

# ---------------- Генерация матрицы смежности ----------------
def generate_adjacency_matrix():
    """
    Генерирует симметричную матрицу смежности для неориентированного графа.
    Параметры:
        n   - количество вершин (размер матрицы)
        mode - тип графа:
            1 - простой (0 или 1 без петель)
            2 - полный (все рёбра, кроме петель)
            3 - с петлями (0 или 1, петли разрешены)
            4 - мультиграф (0..3 кратных рёбер)
    Возвращает:
        matrix - квадратная матрица смежности, заполненная по правилам
    """
    mode = int(input(f"Выбери тип генерируемой матрицы смежности:\n1 - Простой,     2 - Полный\n3 - С петлями,   4 - Мультиграф с мультипетлями\n"))
    if mode  in [1, 2, 3, 4]:
        n = int(input("Введи размер матрицы n: "))

    # clear = lambda: os.system('cls')
    # clear()
    if mode == 1:                # простой граф
        print(f"\nРежим простого графа")
    elif mode == 2:              # полный граф
        print(f"\nРежим полного графа")
    elif mode == 3:              # граф с петлями
        print(f"\nРежим графа с петлями")
    elif mode == 4:              # мультиграф (mode == 4)
        print(f"\nРежим мультиграфа с мультипетлями")
    else:
        print(f"\nТестовая матрица")

    if mode in [1, 2, 3, 4]:
        matrix = [[0] * n for _ in range(n)]

        for i in range(n):
            for j in range(i, n):            # заполняем только верхний треугольник (включая диагональ)
                if mode == 1:                # простой граф
                    val = random.randint(0, 1) if i != j else 0
                elif mode == 2:              # полный граф
                    val = 1 if i != j else 0
                elif mode == 3:              # граф с петлями
                    val = random.randint(0, 1)
                elif mode == 4:              # мультиграф (mode == 4)
                    val = random.randint(0, 3)

                # Симметричное заполнение
                matrix[i][j] = matrix[j][i] = val    
                    
    else:   # Тестовая матрица
        matrix = [
            [0, 1, 0, 1, 0, 0],
            [1, 0, 1, 0, 0, 0],
            [0, 1, 0, 1, 0, 0],
            [1, 0, 1, 0, 1, 0],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0]
            ]

    return matrix

# ---------------- Матрица инцидентности ----------------
def build_incidence_matrix(matrix):
    """
    Строит матрицу инцидентности по матрице смежности.
    Для каждой пары вершин (i,j) с кратностью k > 0 создаётся k рёбер.
    Если вершина и ребро инцидентны:
        - для петли ставится 2
        - для обычного ребра ставится 1
    Возвращает:
        inc   - матрица инцидентности (вершины × рёбра)
        edges - список рёбер в порядке следования столбцов inc
    """
    n = len(matrix)
    edges = []

    # Собираем все рёбра с учётом кратности
    for i in range(n):
        for j in range(i, n):
            for _ in range(matrix[i][j]):
                edges.append((i, j))

    # Инициализируем матрицу инцидентности нулями
    inc = [[0] * len(edges) for _ in range(n)]

    # Заполняем инцидентность для каждого ребра
    for k, (u, v) in enumerate(edges):
        if u == v:                     # петля
            inc[u][k] = 2
        else:                          # обычное ребро
            inc[u][k] = inc[v][k] = 1

    return inc, edges

# ---------------- Визуализация ----------------
def visualize_graph(matrix):
    """
    Рисует граф, используя раскраску через максимальные независимые множества.
    Поддерживаются кратные рёбра (изгибы) и петли.
    """
    G = nx.MultiGraph()
    n = len(matrix)
    
    # ----- Раскраска через максимально пустые подграфы -----
    color_numbers = color_via_maximal_independent_sets(matrix)
    # Словарь для отображения номеров цветов в красивые названия
    color_names = {
        1: "DodgerBlue", 2: "Crimson", 3: "Gold", 4: "MediumSeaGreen",
        5: "DarkOrchid", 6: "Tomato", 7: "DeepSkyBlue", 8: "HotPink",
        9: "OrangeRed", 10: "MediumTurquoise"
    }
    # Если цветов больше, чем в словаре, добавим серый
    max_color = max(color_numbers) if color_numbers else 0
    for i in range(1, max_color + 1):
        if i not in color_names:
            color_names[i] = "Gray"
    
    ColorMatrix = [color_names[c] for c in color_numbers]
    chromatic_number = len(set(color_numbers))
    print(f"\nХроматическое число (по алгоритму МНМ): {chromatic_number}")
    # ---------------------------------------------
    
    G.add_nodes_from(range(n))
    # Добавляем кратные рёбра
    for i in range(n):
        for j in range(i, n):
            for _ in range(matrix[i][j]):
                G.add_edge(i, j)
    
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_color=ColorMatrix, node_size=500)
    nx.draw_networkx_labels(G, pos, font_size=12)
    
    # Отрисовка кратных рёбер с изгибами
    edges_by_pair = {}
    for u, v in G.edges():
        if u != v:
            pair = tuple(sorted((u, v)))
            edges_by_pair.setdefault(pair, []).append((u, v))
    
    for pair, edge_list in edges_by_pair.items():
        num_edges = len(edge_list)
        if num_edges == 1:
            rad_values = [0]
        else:
            rad_values = [0.2 * (i - (num_edges - 1) / 2) for i in range(num_edges)]
        for idx, (u, v) in enumerate(edge_list):
            rad = rad_values[idx]
            nx.draw_networkx_edges(G, pos, edgelist=[(u, v)],
                                   connectionstyle=f'arc3, rad={rad}',
                                   edge_color='red', width=2)
    
    # Петли
    loops = [(u, v) for u, v in G.edges() if u == v]
    if loops:
        nx.draw_networkx_edges(G, pos, edgelist=loops, edge_color='red', width=2)
    
    plt.axis('off')
    plt.show()

# ---------------- Отрисовка таблиц матриц ----------------
def display_matrix(matrix):
    n = len(matrix)
    k = len(matrix[1])
    print("   ", end="")
    for j in range(k):
        print(f"{j:3}", end="")
    print()
    for i, row in enumerate(matrix):
        print(f"{i:3}", end="")
        for val in row:
            print(f"{val:3}", end="")
        print()

def display_incidence_matrix(inc, edges):
    """
    Выводит матрицу инцидентности в удобочитаемом виде.
    Заголовки столбцов: r0, r1, ... (рёбра)
    Заголовки строк: v0, v1, ... (вершины)
    """
    n = len(inc)
    m = len(edges)

    print("\nМатрица инцидентности:")

    # Формируем строку заголовка столбцов
    header = ["    "] + [f"r{k}" for k in range(m)]
    print(" ".join(f"{h:>3}" for h in header))

    # Выводим каждую строку с меткой вершины
    for i in range(n):
        row = [f"v{i}"] + [str(inc[i][j]) for j in range(m)]
        print(" ".join(f"{x:>3}" for x in row))

def display_edges_list(data):
    # print("Вывод в виде таблицы:")
    print("   ", "".join(f"r{i:<3}" for i in range(len(data))))
    print("От:", "".join(f"{a:<4}" for a, _ in data))
    print("До:", "".join(f"{b:<4}" for _, b in data))
    # print(f"Вывод в виде списка:\n{data}")





# ================ Лабораторная работа 2 ================

# ---------------- Перемножение матриц ----------------
def multiply_matrix(a, b):
    n = len(a)
    result = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += a[i][k] * b[k][j]
    return result

# ---------------- Поиск путей ----------------
def compute_shortest_paths_matrix(matrix):
    n = len(matrix)
    output_matrix = [[-1] * n for _ in range(n)]

    # расстояние до самой себя
    for i in range(n):
        output_matrix[i][i] = 0

    # Прямые ребра
    for i in range(n):
        for j in range(n):
            if matrix[i][j] > 0:
                output_matrix[i][j] = 1

    # Текущая степень матрицы смежности
    current_power = [row[:] for row in matrix] # более глубокое копирование матрицы во избежание проблем
    path_length = 1

    # Цикл пока есть непомеченные вершины
    while path_length < n:
        # Умножаем на исходную матрицу смежности
        current_power = multiply_matrix(current_power, matrix)
        path_length += 1

        # Ищем новые пути длины path_length
        changed = False
        for i in range(n):
            for j in range(n):
                # Если расстояние еще не найдено и есть путь длины path_length
                if output_matrix[i][j] == -1 and current_power[i][j] > 0:
                    output_matrix[i][j] = path_length
                    changed = True
        
        # Если на этом шаге не нашли новых путей - заменяем -1 на 0 и выходим
        if not changed:
            for i in range(n):
                for j in range(n):
                    if output_matrix[i][j] == -1:
                        output_matrix[i][j] = output_matrix[j][i] = 0 # можно заменить 0 на float('inf') для корректности
            break

    return output_matrix

# ---------------- Поиск радиуса и диаметра ----------------
def calculate_radius_and_diameter(matrix):
    n = len(matrix)

    path_len_arr = []

    for i in range(len(matrix)):
        path_len_arr.append(max(matrix[i]))

    radius = diameter = max(path_len_arr)

    for i in range(len(path_len_arr)):
        if path_len_arr[i] != 0 and path_len_arr[i] < radius:
            radius = path_len_arr[i]

    central_vertices = [i for i, ecc in enumerate(path_len_arr) if ecc == radius]
    peripheral_vertices = [i for i, ecc in enumerate(path_len_arr) if ecc == diameter]
    isolated_verticies = [i for i, ecc in enumerate(path_len_arr) if ecc == 0]

    print("   ", end="")
    for j in range(n):
        if j < n:
            print(f"{j:3}", end="")
        elif j == n:
            print(f"max", end="")
    print("  max")
    for i, row in enumerate(matrix):
        print(f"{i:3}", end="")
        for val in row:
            print(f"{val:3}", end="")
        print(f"{path_len_arr[i]:4}")

    print(f"\nРадиус: {radius}")
    print(f"Диаметр: {diameter}")
    print(f"Центральные вершины: {central_vertices}")
    print(f"Периферийные вершины: {peripheral_vertices}")
    print(f"Изолированные вершины: {isolated_verticies}")

    return path_len_arr
        




# ================ Лабораторная работа 3 ================

# max_independent_sets = list(nx.find_cliques(nx.complement(Grap)))

# ---------------- Поиск максимально пустых подграфов ----------------
def magu_weissman_maximal_independent_sets(adj_matrix):
    """Возвращает список всех максимальных независимых множеств (как frozenset или set)."""
    n = len(adj_matrix)
    all_vertices = set(range(n))
    
    # Шаг 1: строим список дизъюнктов (рёбер) – КНФ
    clauses = []
    for i in range(n):
        for j in range(i + 1, n):
            if adj_matrix[i][j] != 0:
                clauses.append({i, j})
    
    if not clauses:
        # Нет рёбер – всё множество независимо
        return [all_vertices]
    
    # Шаг 2: перемножение скобок (КНФ -> ДНФ) с поглощением
    # Начинаем с первого ребра как набора элементарных конъюнкций (по одному литералу)
    dnf = [{v} for v in clauses[0]]
    
    for clause in clauses[1:]:
        new_dnf = []
        for term in dnf:
            for v in clause:
                new_term = term.union({v})
                new_dnf.append(new_term)
        # Поглощение: удаляем термы, содержащие другой терм как подмножество
        new_dnf.sort(key=len)
        filtered = []
        for term in new_dnf:
            if not any(existing.issubset(term) for existing in filtered):
                filtered.append(term)
        dnf = filtered
    
    # Шаг 3: dnf содержит минимальные вершинные покрытия.
    # Инвертируем их, чтобы получить максимальные независимые множества.
    maximal_sets = []
    for cover in dnf:
        indep = all_vertices.difference(cover)
        maximal_sets.append(indep)
    return maximal_sets


def color_via_maximal_independent_sets(adj_matrix):
    """
    Раскраска вершин через последовательное выделение максимальных независимых множеств.
    Возвращает список colors, где colors[i] – номер цвета (1, 2, ...) для вершины i.
    """
    n = len(adj_matrix)
    # Преобразуем матрицу в бинарную (0/1), если там были кратности
    bin_adj = [[1 if adj_matrix[i][j] != 0 else 0 for j in range(n)] for i in range(n)]
    
    remaining = set(range(n))        # ещё не окрашенные вершины
    color_of = [0] * n               # 0 означает «не окрашена»
    current_color = 1
    
    while remaining:
        # Построим подматрицу для оставшихся вершин
        # Для удобства перенумеруем оставшиеся вершины индексами 0..k-1
        rem_list = list(remaining)
        idx_of = {v: i for i, v in enumerate(rem_list)}   # от исходного индекса к позиции в подграфе
        k = len(rem_list)
        sub_adj = [[0] * k for _ in range(k)]
        for i, u in enumerate(rem_list):
            for j, v in enumerate(rem_list):
                if bin_adj[u][v]:
                    sub_adj[i][j] = 1
        
        # Находим все максимальные независимые множества в подграфе
        all_max_sets = magu_weissman_maximal_independent_sets(sub_adj)
        if not all_max_sets:
            # На всякий случай: если множество пусто (не должно быть)
            break
        
        # Берём первое максимальное независимое множество
        max_set_idx = all_max_sets[0]   # это set индексов в подграфе (0..k-1)
        # Преобразуем в исходные номера вершин
        max_set_orig = {rem_list[i] for i in max_set_idx}
        
        # Окрашиваем все вершины этого множества в текущий цвет
        for v in max_set_orig:
            color_of[v] = current_color
        
        # Удаляем окрашенные вершины из рассмотрения
        remaining -= max_set_orig
        current_color += 1
    
    return color_of




# ================ Лабораторная работа 4 ================

# ---------------- Генерация графа с весами ----------------
def generate_weighted_matrix(matrix, min_weight=1, max_weight=20):
    n = len(matrix)
    weight_matrix = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(i, n):
            if matrix[i][j] != 0:          # ребро существует
                weight = random.randint(min_weight, max_weight)
                weight_matrix[i][j] = weight
                weight_matrix[j][i] = weight
    return weight_matrix


# ---------------- Алгоритм Дейкстры ----------------
def deikstra(matrix, start, end):
    """
    Алгоритм Дейкстры для графа, заданного матрицей смежности.
    Параметры:
        matrix - квадратная матрица смежности (веса рёбер, 0 = нет ребра)
        start  - индекс начальной вершины (0..n-1)
        end    - индекс конечной вершины
    Возвращает:
        (path, distance) - path: список вершин от start до end,
                           distance: суммарный вес кратчайшего пути.
                           Если пути нет, path = [], distance = inf.
    """
    n = len(matrix)
    # Инициализация
    dist = [float('inf')] * n
    visited = [False] * n
    prev = [-1] * n   # для восстановления пути

    dist[start] = 0

    for _ in range(n):
        # 1. Находим непосещённую вершину с минимальным dist
        u = -1
        min_dist = float('inf')
        for i in range(n):
            if not visited[i] and dist[i] < min_dist:
                min_dist = dist[i]
                u = i
        if u == -1:          # все оставшиеся вершины недостижимы
            break
        visited[u] = True

        # 2. Релаксация всех соседей u
        for v in range(n):
            if not visited[v] and matrix[u][v] != 0:
                weight = matrix[u][v]    # вес ребра (в нашем случае кратность)
                new_dist = dist[u] + weight
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    prev[v] = u

    # Восстановление пути
    if dist[end] == float('inf'):
        return [], float('inf')

    path = []
    cur = end
    while cur != -1:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path, dist[end]




# ================ main ================

# ----------- Лаба 1 -----------
print("========== Лабораторная работа 1 ==========\n")

# Генерация матрицы смежности
matrix = generate_adjacency_matrix()

n = len(matrix)

# Вывод матрицы смежности
print("\nМатрица смежности:")
display_matrix(matrix)

# Получение матрицы инцидентности и списка рёбер
inc, edges = build_incidence_matrix(matrix)
display_incidence_matrix(inc, edges)

# Вывод списка рёбер
print("\nСписок рёбер:")
display_edges_list(edges)


# ----------- Лаба 2 -----------
print("\n\n\n========== Лабораторная работа 2 ==========")

# Вывод матрицы минимальных путей
print("\nМатрица путей:")
path_matrix = compute_shortest_paths_matrix(matrix)    
calculate_radius_and_diameter(path_matrix)


# ----------- Лаба 3 -----------
print("\n\n\n========== Лабораторная работа 3 ==========")

maximal_sets = magu_weissman_maximal_independent_sets(matrix)
print("\nВсе максимальные независимые множества:")
for i, ms in enumerate(maximal_sets, 1):
    print(f"{i}: {ms}")
largest_set = max(maximal_sets, key=len)
print(f"Наибольшее независимое множество: {largest_set} (размер {len(largest_set)})")


# ----------- Лаба 4 -----------
print("\n\n\n========== Лабораторная работа 4 ==========")

start = 0 # начало
end = n-1 # конец

# Вариант с взвешенным графом
# weighted_matrix = generate_weighted_matrix(matrix, min_weight=1, max_weight=5)
# print("\nМатрица весов рёбер:")
# display_matrix(weighted_matrix)
# path, distance = deikstra(weighted_matrix, start, end) # матрица с весом

# Вариант с графом без веса
path, distance = deikstra(matrix, start, end)
if path:
    print(f"Кратчайший путь из {start} в {end}: {path}")
    print(f"Суммарное расстояние (вес): {distance}")
else:
    print(f"Пути из {start} в {end} не существует.")


# ----------- Визуализация графа -----------
visualize_graph(matrix)