# Generated by Django 3.1.4 on 2020-12-25 15:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0002_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_name', models.CharField(max_length=20)),
                ('department_description', models.CharField(max_length=100, null=True)),
                ('department_leader', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('role_department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.role')),
            ],
        ),
    ]
