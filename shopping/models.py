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
    vendor = models.OneToOneField("users.Vendor", on_delete=models.CASCADE, related_name="rule")
    
    min_order_price = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True)
    min_order_quantity = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = _("basket rule")
        verbose_name_plural = _("basket rules")

    def __str__(self):
        return f"Rules for {self.vendor.name}"

    def check_constraints(self, total_quantity, total_price):
        if self.min_order_quantity and total_quantity < self.min_order_quantity:
            raise ValidationError(
                _("برای ثبت سفارش از فروشنده %(vendor)s، حداقل خرید شما باید %(minimum)s %(unit)s باشد.") % {
                    "vendor": self.vendor.name,
                    "minimum": english_to_farsi_digits(self.min_order_quantity),
                    "unit": _("عدد")
                }
            )
        
        if self.min_order_price and total_price < self.min_order_price:
            raise ValidationError(
                _("برای ثبت سفارش از فروشنده %(vendor)s، حداقل خرید شما باید %(minimum)s %(unit)s باشد.") % {
                    "vendor": self.vendor.name,
                    "minimum": english_to_farsi_digits(self.min_order_price),
                    "unit": _("تومان")
                }
            )

    def validate_basket_conditions(self, basket):
        vendor_items = basket.items.filter(product__vendor=self.vendor)
        vendor_items_data = (
            vendor_items.annotate(
                unit_price=models.Case(
                    models.When(
                        product__discount_price__isnull=False,
                        product__discount_price__gt=0,
                        then=F('product__discount_price'),
                    ),
                    default=F('product__price'),
                    output_field=models.PositiveIntegerField(),
                )
            ).annotate(subtotal=F('quantity') * F('unit_price'))
            .aggregate(total_quantity=Sum('quantity'), total_price=Sum('subtotal'))
        )
        
        self.check_constraints(
            total_quantity=vendor_items_data['total_quantity'] or 0, 
            total_price=vendor_items_data['total_price'] or 0
        )
