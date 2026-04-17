from __future__ import annotations

from .frappe_repository import load_loyalty_policy


def enrich_context(context: dict) -> dict:
    normalized = dict(context)
    normalized["available_points"] = int(float(context.get("available_points") or 0))

    loyalty_policy = context.get("loyalty_policy")
    if isinstance(loyalty_policy, str):
        normalized["loyalty_policy"] = load_loyalty_policy(
            policy_name=loyalty_policy,
            company=context.get("company"),
        )
    elif loyalty_policy:
        normalized["loyalty_policy"] = loyalty_policy
    else:
        normalized["loyalty_policy"] = load_loyalty_policy(company=context.get("company"))

    return normalized
