from src.decision.normalizer import normalize_skill_name


def main():
    samples = [
        "Нападение",
        " нападение ",
        "ОБОРОНА",
        "магия света",
        "Мудрость",
        "Магия  Разрушения"
    ]

    print("=== DEBUG NORMALIZER ===")
    for sample in samples:
        normalized = normalize_skill_name(sample)
        print(f"{sample!r} -> {normalized!r}")


if __name__ == "__main__":
    main()