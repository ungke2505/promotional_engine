from __future__ import annotations


def resolve_benefits(benefits: list[dict]) -> list[dict]:
    resolved = []
    exclusive_applied = False

    for benefit in benefits:
        if not benefit:
            continue
        allow_stack = bool(benefit.get("allow_with_other_rules"))
        if exclusive_applied and not allow_stack:
            continue
        resolved.append(benefit)
        if not allow_stack:
            exclusive_applied = True

    return resolved
