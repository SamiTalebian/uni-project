# Generated by Django 4.2.2 on 2023-07-30 09:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Auction', '0006_alter_customuser_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='members',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Auction.customuser'),
        ),
    ]
