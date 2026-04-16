import time
from config import EPSILON, REPEAT_COUNT

# ─── 핵심 연산 & 성능 측정 ──────────────────────────────────────

def mac_operation(pattern, filter_matrix):
    """MAC(Multiply-Accumulate) 연산을 수행한다.
    같은 위치의 원소를 곱한 뒤 모두 합산하여 유사도 점수를 반환한다.
    """
    n = len(pattern)
    total = 0.0
    for i in range(n):
        for j in range(n):
            total += pattern[i][j] * filter_matrix[i][j]
    return total

def compare_scores(score_cross, score_x, epsilon=EPSILON):
    """두 필터 점수를 epsilon 기반으로 비교하여 판정한다."""
    if abs(score_cross - score_x) < epsilon:
        return 'UNDECIDED'
    return 'Cross' if score_cross > score_x else 'X'

def measure_performance(pattern, filter_matrix, repeats=REPEAT_COUNT):
    """MAC 연산을 repeats회 반복 측정하여 평균 시간(초)을 반환한다.
    I/O 시간을 제외하고 순수 연산 시간만 측정한다.
    """
    times = []
    for _ in range(repeats):
        start = time.perf_counter()
        mac_operation(pattern, filter_matrix)
        end = time.perf_counter()
        times.append(end - start)
    return sum(times) / len(times)
