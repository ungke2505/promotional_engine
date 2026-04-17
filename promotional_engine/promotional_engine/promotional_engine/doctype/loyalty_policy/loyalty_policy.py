from frappe.model.document import Document


class LoyaltyPolicy(Document):
    def validate(self):
        self._validate_cashback_settings()

    def _validate_cashback_settings(self):
        if self.point_to_currency_rate and self.point_to_currency_rate < 0:
            raise ValueError("Point to currency rate cannot be negative.")

        if self.maximum_cashback_percent and (
            self.maximum_cashback_percent < 0 or self.maximum_cashback_percent > 100
        ):
            raise ValueError("Maximum cashback percent must be between 0 and 100.")
