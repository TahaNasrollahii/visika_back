from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models import F, Sum
from core.models import TimestampedModel

def english_to_farsi_digits(number):
    farsi_digits = '۰۱۲۳۴۵۶۷۸۹'
    english_digits = '0123456789'
    translation_table = str.maketrans(english_digits, farsi_digits)
    return str(number).translate(translation_table)

class BasketRule(TimestampedModel):
    vendor = models.ForeignKey("users.Vendor", on_delete=models.CASCADE, related_name="rule")
    
    min_order_price = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True)
    min_order_quantity = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"Rules for {self.vendor.name}"

    def check_constraints(self, total_quantity, total_price):
        errors = []
        
        if self.min_order_quantity and total_quantity < self.min_order_quantity:
            raise ValidationError(
                _("For putting order on vendor %(vendor)s, you need to buy at least %(minimum)s %(unit)s") % {
                    "vendor": self.vendor.name,
                    "minimum": english_to_farsi_digits(self.min_order_quantity),
                    "unit": _("Number")
                }
            )
        
        if self.min_order_price and total_price < self.min_order_price:
            raise ValidationError(
                _("For putting order on vendor %(vendor)s, you need to buy at least %(minimum)s %(unit)s") % {
                    "vendor": self.vendor.name,
                    "minimum": english_to_farsi_digits(self.min_order_price),
                    "unit": _("Tooman")
                }
            )
        
        return errors

    def validate_basket_conditions(self, basket):
        vendor_items = basket.items.filter(product__vendor=self.vendor)
        vendor_items_data = (
            vendor_items.annotate(subtotal=F('quantity') * F('final_price'))
            .aggregate(total_quantity=Sum('quantity'), total_price=Sum('subtotal'))
        )
        
        return self.check_constraints(
            total_quantity=vendor_items_data['total_quantity'] or 0, 
            total_price=vendor_items_data['total_price'] or 0
        )
