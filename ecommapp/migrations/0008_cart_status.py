# Generated by Django 5.0.1 on 2024-01-14 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommapp', '0007_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='status',
            field=models.IntegerField(default=1),
        ),
    ]
