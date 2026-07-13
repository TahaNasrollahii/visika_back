import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'visika.settings.local')
django.setup()

from products.models import Category, Product, ProductFeature
from users.models import User, Vendor

Category.objects.all().delete()
Product.objects.all().delete()
ProductFeature.objects.all().delete()
User.objects.filter(role=User.RoleChoices.VENDOR).delete()

def get_or_create_vendor(brand_name):
    try:
        vendor = Vendor.objects.get(name=brand_name)
    except Vendor.DoesNotExist:
        phone = f"+98999{random.randint(1000000, 9999999)}"
        while User.objects.filter(phone_number=phone).exists():
            phone = f"+98999{random.randint(1000000, 9999999)}"
        user = User.objects.create_user(phone_number=phone, password="password123")
        user.first_name = brand_name
        user.requested_brand_name = brand_name
        user.role = User.RoleChoices.VENDOR
        user.status = User.StatusChoices.ACTIVE
        user.save()
        
        user.refresh_from_db()
        vendor = user.vendor
    return vendor

# Create Categories
dairy = Category.objects.create(title="لبنیات", slug="dairy", icon="🥛", color="bg-blue-100 text-blue-600", image="categories/1.jpg")
meat = Category.objects.create(title="گوشت و مرغ", slug="meat", icon="🥩", color="bg-red-100 text-red-600", image="categories/2.jpg")
snacks = Category.objects.create(title="تنقلات", slug="snacks", icon="🍫", color="bg-purple-100 text-purple-600", image="categories/3.jpg")
drinks = Category.objects.create(title="نوشیدنی‌ها", slug="drinks", icon="🥤", color="bg-cyan-100 text-cyan-600", image="categories/4.jpg")
fruits = Category.objects.create(title="میوه و سبزیجات", slug="fruits", icon="🍎", color="bg-green-100 text-green-600", image="categories/5.jpg")
bakery = Category.objects.create(title="نان و شیرینی", slug="bakery", icon="🥐", color="bg-yellow-100 text-yellow-600", image="categories/6.jpg")
breakfast = Category.objects.create(title="صبحانه", slug="breakfast", icon="🍳", color="bg-orange-100 text-orange-600", image="categories/7.jpg")
cleaning = Category.objects.create(title="شوینده و بهداشتی", slug="cleaning", icon="🧼", color="bg-teal-100 text-teal-600", image="categories/8.jpg")
spices = Category.objects.create(title="چاشنی و ادویه", slug="spices", icon="🧂", color="bg-amber-100 text-amber-600", image="categories/9.jpg")


# Create Products (image field is now directly on Product)
p1 = Product.objects.create(title="شیر کم چرب کاله 1 لیتری", price=35000, discount_price=32000, category=dairy, is_best_seller=True, vendor=get_or_create_vendor("کاله"),
                             image="products/Gemini_Generated_Image_3hpnii3hpnii3hpn.png")
p2 = Product.objects.create(title="روغن آفتابگردان اویلا 1.5 لیتری", price=110000, discount_price=95000, badge="پرفروش", is_best_seller=True, vendor=get_or_create_vendor("اویلا"),
                             image="products/Gemini_Generated_Image_67xmen67xmen67xm.png")
p3 = Product.objects.create(title="تخم مرغ 20 عددی تلاونگ", price=85000, is_best_seller=True, vendor=get_or_create_vendor("تلاونگ"), category=breakfast,
                             image="products/Gemini_Generated_Image_6hv3u46hv3u46hv3.png")

p4 = Product.objects.create(title="گوشت چرخ‌کرده گوساله 500 گرمی", price=320000, discount_price=285000, category=meat, is_hot_offer=True, vendor=get_or_create_vendor("پویا پروتئین"),
                             image="products/Gemini_Generated_Image_crjfk1crjfk1crjf.png")
p5 = Product.objects.create(title="مرغ کامل تازه بسته بندی 2 کیلویی", price=195000, discount_price=175000, category=meat, badge="پیشنهاد ویژه", is_hot_offer=True, vendor=get_or_create_vendor("مهیا پروتئین"),
                             image="products/Gemini_Generated_Image_oxu981oxu981oxu9.png")

p6 = Product.objects.create(title="چیپس مکیما طعم کچاپ 100 گرمی", price=25000, discount_price=22000, category=snacks, badge="جدید", vendor=get_or_create_vendor("مکیما"),
                             image="products/Gemini_Generated_Image_67xmen67xmen67xm.png")
p7 = Product.objects.create(title="شکلات تلخ پارمیدا 80 درصد", price=75000, category=snacks, is_best_seller=True, vendor=get_or_create_vendor("پارمیدا"),
                             image="products/Gemini_Generated_Image_3hpnii3hpnii3hpn.png")

p8 = Product.objects.create(title="نوشابه کوکاکولا خانواده 1.5 لیتری", price=32000, discount_price=29000, category=drinks, is_hot_offer=True, vendor=get_or_create_vendor("کوکاکولا"),
                             image="products/Gemini_Generated_Image_crjfk1crjfk1crjf.png")
p9 = Product.objects.create(title="آب معدنی دماوند 1.5 لیتری", price=9000, category=drinks, vendor=get_or_create_vendor("دماوند"),
                             image="products/Gemini_Generated_Image_oxu981oxu981oxu9.png")

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

# 20 more new products
all_categories = [dairy, meat, snacks, drinks, fruits, bakery, breakfast, cleaning, spices]

new_products_data = [
    ("برنج هاشمی درجه یک ۵ کیلویی", "products/prod_rice_1783598614957.png", spices),
    ("چای سیاه سیلان ۵۰۰ گرمی", "products/prod_tea_1783598634428.png", drinks),
    ("پنیر پیتزا مطهر ۱ کیلویی", "products/prod_cheese_1783598643828.png", dairy),
    ("گوجه فرنگی بوته‌ای دستچین", "products/prod_tomato_new.jpg", fruits),
    ("روغن زیتون فرابکر نیم لیتری", "products/prod_oil_2_1783598944186.png", spices),
    ("پودر لباسشویی پرسیل", "products/prod_washing_powder_1783598955868.png", cleaning),
    ("مایع دستشویی صحت", "products/prod_liquid_soap_1783598966285.png", cleaning),
    ("شیر پرچرب پگاه ۱ لیتری", "products/Gemini_Generated_Image_3hpnii3hpnii3hpn.png", dairy),
    ("چیپس نمکی لیمویی مزمز", "products/Gemini_Generated_Image_67xmen67xmen67xm.png", snacks),
    ("تخم بلدرچین ۱۲ عددی", "products/Gemini_Generated_Image_6hv3u46hv3u46hv3.png", breakfast),
    ("گوشت چرخ‌کرده مخلوط", "products/Gemini_Generated_Image_crjfk1crjfk1crjf.png", meat),
    ("مرغ بدون پوست و استخوان", "products/Gemini_Generated_Image_oxu981oxu981oxu9.png", meat),
    ("ماکارونی رشته‌ای مانا", "products/prod_rice_1783598614957.png", snacks),
    ("کره حیوانی میهن ۱۰۰ گرم", "products/prod_cheese_1783598643828.png", dairy),
    ("خامه صبحانه پگاه", "products/Gemini_Generated_Image_3hpnii3hpnii3hpn.png", breakfast),
    ("شامپو سر صحت", "products/prod_liquid_soap_1783598966285.png", cleaning),
    ("کیک براونی شیرین عسل", "products/Gemini_Generated_Image_67xmen67xmen67xm.png", bakery),
    ("قهوه ترک بن مانو", "products/prod_tea_1783598634428.png", drinks),
    ("زعفران سحرخیز یک مثقال", "products/prod_tomato_new.jpg", spices),
    ("سس مایونز مهرام", "products/prod_oil_2_1783598944186.png", spices),
]

for idx, (name, img, cat) in enumerate(new_products_data):
    p = Product.objects.create(
        title=name,
        price=10000 + (idx * 5000),
        discount_price=9000 + (idx * 5000) if idx % 3 == 0 else None,
        category=cat,
        image=img,
        vendor=get_or_create_vendor("متفرقه"),
        is_best_seller=(idx % 4 == 0),
        is_hot_offer=(idx % 5 == 0)
    )
    add_features(p, {"وزن": "متغیر", "کیفیت": "عالی"})

print("Seed completed!")
