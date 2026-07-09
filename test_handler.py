import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'visika.settings')
django.setup()

from third_parties.sms.faraz_sms import SMSHandler

try:
    handler = SMSHandler()
    res = handler.send_sms_with_pattern("09123456789", "1234")
    print("SUCCESS:")
    print(res)
except Exception as e:
    print("ERROR:")
    print(str(e))
