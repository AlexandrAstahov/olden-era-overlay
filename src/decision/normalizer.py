import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"


def load_skills():
    with open(DATA_DIR / "skills.json", "r", encoding="utf-8") as f:
        return json.load(f)


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