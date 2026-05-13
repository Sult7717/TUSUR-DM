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

    clear = lambda: os.system('cls')
    clear()
    if mode == 1:                # простой граф
        print(f"Режим простого графа")
    elif mode == 2:              # полный граф
        print(f"Режим полного графа")
    elif mode == 3:              # граф с петлями
        print(f"Режим графа с петлями")
    elif mode == 4:              # мультиграф (mode == 4)
        print(f"Режим мультиграфа с мультипетлями")
    else:
        print(f"Тестовая матрица")

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
    Рисует граф с использованием библиотеки networkx и matplotlib.
    Поддерживаются кратные рёбра (изгибы) и петли.
    """
    G = nx.MultiGraph()          # мультиграф для хранения кратных рёбер
    n = len(matrix)

    G.add_nodes_from(range(n))

    # Добавляем рёбра из матрицы смежности
    for i in range(n):
        for j in range(i, n):
            for _ in range(matrix[i][j]):
                G.add_edge(i, j)

    # Располагаем вершины с помощью алгоритма spring_layout
    pos = nx.spring_layout(G)

    # Рисуем вершины и их подписи
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=500)
    nx.draw_networkx_labels(G, pos, font_size=12)

    # Группируем обычные рёбра (не петли) по паре вершин,
    # чтобы правильно отрисовать кратные рёбра с разным изгибом
    edges_by_pair = {}
    for u, v in G.edges():
        if u != v:
            pair = tuple(sorted((u, v)))           # упорядоченная пара для неориентированного графа
            edges_by_pair.setdefault(pair, []).append((u, v))

    # Для каждой пары вершин рисуем рёбра с разными радиусами изгиба
    for pair, edge_list in edges_by_pair.items():
        num_edges = len(edge_list)
        if num_edges == 1:
            rad_values = [0]                       # прямое ребро
        else:
            # Симметричные радиуса изгиба: например, для 2 рёбер [-0.1, 0.1],
            # для 3: [-0.2, 0, 0.2] и т.д.
            rad_values = [0.2 * (i - (num_edges - 1) / 2) for i in range(num_edges)]

        for idx, (u, v) in enumerate(edge_list):
            rad = rad_values[idx]
            nx.draw_networkx_edges(
                G, pos, edgelist=[(u, v)],
                connectionstyle=f'arc3, rad={rad}',
                edge_color='red', width=2
            )

    # Петли рисуем стандартным способом (прямые изгибы не поддерживаются)
    loops = [(u, v) for u, v in G.edges() if u == v]
    if loops:
        nx.draw_networkx_edges(G, pos, edgelist=loops,
                               edge_color='red', width=2)

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
        




# ================ main ================

# ----------- Лаба 1 -----------

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

# Вывод матрицы минимальных путей
print("\nМатрица путей:")
path_matrix = compute_shortest_paths_matrix(matrix)    
calculate_radius_and_diameter(path_matrix)


# ----------- Лаба 3 -----------



# ----------- Визуализация графа -----------
visualize_graph(matrix)