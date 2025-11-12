import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qlsv.settings")
django.setup()

from account.models import Account

admin = Account.objects.create_user(
    email="admin@gmail.com",
    password="123456",
    role="Admin"
)
print("✅ Đã tạo tài khoản admin:", admin.email)
