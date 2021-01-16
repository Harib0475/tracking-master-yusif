# Generated by Django 3.1.4 on 2021-01-06 22:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0023_discussion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=100, null=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_completed', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='deadline',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
