from __future__ import annotations

from .frappe_repository import load_rules_from_db


def load_rules(context: dict, campaigns: list[dict]) -> list[dict]:
    rules = context.get("rules")
    if rules:
        return rules

    campaign_names = [campaign.get("name") or campaign.get("campaign_name") for campaign in campaigns]
    return load_rules_from_db(campaign_names)
