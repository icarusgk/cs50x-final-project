# Generated by Django 4.1.4 on 2022-12-18 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_board_user_card_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='description',
            field=models.TextField(blank=True, max_length=500),
        ),
    ]