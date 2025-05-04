import random
import os
import time
import matplotlib.pyplot as plt


iteration_count = 0


def generate_data_files():
    os.makedirs('data', exist_ok=True)
    sizes = [random.randint(100, 10000) for _ in range(50)]
    sizes.sort()
    for i, size in enumerate(sizes):
        data = [random.randint(0, 100000) for _ in range(size)]
        with open(f'data/input_{i+1}_{size}.txt', 'w') as f:
            f.write(' '.join(map(str, data)))


def counting_sort(arr, exp):
    global iteration_count
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    for i in range(n):
        index = arr[i] // exp
        count[index % 10] += 1
        iteration_count += 1

    for i in range(1, 10):
        count[i] += count[i - 1]
        iteration_count += 1

    i = n - 1
    while i >= 0:
        index = arr[i] // exp
        output[count[index % 10] - 1] = arr[i]
        count[index % 10] -= 1
        iteration_count += 1
        i -= 1

    for i in range(n):
        arr[i] = output[i]
        iteration_count += 1


def radix_sort(arr):
    global iteration_count
    iteration_count = 0

    if len(arr) == 0:
        return

    max_num = max(arr)
    exp = 1
    while max_num // exp > 0:
        counting_sort(arr, exp)
        exp *= 10


def run_tests():
    files = []
    for f in os.listdir('data'):
        try:
            if f.startswith("input_") and f.endswith(".txt"):
                size = int(f.split('_')[2].split('.')[0])
                files.append((f, size))
        except (IndexError, ValueError):
            continue

    files.sort(key=lambda x: x[1])
    files = [f[0] for f in files]

    sizes = []
    times = []
    iterations = []

    for file in files:
        with open(f'data/{file}', 'r') as f:
            arr = list(map(int, f.read().split()))
        size = len(arr)
        sizes.append(size)

        start_time = time.perf_counter()
        radix_sort(arr)
        end_time = time.perf_counter()

        times.append(end_time - start_time)
        iterations.append(iteration_count)

        print(f"Файл: {file}, Размер: {size}, Время: {times[-1]:.6f} с, Итерации: {iterations[-1]}")

    return sizes, times, iterations


def plot_results(sizes, times, iterations):
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.plot(sizes, times, marker='o', linestyle='-', color='blue')
    plt.title('Время выполнения Radix Sort')
    plt.xlabel('Размер массива')
    plt.ylabel('Время (сек)')

    plt.subplot(1, 2, 2)
    plt.plot(sizes, iterations, marker='o', linestyle='-', color='orange')
    plt.title('Количество итераций')
    plt.xlabel('Размер массива')
    plt.ylabel('Итерации')

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    generate_data_files()
    sizes, times, iterations = run_tests()
    plot_results(sizes, times, iterations)
