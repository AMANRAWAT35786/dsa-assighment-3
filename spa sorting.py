import random
import time
from typing import Callable, List, Tuple


def insertion_sort(arr: List[int]) -> List[int]:
    """Sort the list in place using insertion sort and return it."""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def merge(left: List[int], right: List[int]) -> List[int]:
    """Merge two sorted lists and return a new sorted list."""
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def merge_sort(arr: List[int]) -> List[int]:
    """Return a sorted list using merge sort."""
    if len(arr) <= 1:
        return arr[:]
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)


def partition(arr: List[int], low: int, high: int) -> int:
    """Lomuto partition scheme using the last element as pivot."""
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quick_sort(arr: List[int], low: int, high: int) -> List[int]:
    """Sort the list in place using quick sort and return it."""
    stack = [(low, high)]
    while stack:
        low, high = stack.pop()
        if low < high:
            pivot_index = partition(arr, low, high)
            if pivot_index - 1 - low > high - (pivot_index + 1):
                stack.append((low, pivot_index - 1))
                stack.append((pivot_index + 1, high))
            else:
                stack.append((pivot_index + 1, high))
                stack.append((low, pivot_index - 1))
    return arr


def quick_sort_wrapper(arr: List[int]) -> List[int]:
    """Wrapper to use quick sort with a simple function signature."""
    if not arr:
        return []
    return quick_sort(arr, 0, len(arr) - 1)


def measure_time(sort_func: Callable[[List[int]], List[int]], arr: List[int]) -> float:
    """Measure execution time for a sorting function on a copy of arr."""
    arr_copy = arr[:]
    start = time.perf_counter()
    sort_func(arr_copy)
    end = time.perf_counter()
    return end - start


def generate_random_list(size: int, seed: int = 42) -> List[int]:
    random.seed(seed + size)
    return [random.randint(1, 100_000) for _ in range(size)]


def generate_sorted_list(size: int) -> List[int]:
    return list(range(1, size + 1))


def generate_reverse_sorted_list(size: int) -> List[int]:
    return list(range(size, 0, -1))


def verify_correctness() -> bool:
    sample = [5, 2, 9, 1, 5, 6]
    expected = [1, 2, 5, 5, 6, 9]
    results = {
        'Insertion Sort': insertion_sort(sample[:]),
        'Merge Sort': merge_sort(sample[:]),
        'Quick Sort': quick_sort_wrapper(sample[:]),
    }
    return all(result == expected for result in results.values())


def format_seconds(seconds: float) -> str:
    return f"{seconds * 1000:.2f} ms"


def run_experiments() -> Tuple[str, List[str]]:
    sizes = [1000, 5000, 10000]
    input_types = [
        ('Random', generate_random_list),
        ('Sorted', generate_sorted_list),
        ('Reverse Sorted', generate_reverse_sorted_list),
    ]
    sort_functions = [
        ('Insertion Sort', insertion_sort),
        ('Merge Sort', merge_sort),
        ('Quick Sort', quick_sort_wrapper),
    ]
    lines = []
    header = (
        f"{'Input Type':<16} | {'Size':<6} | {'Insertion':<14} | {'Merge':<14} | {'Quick':<14}"
    )
    separator = '-' * len(header)
    lines.append(header)
    lines.append(separator)
    for input_name, generator in input_types:
        for size in sizes:
            data = generator(size)
            timings = []
            for _, sort_func in sort_functions:
                elapsed = measure_time(sort_func, data)
                timings.append(format_seconds(elapsed))
            lines.append(
                f"{input_name:<16} | {size:<6} | {timings[0]:<14} | {timings[1]:<14} | {timings[2]:<14}"
            )
    return '\n'.join(lines), lines


def save_output(text: str, filename: str = 'output/output.txt') -> None:
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)


def main() -> None:
    print('Sorting Performance Analyzer (SPA)')
    print('Course: ETCCDS201 - Basics of Data Structures')
    print('Algorithms: Insertion Sort, Merge Sort, Quick Sort')
    print()

    correctness = verify_correctness()
    correctness_text = 'PASS' if correctness else 'FAIL'
    print(f'Correctness check: {correctness_text}')
    print('Expected result: [1, 2, 5, 5, 6, 9]')
    print()

    results_text, lines = run_experiments()
    print('Timing results:')
    print(results_text)
    print()
    print('Notes:')
    print('- Insertion Sort is stable and in-place.')
    print('- Merge Sort is stable and out-of-place.')
    print('- Quick Sort is usually in-place and not stable in this implementation.')

    output_text = []
    output_text.append('Sorting Performance Analyzer (SPA)')
    output_text.append('Course: ETCCDS201 - Basics of Data Structures')
    output_text.append('Algorithms: Insertion Sort, Merge Sort, Quick Sort')
    output_text.append('')
    output_text.append(f'Correctness check: {correctness_text}')
    output_text.append('Expected result: [1, 2, 5, 5, 6, 9]')
    output_text.append('')
    output_text.append('Timing results:')
    output_text.append(results_text)
    output_text.append('')
    output_text.append('Notes:')
    output_text.append('- Insertion Sort is stable and in-place.')
    output_text.append('- Merge Sort is stable and out-of-place.')
    output_text.append('- Quick Sort is usually in-place and not stable in this implementation.')

    save_output('\n'.join(output_text))
    print('Saved results to output/output.txt')


if __name__ == '__main__':
    main()
