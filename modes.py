import json
from config import EPSILON, REPEAT_COUNT
from utils import normalize_label, validate_matrix, extract_size_from_key, generate_pattern
from core import mac_operation, compare_scores, measure_performance

def input_matrix_3x3(prompt):
    """사용자로부터 3×3 행렬을 입력받는다."""
    while True:
        print(prompt)
        matrix = []
        valid = True
        for _ in range(3):
            line = input().strip()
            parts = line.split()
            if len(parts) != 3:
                print("입력 형식 오류: 각 줄에 3개의 숫자를 공백으로 구분해 입력하세요.")
                valid = False
                break
            try:
                row = [float(x) for x in parts]
                matrix.append(row)
            except ValueError:
                print("입력 형식 오류: 숫자만 입력해주세요.")
                valid = False
                break
        if valid and len(matrix) == 3:
            return matrix

def run_mode_1():
    """모드 1: 사용자가 3×3 필터 2개와 패턴을 입력하여 MAC 판정을 수행한다."""
    print("\n#----------------------------------------")
    print("# [1] 필터 입력")
    print("#----------------------------------------")
    filter_a = input_matrix_3x3("필터 A (3줄 입력, 공백 구분)")
    print()
    filter_b = input_matrix_3x3("필터 B (3줄 입력, 공백 구분)")

    print("\n#----------------------------------------")
    print("# [2] 패턴 입력")
    print("#----------------------------------------")
    pattern = input_matrix_3x3("패턴 (3줄 입력, 공백 구분)")

    score_a = mac_operation(pattern, filter_a)
    score_b = mac_operation(pattern, filter_b)

    avg_time_ms = measure_performance(pattern, filter_a) * 1000
    diff = abs(score_a - score_b)
    if diff < EPSILON:
        verdict = "판정 불가"
    else:
        verdict = "A" if score_a > score_b else "B"

    print("\n#----------------------------------------")
    if verdict == "판정 불가":
        print("# [3] MAC 결과 (판정 불가)")
    else:
        print("# [3] MAC 결과")
    print("#----------------------------------------")
    print(f"A 점수: {score_a}")
    print(f"B 점수: {score_b}")
    print(f"연산 시간(평균/{REPEAT_COUNT}회): {avg_time_ms:.3f} ms")
    if verdict == "판정 불가":
        print(f"판정: 판정 불가 (|A-B| < {EPSILON})")
    else:
        print(f"판정: {verdict}")

def run_mode_2():
    """모드 2: data.json에서 필터/패턴을 로드하여 일괄 MAC 판정을 수행한다."""
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("오류: data.json 파일을 찾을 수 없습니다.")
        return
    except json.JSONDecodeError as e:
        print(f"오류: data.json 파싱 실패 - {e}")
        return

    filters_data = data.get('filters', {})
    patterns_data = data.get('patterns', {})

    print("\n#----------------------------------------")
    print("# [1] 필터 로드")
    print("#----------------------------------------")
    filters = {}
    for size_key in sorted(filters_data.keys()):
        filter_pair = filters_data[size_key]
        n = int(size_key.split('_')[1])
        filters[n] = {}
        for label_key, matrix in filter_pair.items():
            std_label = normalize_label(label_key)
            filters[n][std_label] = matrix
        labels = ', '.join(sorted(filters[n].keys()))
        print(f"[OK] {size_key:<8} 필터 로드 완료 ({labels})")

    print("\n#----------------------------------------")
    print("# [2] 패턴 분석 (라벨 정규화 적용)")
    print("#----------------------------------------")
    results = []
    perf_data = {}

    for pat_key in sorted(patterns_data.keys()):
        pat_info = patterns_data[pat_key]
        pattern = pat_info.get('input')
        expected_raw = pat_info.get('expected', '')
        expected = normalize_label(expected_raw)

        print(f"\n--- {pat_key} ---")

        try:
            n = extract_size_from_key(pat_key)
        except (IndexError, ValueError):
            reason = f"[데이터/스키마 문제] 키 형식 오류: '{pat_key}'"
            print(f"판정: FAIL ({reason})")
            results.append((pat_key, False, reason))
            continue

        if n not in filters:
            reason = f"[데이터/스키마 문제] size_{n} 필터 없음"
            print(f"판정: FAIL ({reason})")
            results.append((pat_key, False, reason))
            continue

        valid, msg = validate_matrix(pattern, n)
        if not valid:
            reason = f"[데이터/스키마 문제] 크기 불일치 - {msg}"
            print(f"판정: FAIL ({reason})")
            results.append((pat_key, False, reason))
            continue

        cross_filter = filters[n]['Cross']
        x_filter = filters[n]['X']
        score_cross = mac_operation(pattern, cross_filter)
        score_x = mac_operation(pattern, x_filter)
        
        verdict = compare_scores(score_cross, score_x)

        if verdict == 'UNDECIDED':
            passed = False
            fail_reason = "[수치 비교 문제] 동점(UNDECIDED) 처리 규칙에 따라 FAIL"
            pass_fail = "FAIL (동점 규칙)"
        elif verdict == expected:
            passed = True
            fail_reason = ""
            pass_fail = "PASS"
        else:
            passed = False
            fail_reason = f"[로직 문제] 판정 '{verdict}' ≠ expected '{expected}'"
            pass_fail = "FAIL"

        print(f"Cross 점수: {score_cross}")
        print(f"X 점수: {score_x}")
        print(f"판정: {verdict} | expected: {expected} | {pass_fail}")

        results.append((pat_key, passed, fail_reason))

        if n not in perf_data:
            perf_data[n] = (pattern, cross_filter)

    print("\n#----------------------------------------")
    print(f"# [3] 성능 분석 (평균/{REPEAT_COUNT}회)")
    print("#----------------------------------------")
    sizes = sorted(set([3] + list(perf_data.keys())))
    print(f"{'크기':<12}{'평균 시간(ms)':<16}{'연산 횟수'}")
    print("-" * 40)

    for n in sizes:
        if n in perf_data:
            pat, flt = perf_data[n]
        else:
            pat = generate_pattern(n, 'cross')
            flt = generate_pattern(n, 'cross')

        avg_sec = measure_performance(pat, flt)
        avg_ms = avg_sec * 1000
        ops = n * n
        print(f"{n}×{n:<9}{avg_ms:<16.3f}{ops}")

    print("\n#----------------------------------------")
    print("# [4] 결과 요약")
    print("#----------------------------------------")
    total = len(results)
    passed_count = sum(1 for _, p, _ in results if p)
    failed_count = total - passed_count

    print(f"총 테스트: {total}개")
    print(f"통과:      {passed_count}개")
    print(f"실패:      {failed_count}개")

    if failed_count > 0:
        print("\n실패 케이스:")
        for key, passed, reason in results:
            if not passed:
                print(f"  - {key}: {reason}")
    print("\n(상세 원인 분석 및 복잡도 설명은 README.md의 \"결과 리포트\" 섹션에 작성)")
