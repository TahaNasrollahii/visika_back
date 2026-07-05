from django.db import migrations, models


def copy_images_forward(apps, schema_editor):
    """Copy the first ProductImage.image path into Product.image for each product."""
    Product = apps.get_model('products', 'Product')
    ProductImage = apps.get_model('products', 'ProductImage')

    for product in Product.objects.all():
        first_img = ProductImage.objects.filter(product=product).order_by('created_at').first()
        if first_img and first_img.image:
            product.image = first_img.image
            product.save(update_fields=['image'])


def copy_images_backward(apps, schema_editor):
    """Reverse: recreate a ProductImage row from Product.image."""
    Product = apps.get_model('products', 'Product')
    ProductImage = apps.get_model('products', 'ProductImage')

    for product in Product.objects.all():
        if product.image:
            ProductImage.objects.create(product=product, image=product.image)


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_remove_product_rating_remove_product_reviews_count'),
    ]

    operations = [
        # Step 1: add the new image column directly on Product
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='products/'),
        ),

        # Step 2: copy existing image data from ProductImage → Product
        migrations.RunPython(copy_images_forward, reverse_code=copy_images_backward),

        # Step 3: drop the now-redundant ProductImage table
        migrations.DeleteModel(
            name='ProductImage',
        ),
    ]
