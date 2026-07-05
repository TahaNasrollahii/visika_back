import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'visika.settings.local')
django.setup()

from products.models import Category, Product, ProductImage, ProductFeature

Category.objects.all().delete()
Product.objects.all().delete()
ProductImage.objects.all().delete()
ProductFeature.objects.all().delete()

# Create Categories
dairy = Category.objects.create(title="لبنیات", slug="dairy", icon="🥛", color="bg-blue-100 text-blue-600")
meat = Category.objects.create(title="گوشت و مرغ", slug="meat", icon="🥩", color="bg-red-100 text-red-600")
snacks = Category.objects.create(title="تنقلات", slug="snacks", icon="🍫", color="bg-purple-100 text-purple-600")
drinks = Category.objects.create(title="نوشیدنی‌ها", slug="drinks", icon="🥤", color="bg-cyan-100 text-cyan-600")
fruits = Category.objects.create(title="میوه و سبزیجات", slug="fruits", icon="🍎", color="bg-green-100 text-green-600")
bakery = Category.objects.create(title="نان و شیرینی", slug="bakery", icon="🥐", color="bg-yellow-100 text-yellow-600")
breakfast = Category.objects.create(title="صبحانه", slug="breakfast", icon="🍳", color="bg-orange-100 text-orange-600")
cleaning = Category.objects.create(title="شوینده و بهداشتی", slug="cleaning", icon="🧼", color="bg-teal-100 text-teal-600")
spices = Category.objects.create(title="چاشنی و ادویه", slug="spices", icon="🧂", color="bg-amber-100 text-amber-600")


# Create Products
p1 = Product.objects.create(title="شیر کم چرب کاله 1 لیتری", price=35000, discount_price=32000, category=dairy, is_best_seller=True, brand="کاله", rating=4.5, reviews_count=120)
p2 = Product.objects.create(title="روغن آفتابگردان اویلا 1.5 لیتری", price=110000, discount_price=95000, badge="پرفروش", is_best_seller=True, brand="اویلا", rating=4.2, reviews_count=85)
p3 = Product.objects.create(title="تخم مرغ 20 عددی تلاونگ", price=85000, is_best_seller=True, brand="تلاونگ", rating=4.8, reviews_count=210)

p4 = Product.objects.create(title="گوشت چرخ‌کرده گوساله 500 گرمی", price=320000, discount_price=285000, category=meat, is_hot_offer=True, brand="پویا پروتئین", rating=4.1, reviews_count=45)
p5 = Product.objects.create(title="مرغ کامل تازه بسته بندی 2 کیلویی", price=195000, discount_price=175000, category=meat, badge="پیشنهاد ویژه", is_hot_offer=True, brand="مهیا پروتئین", rating=4.6, reviews_count=150)

p6 = Product.objects.create(title="چیپس مکیما طعم کچاپ 100 گرمی", price=25000, discount_price=22000, category=snacks, badge="جدید", brand="مکیما", rating=3.9, reviews_count=30)
p7 = Product.objects.create(title="شکلات تلخ پارمیدا 80 درصد", price=75000, category=snacks, is_best_seller=True, brand="پارمیدا", rating=4.9, reviews_count=320)

p8 = Product.objects.create(title="نوشابه کوکاکولا خانواده 1.5 لیتری", price=32000, discount_price=29000, category=drinks, is_hot_offer=True, brand="کوکاکولا", rating=4.7, reviews_count=540)
p9 = Product.objects.create(title="آب معدنی دماوند 1.5 لیتری", price=9000, category=drinks, brand="دماوند", rating=4.3, reviews_count=95)

# Add mock image paths (reusing images for the new ones since we only have 5 real images)
ProductImage.objects.create(product=p1, image="products/Gemini_Generated_Image_3hpnii3hpnii3hpn.png")
ProductImage.objects.create(product=p2, image="products/Gemini_Generated_Image_67xmen67xmen67xm.png")
ProductImage.objects.create(product=p3, image="products/Gemini_Generated_Image_6hv3u46hv3u46hv3.png")
ProductImage.objects.create(product=p4, image="products/Gemini_Generated_Image_crjfk1crjfk1crjf.png")
ProductImage.objects.create(product=p5, image="products/Gemini_Generated_Image_oxu981oxu981oxu9.png")
ProductImage.objects.create(product=p6, image="products/Gemini_Generated_Image_67xmen67xmen67xm.png") # Reusing
ProductImage.objects.create(product=p7, image="products/Gemini_Generated_Image_3hpnii3hpnii3hpn.png") # Reusing
ProductImage.objects.create(product=p8, image="products/Gemini_Generated_Image_crjfk1crjfk1crjf.png") # Reusing
ProductImage.objects.create(product=p9, image="products/Gemini_Generated_Image_oxu981oxu981oxu9.png") # Reusing

# Create Features
def add_features(product, features_dict):
    for k, v in features_dict.items():
        ProductFeature.objects.create(product=product, title=k, value=v)

add_features(p1, {"وزن": "۱ لیتر", "شرایط نگهداری": "در یخچال (دمای ۱ تا ۴ درجه)", "شماره پروانه": "۳۴/۱۰۲۳۹", "ترکیبات": "شیر پاستوریزه کم چرب"})
add_features(p2, {"حجم": "۱.۵ لیتر", "نوع روغن": "آفتابگردان", "مخصوص": "پخت و پز و سالاد", "شماره پروانه": "۵۶/۱۲۳۴۵"})
add_features(p3, {"تعداد": "۲۰ عدد", "اندازه": "متوسط", "شرایط نگهداری": "در جای خنک"})
add_features(p4, {"وزن": "۵۰۰ گرم", "نوع گوشت": "گوساله چرخ‌کرده", "درصد چربی": "۱۵ درصد", "شرایط نگهداری": "در فریزر"})
add_features(p5, {"وزن": "۲ کیلوگرم", "نوع": "مرغ کامل", "بسته بندی": "بشقابی روکش‌دار", "شرایط نگهداری": "در یخچال یا فریزر"})
add_features(p6, {"وزن": "۱۰۰ گرم", "طعم": "کچاپ", "شرکت سازنده": "مکیما"})
add_features(p7, {"وزن": "۱۰۰ گرم", "درصد کاکائو": "۸۰٪", "نوع": "تخته‌ای"})
add_features(p8, {"حجم": "۱.۵ لیتر", "طعم": "کولا", "نوع بسته‌بندی": "بطری پلاستیکی"})
add_features(p9, {"حجم": "۱.۵ لیتر", "نوع آب": "آب معدنی طبیعی", "سرچشمه": "دماوند"})

print("Seed completed!")
