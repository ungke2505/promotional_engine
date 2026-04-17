from frappe.model.document import Document


class PromotionRule(Document):
    def validate(self):
        if self.maximum_discount_percent and (
            self.maximum_discount_percent < 0 or self.maximum_discount_percent > 100
        ):
            raise ValueError("Maximum discount percent must be between 0 and 100.")
