import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'urbanAI_api.settings')
django.setup()

from django.contrib.auth.models import User

# Получаем пользователя admin
admin = User.objects.get(username='admin')
# Устанавливаем пароль
admin.set_password('admin')
# Сохраняем изменения
admin.save()

print("Password for admin user has been set to 'admin'") 