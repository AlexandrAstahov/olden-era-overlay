import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"


def load_json(filename: str):
    with open(DATA_DIR / filename, "r", encoding="utf-8") as f:
        return json.load(f)


def load_rules():
    return load_json("rules.json")


def load_skills():
    return load_json("skills.json")


def get_skill_map():
    skills = load_skills()
    return {skill["name_ru"]: skill for skill in skills}


def evaluate_skill_options(archetype: str, offered_skills: list[str], current_skills: list[str] | None = None):
    if current_skills is None:
        current_skills = []

    rules = load_rules()
    skill_map = get_skill_map()

    archetype_rules = rules["archetypes"][archetype]
    base_weights = archetype_rules["base_weights"]
    synergy_rules = rules.get("synergy_rules", [])

    results = []

    for skill_name in offered_skills:
        score = base_weights.get(skill_name, 0)
        reasons = [f"Базовый вес: {score}"]

        if skill_name not in skill_map:
            reasons.append("Навык отсутствует в skills.json")
        else:
            reasons.append(f"Навык найден в базе: {skill_name}")

        for synergy in synergy_rules:
            if synergy["if_has"] in current_skills and synergy["boosts"] == skill_name:
                modifier = synergy["modifier"]
                score += modifier
                reasons.append(f"Синергия +{modifier}: {synergy['reason']}")

        results.append({
            "skill_name": skill_name,
            "score": score,
            "reasons": reasons
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results


def choose_best_skill(archetype: str, offered_skills: list[str], current_skills: list[str] | None = None):
    results = evaluate_skill_options(archetype, offered_skills, current_skills)
    best = results[0] if results else None
    return best, results