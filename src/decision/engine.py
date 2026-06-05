import json
from pathlib import Path

from src.decision.normalizer import normalize_skill_name


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


def normalize_skill_list(raw_skill_names: list[str]):
    normalized = []
    unknown = []

    for raw_name in raw_skill_names:
        canonical = normalize_skill_name(raw_name)
        if canonical:
            normalized.append(canonical)
        else:
            unknown.append(raw_name)

    return normalized, unknown


def evaluate_skill_options(archetype: str, offered_skills: list[str], current_skills: list[str] | None = None):
    if current_skills is None:
        current_skills = []

    rules = load_rules()
    skill_map = get_skill_map()

    normalized_offered_skills, unknown_offered = normalize_skill_list(offered_skills)
    normalized_current_skills, unknown_current = normalize_skill_list(current_skills)

    archetype_rules = rules["archetypes"][archetype]
    base_weights = archetype_rules["base_weights"]
    synergy_rules = rules.get("synergy_rules", [])

    results = []

    for skill_name in normalized_offered_skills:
        score = base_weights.get(skill_name, 0)
        reasons = [f"Базовый вес: {score}"]

        if skill_name not in skill_map:
            reasons.append("Навык отсутствует в skills.json")
        else:
            reasons.append(f"Навык найден в базе: {skill_name}")

        for synergy in synergy_rules:
            if synergy["if_has"] in normalized_current_skills and synergy["boosts"] == skill_name:
                modifier = synergy["modifier"]
                score += modifier
                reasons.append(f"Синергия +{modifier}: {synergy['reason']}")

        results.append({
            "skill_name": skill_name,
            "score": score,
            "reasons": reasons
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    return {
        "results": results,
        "normalized_offered_skills": normalized_offered_skills,
        "normalized_current_skills": normalized_current_skills,
        "unknown_offered_skills": unknown_offered,
        "unknown_current_skills": unknown_current
    }


def choose_best_skill(archetype: str, offered_skills: list[str], current_skills: list[str] | None = None):
    evaluation = evaluate_skill_options(archetype, offered_skills, current_skills)
    results = evaluation["results"]
    best = results[0] if results else None
    return best, evaluation