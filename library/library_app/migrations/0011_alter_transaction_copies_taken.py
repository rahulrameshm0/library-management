# Generated by Django 5.1.7 on 2025-03-20 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0010_transaction_copies_taken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='copies_taken',
            field=models.IntegerField(default=1),
        ),
    ]
