# Generated by Django 4.2.2 on 2023-07-30 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Auction', '0009_alter_contract_members'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='bidders',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
