import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'visika.settings.local')
django.setup()

from products.models import Category, Product, ProductFeature

Category.objects.all().delete()
Product.objects.all().delete()
ProductFeature.objects.all().delete()

# Create Categories
dairy = Category.objects.create(title="لبنیات", slug="dairy", icon="🥛", color="bg-blue-100 text-blue-600", image="categories/cat_dairy_1783598508290.png")
meat = Category.objects.create(title="گوشت و مرغ", slug="meat", icon="🥩", color="bg-red-100 text-red-600", image="categories/cat_meat_1783598519411.png")
snacks = Category.objects.create(title="تنقلات", slug="snacks", icon="🍫", color="bg-purple-100 text-purple-600", image="categories/cat_snacks_1783598530410.png")
drinks = Category.objects.create(title="نوشیدنی‌ها", slug="drinks", icon="🥤", color="bg-cyan-100 text-cyan-600", image="categories/cat_drinks_1783598539265.png")
fruits = Category.objects.create(title="میوه و سبزیجات", slug="fruits", icon="🍎", color="bg-green-100 text-green-600", image="categories/cat_fruits_1783598549345.png")
bakery = Category.objects.create(title="نان و شیرینی", slug="bakery", icon="🥐", color="bg-yellow-100 text-yellow-600", image="categories/cat_bakery_1783598561618.png")
breakfast = Category.objects.create(title="صبحانه", slug="breakfast", icon="🍳", color="bg-orange-100 text-orange-600", image="categories/cat_breakfast_1783598572835.png")
cleaning = Category.objects.create(title="شوینده و بهداشتی", slug="cleaning", icon="🧼", color="bg-teal-100 text-teal-600", image="categories/cat_cleaning_1783598583893.png")
spices = Category.objects.create(title="چاشنی و ادویه", slug="spices", icon="🧂", color="bg-amber-100 text-amber-600", image="categories/cat_spices_1783598593480.png")


# Create Products (image field is now directly on Product)
p1 = Product.objects.create(title="شیر کم چرب کاله 1 لیتری", price=35000, discount_price=32000, category=dairy, is_best_seller=True, brand="کاله",
                             image="products/Gemini_Generated_Image_3hpnii3hpnii3hpn.png")
p2 = Product.objects.create(title="روغن آفتابگردان اویلا 1.5 لیتری", price=110000, discount_price=95000, badge="پرفروش", is_best_seller=True, brand="اویلا",
                             image="products/Gemini_Generated_Image_67xmen67xmen67xm.png")
p3 = Product.objects.create(title="تخم مرغ 20 عددی تلاونگ", price=85000, is_best_seller=True, brand="تلاونگ", category=breakfast,
                             image="products/Gemini_Generated_Image_6hv3u46hv3u46hv3.png")

p4 = Product.objects.create(title="گوشت چرخ‌کرده گوساله 500 گرمی", price=320000, discount_price=285000, category=meat, is_hot_offer=True, brand="پویا پروتئین",
                             image="products/Gemini_Generated_Image_crjfk1crjfk1crjf.png")
p5 = Product.objects.create(title="مرغ کامل تازه بسته بندی 2 کیلویی", price=195000, discount_price=175000, category=meat, badge="پیشنهاد ویژه", is_hot_offer=True, brand="مهیا پروتئین",
                             image="products/Gemini_Generated_Image_oxu981oxu981oxu9.png")

p6 = Product.objects.create(title="چیپس مکیما طعم کچاپ 100 گرمی", price=25000, discount_price=22000, category=snacks, badge="جدید", brand="مکیما",
                             image="products/Gemini_Generated_Image_67xmen67xmen67xm.png")
p7 = Product.objects.create(title="شکلات تلخ پارمیدا 80 درصد", price=75000, category=snacks, is_best_seller=True, brand="پارمیدا",
                             image="products/Gemini_Generated_Image_3hpnii3hpnii3hpn.png")

p8 = Product.objects.create(title="نوشابه کوکاکولا خانواده 1.5 لیتری", price=32000, discount_price=29000, category=drinks, is_hot_offer=True, brand="کوکاکولا",
                             image="products/Gemini_Generated_Image_crjfk1crjfk1crjf.png")
p9 = Product.objects.create(title="آب معدنی دماوند 1.5 لیتری", price=9000, category=drinks, brand="دماوند",
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
new_images = [
    "products/prod_cheese_1783598643828.png",
    "products/prod_oil_1783598624369.png",
    "products/prod_rice_1783598614957.png",
    "products/prod_tea_1783598634428.png",
    "products/prod_tomato_1783598653011.png"
]

all_categories = [dairy, meat, snacks, drinks, fruits, bakery, breakfast, cleaning, spices]

new_product_names = [
    "برنج هاشمی درجه یک ۵ کیلویی", "چای سیاه سیلان ۵۰۰ گرمی", "پنیر پیتزا مطهر ۱ کیلویی", 
    "گوجه فرنگی بوته‌ای دستچین", "روغن زیتون فرابکر نیم لیتری", "پودر لباسشویی پرسیل", 
    "مایع دستشویی صحت", "ماکارونی رشته‌ای مانا", "سس مایونز مهرام", "خیار گلخانه‌ای درجه یک",
    "سیب زمینی زرد پیازی", "بیسکوییت ساقه طلایی", "رب گوجه فرنگی تبرک", "کره حیوانی میهن ۱۰۰ گرم",
    "خامه صبحانه پگاه", "ماست چکیده کاله", "شامپو سر صحت", "کیک براونی شیرین عسل",
    "قهوه ترک بن مانو", "زعفران سحرخیز یک مثقال"
]

for idx, name in enumerate(new_product_names):
    p = Product.objects.create(
        title=name,
        price=10000 + (idx * 5000),
        discount_price=9000 + (idx * 5000) if idx % 3 == 0 else None,
        category=random.choice(all_categories),
        image=new_images[idx % len(new_images)],
        brand="متفرقه",
        is_best_seller=(idx % 4 == 0),
        is_hot_offer=(idx % 5 == 0)
    )
    add_features(p, {"وزن": "متغیر", "کیفیت": "عالی"})

print("Seed completed!")
