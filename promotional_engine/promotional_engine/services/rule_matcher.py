from __future__ import annotations


def select_eligible_rules(
    context: dict,
    campaigns: list[dict],
    cart_summary: dict,
    rules: list[dict],
) -> list[dict]:
    campaign_names = {campaign.get("name") or campaign.get("campaign_name") for campaign in campaigns}
    eligible = []

    for rule in rules:
        if not _is_rule_active(rule):
            continue
        if campaign_names and rule.get("campaign") not in campaign_names:
            continue
        if not _matches_context(rule, context, cart_summary):
            continue
        eligible.append(rule)

    return sorted(eligible, key=lambda item: int(item.get("priority") or 10))


def _is_rule_active(rule: dict) -> bool:
    if "is_active" not in rule:
        return True
    return bool(rule.get("is_active"))


def _matches_context(rule: dict, context: dict, cart_summary: dict) -> bool:
    if rule.get("pos_profile") and rule.get("pos_profile") != context.get("pos_profile"):
        return False
    if rule.get("customer_group") and rule.get("customer_group") != context.get("customer_group"):
        return False
    if rule.get("territory") and rule.get("territory") != context.get("territory"):
        return False
    if (rule.get("minimum_qty") or 0) > cart_summary["total_qty"]:
        return False
    if (rule.get("minimum_amount") or 0) > cart_summary["subtotal"]:
        return False
    if (rule.get("minimum_distinct_items") or 0) > cart_summary["distinct_items"]:
        return False
    if not _matches_dynamic_conditions(rule.get("conditions") or [], context, cart_summary):
        return False
    return True


def _matches_dynamic_conditions(conditions: list[dict], context: dict, cart_summary: dict) -> bool:
    for condition in conditions:
        if not _evaluate_condition(condition, context, cart_summary):
            return False
    return True


def _evaluate_condition(condition: dict, context: dict, cart_summary: dict) -> bool:
    left = _resolve_condition_value(condition.get("field_name"), context, cart_summary)
    right = _coerce_value(condition.get("value"), condition.get("value_type"))
    operator = (condition.get("operator") or "=").strip()

    if operator == "=":
        return left == right
    if operator == "!=":
        return left != right
    if operator == ">":
        return left > right
    if operator == ">=":
        return left >= right
    if operator == "<":
        return left < right
    if operator == "<=":
        return left <= right
    if operator == "contains":
        return right in (left or [])
    if operator == "in":
        return left in _ensure_list(right)
    return False


def _resolve_condition_value(field_name: str | None, context: dict, cart_summary: dict):
    lookup = {
        "customer": context.get("customer"),
        "customer_group": context.get("customer_group"),
        "territory": context.get("territory"),
        "company": context.get("company"),
        "pos_profile": context.get("pos_profile"),
        "coupon_code": context.get("coupon_code"),
        "available_points": context.get("available_points"),
        "subtotal": cart_summary.get("subtotal"),
        "total_qty": cart_summary.get("total_qty"),
        "distinct_items": cart_summary.get("distinct_items"),
        "item_codes": cart_summary.get("item_codes"),
        "item_groups": cart_summary.get("item_groups_list"),
    }
    return lookup.get(field_name)


def _coerce_value(value, value_type: str | None):
    if value_type == "Int":
        return int(float(value or 0))
    if value_type == "Float":
        return float(value or 0)
    if value_type == "JSON":
        return _ensure_list(value)
    return value


def _ensure_list(value):
    if isinstance(value, list):
        return value
    if value is None:
        return []
    return [item.strip() for item in str(value).split(",") if item.strip()]
