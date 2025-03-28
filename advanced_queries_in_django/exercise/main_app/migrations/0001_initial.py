# Generated by Django 5.0.4 on 2025-03-22 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RealEstateListing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_type', models.CharField(choices=[('House', 'House'), ('Flat', 'Flat'), ('Villa', 'Villa'), ('Cottage', 'Cottage'), ('Studio', 'Studio')], max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('bedrooms', models.PositiveIntegerField()),
                ('location', models.CharField(max_length=100)),
            ],
        ),
    ]
