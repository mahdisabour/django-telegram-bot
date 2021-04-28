# Generated by Django 3.2 on 2021-04-28 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0034_alter_vipmembers_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vipmembers',
            name='gender',
            field=models.CharField(blank=True, choices=[('female', 'زن'), ('male', 'مرد'), ('unknown', 'ناشناخته')], max_length=10, null=True),
        ),
    ]