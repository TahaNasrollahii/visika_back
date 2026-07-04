import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'visika.settings.local')
django.setup()

from products.models import Category, Product, ProductImage

Category.objects.all().delete()
Product.objects.all().delete()
ProductImage.objects.all().delete()

# Create Categories
dairy = Category.objects.create(title="لبنیات", slug="dairy", icon="🥛", color="bg-blue-100 text-blue-600")
meat = Category.objects.create(title="گوشت و مرغ", slug="meat", icon="🥩", color="bg-red-100 text-red-600")

# Create Products
p1 = Product.objects.create(title="شیر کم چرب کاله 1 لیتری", price=35000, discount_price=32000, category=dairy, is_best_seller=True)
p2 = Product.objects.create(title="روغن آفتابگردان اویلا 1.5 لیتری", price=110000, discount_price=95000, badge="پرفروش", is_best_seller=True)
p3 = Product.objects.create(title="تخم مرغ 20 عددی تلاونگ", price=85000, is_best_seller=True)

p4 = Product.objects.create(title="گوشت چرخ‌کرده گوساله 500 گرمی", price=320000, discount_price=285000, category=meat, is_hot_offer=True)
p5 = Product.objects.create(title="مرغ کامل تازه بسته بندی 2 کیلویی", price=195000, discount_price=175000, category=meat, badge="پیشنهاد ویژه", is_hot_offer=True)

# Add mock image paths (these exist in frontend public/products)
ProductImage.objects.create(product=p1, image="products/Gemini_Generated_Image_3hpnii3hpnii3hpn.png")
ProductImage.objects.create(product=p2, image="products/Gemini_Generated_Image_67xmen67xmen67xm.png")
ProductImage.objects.create(product=p3, image="products/Gemini_Generated_Image_6hv3u46hv3u46hv3.png")
ProductImage.objects.create(product=p4, image="products/Gemini_Generated_Image_crjfk1crjfk1crjf.png")
ProductImage.objects.create(product=p5, image="products/Gemini_Generated_Image_oxu981oxu981oxu9.png")

print("Seed completed!")
