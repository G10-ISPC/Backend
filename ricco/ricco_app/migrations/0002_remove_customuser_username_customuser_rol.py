# Generated by Django 4.2 on 2024-10-13 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ricco_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='username',
        ),
        migrations.AddField(
            model_name='customuser',
            name='rol',
            field=models.CharField(choices=[('admin', 'Admin'), ('cliente', 'Cliente')], default='cliente', max_length=10),
        ),
    ]
