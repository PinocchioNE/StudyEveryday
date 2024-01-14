import os
import django

# 确保替换 'your_project_name.settings' 为您的 Django 项目的设置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_management.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

def create_staff_account(username, email, password, id_card, phone_number):
    User = get_user_model()
    if User.objects.filter(username=username).exists():
        print(f"Username {username} already exists.")
        return
    if User.objects.filter(email=email).exists():
        print(f"Email {email} already exists.")
        return
    if User.objects.filter(id_card=id_card).exists():
        print(f"ID card {id_card} already exists.")
        return
    if User.objects.filter(phone_number=phone_number).exists():
        print(f"Phone number {phone_number} already exists.")
        return

    user = User.objects.create(
        username=username,
        email=email,
        password=make_password(password),
        id_card=id_card,
        phone_number=phone_number,
        is_staff_member=True
    )
    print(f"Staff account created for {username}")

# 示例：创建员工账户
create_staff_account('staff1', 'staff1@example.com', 'password123', '123456789012345678', '9876543210')
create_staff_account('staff2', 'staff2@example.com', 'password123', '123456789012345679', '9876543211')
