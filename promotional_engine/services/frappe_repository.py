from __future__ import annotations

try:
    import frappe  # type: ignore
except ImportError:  # pragma: no cover
    frappe = None


def is_frappe_available() -> bool:
    return frappe is not None


def load_campaigns_from_db() -> list[dict]:
    if not frappe:
        return []

    campaign_names = frappe.get_all(
        "Promotion Campaign",
        filters={"status": ["in", ["Active", "Draft"]]},
        pluck="name",
    )
    return [frappe.get_doc("Promotion Campaign", name).as_dict() for name in campaign_names]


def load_rules_from_db(campaign_names: list[str] | None = None) -> list[dict]:
    if not frappe:
        return []

    filters = {"is_active": 1}
    if campaign_names:
        filters["campaign"] = ["in", campaign_names]

    rule_names = frappe.get_all("Promotion Rule", filters=filters, pluck="name")
    return [frappe.get_doc("Promotion Rule", name).as_dict() for name in rule_names]


def load_loyalty_policy(policy_name: str | None = None, company: str | None = None) -> dict:
    if not frappe:
        return {}

    if policy_name:
        return frappe.get_doc("Loyalty Policy", policy_name).as_dict()

    filters = {"is_active": 1}
    if company:
        filters["company"] = company
    names = frappe.get_all("Loyalty Policy", filters=filters, order_by="modified desc", pluck="name")
    if not names:
        return {}
    return frappe.get_doc("Loyalty Policy", names[0]).as_dict()
