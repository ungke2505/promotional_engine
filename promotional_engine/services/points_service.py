from __future__ import annotations

import math


def evaluate_points_rule(rule: dict, context: dict, cart_summary: dict) -> dict | None:
    rule_type = rule.get("rule_type")
    if rule_type not in {"Points Earn", "Points Redeem"}:
        return None

    if rule_type == "Points Earn":
        earned = _calculate_earned_points(rule, cart_summary)
        if earned <= 0:
            return None
        return {
            "type": "points",
            "rule_name": rule.get("rule_name"),
            "campaign": rule.get("campaign"),
            "points_earned": earned,
            "points_redeemed": 0,
            "cashback_amount": 0,
            "discount_amount": 0,
            "redemption_method": None,
        }

    return _calculate_redemption(rule, context, cart_summary)


def _calculate_earned_points(rule: dict, cart_summary: dict) -> int:
    earn_rate = float(rule.get("discount_value") or 0)
    if earn_rate <= 0:
        return 0
    return int(cart_summary["subtotal"] // earn_rate)


def _calculate_redemption(rule: dict, context: dict, cart_summary: dict) -> dict | None:
    available_points = int(float(context.get("available_points") or 0))
    loyalty_policy = context.get("loyalty_policy") or {}
    minimum_points = int(float(loyalty_policy.get("minimum_redeem_points") or 0))
    if available_points <= 0 or available_points < minimum_points:
        return None

    rate = float(loyalty_policy.get("point_to_currency_rate") or loyalty_policy.get("redeem_rate") or 0)
    if rate <= 0:
        return None

    method = _resolve_redemption_method(rule, loyalty_policy)
    max_by_amount = float(loyalty_policy.get("maximum_redeem_amount") or cart_summary["subtotal"])
    max_percent = float(loyalty_policy.get("maximum_cashback_percent") or 100)
    max_by_percent = cart_summary["subtotal"] * (max_percent / 100)
    allowed_currency = min(cart_summary["subtotal"], max_by_amount, max_by_percent)
    if allowed_currency <= 0:
        return None

    raw_points_to_use = allowed_currency / rate
    points_to_use = min(
        available_points,
        _round_points(raw_points_to_use, loyalty_policy.get("rounding_method")),
    )
    if not loyalty_policy.get("allow_partial_redemption", 1) and points_to_use != available_points:
        return None
    if points_to_use < minimum_points:
        return None

    currency_value = min(points_to_use * rate, allowed_currency)
    return {
        "type": "points",
        "rule_name": rule.get("rule_name"),
        "campaign": rule.get("campaign"),
        "points_earned": 0,
        "points_redeemed": points_to_use,
        "cashback_amount": currency_value if method == "Cashback" else 0,
        "discount_amount": currency_value if method != "Cashback" else 0,
        "redemption_method": method,
        "remaining_points": max(available_points - points_to_use, 0),
    }


def _resolve_redemption_method(rule: dict, loyalty_policy: dict) -> str:
    action = rule.get("points_action")
    if action == "Cashback":
        return "Cashback"
    if action == "Discount":
        return "Discount"
    method = loyalty_policy.get("redemption_method") or "Discount"
    return "Cashback" if method == "Cashback" else "Discount"


def _round_points(value: float, method: str | None) -> int:
    method = (method or "Floor").lower()
    if method == "ceil":
        return int(math.ceil(value))
    if method == "nearest":
        return int(round(value))
    return int(math.floor(value))
