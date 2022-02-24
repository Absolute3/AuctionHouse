# Generated by Django 3.2.9 on 2022-02-09 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='item_status',
            field=models.CharField(choices=[('OPEN', 'OPEN'), ('CLOSED', 'CLOSED')], default='OPEN', max_length=6),
        ),
    ]
