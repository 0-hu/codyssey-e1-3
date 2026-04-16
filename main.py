"""
Mini NPU 시뮬레이터
- MAC(Multiply-Accumulate) 연산을 이용한 Cross/X 패턴 판별기
- 모드 1: 사용자 입력 (3×3)
- 모드 2: data.json 일괄 분석
"""
from modes import run_mode_1, run_mode_2

def main():
    """프로그램 진입점: 모드를 선택하고 실행한다."""
    print("=== Mini NPU Simulator ===\n")
    print("[모드 선택]")
    print("1. 사용자 입력 (3x3)")
    print("2. data.json 분석")

    choice = input("선택: ").strip()

    if choice == '1':
        run_mode_1()
    elif choice == '2':
        run_mode_2()
    else:
        print("잘못된 선택입니다. 1 또는 2를 입력하세요.")

if __name__ == '__main__':
    main()
