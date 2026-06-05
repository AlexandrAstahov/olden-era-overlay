import json
from pathlib import Path

from src.decision.engine import choose_best_skill


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEST_CASE_PATH = PROJECT_ROOT / "data" / "test_cases" / "skill_pick_case_01.json"


def load_test_case(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    case = load_test_case(TEST_CASE_PATH)

    archetype = case["archetype"]
    current_skills = case["current_skills"]
    offered_skills = case["offered_skills"]
    expected_best = case.get("expected_best")

    best, results = choose_best_skill(
        archetype=archetype,
        offered_skills=offered_skills,
        current_skills=current_skills
    )

    print("=== DEBUG SKILL PICK ===")
    print(f"Кейс: {case['case_id']}")
    print(f"Описание: {case['description']}")
    print(f"Архетип: {archetype}")
    print(f"Текущие навыки: {', '.join(current_skills)}")
    print(f"Предложенные навыки: {', '.join(offered_skills)}")
    print()

    print("Оценка вариантов:")
    for item in results:
        print(f"- {item['skill_name']}: {item['score']}")
        for reason in item["reasons"]:
            print(f"  * {reason}")

    print()
    print("Лучший выбор:")
    print(f"{best['skill_name']} -> score {best['score']}")

    if expected_best:
        print()
        print("Проверка ожидания:")
        if best["skill_name"] == expected_best:
            print(f"OK: ожидался {expected_best}, результат совпадает")
        else:
            print(f"FAIL: ожидался {expected_best}, получен {best['skill_name']}")


if __name__ == "__main__":
    main()