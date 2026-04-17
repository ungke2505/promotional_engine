import unittest

from promotional_engine.promotional_engine.services.promotion_evaluator import evaluate_cart


class PromotionEngineTestCase(unittest.TestCase):
    def test_applies_cart_discount_and_points_cashback(self):
        result = evaluate_cart(
            {
                "cart": [
                    {"item_code": "ITEM-001", "item_group": "Beverages", "qty": 2, "rate": 50000},
                    {"item_code": "ITEM-002", "item_group": "Snacks", "qty": 1, "rate": 25000},
                ],
                "pos_profile": "Main POS",
                "available_points": 120,
                "loyalty_policy": {
                    "minimum_redeem_points": 50,
                    "point_to_currency_rate": 100,
                    "maximum_redeem_amount": 10000,
                    "maximum_cashback_percent": 20,
                    "rounding_method": "Floor",
                    "allow_partial_redemption": 1,
                    "redemption_method": "Cashback",
                },
                "campaigns": [{"name": "PROMO-APR", "status": "Active"}],
                "rules": [
                    {
                        "campaign": "PROMO-APR",
                        "rule_name": "Ten Percent Cart",
                        "rule_type": "Cart Discount",
                        "discount_type": "Percent",
                        "discount_value": 10,
                        "minimum_amount": 100000,
                        "priority": 5,
                        "allow_with_other_rules": 1,
                        "is_active": 1,
                    },
                    {
                        "campaign": "PROMO-APR",
                        "rule_name": "Points To Cashback",
                        "rule_type": "Points Redeem",
                        "points_action": "Cashback",
                        "priority": 10,
                        "allow_with_other_rules": 1,
                        "is_active": 1,
                    },
                ],
            }
        )

        self.assertEqual(result["applied_rules"], ["Ten Percent Cart", "Points To Cashback"])
        self.assertEqual(result["points_result"]["points_redeemed"], 100)
        self.assertEqual(result["points_result"]["cashback_amount"], 10000.0)
        self.assertEqual(result["totals_after"]["net_total"], 112500.0)

    def test_dynamic_condition_filters_rule(self):
        result = evaluate_cart(
            {
                "cart": [
                    {"item_code": "ITEM-001", "item_group": "Beverages", "qty": 1, "rate": 50000},
                ],
                "customer_group": "VIP",
                "campaigns": [{"name": "PROMO-VIP", "status": "Active"}],
                "rules": [
                    {
                        "campaign": "PROMO-VIP",
                        "rule_name": "VIP Cart Discount",
                        "rule_type": "Cart Discount",
                        "discount_type": "Amount",
                        "discount_value": 5000,
                        "is_active": 1,
                        "conditions": [
                            {
                                "field_name": "customer_group",
                                "operator": "=",
                                "value_type": "Data",
                                "value": "VIP",
                            }
                        ],
                    }
                ],
            }
        )

        self.assertEqual(result["applied_rules"], ["VIP Cart Discount"])
        self.assertEqual(result["cart_discounts"][0]["amount"], 5000.0)

    def test_dynamic_condition_blocks_rule(self):
        result = evaluate_cart(
            {
                "cart": [
                    {"item_code": "ITEM-001", "item_group": "Beverages", "qty": 1, "rate": 50000},
                ],
                "customer_group": "REGULAR",
                "campaigns": [{"name": "PROMO-VIP", "status": "Active"}],
                "rules": [
                    {
                        "campaign": "PROMO-VIP",
                        "rule_name": "VIP Cart Discount",
                        "rule_type": "Cart Discount",
                        "discount_type": "Amount",
                        "discount_value": 5000,
                        "is_active": 1,
                        "conditions": [
                            {
                                "field_name": "customer_group",
                                "operator": "=",
                                "value_type": "Data",
                                "value": "VIP",
                            }
                        ],
                    }
                ],
            }
        )

        self.assertEqual(result["applied_rules"], [])
        self.assertEqual(result["messages"], ["No promotions matched the current cart context."])


if __name__ == "__main__":
    unittest.main()
