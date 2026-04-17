from __future__ import annotations

from .benefit_calculator import evaluate_rule
from .campaign_loader import load_active_campaigns
from .context_builder import enrich_context
from .cart_utils import normalize_cart_items, summarize_cart
from .conflict_resolver import resolve_benefits
from .rule_loader import load_rules
from .rule_matcher import select_eligible_rules


def evaluate_cart(context: dict) -> dict:
    context = enrich_context(context)
    cart_items = normalize_cart_items(context.get("cart"))
    cart_summary = summarize_cart(cart_items)
    campaigns = load_active_campaigns(context)
    rules = load_rules(context, campaigns)
    eligible_rules = select_eligible_rules(context, campaigns, cart_summary, rules)

    evaluated_benefits = []
    for rule in eligible_rules:
        benefit = evaluate_rule(rule, context, cart_items, cart_summary)
        if benefit:
            benefit["priority"] = int(rule.get("priority") or 10)
            benefit["allow_with_other_rules"] = bool(rule.get("allow_with_other_rules"))
            evaluated_benefits.append(benefit)

    resolved_benefits = resolve_benefits(
        sorted(evaluated_benefits, key=lambda item: item.get("priority", 10))
    )
    return _build_response(context, cart_summary, eligible_rules, resolved_benefits)


def _build_response(
    context: dict,
    cart_summary: dict,
    eligible_rules: list[dict],
    resolved_benefits: list[dict],
) -> dict:
    line_discounts = []
    cart_discounts = []
    free_items = []
    coupon_result = None
    points_result = {
        "points_earned": 0,
        "points_redeemed": 0,
        "cashback_amount": 0,
        "discount_amount": 0,
        "remaining_points": int(float(context.get("available_points") or 0)),
    }
    applied_rules = []
    messages = []

    for benefit in resolved_benefits:
        applied_rules.append(benefit.get("rule_name"))
        if benefit["type"] == "item_discount":
            line_discounts.extend(benefit.get("line_discounts", []))
        elif benefit["type"] == "cart_discount":
            cart_discounts.append(
                {
                    "rule_name": benefit.get("rule_name"),
                    "amount": benefit.get("amount", 0),
                }
            )
        elif benefit["type"] == "free_item":
            free_items.extend(benefit.get("items", []))
        elif benefit["type"] == "coupon":
            coupon_result = benefit
        elif benefit["type"] == "points":
            points_result["points_earned"] += int(benefit.get("points_earned") or 0)
            points_result["points_redeemed"] += int(benefit.get("points_redeemed") or 0)
            points_result["cashback_amount"] += float(benefit.get("cashback_amount") or 0)
            points_result["discount_amount"] += float(benefit.get("discount_amount") or 0)
            if "remaining_points" in benefit:
                points_result["remaining_points"] = int(benefit["remaining_points"])
            if benefit.get("redemption_method"):
                points_result["redemption_method"] = benefit.get("redemption_method")

    total_line_discount = sum(item.get("discount_amount", 0) for item in line_discounts)
    total_cart_discount = sum(item.get("amount", 0) for item in cart_discounts)
    total_discount = total_line_discount + total_cart_discount + points_result["discount_amount"]
    net_total = max(cart_summary["subtotal"] - total_discount, 0)

    if not applied_rules:
        messages.append("No promotions matched the current cart context.")
    if points_result["cashback_amount"]:
        messages.append("Points redemption generated cashback value.")

    return {
        "applied_rules": applied_rules,
        "eligible_offers": [rule.get("rule_name") for rule in eligible_rules],
        "line_discounts": line_discounts,
        "cart_discounts": cart_discounts,
        "free_items": free_items,
        "coupon_result": coupon_result,
        "points_result": points_result,
        "messages": messages,
        "totals_before": {
            "subtotal": cart_summary["subtotal"],
            "qty": cart_summary["total_qty"],
            "distinct_items": cart_summary["distinct_items"],
        },
        "totals_after": {
            "discount_total": total_discount,
            "cashback_amount": points_result["cashback_amount"],
            "net_total": net_total,
        },
    }
