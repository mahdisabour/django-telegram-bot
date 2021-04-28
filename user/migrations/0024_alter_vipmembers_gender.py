# Generated by Django 3.2 on 2021-04-27 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0023_alter_vipmembers_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vipmembers',
            name='gender',
            field=models.CharField(blank=True, choices=[('male', 'مرد'), ('unknown', 'ناشناخته'), ('female', 'زن')], max_length=10, null=True),
        ),
    ]
