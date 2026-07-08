import datetime
import json
from django.utils import timezone
from django.db.models import Sum, Count
from users.models import User, Vendor
from products.models import Product
from orders.models import Cart, Order

def dashboard_callback(request, context):
    now = timezone.now()
    today = now.date()
    
    users_count = User.objects.count()
    active_vendors = Vendor.objects.filter(is_active=True).count()
    inactive_vendors = Vendor.objects.filter(is_active=False).count()
    total_vendors = active_vendors + inactive_vendors
    
    products_count = Product.objects.count()
    baskets_today = Cart.objects.filter(created_at__date=today).count()
    
    # Orders last 7 days chart data
    days = []
    order_counts = []
    for i in range(6, -1, -1):
        day = today - datetime.timedelta(days=i)
        count = Order.objects.filter(created_at__date=day).count()
        # format day as 'Mon', 'Tue'
        days.append(day.strftime("%a"))
        order_counts.append(count)
        
    chart_data = json.dumps({
        "labels": days,
        "datasets": [{
            "label": "Daily count",
            "data": order_counts,
            "borderColor": "#e85d04", # matching unfold brand color or primary
            "backgroundColor": "transparent",
            "tension": 0.4
        }]
    })

    # Most sold products
    top_products = Product.objects.annotate(
        sold_count=Sum('orderitem__quantity')
    ).exclude(sold_count=None).order_by('-sold_count')[:5]
    
    # Real low stock items
    low_stock = Product.objects.filter(stock__lte=5).order_by('stock')[:5]

    active_vendors_percent = int((active_vendors / total_vendors * 100)) if total_vendors > 0 else 0

    context.update({
        "users_count": users_count,
        "active_vendors": active_vendors,
        "inactive_vendors": inactive_vendors,
        "total_vendors": total_vendors,
        "active_vendors_percent": active_vendors_percent,
        "products_count": products_count,
        "baskets_today": baskets_today,
        "chart_data": chart_data,
        "top_products": top_products,
        "low_stock": low_stock,
    })
    
    return context
