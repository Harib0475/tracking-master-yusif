# Generated by Django 3.1.5 on 2021-01-14 18:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0031_todo_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='devicecategory',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.brandname'),
        ),
    ]