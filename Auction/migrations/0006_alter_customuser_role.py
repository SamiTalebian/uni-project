# Generated by Django 4.2.3 on 2023-07-09 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Auction', '0005_customuser_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('bidder', '1'), ('contract_maker', '2')], max_length=40, null=True),
        ),
    ]
