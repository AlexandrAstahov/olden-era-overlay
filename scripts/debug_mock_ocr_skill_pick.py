import json
from pathlib import Path

from src.decision.engine import choose_best_skill


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MOCK_OCR_FILE = PROJECT_ROOT / "data" / "mock_ocr" / "mock_skill_pick_01.json"


def load_mock_ocr(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    payload = load_mock_ocr(MOCK_OCR_FILE)

    if payload["screen_type"] != "skill-pick":
        print(f"Неподдерживаемый тип экрана: {payload['screen_type']}")
        return

    best, evaluation = choose_best_skill(
        archetype=payload["archetype"],
        offered_skills=payload["offered_skills"],
        current_skills=payload["current_skills"]
    )

    print("=== DEBUG MOCK OCR SKILL PICK ===")
    print(f"Файл: {payload['source_file']}")
    print(f"Герой: {payload['hero_name']}")
    print(f"Класс: {payload['hero_class']}")
    print(f"Архетип: {payload['archetype']}")
    print(f"Текущие навыки (raw): {', '.join(payload['current_skills'])}")
    print(f"Предложенные навыки (raw): {', '.join(payload['offered_skills'])}")
    print(f"Текущие навыки (normalized): {', '.join(evaluation['normalized_current_skills'])}")
    print(f"Предложенные навыки (normalized): {', '.join(evaluation['normalized_offered_skills'])}")

    if evaluation["unknown_current_skills"]:
        print(f"Не распознаны текущие навыки: {', '.join(evaluation['unknown_current_skills'])}")

    if evaluation["unknown_offered_skills"]:
        print(f"Не распознаны предложенные навыки: {', '.join(evaluation['unknown_offered_skills'])}")

    print()
    print("Оценка вариантов:")
    for item in evaluation["results"]:
        print(f"- {item['skill_name']}: {item['score']}")
        for reason in item["reasons"]:
            print(f"  * {reason}")

    print()
    print("Рекомендация:")
    if best:
        print(f"Текущий выбор:")
        print(f"Навык: {best['skill_name']}")
        print("Почему: лучший результат по базовым весам и синергиям")
    else:
        print("Не удалось выбрать навык")


if __name__ == "__main__":
    main()