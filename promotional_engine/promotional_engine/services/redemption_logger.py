from __future__ import annotations

from datetime import datetime

from .frappe_repository import is_frappe_available

try:
    import frappe  # type: ignore
except ImportError:  # pragma: no cover
    frappe = None


def log_redemption(payload: dict) -> dict:
    if not is_frappe_available() or not frappe:
        return {
            "created": False,
            "message": "Frappe is not available in this environment.",
            "payload": payload,
        }

    doc = frappe.get_doc(
        {
            "doctype": "Promotion Redemption",
            "posting_datetime": payload.get("posting_datetime") or datetime.utcnow(),
            "campaign": payload.get("campaign"),
            "rule": payload.get("rule"),
            "sales_invoice": payload.get("sales_invoice"),
            "customer": payload.get("customer"),
            "coupon_code": payload.get("coupon_code"),
            "points_used": payload.get("points_used"),
            "discount_amount": payload.get("discount_amount"),
            "pos_profile": payload.get("pos_profile"),
        }
    )
    doc.insert(ignore_permissions=True)
    return {"created": True, "name": doc.name}
