# Generated by Django 2.0 on 2018-12-23 02:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0009_menu_isveg'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderedItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('price', models.FloatField(default=0)),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.Menu')),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('tokenNum', models.AutoField(primary_key=True, serialize=False)),
                ('totalAmount', models.FloatField(default=0)),
                ('timetokenPlaced', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TokenItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('price', models.FloatField(default=0)),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.Menu')),
                ('tokens', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.Token')),
            ],
        ),
        migrations.RenameModel(
            old_name='Backup',
            new_name='History',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='menu',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='orderList',
        ),
        migrations.RemoveField(
            model_name='orderlist',
            name='isFinished',
        ),
        migrations.RemoveField(
            model_name='orderlist',
            name='tableNum',
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
        migrations.DeleteModel(
            name='TableNum',
        ),
        migrations.AddField(
            model_name='ordereditem',
            name='orderList',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.OrderList'),
        ),
    ]
