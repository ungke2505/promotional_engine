from __future__ import annotations

from collections import Counter


def normalize_cart_items(cart):
    normalized = []
    for row in cart or []:
        qty = float(row.get("qty") or 0)
        rate = float(row.get("rate") or row.get("price") or 0)
        amount = float(row.get("amount") or qty * rate)
        normalized.append(
            {
                "item_code": row.get("item_code"),
                "item_group": row.get("item_group"),
                "brand": row.get("brand"),
                "qty": qty,
                "rate": rate,
                "amount": amount,
            }
        )
    return normalized


def summarize_cart(cart_items):
    total_qty = sum(item["qty"] for item in cart_items)
    subtotal = sum(item["amount"] for item in cart_items)
    distinct_items = len({item["item_code"] for item in cart_items if item["item_code"]})
    item_groups = Counter(item["item_group"] for item in cart_items if item["item_group"])
    item_codes = [item["item_code"] for item in cart_items if item["item_code"]]
    return {
        "total_qty": total_qty,
        "subtotal": subtotal,
        "distinct_items": distinct_items,
        "item_groups": dict(item_groups),
        "item_groups_list": list(item_groups.keys()),
        "item_codes": item_codes,
    }
