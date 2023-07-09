# Generated by Django 4.2.3 on 2023-07-09 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Auction', '0004_customuser_remove_contract_bidders_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('1', 'bidder'), ('2', 'contract_maker')], max_length=40, null=True),
        ),
    ]
