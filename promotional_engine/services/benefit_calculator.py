from __future__ import annotations

from .points_service import evaluate_points_rule


def evaluate_rule(rule: dict, context: dict, cart_items: list[dict], cart_summary: dict) -> dict | None:
    rule_type = rule.get("rule_type")

    if rule_type == "Cart Discount":
        amount = _calculate_discount(rule, cart_summary["subtotal"])
        if amount <= 0:
            return None
        return {
            "type": "cart_discount",
            "rule_name": rule.get("rule_name"),
            "campaign": rule.get("campaign"),
            "amount": amount,
        }

    if rule_type == "Item Discount":
        line_discounts = _calculate_item_discounts(rule, cart_items)
        if not line_discounts:
            return None
        return {
            "type": "item_discount",
            "rule_name": rule.get("rule_name"),
            "campaign": rule.get("campaign"),
            "line_discounts": line_discounts,
        }

    if rule_type == "Buy X Get Y":
        if not rule.get("free_item_code") or not rule.get("free_qty"):
            return None
        return {
            "type": "free_item",
            "rule_name": rule.get("rule_name"),
            "campaign": rule.get("campaign"),
            "items": [
                {
                    "item_code": rule.get("free_item_code"),
                    "qty": float(rule.get("free_qty") or 0),
                }
            ],
        }

    if rule_type == "Coupon Validation":
        expected = rule.get("coupon_code")
        provided = context.get("coupon_code")
        if expected and provided and expected == provided:
            return {
                "type": "coupon",
                "rule_name": rule.get("rule_name"),
                "campaign": rule.get("campaign"),
                "valid": True,
                "coupon_code": provided,
            }
        return None

    return evaluate_points_rule(rule, context, cart_summary)


def _calculate_discount(rule: dict, base_amount: float) -> float:
    discount_type = rule.get("discount_type") or "Percent"
    discount_value = float(rule.get("discount_value") or 0)
    if discount_value <= 0:
        return 0
    if discount_type == "Amount":
        return min(discount_value, base_amount)

    amount = base_amount * (discount_value / 100)
    max_percent = float(rule.get("maximum_discount_percent") or 100)
    return min(amount, base_amount * (max_percent / 100))


def _calculate_item_discounts(rule: dict, cart_items: list[dict]) -> list[dict]:
    discounts = []
    for item in cart_items:
        if rule.get("item_code") and rule.get("item_code") != item.get("item_code"):
            continue
        if rule.get("item_group") and rule.get("item_group") != item.get("item_group"):
            continue
        amount = _calculate_discount(rule, item.get("amount") or 0)
        if amount <= 0:
            continue
        discounts.append(
            {
                "item_code": item.get("item_code"),
                "discount_amount": amount,
            }
        )
    return discounts
