# Generated by Django 4.2 on 2025-02-18 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ricco_app', '0005_alter_compra_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='compra',
            name='detalles',
            field=models.JSONField(default=list),
        ),
    ]
