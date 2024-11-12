from django.db import migrations
from django.contrib.auth.models import Group, Permission


def create_user_roles(apps, schema_editor):
    roles = ['Администратор', 'Инженер', 'Инженер', 'Менеджер', 'Руководитель']

    for role in roles:
        group, created = Group.objects.get_or_create(name=role)
        if created:
            print(f"Группа '{role}' создана")
        else:
            print(f"Группа '{role}' уже существует")


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunPython(create_user_roles),
    ]
