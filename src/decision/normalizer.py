from src.decision.engine import load_skills


def normalize_text(value: str) -> str:
    return " ".join(value.strip().lower().replace("ё", "е").split())


def build_skill_alias_map():
    skills = load_skills()
    alias_map = {}

    for skill in skills:
        canonical_name = skill["name_ru"]
        all_names = [canonical_name] + skill.get("aliases", [])

        for name in all_names:
            alias_map[normalize_text(name)] = canonical_name

    return alias_map


def normalize_skill_name(raw_name: str):
    alias_map = build_skill_alias_map()
    normalized = normalize_text(raw_name)
    return alias_map.get(normalized)