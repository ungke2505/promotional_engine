import frappe

from .services.promotion_evaluator import evaluate_cart
from .services.redemption_logger import log_redemption


@frappe.whitelist()
def get_applicable_promotions(
    cart=None,
    customer=None,
    customer_group=None,
    territory=None,
    company=None,
    pos_profile=None,
    coupon_code=None,
    available_points=None,
    loyalty_policy=None,
    campaigns=None,
    rules=None,
):
    """Server entry point intended for POSAwesome cart evaluation."""
    context = {
        "cart": frappe.parse_json(cart) if cart else [],
        "customer": customer,
        "customer_group": customer_group,
        "territory": territory,
        "company": company,
        "pos_profile": pos_profile,
        "coupon_code": coupon_code,
        "available_points": available_points,
        "loyalty_policy": frappe.parse_json(loyalty_policy) if loyalty_policy else None,
        "campaigns": frappe.parse_json(campaigns) if campaigns else None,
        "rules": frappe.parse_json(rules) if rules else None,
    }
    return evaluate_cart(context)


@frappe.whitelist()
def log_promotion_redemption(redemption_payload=None):
    payload = frappe.parse_json(redemption_payload) if redemption_payload else {}
    return log_redemption(payload)
