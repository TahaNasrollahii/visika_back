import os, django

os.environ['ALLOWED_HOSTS'] = '*'
os.environ['DJANGO_SETTINGS_MODULE'] = 'visika.settings.local'
django.setup()

from django.test import Client

c = Client()
try:
    r = c.get('/products/categories/', HTTP_HOST='localhost')
    print("STATUS:", r.status_code)
    if r.status_code == 500:
        print(r.content.decode())
except Exception as e:
    import traceback
    traceback.print_exc()
