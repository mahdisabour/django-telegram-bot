# Generated by Django 3.2 on 2021-04-27 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20210427_0952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vipmembers',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vipmembers',
            name='gender',
            field=models.CharField(blank=True, choices=[('female', 'زن'), ('male', 'مرد'), ('unknown', 'ناشناخته')], max_length=10, null=True),
        ),
    ]