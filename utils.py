# ─── 유틸리티 ───────────────────────────────────────────

from config import LABEL_MAP

def normalize_label(value):
    """입력 라벨을 표준 라벨(Cross/X)로 정규화한다."""
    return LABEL_MAP.get(value.lower().strip(), value)

def validate_matrix(matrix, expected_size):
    """행렬이 expected_size × expected_size인지 검증한다.
    Returns: (유효 여부, 오류 메시지)
    """
    if len(matrix) != expected_size:
        return False, f"행 수 불일치: {len(matrix)} != {expected_size}"
    for i, row in enumerate(matrix):
        if len(row) != expected_size:
            return False, f"행 {i}의 열 수 불일치: {len(row)} != {expected_size}"
    return True, ""

def extract_size_from_key(key):
    """패턴 키(예: 'size_5_1')에서 크기 N을 추출한다."""
    parts = key.split('_')
    return int(parts[1])

def generate_pattern(n, pattern_type):
    """n×n 크기의 Cross 또는 X 패턴을 자동 생성한다.
    성능 분석에서 3×3 등 기본 패턴이 필요할 때 사용한다.
    """
    mid = n // 2
    result = []
    for i in range(n):
        row = []
        for j in range(n):
            if pattern_type == 'cross':
                row.append(1 if (i == mid or j == mid) else 0)
            else:  # 'x'
                row.append(1 if (i == j or i + j == n - 1) else 0)
        result.append(row)
    return result
