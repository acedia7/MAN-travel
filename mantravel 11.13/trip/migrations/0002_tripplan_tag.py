# Generated by Django 4.2.16 on 2024-11-13 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tripplan',
            name='tag',
            field=models.TextField(blank=True, null=True, verbose_name='标签'),
        ),
    ]