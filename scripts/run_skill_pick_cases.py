import json
from pathlib import Path

from src.decision.engine import choose_best_skill


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEST_CASES_DIR = PROJECT_ROOT / "data" / "test_cases"


def load_case(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    case_files = sorted(TEST_CASES_DIR.glob("skill_pick_case_*.json"))

    if not case_files:
        print("Нет тест-кейсов в data/test_cases")
        return

    total = 0
    passed = 0

    print("=== RUN SKILL PICK CASES ===")
    print()

    for case_file in case_files:
        case = load_case(case_file)

        best, evaluation = choose_best_skill(
            archetype=case["archetype"],
            offered_skills=case["offered_skills"],
            current_skills=case["current_skills"]
        )

        results = evaluation["results"]
        total += 1
        expected = case.get("expected_best")
        ok = best is not None and best["skill_name"] == expected

        if ok:
            passed += 1

        print(f"[{case['case_id']}] {case['description']}")
        print(f"Архетип: {case['archetype']}")
        print(f"Текущие навыки (raw): {', '.join(case['current_skills'])}")
        print(f"Предложенные навыки (raw): {', '.join(case['offered_skills'])}")
        print(f"Текущие навыки (normalized): {', '.join(evaluation['normalized_current_skills'])}")
        print(f"Предложенные навыки (normalized): {', '.join(evaluation['normalized_offered_skills'])}")

        if evaluation["unknown_current_skills"]:
            print(f"Не распознаны текущие навыки: {', '.join(evaluation['unknown_current_skills'])}")

        if evaluation["unknown_offered_skills"]:
            print(f"Не распознаны предложенные навыки: {', '.join(evaluation['unknown_offered_skills'])}")

        print("Оценка вариантов:")
        for item in results:
            print(f"- {item['skill_name']}: {item['score']}")

        print(f"Ожидалось: {expected}")
        print(f"Получено: {best['skill_name'] if best else 'None'}")
        print(f"Результат: {'OK' if ok else 'FAIL'}")
        print()

    print("=== SUMMARY ===")
    print(f"Пройдено: {passed}/{total}")

    if passed == total:
        print("Все тест-кейсы пройдены")
    else:
        print("Есть непройденные тест-кейсы")


if __name__ == "__main__":
    main()