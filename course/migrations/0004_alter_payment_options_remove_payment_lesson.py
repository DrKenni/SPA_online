# Generated by Django 4.2.5 on 2023-09-21 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_payment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payment',
            options={'ordering': ('-course', '-date', '-method'), 'verbose_name': 'Платеж', 'verbose_name_plural': 'Платежи'},
        ),
        migrations.RemoveField(
            model_name='payment',
            name='lesson',
        ),
    ]