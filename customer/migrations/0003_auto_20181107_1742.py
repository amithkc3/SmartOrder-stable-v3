# Generated by Django 2.0 on 2018-11-07 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_auto_20181104_0019'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderlist',
            name='isFinished',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='backup',
            name='timeStamp',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]