# Generated by Django 3.1.4 on 2021-01-08 09:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0024_auto_20210107_0018'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectuser',
            old_name='member',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='task',
            name='member',
        ),
        migrations.AddField(
            model_name='task',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.projectuser'),
        ),
    ]
