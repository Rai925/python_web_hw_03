import time
from multiprocessing import Pool, cpu_count


def factorize(*numbers):
    results = []
    for num in numbers:
        factors = []
        for i in range(1, num + 1):
            if num % i == 0:
                factors.append(i)
        results.append(factors)
    return results


def factorize_single(num):
    factors = []
    for i in range(1, num + 1):
        if num % i == 0:
            factors.append(i)
    return factors


def factorize_parallel(*numbers):
    with Pool(cpu_count()) as pool:
        results = pool.map(factorize_single, numbers)
    return results


if __name__ == "__main__":
    # Перевірка роботи синхронної функції
    a, b, c, d = factorize(128, 255, 99999, 10651060)

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [
        1,
        2,
        4,
        5,
        7,
        10,
        14,
        20,
        28,
        35,
        70,
        140,
        76079,
        152158,
        304316,
        380395,
        532553,
        760790,
        1065106,
        1521580,
        2130212,
        2662765,
        5325530,
        10651060,
    ]

    # Перевірка роботи покращеної функції
    a, b, c, d = factorize_parallel(128, 255, 99999, 10651060)

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [
        1,
        2,
        4,
        5,
        7,
        10,
        14,
        20,
        28,
        35,
        70,
        140,
        76079,
        152158,
        304316,
        380395,
        532553,
        760790,
        1065106,
        1521580,
        2130212,
        2662765,
        5325530,
        10651060,
    ]

    # Заміряємо час виконання синхронної функції
    start_time_sync = time.time()
    factorize(128, 255, 99999, 10651060)
    end_time_sync = time.time()
    print(
        "Час виконання синхронної функції factorize:",
        end_time_sync - start_time_sync,
        "секунд",
    )

    # Заміряємо час виконання покращеної функції
    start_time_parallel = time.time()
    factorize_parallel(128, 255, 99999, 10651060)
    end_time_parallel = time.time()
    print(
        "Час виконання покращеної функції factorize:",
        end_time_parallel - start_time_parallel,
        "секунд",
    )
