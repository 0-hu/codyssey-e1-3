"""data.json 생성 스크립트 (일회성 사용 후 삭제)"""
import json


def gen_cross(n):
    """n×n 십자가(Cross) 패턴 생성"""
    mid = n // 2
    return [[1 if (i == mid or j == mid) else 0 for j in range(n)] for i in range(n)]


def gen_x(n):
    """n×n X 패턴 생성"""
    return [[1 if (i == j or i + j == n - 1) else 0 for j in range(n)] for i in range(n)]


data = {
    "filters": {
        "size_5": {"cross": gen_cross(5), "x": gen_x(5)},
        "size_13": {"cross": gen_cross(13), "x": gen_x(13)},
        "size_25": {"cross": gen_cross(25), "x": gen_x(25)}
    },
    "patterns": {
        # 정상 케이스 (PASS 예상)
        "size_5_1": {"input": gen_x(5), "expected": "x"},
        "size_5_2": {"input": gen_cross(5), "expected": "+"},
        "size_13_1": {"input": gen_cross(13), "expected": "+"},
        "size_13_2": {"input": gen_x(13), "expected": "x"},
        "size_25_1": {"input": gen_cross(25), "expected": "+"},
        "size_25_2": {"input": gen_x(25), "expected": "x"},
        # 동점 케이스 — 전체 1로 채운 패턴: Cross/X 점수 동일 → UNDECIDED → FAIL
        "size_13_3": {"input": [[1] * 13 for _ in range(13)], "expected": "x"},
        # 크기 불일치 케이스 — 5×5 키인데 3×3 데이터 → 스키마 검증 FAIL
        "size_5_3": {"input": [[1, 0, 1], [0, 1, 0], [1, 0, 1]], "expected": "+"}
    }
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("data.json 생성 완료")
