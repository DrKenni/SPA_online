# Generated by Django 4.2.5 on 2023-10-04 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_course_owner_lesson_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='stripe_id',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='id оплаты в stripe'),
        ),
        migrations.AddField(
            model_name='payment',
            name='stripe_status',
            field=models.CharField(default='open', max_length=15, verbose_name='статус'),
        ),
        migrations.AddField(
            model_name='payment',
            name='stripe_url',
            field=models.TextField(blank=True, null=True, verbose_name='url на платеж'),
        ),
    ]
