# Generated by Django 2.0 on 2018-11-07 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_auto_20181107_1742'),
    ]

    operations = [
        migrations.AddField(
            model_name='backup',
            name='itemName',
            field=models.CharField(default='NA', max_length=30),
        ),
    ]
